/* 
# Copyright (c) 2010-2020 Andrew Dalke Scientific, AB (Sweden)
#
# All chemfp 1.x software is distributed with the following license:
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
*/

#include <limits.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "heapq.h"
#include "chemfp.h"
#include "chemfp_internal.h"

#if defined(_OPENMP)
  #include <omp.h>
#endif


enum scoring_directions {
  UP_OR_DOWN = 0,
  UP_ONLY, 
  DOWN_ONLY,
  FINISHED
};

typedef struct {
  int direction;
  int query_popcount;
  int max_popcount;
  int popcount;
  int up_popcount;
  int down_popcount;
  double score;
} PopcountSearchOrder;

static void init_search_order(PopcountSearchOrder *popcount_order, int query_popcount,
                              int max_popcount) {
  popcount_order->query_popcount = query_popcount;
  popcount_order->popcount = query_popcount;
  popcount_order->max_popcount = max_popcount;
  if (query_popcount <= 0) {
    popcount_order->direction = UP_ONLY;
    popcount_order->down_popcount = 0;
  } else {
    popcount_order->direction = UP_OR_DOWN;
    popcount_order->down_popcount = query_popcount-1;
  }
  popcount_order->up_popcount = query_popcount;
}

static void ordering_no_higher(PopcountSearchOrder *popcount_order) {
  switch (popcount_order->direction) {
  case UP_OR_DOWN:
    popcount_order->direction = DOWN_ONLY;
    break;
  case UP_ONLY:
    popcount_order->direction = FINISHED;
    break;
  default:
    break;
  }
}
static void ordering_no_lower(PopcountSearchOrder *popcount_order) {
  switch (popcount_order->direction) {
  case UP_OR_DOWN:
    popcount_order->direction = UP_ONLY;
    break;
  case DOWN_ONLY:
    popcount_order->direction = FINISHED;
    break;
  default:
    break;
  }
}


#define UP_SCORE(po) (((double)(po->query_popcount))/po->up_popcount)
#define DOWN_SCORE(po) (((double)(po->down_popcount))/po->query_popcount)

static int next_popcount(PopcountSearchOrder *popcount_order, double threshold) {
  double up_score, down_score;

  switch (popcount_order->direction) {
  case UP_OR_DOWN:
    up_score = UP_SCORE(popcount_order);
    down_score = DOWN_SCORE(popcount_order);
    if (up_score >= down_score) {
      popcount_order->popcount = (popcount_order->up_popcount)++;
      popcount_order->score = up_score;
      if (popcount_order->up_popcount > popcount_order->max_popcount) {
        popcount_order->direction = DOWN_ONLY;
      }
    } else {
      popcount_order->popcount = (popcount_order->down_popcount)--;
      popcount_order->score = down_score;
      if (popcount_order->down_popcount < 0) {
        popcount_order->direction = UP_ONLY;
      }
    }
    break;
   
  case UP_ONLY:
    popcount_order->score = UP_SCORE(popcount_order);
    popcount_order->popcount = (popcount_order->up_popcount)++;
    if (popcount_order->up_popcount > popcount_order->max_popcount) {
      popcount_order->direction = FINISHED;
    }
    break;
    
  case DOWN_ONLY:
    popcount_order->score = DOWN_SCORE(popcount_order);
    popcount_order->popcount = (popcount_order->down_popcount)--;
    if (popcount_order->down_popcount < 0) {
      popcount_order->direction = FINISHED;
    }
    break;

  default:
    return 0;
  }

  /* If the best possible score is under the threshold then we're done. */
  if (popcount_order->score < threshold) {
    popcount_order->direction = FINISHED;
    return 0;
  }
  return 1;

}

static int 
check_bounds(PopcountSearchOrder *popcount_order,
             int *start, int *end, int target_start, int target_end) {
  if (*start > target_end) {
    ordering_no_higher(popcount_order);
    return 0;
  }
  if (*end < target_start) {
    ordering_no_lower(popcount_order);
    return 0;
  }

  if (*start < target_start) {
    *start = target_start;
  }
  if (*end > target_end) {
    *end = target_end;
  }
  return 1;
}


/**** Support for the k-nearest code ****/

static int double_score_lt(chemfp_search_result *result, int i, int j) {
  if (result->scores[i] < result->scores[j])
    return 1;
  if (result->scores[i] > result->scores[j])
    return 0;
  /* Sort in descending order by index. (XXX important or overkill?) */
  return (result->indices[i] >= result->indices[j]);
}
static void double_score_swap(chemfp_search_result *result, int i, int j) {
  int tmp_index = result->indices[i];
  double tmp_score = result->scores[i];
  result->indices[i] = result->indices[j];
  result->scores[i] = result->scores[j];
  result->indices[j] = tmp_index;
  result->scores[j] = tmp_score;
}


void chemfp_knearest_results_finalize(chemfp_search_result *results_start,
                                      chemfp_search_result *results_end) {
  chemfp_search_result *result;
  for (result = results_start; result < results_end; result++) {
    /* Sort the elements */
    chemfp_heapq_heapsort(result->num_hits, result, (chemfp_heapq_lt) double_score_lt,
                          (chemfp_heapq_swap) double_score_swap);
  }
}


#define MAX(x, y) ((x) > (y) ? (x) : (y))



/******* Low-level 'contains' code.  ******/
/* Single-threaded single query against multiple targets */


#define CONTAINS_KERNEL_ARGUMENTS \
    int num_words,                                                      \
                                                                        \
    /* Query fingerprint arena, start and end indices */                \
    const unsigned char *query_fp_bytes,                                \
                                                                        \
    /* Target arena, start and end indices */                           \
    int target_storage_size, const unsigned char *target_arena,         \
    int target_start, int target_end,                                   \
                                                                        \
    /* Results go here.  */                                             \
    chemfp_search_result *results

#define CONTAINS_N_BYTE_BODY(typename) \
  int target_index;                                                     \
  const typename *query_fp = (typename *) query_fp_bytes, *target_fp;   \
  int word, probe_word = 0;                                             \
                                                                        \
  for (target_index = target_start; target_index < target_end; target_index++) { \
    target_fp = (const typename *) (target_arena + target_index * (long) target_storage_size); \
    if ((query_fp[probe_word] & target_fp[probe_word]) != query_fp[probe_word]) { \
      continue;                                                         \
    }                                                                   \
    /* This probe failed. Perhaps there's a better? Advance to the next. */ \
    probe_word = (probe_word + 1) % num_words;                          \
                                                                        \
    /* Check if the query fingerprint contains the target. */           \
    for (word=0; word<num_words; word++) {                              \
      if ((query_fp[word] & target_fp[word]) != query_fp[word]) {       \
        goto end;                                                       \
      }                                                                 \
    }                                                                   \
    if (!chemfp_add_hit(results, target_index, 0.0)) {                  \
      return 1;                                                         \
    }                                                                   \
   end:                                                                 \
    ((void)0); /* Dummy so I have a goto target. */                     \
   }                                                                    \
  return 0;


/* 1-byte aligned */
static int
chemfp_contains_arena_1_byte_aligned(CONTAINS_KERNEL_ARGUMENTS) {
  CONTAINS_N_BYTE_BODY(uint8_t);
}

/* 4-byte aligned */
static int
chemfp_contains_arena_4_byte_aligned(CONTAINS_KERNEL_ARGUMENTS) {
  CONTAINS_N_BYTE_BODY(uint32_t);
}

/* 8-byte aligned */
static int
chemfp_contains_arena_8_byte_aligned(CONTAINS_KERNEL_ARGUMENTS) {
  CONTAINS_N_BYTE_BODY(uint64_t);
}

#define CONTAINS_SINGLE_WORD_BODY(typename) \
  int target_index;                                                     \
  typename query_fp_word = *((const typename *)query_fp_bytes);         \
  typename target_fp_word;                                              \
                                                                        \
  for (target_index = target_start; target_index < target_end; target_index++) { \
    target_fp_word = *((const typename *) (target_arena + target_index * (long) target_storage_size)); \
    if ((query_fp_word & target_fp_word) != query_fp_word) {            \
      continue;                                                         \
    }                                                                   \
    if (!chemfp_add_hit(results, target_index, 0.0)) {                  \
      return 1;                                                         \
    }                                                                   \
   }                                                                    \
  return 0;


/* Special case for 1-word searches*/
static int
chemfp_contains_arena_single_word_1(CONTAINS_KERNEL_ARGUMENTS) {
  CONTAINS_SINGLE_WORD_BODY(uint8_t);
}

static int
chemfp_contains_arena_single_word_4(CONTAINS_KERNEL_ARGUMENTS) {
  CONTAINS_SINGLE_WORD_BODY(uint32_t);
}

static int
chemfp_contains_arena_single_word_8(CONTAINS_KERNEL_ARGUMENTS) {
  CONTAINS_SINGLE_WORD_BODY(uint64_t);
}

/***** Find the min required count ***/

#define DOUBLE_CHECK_MIN_REQUIRED 0

int
chemfp_get_min_intersect_popcount(int popcount_sum, double threshold) {
  int C;
  if (popcount_sum == 0) {
    /* This should never happen. But if does, chemfp says that */
    /* tanimoto(0, 0) = 0 */
    if (threshold <= 0.0) {
      return 0;
    }
    return 1;
  }
  /* This may round down (because of numeric issues?) */
  C = (int)(threshold * popcount_sum / (1 + threshold));

  /* If it is too small, round up */
  if (((double) C) / ((double)(popcount_sum - C)) < threshold) {
    C++;
#if DOUBLE_CHECK_MIN_REQUIRED == 1
    if (C != popcount_sum) {
      double score = ((double)C) / ((double)(popcount_sum - C));
      if (score < threshold) {
        fprintf(stderr,
                "get_min_intersect_popcount: over error: "
                "popcount_sum=%d threshold=%f C=%d score=%f\n",
                popcount_sum, threshold, C, score);
      }
    }
#endif
  }
#if DOUBLE_CHECK_MIN_REQUIRED == 1
  else if (C > 0) {
    double score = ((double)(C-1)) / ((double)(popcount_sum - C + 1));
    if (score >= threshold) {
      fprintf(stderr,
              "get_min_intersect_popcount: under error: "
              "popcount_sum=%d threshold=%f C=%d score=%f\n",
              popcount_sum, threshold, C, score);
    }
  }
#endif
  return C;
}


/*** forward-compatibitity options for chemfp 3.3 ***/

/* Backported from chemfp-3.3. Keep the error checking, but doesn't do anything */
int chemfp_get_option_use_specialized_algorithms(void) {
  return 0;
}
int chemfp_set_option_use_specialized_algorithms(int value) {
  if (value == 0 || value == 1) {
    return CHEMFP_OK;
  }
  return CHEMFP_BAD_ARG;
}

static int chemfp_num_column_threads = 0;
int chemfp_get_option_num_column_threads(void) {
  char *s, *end_s;
  long value = chemfp_num_column_threads;
  int num_threads = 1; /* chemfp 1.x only handles single-threaded single-query search */
  if (value == 0) {
    /* Need to initialize */
    value = 1;
    s = getenv("CHEMFP_NUM_COLUMN_THREADS");
    if (s != NULL) {
      /* Don't allow leading whitespace or '+'/'-' */
      if ('0' <= s[0] && s[0] <= '9') {
        value = strtol(s, &end_s, 10);
        /* Must process the entire variable */
        if (*end_s != '\0') {
          value = 1;
          fprintf(stderr, "chemfp: error: unable to parse $CHEMFP_NUM_COLUMN_THREADS.\n");
        } else if (value > 64) {
          value = 64;
          fprintf(stderr, "chemfp: error: $CHEMFP_NUM_COLUMN_THREADS too large. Using 64.\n");
        }
      } else {
        value = 1;
        fprintf(stderr, "chemfp: error: $CHEMFP_NUM_COLUMN_THREADS must only have digits.\n");
      }
    }
    chemfp_set_option_num_column_threads((int) value);
    value = chemfp_num_column_threads;
  }
  if (value > num_threads) {
    return num_threads;
  }
  return (int) value;
}
int chemfp_set_option_num_column_threads(int value) {
  if (value == 0) {
    value = 1;
  } else if (value < 0) {
    return CHEMFP_BAD_ARG;
  } else if (value > 64) {
    /* don't be silly */
    value = 64;
  }
  chemfp_num_column_threads = value;
  return CHEMFP_OK;
}


static int chemfp_report_algorithm = 0;
static const char *previous_algorithm_category = NULL;
static const char *previous_algorithm_name = NULL;
static int previous_num_threads = 0;

void
report_algorithm(const char *algorithm_category, const char *algorithm_name,
                 int uses_threads) {
  int num_threads;
  if (!chemfp_report_algorithm) {
    return;
  }
  if (!uses_threads) {
    num_threads = 1;
  } else {
    num_threads = chemfp_get_num_threads();
  }
  if (algorithm_category == previous_algorithm_category && algorithm_name == previous_algorithm_name &&
     previous_num_threads == num_threads) {
    return;
  }
  previous_algorithm_category = algorithm_category;
  previous_algorithm_name = algorithm_name;
  previous_num_threads = num_threads;
  
  if (uses_threads) {
    if (num_threads >= 2) {
      fprintf(stderr, "chemfp search using %s, %s, %d threads\n", algorithm_category, algorithm_name, num_threads);
    } else {
      fprintf(stderr, "chemfp search using %s, %s, 1 thread\n", algorithm_category, algorithm_name);
    }
  } else {
    fprintf(stderr, "chemfp search using %s, %s\n", algorithm_category, algorithm_name);
  }
}

int chemfp_get_option_report_algorithm(void) {
  return chemfp_report_algorithm;
}
int chemfp_set_option_report_algorithm(int value) {
  if (value == 0 || value == 1) {
    chemfp_report_algorithm = value;
    /* Reset (this is not thread safe, but I don't care) */
    previous_algorithm_category = NULL;
    previous_algorithm_name = NULL;
    return CHEMFP_OK;
  }
  return CHEMFP_BAD_ARG;
}


                             
/***** Define the main interface code ***/

#if defined(_OPENMP)

#define RENAME(name) name ## _single
#define USE_OPENMP 0
#include "search_core.c"
#undef RENAME
#undef USE_OPENMP

#define RENAME(name) name ## _openmp
#define USE_OPENMP 1
#include "search_core.c"
#undef RENAME
#undef USE_OPENMP


/* Dispatch based on the number of threads in use */

int chemfp_count_tanimoto_arena(
        /* Count all matches within the given threshold */
        double threshold,

        /* Number of bits in the fingerprint */
        int num_bits,

        /* Query arena, start and end indices */
        int query_storage_size,
        const unsigned char *query_arena, int query_start, int query_end,

        /* Target arena, start and end indices */
        int target_storage_size,
        const unsigned char *target_arena, int target_start, int target_end,

        /* Target popcount distribution information */
        int *target_popcount_indices,

        /* Results go into these arrays  */
        int *result_counts
                                   ) {
  if (chemfp_get_num_threads() <= 1)  {
    if (target_popcount_indices == NULL) {
      report_algorithm("count Tanimoto arena, no-index", "single threaded (generic)", 0);
    } else {
      report_algorithm("count Tanimoto arena, index", "single threaded (generic)", 0);
    }
    return chemfp_count_tanimoto_arena_single(
                           threshold, num_bits,
                           query_storage_size, query_arena, query_start, query_end,
                           target_storage_size, target_arena, target_start, target_end,
                           target_popcount_indices, result_counts);
  } else {
    if (target_popcount_indices == NULL) {
      report_algorithm("count Tanimoto arena, no-index", "OpenMP (generic)", 1);
    } else {
      report_algorithm("count Tanimoto arena, index", "OpenMP (generic)", 1);
    }
    return chemfp_count_tanimoto_arena_openmp(
                           threshold, num_bits,
                           query_storage_size, query_arena, query_start, query_end,
                           target_storage_size, target_arena, target_start, target_end,
                           target_popcount_indices, result_counts);
  }
}

int chemfp_threshold_tanimoto_arena(
        /* Within the given threshold */
        double threshold,

        /* Number of bits in the fingerprint */
        int num_bits,

        /* Query arena, start and end indices */
        int query_storage_size, const unsigned char *query_arena,
        int query_start, int query_end,

        /* Target arena, start and end indices */
        int target_storage_size, const unsigned char *target_arena,
        int target_start, int target_end,

        /* Target popcount distribution information */
        /*  (must have at least num_bits+1 elements) */
        int *target_popcount_indices,

        /* Results go here */
        chemfp_search_result *results) {

  if (chemfp_get_num_threads() <= 1) {
    if (target_popcount_indices == NULL) {
      report_algorithm("threshold Tanimoto arena, no-index", "single threaded (generic)", 0);
    } else {
      report_algorithm("threshold Tanimoto arena, index", "single threaded (generic)", 0);
    }
    return chemfp_threshold_tanimoto_arena_single(
                           threshold, num_bits,
                           query_storage_size, query_arena, query_start, query_end,
                           target_storage_size, target_arena, target_start, target_end,
                           target_popcount_indices, results);
  } else {
    if (target_popcount_indices == NULL) {
      report_algorithm("threshold Tanimoto arena, no-index", "OpenMP (generic)", 1);
    } else {
      report_algorithm("threshold Tanimoto arena, index", "OpenMP threaded (generic)", 1);
    }
    return chemfp_threshold_tanimoto_arena_openmp(
                           threshold, num_bits,
                           query_storage_size, query_arena, query_start, query_end,
                           target_storage_size, target_arena, target_start, target_end,
                           target_popcount_indices, results);
  }
}

int chemfp_knearest_tanimoto_arena(
        /* Find the 'k' nearest items */
        int k,
        /* Within the given threshold */
        double threshold,

        /* Number of bits in the fingerprint */
        int num_bits,

        /* Query arena, start and end indices */
        int query_storage_size, const unsigned char *query_arena,
        int query_start, int query_end,

        /* Target arena, start and end indices */
        int target_storage_size, const unsigned char *target_arena,
        int target_start, int target_end,

        /* Target popcount distribution information */
        /*  (must have at least num_bits+1 elements) */
        int *target_popcount_indices,

        /* Results go here */
        chemfp_search_result *results) {

  if (chemfp_get_num_threads() <= 1) {
    if (target_popcount_indices == NULL) {
      report_algorithm("knearest Tanimoto arena, no-index", "single threaded (generic)", 0);
    } else {
      report_algorithm("knearest Tanimoto arena, index", "single threaded (generic)", 0);
    }
    return chemfp_knearest_tanimoto_arena_single(
                           k, threshold, num_bits,
                           query_storage_size, query_arena, query_start, query_end,
                           target_storage_size, target_arena, target_start, target_end,
                           target_popcount_indices, results);
  } else {
    if (target_popcount_indices == NULL) {
      report_algorithm("knearest Tanimoto arena, no-index", "OpenMP (generic)", 1);
    } else {
      report_algorithm("knearest Tanimoto arena, index", "OpenMP (generic)", 1);
    }
    return chemfp_knearest_tanimoto_arena_openmp(
                           k, threshold, num_bits,
                           query_storage_size, query_arena, query_start, query_end,
                           target_storage_size, target_arena, target_start, target_end,
                           target_popcount_indices, results);
  }
}

int chemfp_count_tanimoto_hits_arena_symmetric(
        /* Count all matches within the given threshold */
        double threshold,

        /* Number of bits in the fingerprint */
        int num_bits,

        /* Fingerprint arena */
        int storage_size, const unsigned char *arena,

        /* Row start and end indices */
        int query_start, int query_end,

        /* Column start and end indices */
        int target_start, int target_end,

        /* Target popcount distribution information */
        int *popcount_indices,

        /* Results _increment_ existing values in the array - remember to initialize! */
        int *result_counts
                                               ) {
  if (chemfp_get_num_threads() <= 1) {
    report_algorithm("count Tanimoto arena symmetric", "single threaded (generic)", 0);
    return chemfp_count_tanimoto_hits_arena_symmetric_single(
                           threshold, num_bits, storage_size, arena,
                           query_start, query_end, target_start, target_end,
                           popcount_indices, result_counts);
  } else {
    report_algorithm("count Tanimoto arena symmetric", "OpenMP (generic)", 1);
    return chemfp_count_tanimoto_hits_arena_symmetric_openmp(
                           threshold, num_bits, storage_size, arena,
                           query_start, query_end, target_start, target_end,
                           popcount_indices, result_counts);
  }
}

int chemfp_threshold_tanimoto_arena_symmetric(
        /* Within the given threshold */
        double threshold,

        /* Number of bits in the fingerprint */
        int num_bits,

        /* Arena */
        int storage_size, const unsigned char *arena,

        /* start and end indices for the rows and columns */
        int query_start, int query_end,
        int target_start, int target_end,
        
        /* Target popcount distribution information */
        /*  (must have at least num_bits+1 elements) */
        int *popcount_indices,

        /* Results go here */
        /* NOTE: This must have enough space for all of the fingerprints! */
        chemfp_search_result *results) {
  if (chemfp_get_num_threads() <= 1) {
    report_algorithm("threshold Tanimoto arena symmetric", "single threaded (generic)", 1);
    return chemfp_threshold_tanimoto_arena_symmetric_single(
                           threshold, num_bits, storage_size, arena,
                           query_start, query_end, target_start, target_end,
                           popcount_indices, results);
  } else {
    report_algorithm("threshold Tanimoto arena symmetric", "OpenMP (generic)", 1);
    return chemfp_threshold_tanimoto_arena_symmetric_openmp(
                           threshold, num_bits, storage_size, arena,
                           query_start, query_end, target_start, target_end,
                           popcount_indices, results);
  }
}

int chemfp_knearest_tanimoto_arena_symmetric(
        /* Find the 'k' nearest items */
        int k,
        /* Within the given threshold */
        double threshold,

        /* Number of bits in the fingerprint */
        int num_bits,

        /* Arena */
        int storage_size, const unsigned char *arena,

        /* start and end indices for the rows and columns */
        int query_start, int query_end,
        int target_start, int target_end,
        
        /* Target popcount distribution information */
        /*  (must have at least num_bits+1 elements) */
        int *popcount_indices,

        /* Results go into these arrays  */
        chemfp_search_result *results) {
  if (chemfp_get_num_threads() <= 1) {
    report_algorithm("knearest Tanimoto arena symmetric", "single threaded (generic)", 0);
    return chemfp_knearest_tanimoto_arena_symmetric_single(
                           k, threshold, num_bits, storage_size, arena,
                           query_start, query_end, target_start, target_end,
                           popcount_indices, results);
  } else {
    report_algorithm("knearest Tanimoto arena symmetric", "OpenMP (generic)", 1);
    return chemfp_knearest_tanimoto_arena_symmetric_openmp(
                           k, threshold, num_bits, storage_size, arena,
                           query_start, query_end, target_start, target_end,
                           popcount_indices, results);
  }
}  
  

#else

/* Not compiling for OpenMP; don't need the run-time switch */
/* Instead, just rename the function */

#define RENAME(name) name
#define USE_OPENMP 0
#include "search_core.c"
#undef USE_OPENMP
#undef RENAME

#endif

/* Start of contains screening.  */

static int
get_arena_alignment(int storage_size, const unsigned char *arena) {
  if (ALIGNMENT(arena, 8) == 0) {
    if (storage_size % 8 == 0) {
      return 8;
    }
  }
  if (ALIGNMENT(arena, 4) == 0) {
    if (storage_size % 4 == 0) {
      return 4;
    }
  }
  return 1;
}


typedef int (*chemfp_contains_search_f)(CONTAINS_KERNEL_ARGUMENTS);

int chemfp_contains_arena(
	/* Size of the fingerprints */
	int num_bits,

        /* Query arena, start and end indices */
        int query_storage_size, const unsigned char *query_arena,
	int query_start, int query_end,

        /* Target arena, start and end indices */
        int target_storage_size, const unsigned char *target_arena,
	int target_start, int target_end,

        /* Target popcount distribution information */
        int *target_popcount_indices,

        /* Results go into these arrays  */
        chemfp_search_result *results
                                   ) {
  int query_index;
  const unsigned char *query_fp;
  int fp_size = (num_bits+7) / 8;
  int query_alignment, target_alignment, alignment;
  int num_words = 0;
  chemfp_contains_search_f arena_contains_search = chemfp_contains_arena_single_word_1;
  chemfp_popcount_f calc_popcount;
  int query_popcount, start, target_index;
  int has_error = 0;

  if ((query_start >= query_end) ||
      (target_start >= target_end)) {
    return CHEMFP_OK;
  }
  
  query_alignment = get_arena_alignment(query_storage_size, query_arena);
  target_alignment = get_arena_alignment(target_storage_size, target_arena);
  if (query_alignment < target_alignment) {
    alignment = query_alignment;
  } else {
    alignment = target_alignment;
  }

  num_words = (fp_size + alignment - 1) / alignment;

  if (num_words == 1) {
    /* special case support for single word (1 byte, 4 byte, and 8 byte) fingerprints */
    /* It's a bit excessive to do this, since few people have 8/32/64-bit fingerprints */
    /* But it makes me feel better knowing I don't have the double-check overhead */
    /* that the normal code would have. */
    /* My test case is about 25% faster. */
    switch (alignment) {
    case 8:
      arena_contains_search = chemfp_contains_arena_single_word_8;
      break;
    case 4:
      arena_contains_search = chemfp_contains_arena_single_word_4;
      break;
    case 1:
      arena_contains_search = chemfp_contains_arena_single_word_1;
    }
  } else {
    switch (alignment) {
    case 8:
      arena_contains_search = chemfp_contains_arena_8_byte_aligned;
      break;
    case 4:
      arena_contains_search = chemfp_contains_arena_4_byte_aligned;
      break;
    default:
      arena_contains_search = chemfp_contains_arena_1_byte_aligned;
    }
  }


  /* XXX TODO: special case query_popcount == 0 */
  /* Not hard to special case query_popcount == 1 */
  /* But do those occur enough to have special cases? */

  if (target_popcount_indices == NULL) {
    /* Handle the case when precomputed target popcounts aren't available. */
    /* This is a slower algorithm because it tests everything. */
    /* TODO: add OpenMP.  */
    for (query_index = query_start; query_index < query_end; query_index++) {
      query_fp = query_arena + (query_index * query_storage_size);

      /* TODO: special case the empty query */

      has_error = (has_error ||
                   arena_contains_search(num_words, query_fp,
                                         target_storage_size, target_arena, target_start, target_end,
                                         results + query_index - query_start
                                         ));
    }
    if (has_error) {
      return CHEMFP_NO_MEM;
    }
    return CHEMFP_OK;
  }

  /* Precomputed target popcounts aren't available. */
  /* I can save a bit of time (about 4% according to my tests) by limiting my search range. */

  calc_popcount = chemfp_select_popcount(num_bits, query_storage_size, query_arena);

  /* TODO: add OpenMP. */
  for (query_index = query_start; query_index < query_end; query_index++) {
    query_fp = query_arena + (query_index * (long) query_storage_size);
    query_popcount = calc_popcount(fp_size, query_fp);

    /* Special case the empty query */
    if (query_popcount == 0) {
      for (target_index=target_start; target_index<target_end; target_index++) {
        chemfp_add_hit(results + query_index - query_start, target_index, 0.0);
      }
      continue;
    }

    start = target_popcount_indices[query_popcount];
    if (start < target_start) {
      start = target_start;
    }
    
    has_error = (has_error ||
                 arena_contains_search(num_words, query_fp,
                                       target_storage_size, target_arena, start, target_end,
                                       results + query_index - query_start
                                       ));
  }
  if (has_error) {
    return CHEMFP_NO_MEM;
  }
  return CHEMFP_OK;
}

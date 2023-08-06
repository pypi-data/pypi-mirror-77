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

/* This is a rather cumbersome solution to two problems I have with OpenMP.

 1) multiple threads and OpenMP don't mix on a Mac. It segfaults
 during the first openmp call. I want people to be able to use chemfp
 in multi-threaded environments, even with diminished performance, so
 the single thread version should not go through the OpenMP path.

 2) I measured a roughly 5% performance penalty hit with a single
 thread using OpenMP vs. the code compiled without OpenMP.

My solution is to compile the core code twice, one for each path. The
RENAME macro rewrites

   int RENAME(chemfp_count_tanimoto_arena)

to one of:

 static int chemfp_count_tanimoto_arena_single -- single-threaded, compiler supports OpenMP
 static int chemfp_count_tanimoto_arena_openmp -- multiple OpenMP threads
 int chemfp_count_tanimoto_arena -- single-threaded, compiler does not support OpenMP

depending on the circumstances. In a normal build, where OpenMP is
available, then this file will be #include'd twice.

*/

/* count code */
int RENAME(chemfp_count_tanimoto_arena)(
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
  int query_index, target_index;
  const unsigned char *query_fp, *target_fp;
  int start, end;
  int count;
  int fp_size = (num_bits+7) / 8;
  double score;
  int popcount_sum, min_popcount;
  int query_popcount, start_target_popcount, end_target_popcount;
  int target_popcount;
  int intersect_popcount;

  chemfp_popcount_f calc_popcount;
  chemfp_intersect_popcount_f calc_intersect_popcount;
  
  if (query_start >= query_end) {
    /* No queries */
    return CHEMFP_OK;
  }
  /* Prevent overflow if someone uses a threshold of, say, 1E-80 */
  /* (Not really needed unless you trap IEEE 754 overflow errors) */
  if (threshold > 0.0 && threshold < 1.0/num_bits) {
    threshold = 0.5 / num_bits;
  }
  if ((target_start >= target_end) || threshold > 1.0) {
    for (query_index = 0; query_index < (query_end-query_start); query_index++) {
      /* No possible targets */
      result_counts[query_index] = 0;
    }
    return CHEMFP_OK;
  }

  if (threshold <= 0.0) {
    /* Everything will match, so there's no need to figure that out */
    for (query_index = 0; query_index < (query_end-query_start); query_index++) {
      result_counts[query_index] = (target_end - target_start);
    }
    return CHEMFP_OK;
  }

  if (target_popcount_indices == NULL) {
    long numerator, denominator;
    
    /* Choose popcounts optimized for this case */
    chemfp_popcount_f calc_query_popcount = chemfp_select_popcount(num_bits, query_storage_size, query_arena);
    chemfp_popcount_f calc_target_popcount = chemfp_select_popcount(num_bits, target_storage_size, target_arena);
    calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, query_storage_size, query_arena,
                target_storage_size, target_arena);
    denominator = num_bits * CHEMFP_FLOAT_SCALE;
    /* Round down, which makes a slightly wider filter than needed */
    numerator = (long)(threshold * denominator);

    /* Handle the case when precomputed targets aren't available. */
    /* This is a slower algorithm because it tests everything. */
#if USE_OPENMP == 1
    #pragma omp parallel for \
        private(query_fp, query_popcount, target_fp, target_popcount, \
                intersect_popcount, count, target_index, score) \
        schedule(dynamic)
#endif
    for (query_index = 0; query_index < (query_end-query_start); query_index++) {
      query_fp = query_arena + (query_start + query_index) * (long) query_storage_size;
      query_popcount = calc_query_popcount(fp_size, query_fp);
      if (query_popcount == 0) {
        /* The score will always be 0. (chemfp says that 0/0 = 0). */
        /* Since the threshold > 0, this query will never match */
        continue;
      }
      
      target_fp = target_arena + (target_start * (long) target_storage_size);
      
      count = 0;

      for (target_index = target_start; target_index < target_end;
           target_index++, target_fp += target_storage_size) {
        target_popcount = calc_target_popcount(fp_size, target_fp);
        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
  
        if (denominator * intersect_popcount  >=
              numerator * (query_popcount + target_popcount - intersect_popcount)) {
          score = ((double)intersect_popcount) / (query_popcount + target_popcount - intersect_popcount);
          if (score >= threshold) {
            count++;
          }
        }
      }
      result_counts[query_index] = count;
    }
    return CHEMFP_OK;
  }
                                                   
  /* Choose popcounts optimized for this case */
  calc_popcount = chemfp_select_popcount(num_bits, query_storage_size, query_arena);
  calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, query_storage_size, query_arena,
                target_storage_size, target_arena);

  /* This uses the limits from Swamidass and Baldi */
  /* It doesn't use the search ordering because it's supposed to find everything */
#if USE_OPENMP == 1
  #pragma omp parallel for \
      private(query_fp, query_popcount, start_target_popcount, end_target_popcount, \
              count, target_popcount, start, end, target_fp, popcount_sum, min_popcount, target_index, intersect_popcount, score) \
      schedule(dynamic)
#endif
  for (query_index = 0; query_index < (query_end-query_start); query_index++) {
    query_fp = query_arena + (query_start + query_index) * (long) query_storage_size;
    query_popcount = calc_popcount(fp_size, query_fp);
    /* Special case when popcount(query) == 0; everything has a score of 0.0 */
    if (query_popcount == 0) {
      if (threshold == 0.0) {
        result_counts[query_index] = (target_end - target_start);
      }
      continue;
    }
    /* Figure out which fingerprints to search */
    if (threshold == 0.0) {
      start_target_popcount = 0;
      end_target_popcount = num_bits;
    } else {
      start_target_popcount = (int)(query_popcount * threshold);
      end_target_popcount = (int)(ceil(query_popcount / threshold));
      if (end_target_popcount > num_bits) {
        end_target_popcount = num_bits;
      }
    }
    count = 0;
    for (target_popcount = start_target_popcount; target_popcount <= end_target_popcount;
         target_popcount++) {
      start = target_popcount_indices[target_popcount];
      end = target_popcount_indices[target_popcount+1];
      if (start < target_start) {
        start = target_start;
      }
      if (end > target_end) {
        end = target_end;
      }

      target_fp = target_arena + (start * (long) target_storage_size);
      popcount_sum = query_popcount + target_popcount;
      min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, threshold);
      
      for (target_index = start; target_index < end;
           target_index++, target_fp += target_storage_size) {
        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
        if (intersect_popcount >= min_popcount) {
          count++;
        }
      }
    }
    result_counts[query_index] = count;
  } /* went through each of the queries */
  return CHEMFP_OK;
}

int RENAME(chemfp_threshold_tanimoto_arena)(
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

  int query_index, target_index;
  const unsigned char *query_fp, *target_fp;
  int start, end;
  int fp_size = (num_bits+7) / 8;
  double score;
  int query_popcount, start_target_popcount, end_target_popcount;
  int target_popcount;
  int intersect_popcount, popcount_sum, min_popcount;
  int add_hit_error = 0;

  chemfp_popcount_f calc_popcount;
  chemfp_intersect_popcount_f calc_intersect_popcount;
  
  if (query_start >= query_end) {
    /* No queries */
    return CHEMFP_OK;
  }

  /* Prevent overflow if someone uses a threshold of, say, 1E-80 */
  /* (Not really needed unless you trap IEEE 754 overflow errors) */
  if (threshold > 0.0 && threshold < 1.0/num_bits) {
    threshold = 0.5 / num_bits;
  }
  if ((target_start >= target_end) || threshold > 1.0) {
    return CHEMFP_OK;
  }

  if (target_popcount_indices == NULL) {
    /* Handle the case when precomputed targets aren't available. */
    /* This is a slower algorithm because it tests everything. */
    long numerator, denominator;
    
    /* Choose popcounts optimized for this case */
    chemfp_popcount_f calc_query_popcount = chemfp_select_popcount(num_bits, query_storage_size, query_arena);
    chemfp_popcount_f calc_target_popcount = chemfp_select_popcount(num_bits, target_storage_size, target_arena);
    calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, query_storage_size, query_arena,
                target_storage_size, target_arena);
    denominator = num_bits * CHEMFP_FLOAT_SCALE;
    /* Round down, which makes a slightly wider filter than needed */
    numerator = (long)(threshold * denominator);
    
#if USE_OPENMP == 1
    #pragma omp parallel for \
       private(query_fp, query_popcount, target_fp, target_popcount, target_index, \
               intersect_popcount, score)                  \
       schedule(dynamic)
#endif
    for (query_index = query_start; query_index < query_end; query_index++) {
      query_fp = query_arena + (query_index * (long) query_storage_size);
      query_popcount = calc_query_popcount(fp_size, query_fp);
      if (query_popcount == 0) {
        /* Special case when popcount(query) == 0; everything has a score of 0.0 */
        if (threshold == 0.0) {
          for (target_index = target_start; target_index < target_end; target_index++) {
            if (!chemfp_add_hit(results+(query_index-query_start), target_index, 0.0)) {
              add_hit_error = 1;
            }
          }
        }
        continue;
      }
      
      target_fp = target_arena + (target_start * (long) target_storage_size);
      /* Handle the popcount(query) == 0 special case? */
      for (target_index = target_start; target_index < target_end;
           target_index++, target_fp += target_storage_size) {
        target_popcount = calc_target_popcount(fp_size, target_fp);
        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
        
        if (denominator * intersect_popcount  >=
              numerator * (query_popcount + target_popcount - intersect_popcount)) {
          score = ((double)intersect_popcount) / (query_popcount + target_popcount - intersect_popcount);
          if (score >= threshold) {
            if (!chemfp_add_hit(results+(query_index-query_start), target_index, score)) {
              add_hit_error = 1;
            }
          }
        } /* fast rejection test */
      }
    }
    if (add_hit_error) {
      return CHEMFP_NO_MEM;
    }
    return CHEMFP_OK;
  }
  

  calc_popcount = chemfp_select_popcount(num_bits, query_storage_size, query_arena);
  calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, query_storage_size, query_arena,
                target_storage_size, target_arena);
  
  /* This uses the limits from Swamidass and Baldi */
  /* It doesn't use the search ordering because it's supposed to find everything */

#if USE_OPENMP == 1
  #pragma omp parallel for \
      private(query_fp, query_popcount, target_index, target_fp, start_target_popcount, \
              end_target_popcount, target_popcount, start, end, popcount_sum, min_popcount,  \
              intersect_popcount, score) \
      schedule(dynamic)
#endif
  for (query_index = query_start; query_index < query_end; query_index++) {
    query_fp = query_arena + (query_index * (long) query_storage_size);
    query_popcount = calc_popcount(fp_size, query_fp);
    /* Special case when popcount(query) == 0; everything has a score of 0.0 */
    if (query_popcount == 0) {
      if (threshold == 0.0) {
        for (target_index = target_start; target_index < target_end; target_index++) {
          if (!chemfp_add_hit(results+(query_index-query_start), target_index, 0.0)) {
            add_hit_error = 1;
          }
        }
      }
      continue;
    }

    /* Figure out which fingerprints to search */
    if (threshold == 0.0) {
      start_target_popcount = 0;
      end_target_popcount = num_bits;
    } else {
      start_target_popcount = (int)(query_popcount * threshold);
      end_target_popcount = (int)(ceil(query_popcount / threshold));
      if (end_target_popcount > num_bits) {
        end_target_popcount = num_bits;
      }
    }
    for (target_popcount=start_target_popcount; target_popcount<=end_target_popcount;
         target_popcount++) {
      start = target_popcount_indices[target_popcount];
      end = target_popcount_indices[target_popcount+1];
      if (start < target_start) {
        start = target_start;
      }
      if (end > target_end) {
        end = target_end;
      }

      target_fp = target_arena + (start * (long) target_storage_size);
      popcount_sum = query_popcount + target_popcount;
      min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, threshold);
      
      for (target_index = start; target_index < end;
           target_index++, target_fp += target_storage_size) {
        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);

        if (intersect_popcount >= min_popcount) {
          score = ((double) intersect_popcount) / (popcount_sum - intersect_popcount);
          if (!chemfp_add_hit(results+(query_index-query_start), target_index, score)) {
            add_hit_error = 1;
          }
        }
      }
    }
  } /* went through each of the queries */
  if (add_hit_error) {
    return CHEMFP_NO_MEM;
  }
  return CHEMFP_OK;
}



static int 
RENAME(knearest_tanimoto_arena_no_popcounts)(
        /* Find the 'k' nearest items */
        int k,
        /* Within the given threshold */
        double threshold,

        /* Fingerprint size in bits */
        int num_bits,

        /* Query arena, start and end indices */
        int query_storage_size, const unsigned char *query_arena,
        int query_start, int query_end,

        /* Target arena, start and end indices */
        int target_storage_size, const unsigned char *target_arena,
        int target_start, int target_end,

        /* Results go into these arrays  */
        chemfp_search_result *results
                                   ) {
  int query_index, target_index;
  int fp_size = (num_bits+7)/8;
  const unsigned char *query_fp, *target_fp;
  double query_threshold, score;
  chemfp_search_result *result;
  int add_hit_error = 0;
  int query_popcount, target_popcount, intersect_popcount;
  chemfp_popcount_f calc_query_popcount, calc_target_popcount;
  chemfp_intersect_popcount_f calc_intersect_popcount;
  long numerator, denominator;

  calc_query_popcount = chemfp_select_popcount(num_bits, query_storage_size, query_arena);
  calc_target_popcount = chemfp_select_popcount(num_bits, target_storage_size, target_arena);
  calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, query_storage_size, query_arena,
                target_storage_size, target_arena);
  
  denominator = (long)(num_bits * CHEMFP_FLOAT_SCALE);
  
#if USE_OPENMP == 1
#pragma omp parallel for private(query_fp, query_popcount, result, numerator, query_threshold, \
                                 target_fp, target_index, target_popcount, intersect_popcount, score)
#endif
  for (query_index = 0; query_index < (query_end-query_start); query_index++) {
    query_fp = query_arena + (query_start+query_index) * (long) query_storage_size;

    query_popcount = calc_query_popcount(fp_size, query_fp);
    result = results+query_index;
    query_threshold = threshold;
    numerator = (long)(query_threshold * denominator);
    
    target_fp = target_arena + (target_start * (long) query_storage_size);
    target_index = target_start;

    if (query_popcount == 0) {
      /* The score will always be 0 */
      if (query_threshold == 0.0) {
        /* The user wants zeros */
        for (; target_index < target_end;
             target_index++, target_fp += target_storage_size) {
          if (!chemfp_add_hit(result, target_index, 0.0)) {
            add_hit_error = 1;
          }
          if (result->num_hits == k) {
            /* The scores are all 0.0 so there's no need to heapify */
            break;
          }
        }
      }
      continue;
    }
    
    for (; target_index < target_end;
         target_index++, target_fp += target_storage_size) {
      target_popcount = calc_target_popcount(fp_size, target_fp);
      intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
      if (denominator * intersect_popcount  >=
            numerator * (query_popcount + target_popcount - intersect_popcount)) {
        score = ((double)intersect_popcount) / (query_popcount + target_popcount - intersect_popcount);
        if (score >= query_threshold) {
          if (!chemfp_add_hit(result, target_index, score)) {
  	  add_hit_error = 1;
  	}
          if (result->num_hits == k) {
            chemfp_heapq_heapify(k, result, (chemfp_heapq_lt) double_score_lt,
                                 (chemfp_heapq_swap) double_score_swap);
            query_threshold = result->scores[0];
            numerator = (long)(query_threshold * denominator);
            /* Since we leave the loop early, I need to advance the pointers */
            target_index++;
            target_fp += target_storage_size;
            break;
          }
        }
      }
    }
    /* Either we've reached the end of the fingerprints or the heap is full */
    if (result->num_hits == k) {
      /* Continue scanning through the fingerprints */
      for (; target_index < target_end;
           target_index++, target_fp += target_storage_size) {
        target_popcount = calc_target_popcount(fp_size, target_fp);
        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
        
        if (denominator * intersect_popcount  >=
            numerator * (query_popcount + target_popcount - intersect_popcount)) {
          score = ((double)intersect_popcount) / (query_popcount + target_popcount - intersect_popcount);

          /* We need to be strictly *better* than what's in the heap */
          if (score > query_threshold) {
            result->indices[0] = target_index;
            result->scores[0] = score;
            chemfp_heapq_siftup(k, result, 0, (chemfp_heapq_lt) double_score_lt,
                                (chemfp_heapq_swap) double_score_swap);
            query_threshold = result->scores[0];
          } /* heapreplaced the old smallest item with the new item */
        }
      } /* fast reject test */
      /* End of the fingerprint scan */
    } else {
      /* The heap isn't full, so we haven't yet heapified it. */
      chemfp_heapq_heapify(result->num_hits, result,  (chemfp_heapq_lt) double_score_lt,
                           (chemfp_heapq_swap) double_score_swap);
    }
  } /* Loop through the queries */

  if (add_hit_error) {
    return CHEMFP_NO_MEM;
  }
  return CHEMFP_OK;
}


int RENAME(chemfp_knearest_tanimoto_arena)(
        /* Find the 'k' nearest items */
        int k,
        /* Within the given threshold */
        double threshold,

        /* Size of the fingerprints and size of the storage block */
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

  int fp_size;
  int query_popcount, target_popcount, intersect_popcount;
  double score, best_possible_score, query_threshold;
  int popcount_sum, min_popcount;
  const unsigned char *query_fp, *target_fp;
  int query_index, target_index;
  int start, end;
  PopcountSearchOrder popcount_order;
  chemfp_search_result *result;
  int add_hit_error = 0;
  chemfp_popcount_f calc_popcount;
  chemfp_intersect_popcount_f calc_intersect_popcount;

  /* This is C. We don't check for illegal input values. */
  if (query_start >= query_end) {
    return CHEMFP_OK;
  }
  /* k == 0 is a valid input, and of course the result is no matches */
  if (k == 0) {
    return CHEMFP_OK;
  }
  fp_size = (num_bits+7)/8;
  /* Prevent overflow if someone uses a threshold of, say, 1E-80 */
  /* The smallest possible positive score is 1/num_bits so */
  /* scale up too-small values to one that's more reasonable */
  if (threshold > 0.0 && threshold < 1.0/num_bits) {
    threshold = 0.5 / num_bits;
  }

  if (target_popcount_indices == NULL) {
    /* precomputed targets aren't available. Use the slower algorithm. */
    return RENAME(knearest_tanimoto_arena_no_popcounts)(
        k, threshold, num_bits,
        query_storage_size, query_arena, query_start, query_end,
        target_storage_size, target_arena, target_start, target_end,
        results);
  }

  /* Choose popcounts optimized for this case */
  calc_popcount = chemfp_select_popcount(num_bits, query_storage_size, query_arena);
  calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, query_storage_size, query_arena,
                target_storage_size, target_arena);

  
  /* Loop through the query fingerprints */
#if USE_OPENMP == 1
  #pragma omp parallel for \
    private(result, query_fp, query_threshold, query_popcount, popcount_order, \
            target_index, target_fp, target_popcount, best_possible_score, \
	    start, end, popcount_sum, min_popcount, intersect_popcount, score) schedule(dynamic)
    
#endif
  for (query_index=0; query_index < (query_end-query_start); query_index++) {
    result = results+query_index;
    query_fp = query_arena + (query_start+query_index) * (long) query_storage_size;

    query_threshold = threshold;
    query_popcount = calc_popcount(fp_size, query_fp);

    if (query_popcount == 0) {
      /* By definition, tanimoto(X, 0) = 0, so check that something should be added. */
      if (threshold > 0.0) {
        continue;
      }
      /* This is chemically meaningless, but it has to return k items. */
      for (target_index=target_start; target_index<target_end; target_index++) {
        if (!chemfp_add_hit(result, target_index, 0.0)) {
	  add_hit_error = 1;
	}
        if (result->num_hits >= k) {
          break;
        }
      }
      continue;
    }

    /* Search the bins using the ordering from Swamidass and Baldi.*/
    init_search_order(&popcount_order, query_popcount, num_bits);

    /* Look through the sections of the arena in optimal popcount order */
    while (next_popcount(&popcount_order, query_threshold)) {
      target_popcount = popcount_order.popcount;
      best_possible_score = popcount_order.score;

      /* If we can't beat the query threshold then we're done with the targets */
      if (best_possible_score < query_threshold) {
        break;
      }

      /* Scan through the targets which have the given popcount */
      start = target_popcount_indices[target_popcount];
      end = target_popcount_indices[target_popcount+1];
      
      if (!check_bounds(&popcount_order, &start, &end, target_start, target_end)) {
        continue;
      }

      /* Iterate over the target fingerprints */
      target_fp = target_arena + start * (long) target_storage_size;
      popcount_sum = query_popcount + target_popcount;
      min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, query_threshold);

      target_index = start;

      /* There are fewer than 'k' elements in the heap*/
      if (result->num_hits < k) {
        for (; target_index<end; target_index++, target_fp += target_storage_size) {
          intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);

          /* The heap isn't full; only check if we're at or above the query threshold */
          if (intersect_popcount >= min_popcount) {
            score = ((double) intersect_popcount) / (popcount_sum - intersect_popcount);
            if (!chemfp_add_hit(result, target_index, score)) {
  	      add_hit_error = 1;
  	    }
            if (result->num_hits == k) {
              chemfp_heapq_heapify(k, result,  (chemfp_heapq_lt) double_score_lt,
                                   (chemfp_heapq_swap) double_score_swap);
              query_threshold = result->scores[0];
              min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, query_threshold);
              
              /* We're going to jump to the "heap is full" section */
              /* Since we leave the loop early, I need to advance the pointers */
              target_index++;
              target_fp += target_storage_size;

              goto heap_replace;
            } /* Added to heap */
          } /* fast rejection test */
        } /* Went through target fingerprints */

        /* If we're here then the heap did not fill up. Try the next popcount */
        continue;
      }

    heap_replace:
      /* We only get here if the heap contains k element */

      /* Earlier we tested for "best_possible_score<query_threshold". */
      /* The test to replace an element in the heap is more stringent. */
      if (query_threshold >= best_possible_score) {
        /* Can't do better. Might as well give up. */
        break;
      }

      /* Scan through the target fingerprints; can we improve over the threshold? */
      for (; target_index<end; target_index++, target_fp += target_storage_size) {

        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
        if (intersect_popcount >= min_popcount) {
          score = ((double)intersect_popcount) / (popcount_sum - intersect_popcount);
          
          /* We need to be strictly *better* than what's in the heap */
          if (score > query_threshold) {
            result->indices[0] = target_index;
            result->scores[0] = score;
            chemfp_heapq_siftup(k, result, 0, (chemfp_heapq_lt) double_score_lt,
                                (chemfp_heapq_swap) double_score_swap);
            query_threshold = result->scores[0];
            if (query_threshold >= best_possible_score) {
              /* we can't do any better in this section (or in later ones) */
              break;
            }
            min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, query_threshold);
          } /* heapreplaced the old smallest item with the new item */
        } /* fast rejection test */
      } /* looped over fingerprints */
    } /* Went through all the popcount regions */

    /* We have scanned all the fingerprints. Is the heap full? */
    if (result->num_hits < k) {
      /* Not full, so need to heapify it. */
      chemfp_heapq_heapify(result->num_hits, result, (chemfp_heapq_lt) double_score_lt,
                           (chemfp_heapq_swap) double_score_swap);
    }
  } /* looped over all queries */
  if (add_hit_error) {
    return CHEMFP_NO_MEM;
  }
  return CHEMFP_OK;
}



/***** Special support for the NxN symmetric case ******/

int RENAME(chemfp_count_tanimoto_hits_arena_symmetric)(
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
        int *target_popcount_indices,

        /* Results _increment_ existing values in the array - remember to initialize! */
        int *result_counts
                                          ) {
  int fp_size = (num_bits+7) / 8;
  int query_index, target_index;
  int start, end;
  int query_popcount, target_popcount;
  int start_target_popcount, end_target_popcount, intersect_popcount;
  int count;
  double score;
  int popcount_sum, min_popcount;
  const unsigned char *query_fp, *target_fp;
  chemfp_popcount_f calc_popcount;
  chemfp_intersect_popcount_f calc_intersect_popcount;
  
#if USE_OPENMP == 1
  /* Reduce contention by using a per-thread counts array. For details see: */
  /* http://www.dalkescientific.com/writings/diary/archive/2012/01/17/I_parallelize_an_algorithm.html */
  int i;
  int num_threads;
  int *parallel_counts;
  int *per_thread_counts;
  int per_thread_size;
#endif

  /* Check that we're not obviously in the lower triangle */
  if (query_start >= target_end) {  /* No possible hits */
    return CHEMFP_OK;
  }

  /* Shift the target towards the upper triangle, if needed */
  if (target_start < query_start) {
    target_start = query_start;
  }

  /* Check for edge cases */
  if ((query_start >= query_end) ||
      (target_start >= target_end) ||
      (threshold > 1.0)) {
    return CHEMFP_OK;
  }

  if (threshold <= 0.0) {
    /* By definition, everything matches */
    /* FIXME: this is inelegant. I'm finding the symmetry and boundary conditions a bit tricky */
    for (query_index=query_start; query_index<query_end; query_index++) {
      for (target_index=MAX(query_index+1, target_start);
           target_index<target_end; target_index++) {
        result_counts[query_index] += 1;
        result_counts[target_index] += 1;
      }
    }
    return CHEMFP_OK;
  }


  /* Prevent overflow if someone uses a threshold of, say, 1E-80 */
  /* (Not really needed unless you trap IEEE 754 overflow errors) */
  if (threshold > 0.0 && threshold < 1.0/num_bits) {
    threshold = 0.5 / num_bits;
  }

  /* target_popcount_indices must exist; if you don't care for the factor */
  /* of two performance increase by precomputing/presorting based on popcount */
  /* then why are you interested in the factor of two based on symmetry? */
                                                   
  /* Choose popcount methods optimized for this case */
  calc_popcount = chemfp_select_popcount(num_bits, storage_size, arena);
  calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, storage_size, arena, storage_size, arena);
  
  /* This uses the limits from Swamidass and Baldi */
#if USE_OPENMP == 1
  num_threads = omp_get_max_threads();
  per_thread_size = MAX(query_end, target_end);
  parallel_counts = (int *) calloc(num_threads * per_thread_size, sizeof(int));
  if (!parallel_counts) {
    return CHEMFP_NO_MEM;
  }
  #pragma omp parallel for \
      private(query_fp, query_popcount, start_target_popcount, end_target_popcount,  \
              count, target_popcount, start, end, target_fp, popcount_sum, min_popcount, \
              target_index, intersect_popcount, score, per_thread_counts) \
      schedule(dynamic)
#endif
  for (query_index = query_start; query_index < query_end; query_index++) {
    query_fp = arena + (query_index * (long) storage_size);
    query_popcount = calc_popcount(fp_size, query_fp);
#if USE_OPENMP == 1
    per_thread_counts = parallel_counts+(omp_get_thread_num() * per_thread_size);
#endif

    /* Special case when popcount(query) == 0; everything has a score of 0.0 */
    if (query_popcount == 0) {
      continue;
    }
    /* Figure out which fingerprints to search */
    start_target_popcount = (int)(query_popcount * threshold);
    end_target_popcount = (int)(ceil(query_popcount / threshold));
    if (end_target_popcount > num_bits) {
      end_target_popcount = num_bits;
    }

    count = 0;
    for (target_popcount = start_target_popcount; target_popcount <= end_target_popcount;
         target_popcount++) {
      start = target_popcount_indices[target_popcount];
      end = target_popcount_indices[target_popcount+1];
      if (start < target_start) {
        start = target_start;
      }
      start = MAX(query_index+1, start);
      if (end > target_end) {
        end = target_end;
      }

      target_fp = arena + (start * (long) storage_size);
      popcount_sum = query_popcount + target_popcount;
      min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, threshold);
      
      for (target_index = start; target_index < end;
           target_index++, target_fp += storage_size) {
        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
        if (intersect_popcount >= min_popcount) {
          score = ((double)intersect_popcount) / (popcount_sum - intersect_popcount);
          if (score >= threshold) {
            /* Can accumulate the score for the row. This is likely a register */
            /* instead of a memory location so should be slightly faster. */
            count++;
            /* I can't use the same technique for the symmetric match */
#if USE_OPENMP == 1
            per_thread_counts[target_index]++;
#else
            result_counts[target_index]++;
#endif
          }
        } /* fast rejection test */
      }
    }

    /* Save the accumulated row counts */
#if USE_OPENMP == 1
    if (count) {
      per_thread_counts[query_index] += count;
    }
#else
    result_counts[query_index] += count;
#endif

  } /* went through each of the queries */

#if USE_OPENMP == 1
  /* Merge the per-thread results into the counts array */
  /* TODO: start from MIN(query_start, query_end) */
  /* TODO: parallelize? */
  for (query_index = 0; query_index < per_thread_size; query_index++) {
    count = 0;
    for (i=0; i<num_threads; i++) {
      count += parallel_counts[per_thread_size * i + query_index];
    }
    result_counts[query_index] += count;
  }
  free(parallel_counts);
#endif
  return CHEMFP_OK;
}

int RENAME(chemfp_threshold_tanimoto_arena_symmetric)(
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

  int fp_size = (num_bits+7) / 8;
  int query_index, target_index;
  int start, end;
  const unsigned char *query_fp, *target_fp;
  int query_popcount, target_popcount;
  int start_target_popcount, end_target_popcount;
  chemfp_popcount_f calc_popcount;
  chemfp_intersect_popcount_f calc_intersect_popcount;
  int popcount_sum, intersect_popcount, min_popcount;
  double score;
  int add_hit_error = 0;

  /* Check that we're not obviously in the lower triangle */
  if (query_start >= target_end) {  /* No possible hits */
    return CHEMFP_OK;
  }

  /* Shift the target towards the upper triangle, if needed */
  if (target_start < query_start) {
    target_start = query_start;
  }

  /* Corner cases where I don't need to do anything */
  if ((query_start >= query_end) ||
      (target_start >= target_end) ||
      (threshold > 1.0)) {
    return CHEMFP_OK;
  }

  /* if (threshold == 0.0) { */ /* TODO: Optimize this case */


  /* Prevent overflow if someone uses a threshold of, say, 1E-80 */
  if (threshold > 0.0 && threshold < 1.0/num_bits) {
    threshold = 0.5 / num_bits;
  }

  /* Offset the results so the results[query_start] is the first term */
  results -= query_start;

  calc_popcount = chemfp_select_popcount(num_bits, storage_size, arena);
  calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, storage_size, arena, storage_size, arena);

  /* This uses the limits from Swamidass and Baldi */
  /* It doesn't use the search ordering because it's supposed to find everything */
  
#if USE_OPENMP == 1
  #pragma omp parallel for \
      private(query_fp, query_popcount, start_target_popcount, end_target_popcount, \
              target_popcount, start, end, target_fp, popcount_sum, min_popcount,   \
              target_index, intersect_popcount, score)                              \
      schedule(dynamic)
#endif
  for (query_index = query_start; query_index < query_end; query_index++) {
    query_fp = arena + (query_index * (long) storage_size);
    query_popcount = calc_popcount(fp_size, query_fp);

    /* Special case when popcount(query) == 0; everything has a score of 0.0 */
    if (query_popcount == 0) {
      if (threshold == 0.0) {
        /* Only populate the upper triangle */
        target_index = MAX(query_index+1, target_start);
        for (;target_index < target_end; target_index++) {
          if (!chemfp_add_hit(results+query_index, target_index, 0.0)) {
            add_hit_error = 1;
          }
        }
      }
      continue;
    }
    /* Figure out which fingerprints to search, based on the popcount */
    if (threshold == 0.0) {
      start_target_popcount = 0;
      end_target_popcount = num_bits;
    } else {
      start_target_popcount = (int)(query_popcount * threshold);
      end_target_popcount = (int)(ceil(query_popcount / threshold));
      if (end_target_popcount > num_bits) {
        end_target_popcount = num_bits;
      }
    }

    for (target_popcount=start_target_popcount; target_popcount<=end_target_popcount;
         target_popcount++) {
      start = popcount_indices[target_popcount];
      end = popcount_indices[target_popcount+1];
      if (start < target_start) {
        start = target_start;
      }
      if (end > target_end) {
        end = target_end;
      }

      popcount_sum = query_popcount + target_popcount;
      min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, threshold);
      
      for (target_index = MAX(query_index+1, start); target_index < end; target_index++) {
        target_fp = arena + (target_index * (long) storage_size);
        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);

        if (intersect_popcount >= min_popcount) {
          score = ((double) intersect_popcount) / (popcount_sum - intersect_popcount);
	  /* The previous test is slighly too wide. Test again to be certain. */
	  if (score >= threshold) {
	    /* Add to the upper triangle */
	    if (!chemfp_add_hit(results+query_index, target_index, score)) {
	      add_hit_error = 1;
	    }
	  }
        }
      }
    }
  } /* went through each of the queries */
  if (add_hit_error) {
    return CHEMFP_NO_MEM;
  }
  return CHEMFP_OK;
}

/* I couldn't figure out a way to take advantage of symmetry */
/* This is the same as the NxM algorithm except that it excludes self-matches */
int RENAME(chemfp_knearest_tanimoto_arena_symmetric)(
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
        chemfp_search_result *results
                                   ) {

  int fp_size;
  int query_popcount, target_popcount, intersect_popcount;
  double score, best_possible_score, query_threshold;
  int popcount_sum, min_popcount;
  const unsigned char *query_fp, *target_fp;
  int query_index, target_index;
  int start, end;
  PopcountSearchOrder popcount_order;
  chemfp_search_result *result;
  int add_hit_error = 0;
  chemfp_popcount_f calc_popcount;
  chemfp_intersect_popcount_f calc_intersect_popcount;

  if (query_start >= query_end) {
    return 0;
  }
  /* k == 0 is a valid input, and of course the result is no matches */
  if (k == 0) {
    return CHEMFP_OK;
  }
  fp_size = (num_bits+7)/8;

  /* Prevent overflow if someone uses a threshold of, say, 1E-80 */
  /* The smallest possible positive score is 1/num_bits so */
  /* scale up too-small values to one that's more reasonable */
  if (threshold > 0.0 && threshold < 1.0/num_bits) {
    threshold = 0.5 / num_bits;
  }

  /* Choose popcounts optimized for this case */
  calc_popcount = chemfp_select_popcount(num_bits, storage_size, arena);
  calc_intersect_popcount = chemfp_select_intersect_popcount(
                num_bits, storage_size, arena, storage_size, arena);

  /* Loop through the query fingerprints */
#if USE_OPENMP == 1
  #pragma omp parallel for \
    private(result, query_fp, query_threshold, query_popcount, popcount_order, \
          target_popcount, best_possible_score, start, end, target_fp, \
            popcount_sum, min_popcount, target_index, intersect_popcount, score) \
      schedule(dynamic)
#endif
  for (query_index=query_start; query_index < query_end; query_index++) {
    result = results+(query_index-query_start);
    query_fp = arena + query_index * (long) storage_size;

    query_threshold = threshold;
    query_popcount = calc_popcount(fp_size, query_fp);

    if (query_popcount == 0) {
      if (threshold == 0.0) {
	/* Return the first k. This is chemically meaningless. */
	for (target_index=target_start; target_index<target_end; target_index++) {
	  if (query_index != target_index) {
	    if (!chemfp_add_hit(result, target_index, 0.0)) {
	      add_hit_error = 1;
	    }
	    if (result->num_hits >= k) {
	      break;
	    }
	  }
	}
	/* Need to heapify it. */
	chemfp_heapq_heapify(result->num_hits, result, (chemfp_heapq_lt) double_score_lt,
			     (chemfp_heapq_swap) double_score_swap);
	continue;
      }
      /* By definition this will not match anything. */
      continue;
    }

    /* Search the bins using the ordering from Swamidass and Baldi.*/
    init_search_order(&popcount_order, query_popcount, num_bits);

    /* Look through the sections of the arena in optimal popcount order */
    while (next_popcount(&popcount_order, query_threshold)) {
      target_popcount = popcount_order.popcount;
      best_possible_score = popcount_order.score;

      /* If we can't beat the query threshold then we're done with the targets */
      if (best_possible_score < query_threshold) {
        break;
      }

      /* Scan through the targets which have the given popcount */
      start = popcount_indices[target_popcount];
      end = popcount_indices[target_popcount+1];

      if (!check_bounds(&popcount_order, &start, &end, target_start, target_end)) {
        continue;
      }

      /* Iterate over the target fingerprints */
      target_fp = arena + start * (long) storage_size;
      popcount_sum = query_popcount + target_popcount;
      min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, query_threshold);

      target_index = start;

      /* There are fewer than 'k' elements in the heap*/
      if (result->num_hits < k) {
        for (; target_index<end; target_index++, target_fp += storage_size) {
          intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
          if (intersect_popcount >= min_popcount) {
            score = ((double) intersect_popcount) / (popcount_sum - intersect_popcount);

            /* The heap isn't full; only check if we're at or above the query threshold */
            if (score >= query_threshold) {
              if (query_index == target_index) {
                continue; /* Don't match self */
              }
              if (!chemfp_add_hit(result, target_index, score)) {
                add_hit_error = 1;
              }
              if (result->num_hits == k) {
                chemfp_heapq_heapify(k, result,  (chemfp_heapq_lt) double_score_lt,
                                     (chemfp_heapq_swap) double_score_swap);
                query_threshold = result->scores[0];
                min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, query_threshold);
                
                /* We're going to jump to the "heap is full" section */
                /* Since we leave the loop early, I need to advance the pointers */
                target_index++;
                target_fp += storage_size;
                goto heap_replace;
              }
            } /* Added to heap */
          } /* fast rejection test */
        } /* Went through target fingerprints */

        /* If we're here then the heap did not fill up. Try the next popcount */
        continue;
      }

    heap_replace:
      /* We only get here if the heap contains k element */

      /* Earlier we tested for "best_possible_score<query_threshold". */
      /* The test to replace an element in the heap is more stringent. */
      if (query_threshold >= best_possible_score) {
        /* Can't do better. Might as well give up. */
        break;
      }

      /* Scan through the target fingerprints; can we improve over the threshold? */
      for (; target_index<end; target_index++, target_fp += storage_size) {

        intersect_popcount = calc_intersect_popcount(fp_size, query_fp, target_fp);
        if (intersect_popcount >= min_popcount) {
          score = ((double) intersect_popcount) / (popcount_sum - intersect_popcount);

          /* We need to be strictly *better* than what's in the heap */
          if (score > query_threshold) {
            if (query_index == target_index) {
              continue; /* Don't match self */
            }
            result->indices[0] = target_index;
            result->scores[0] = score;
            chemfp_heapq_siftup(k, result, 0, (chemfp_heapq_lt) double_score_lt,
                                (chemfp_heapq_swap) double_score_swap);
            query_threshold = result->scores[0];
            if (query_threshold >= best_possible_score) {
              /* we can't do any better in this section (or in later ones) */
              break;
            }
            min_popcount = chemfp_get_min_intersect_popcount(popcount_sum, query_threshold);
          } /* heapreplaced the old smallest item with the new item */
        } /* fast integer rejection test */
      } /* looped over fingerprints */
    } /* Went through all the popcount regions */

    /* We have scanned all the fingerprints. Is the heap full? */
    if (result->num_hits < k) {
      /* Not full, so need to heapify it. */
      chemfp_heapq_heapify(result->num_hits, result, (chemfp_heapq_lt) double_score_lt,
                           (chemfp_heapq_swap) double_score_swap);
    }
  } /* looped over all queries */
  if (add_hit_error) {
    return CHEMFP_NO_MEM;
  }
  return CHEMFP_OK;
}

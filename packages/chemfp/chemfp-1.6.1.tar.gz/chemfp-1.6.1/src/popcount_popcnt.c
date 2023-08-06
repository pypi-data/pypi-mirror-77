/* 
# Copyright (c) 2011-2018 Andrew Dalke Scientific, AB (Sweden)
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
/**
 * @brief   Contains portable popcount functions using the POPCNT
 *          (SSE4.2) instruction for molecular fingerprints.
 * @author  Kim Walisch, <kim.walisch@gmail.com>
 * @version 1.0
 * @date    2011
 *
 * The code within this file has been tested successfully with the
 * following compilers and operating systems:
 *
 * GNU GCC 4.4                    Linux i386 & x86-64 
 * LLVM clang 2.8,                Linux i386 & x86-64
 * Oracle Solaris Studio 12.2,    Linux i386 & x86-64
 * Intel C++ Composer XE 2011,    Linux i386 & x86-64, Windows 7 64-bit
 * GNU GCC 3.3,                   VMware Linux i386
 * GNU GCC 4.6,                   VMware Linux i386 & x86-64
 * Apple llvm-gcc-4.2,            Mac OS X 10.7
 * Apple clang version 3.0,       Mac OS X 10.7
 * Microsoft Visual Studio 2010,  Windows 7 64-bit
 * MinGW-w64 GCC 4.6,             Windows 7 64-bit
 */

#include "popcount.h"
#include <stdint.h>
#include <stdio.h>

#if defined(_MSC_VER) && (defined(_WIN32) || defined(_WIN64))
  #include <nmmintrin.h> /* _mm_popcnt_u32(), _mm_popcnt_u64() */
#endif

/** Convenience functions for the POPCNT instruction. */

#if defined(_MSC_VER) && defined(_WIN64)
static uint64_t POPCNT64(uint64_t x) {
  return _mm_popcnt_u64(x);
}
#elif defined(_MSC_VER) && defined(_WIN32)
static uint32_t POPCNT32(uint32_t x) {
  return _mm_popcnt_u32(x);
}
#elif defined(__x86_64__)
static uint64_t POPCNT64(uint64_t x) {
/* GNU GCC >= 4.2 supports the POPCNT instruction */
/* APD: Apple's gcc-4.0 supports POPCNT and RHEL5's gcc-4.1 supports POPCNT */
/* I'll assume that 4.2 is good enough. Is there a better feature test for this? */
#if !defined(__GNUC__) || (__GNUC__ >= 4 && __GNUC_MINOR__ >= 1)
  __asm__ ("popcnt %1, %0" : "=r" (x) : "0" (x));
#endif
  return x;
}
#elif defined(__i386__) || defined(__i386)
static uint32_t POPCNT32(uint32_t x) {
/* GNU GCC >= 4.2 supports the POPCNT instruction */
#if !defined(__GNUC__) || (__GNUC__ >= 4 && __GNUC_MINOR__ >= 1)
  __asm__ ("popcnt %1, %0" : "=r" (x) : "0" (x));
#endif
  return x;
}
#endif

/**
 * Count the number of bits set in a fingerprint using the
 * the POPCNT (SSE4.2) instruction.
 * @warning  Use (get_cpuid_flags() & bit_POPCNT) to test if
 *           the CPU supports the POPCNT instruction.
 */
int chemfp_popcount_popcnt(int size, const uint64_t *fp) {
  int bit_count = 0;
  int i;
#if defined(_WIN64) || defined(__x86_64__)
  size = (size + 7) / 8;
  for (i = 0; i < size; i++)
    bit_count += (int) POPCNT64(fp[i]);
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  size = (size + 3) / 4;
  for (i = 0; i < size; i++)
    bit_count += (int) POPCNT32(fp_32[i]);
#else
  UNUSED(size);
  UNUSED(fp);
  i=0;
#endif
  return bit_count;
}

/**
 * Count the number of bits set within the intersection of two
 * fingerprints using the POPCNT (SSE4.2) instruction.
 * @warning  Use (get_cpuid_flags() & bit_POPCNT) to test if
 *           the CPU supports the POPCNT instruction.
 */
int chemfp_intersect_popcount_popcnt(int size, const uint64_t *fp1, const uint64_t *fp2) {
  int bit_count = 0;
  int i;
#if defined(_WIN64) || defined(__x86_64__)
  size = (size + 7) / 8;
  for (i = 0; i < size; i++)
    bit_count += (int) POPCNT64(fp1[i] & fp2[i]);
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  size = (size + 3) / 4;
  for (i = 0; i < size; i++)
    bit_count += (int) POPCNT32(fp1_32[i] & fp2_32[i]);
#else
  UNUSED(size);
  UNUSED(fp1);
  UNUSED(fp2);
  i=0;
#endif
  return bit_count;
}

/******* Special POPCNT cases *****/

/* popcount (64 bits) */
int
chemfp_popcount_popcnt_8(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (64 bits) */
int
chemfp_intersect_popcount_popcnt_8(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (128 bits) */
int
chemfp_popcount_popcnt_16(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT32(fp_32[ 3])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (128 bits) */
int
chemfp_intersect_popcount_popcnt_16(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (192 bits) */
int
chemfp_popcount_popcnt_24(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT32(fp_32[ 5])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (192 bits) */
int
chemfp_intersect_popcount_popcnt_24(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (256 bits) */
int
chemfp_popcount_popcnt_32(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT32(fp_32[ 7])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (256 bits) */
int
chemfp_intersect_popcount_popcnt_32(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (320 bits) */
int
chemfp_popcount_popcnt_40(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT32(fp_32[ 9])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (320 bits) */
int
chemfp_intersect_popcount_popcnt_40(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (384 bits) */
int
chemfp_popcount_popcnt_48(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT32(fp_32[11])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (384 bits) */
int
chemfp_intersect_popcount_popcnt_48(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT32(fp1_32[11] & fp2_32[11])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (448 bits) */
int
chemfp_popcount_popcnt_56(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT32(fp_32[13])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (448 bits) */
int
chemfp_intersect_popcount_popcnt_56(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT32(fp1_32[13] & fp2_32[13])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (512 bits) */
int
chemfp_popcount_popcnt_64(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT32(fp_32[15])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (512 bits) */
int
chemfp_intersect_popcount_popcnt_64(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT32(fp1_32[15] & fp2_32[15])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (576 bits) */
int
chemfp_popcount_popcnt_72(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])) +
          ((int) POPCNT64(fp[ 8])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT64(fp_32[15])) +
          ((int) POPCNT64(fp_32[16])) +
          ((int) POPCNT32(fp_32[17])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (576 bits) */
int
chemfp_intersect_popcount_popcnt_72(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
          ((int) POPCNT64(fp1[ 8] & fp2[ 8])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT64(fp1_32[15] & fp2_32[15])) +
          ((int) POPCNT64(fp1_32[16] & fp2_32[16])) +
          ((int) POPCNT32(fp1_32[17] & fp2_32[17])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (640 bits) */
int
chemfp_popcount_popcnt_80(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])) +
          ((int) POPCNT64(fp[ 8])) +
          ((int) POPCNT64(fp[ 9])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT64(fp_32[15])) +
          ((int) POPCNT64(fp_32[16])) +
          ((int) POPCNT64(fp_32[17])) +
          ((int) POPCNT64(fp_32[18])) +
          ((int) POPCNT32(fp_32[19])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (640 bits) */
int
chemfp_intersect_popcount_popcnt_80(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
          ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
          ((int) POPCNT64(fp1[ 9] & fp2[ 9])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT64(fp1_32[15] & fp2_32[15])) +
          ((int) POPCNT64(fp1_32[16] & fp2_32[16])) +
          ((int) POPCNT64(fp1_32[17] & fp2_32[17])) +
          ((int) POPCNT64(fp1_32[18] & fp2_32[18])) +
          ((int) POPCNT32(fp1_32[19] & fp2_32[19])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (704 bits) */
int
chemfp_popcount_popcnt_88(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])) +
          ((int) POPCNT64(fp[ 8])) +
          ((int) POPCNT64(fp[ 9])) +
          ((int) POPCNT64(fp[10])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT64(fp_32[15])) +
          ((int) POPCNT64(fp_32[16])) +
          ((int) POPCNT64(fp_32[17])) +
          ((int) POPCNT64(fp_32[18])) +
          ((int) POPCNT64(fp_32[19])) +
          ((int) POPCNT64(fp_32[20])) +
          ((int) POPCNT32(fp_32[21])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (704 bits) */
int
chemfp_intersect_popcount_popcnt_88(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
          ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
          ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
          ((int) POPCNT64(fp1[10] & fp2[10])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT64(fp1_32[15] & fp2_32[15])) +
          ((int) POPCNT64(fp1_32[16] & fp2_32[16])) +
          ((int) POPCNT64(fp1_32[17] & fp2_32[17])) +
          ((int) POPCNT64(fp1_32[18] & fp2_32[18])) +
          ((int) POPCNT64(fp1_32[19] & fp2_32[19])) +
          ((int) POPCNT64(fp1_32[20] & fp2_32[20])) +
          ((int) POPCNT32(fp1_32[21] & fp2_32[21])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (768 bits) */
int
chemfp_popcount_popcnt_96(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])) +
          ((int) POPCNT64(fp[ 8])) +
          ((int) POPCNT64(fp[ 9])) +
          ((int) POPCNT64(fp[10])) +
          ((int) POPCNT64(fp[11])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT64(fp_32[15])) +
          ((int) POPCNT64(fp_32[16])) +
          ((int) POPCNT64(fp_32[17])) +
          ((int) POPCNT64(fp_32[18])) +
          ((int) POPCNT64(fp_32[19])) +
          ((int) POPCNT64(fp_32[20])) +
          ((int) POPCNT64(fp_32[21])) +
          ((int) POPCNT64(fp_32[22])) +
          ((int) POPCNT32(fp_32[23])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (768 bits) */
int
chemfp_intersect_popcount_popcnt_96(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
          ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
          ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
          ((int) POPCNT64(fp1[10] & fp2[10])) +
          ((int) POPCNT64(fp1[11] & fp2[11])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT64(fp1_32[15] & fp2_32[15])) +
          ((int) POPCNT64(fp1_32[16] & fp2_32[16])) +
          ((int) POPCNT64(fp1_32[17] & fp2_32[17])) +
          ((int) POPCNT64(fp1_32[18] & fp2_32[18])) +
          ((int) POPCNT64(fp1_32[19] & fp2_32[19])) +
          ((int) POPCNT64(fp1_32[20] & fp2_32[20])) +
          ((int) POPCNT64(fp1_32[21] & fp2_32[21])) +
          ((int) POPCNT64(fp1_32[22] & fp2_32[22])) +
          ((int) POPCNT32(fp1_32[23] & fp2_32[23])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (832 bits) */
int
chemfp_popcount_popcnt_104(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])) +
          ((int) POPCNT64(fp[ 8])) +
          ((int) POPCNT64(fp[ 9])) +
          ((int) POPCNT64(fp[10])) +
          ((int) POPCNT64(fp[11])) +
          ((int) POPCNT64(fp[12])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT64(fp_32[15])) +
          ((int) POPCNT64(fp_32[16])) +
          ((int) POPCNT64(fp_32[17])) +
          ((int) POPCNT64(fp_32[18])) +
          ((int) POPCNT64(fp_32[19])) +
          ((int) POPCNT64(fp_32[20])) +
          ((int) POPCNT64(fp_32[21])) +
          ((int) POPCNT64(fp_32[22])) +
          ((int) POPCNT64(fp_32[23])) +
          ((int) POPCNT64(fp_32[24])) +
          ((int) POPCNT32(fp_32[25])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (832 bits) */
int
chemfp_intersect_popcount_popcnt_104(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
          ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
          ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
          ((int) POPCNT64(fp1[10] & fp2[10])) +
          ((int) POPCNT64(fp1[11] & fp2[11])) +
          ((int) POPCNT64(fp1[12] & fp2[12])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT64(fp1_32[15] & fp2_32[15])) +
          ((int) POPCNT64(fp1_32[16] & fp2_32[16])) +
          ((int) POPCNT64(fp1_32[17] & fp2_32[17])) +
          ((int) POPCNT64(fp1_32[18] & fp2_32[18])) +
          ((int) POPCNT64(fp1_32[19] & fp2_32[19])) +
          ((int) POPCNT64(fp1_32[20] & fp2_32[20])) +
          ((int) POPCNT64(fp1_32[21] & fp2_32[21])) +
          ((int) POPCNT64(fp1_32[22] & fp2_32[22])) +
          ((int) POPCNT64(fp1_32[23] & fp2_32[23])) +
          ((int) POPCNT64(fp1_32[24] & fp2_32[24])) +
          ((int) POPCNT32(fp1_32[25] & fp2_32[25])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (896 bits) */
int
chemfp_popcount_popcnt_112(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])) +
          ((int) POPCNT64(fp[ 8])) +
          ((int) POPCNT64(fp[ 9])) +
          ((int) POPCNT64(fp[10])) +
          ((int) POPCNT64(fp[11])) +
          ((int) POPCNT64(fp[12])) +
          ((int) POPCNT64(fp[13])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT64(fp_32[15])) +
          ((int) POPCNT64(fp_32[16])) +
          ((int) POPCNT64(fp_32[17])) +
          ((int) POPCNT64(fp_32[18])) +
          ((int) POPCNT64(fp_32[19])) +
          ((int) POPCNT64(fp_32[20])) +
          ((int) POPCNT64(fp_32[21])) +
          ((int) POPCNT64(fp_32[22])) +
          ((int) POPCNT64(fp_32[23])) +
          ((int) POPCNT64(fp_32[24])) +
          ((int) POPCNT64(fp_32[25])) +
          ((int) POPCNT64(fp_32[26])) +
          ((int) POPCNT32(fp_32[27])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (896 bits) */
int
chemfp_intersect_popcount_popcnt_112(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
          ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
          ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
          ((int) POPCNT64(fp1[10] & fp2[10])) +
          ((int) POPCNT64(fp1[11] & fp2[11])) +
          ((int) POPCNT64(fp1[12] & fp2[12])) +
          ((int) POPCNT64(fp1[13] & fp2[13])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT64(fp1_32[15] & fp2_32[15])) +
          ((int) POPCNT64(fp1_32[16] & fp2_32[16])) +
          ((int) POPCNT64(fp1_32[17] & fp2_32[17])) +
          ((int) POPCNT64(fp1_32[18] & fp2_32[18])) +
          ((int) POPCNT64(fp1_32[19] & fp2_32[19])) +
          ((int) POPCNT64(fp1_32[20] & fp2_32[20])) +
          ((int) POPCNT64(fp1_32[21] & fp2_32[21])) +
          ((int) POPCNT64(fp1_32[22] & fp2_32[22])) +
          ((int) POPCNT64(fp1_32[23] & fp2_32[23])) +
          ((int) POPCNT64(fp1_32[24] & fp2_32[24])) +
          ((int) POPCNT64(fp1_32[25] & fp2_32[25])) +
          ((int) POPCNT64(fp1_32[26] & fp2_32[26])) +
          ((int) POPCNT32(fp1_32[27] & fp2_32[27])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (960 bits) */
int
chemfp_popcount_popcnt_120(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])) +
          ((int) POPCNT64(fp[ 8])) +
          ((int) POPCNT64(fp[ 9])) +
          ((int) POPCNT64(fp[10])) +
          ((int) POPCNT64(fp[11])) +
          ((int) POPCNT64(fp[12])) +
          ((int) POPCNT64(fp[13])) +
          ((int) POPCNT64(fp[14])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT64(fp_32[15])) +
          ((int) POPCNT64(fp_32[16])) +
          ((int) POPCNT64(fp_32[17])) +
          ((int) POPCNT64(fp_32[18])) +
          ((int) POPCNT64(fp_32[19])) +
          ((int) POPCNT64(fp_32[20])) +
          ((int) POPCNT64(fp_32[21])) +
          ((int) POPCNT64(fp_32[22])) +
          ((int) POPCNT64(fp_32[23])) +
          ((int) POPCNT64(fp_32[24])) +
          ((int) POPCNT64(fp_32[25])) +
          ((int) POPCNT64(fp_32[26])) +
          ((int) POPCNT64(fp_32[27])) +
          ((int) POPCNT64(fp_32[28])) +
          ((int) POPCNT32(fp_32[29])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (960 bits) */
int
chemfp_intersect_popcount_popcnt_120(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
          ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
          ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
          ((int) POPCNT64(fp1[10] & fp2[10])) +
          ((int) POPCNT64(fp1[11] & fp2[11])) +
          ((int) POPCNT64(fp1[12] & fp2[12])) +
          ((int) POPCNT64(fp1[13] & fp2[13])) +
          ((int) POPCNT64(fp1[14] & fp2[14])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT64(fp1_32[15] & fp2_32[15])) +
          ((int) POPCNT64(fp1_32[16] & fp2_32[16])) +
          ((int) POPCNT64(fp1_32[17] & fp2_32[17])) +
          ((int) POPCNT64(fp1_32[18] & fp2_32[18])) +
          ((int) POPCNT64(fp1_32[19] & fp2_32[19])) +
          ((int) POPCNT64(fp1_32[20] & fp2_32[20])) +
          ((int) POPCNT64(fp1_32[21] & fp2_32[21])) +
          ((int) POPCNT64(fp1_32[22] & fp2_32[22])) +
          ((int) POPCNT64(fp1_32[23] & fp2_32[23])) +
          ((int) POPCNT64(fp1_32[24] & fp2_32[24])) +
          ((int) POPCNT64(fp1_32[25] & fp2_32[25])) +
          ((int) POPCNT64(fp1_32[26] & fp2_32[26])) +
          ((int) POPCNT64(fp1_32[27] & fp2_32[27])) +
          ((int) POPCNT64(fp1_32[28] & fp2_32[28])) +
          ((int) POPCNT32(fp1_32[29] & fp2_32[29])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/* popcount (1024 bits) */
int
chemfp_popcount_popcnt_128(ssize_t size, const uint64_t *fp) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp[ 0])) +
          ((int) POPCNT64(fp[ 1])) +
          ((int) POPCNT64(fp[ 2])) +
          ((int) POPCNT64(fp[ 3])) +
          ((int) POPCNT64(fp[ 4])) +
          ((int) POPCNT64(fp[ 5])) +
          ((int) POPCNT64(fp[ 6])) +
          ((int) POPCNT64(fp[ 7])) +
          ((int) POPCNT64(fp[ 8])) +
          ((int) POPCNT64(fp[ 9])) +
          ((int) POPCNT64(fp[10])) +
          ((int) POPCNT64(fp[11])) +
          ((int) POPCNT64(fp[12])) +
          ((int) POPCNT64(fp[13])) +
          ((int) POPCNT64(fp[14])) +
          ((int) POPCNT64(fp[15])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  UNUSED(size);
  return (((int) POPCNT32(fp_32[ 0])) +
          ((int) POPCNT64(fp_32[ 1])) +
          ((int) POPCNT64(fp_32[ 2])) +
          ((int) POPCNT64(fp_32[ 3])) +
          ((int) POPCNT64(fp_32[ 4])) +
          ((int) POPCNT64(fp_32[ 5])) +
          ((int) POPCNT64(fp_32[ 6])) +
          ((int) POPCNT64(fp_32[ 7])) +
          ((int) POPCNT64(fp_32[ 8])) +
          ((int) POPCNT64(fp_32[ 9])) +
          ((int) POPCNT64(fp_32[10])) +
          ((int) POPCNT64(fp_32[11])) +
          ((int) POPCNT64(fp_32[12])) +
          ((int) POPCNT64(fp_32[13])) +
          ((int) POPCNT64(fp_32[14])) +
          ((int) POPCNT64(fp_32[15])) +
          ((int) POPCNT64(fp_32[16])) +
          ((int) POPCNT64(fp_32[17])) +
          ((int) POPCNT64(fp_32[18])) +
          ((int) POPCNT64(fp_32[19])) +
          ((int) POPCNT64(fp_32[20])) +
          ((int) POPCNT64(fp_32[21])) +
          ((int) POPCNT64(fp_32[22])) +
          ((int) POPCNT64(fp_32[23])) +
          ((int) POPCNT64(fp_32[24])) +
          ((int) POPCNT64(fp_32[25])) +
          ((int) POPCNT64(fp_32[26])) +
          ((int) POPCNT64(fp_32[27])) +
          ((int) POPCNT64(fp_32[28])) +
          ((int) POPCNT64(fp_32[29])) +
          ((int) POPCNT64(fp_32[30])) +
          ((int) POPCNT32(fp_32[31])));
#else
  UNUSED(fp);
  return 0;
#endif
}

/* intersection popcount (1024 bits) */
int
chemfp_intersect_popcount_popcnt_128(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
#if defined(_WIN64) || defined(__x86_64__)
  UNUSED(size);
  return (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
          ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
          ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
          ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
          ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
          ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
          ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
          ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
          ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
          ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
          ((int) POPCNT64(fp1[10] & fp2[10])) +
          ((int) POPCNT64(fp1[11] & fp2[11])) +
          ((int) POPCNT64(fp1[12] & fp2[12])) +
          ((int) POPCNT64(fp1[13] & fp2[13])) +
          ((int) POPCNT64(fp1[14] & fp2[14])) +
          ((int) POPCNT64(fp1[15] & fp2[15])));
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  UNUSED(size);
  return (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
          ((int) POPCNT64(fp1_32[ 1] & fp2_32[ 1])) +
          ((int) POPCNT64(fp1_32[ 2] & fp2_32[ 2])) +
          ((int) POPCNT64(fp1_32[ 3] & fp2_32[ 3])) +
          ((int) POPCNT64(fp1_32[ 4] & fp2_32[ 4])) +
          ((int) POPCNT64(fp1_32[ 5] & fp2_32[ 5])) +
          ((int) POPCNT64(fp1_32[ 6] & fp2_32[ 6])) +
          ((int) POPCNT64(fp1_32[ 7] & fp2_32[ 7])) +
          ((int) POPCNT64(fp1_32[ 8] & fp2_32[ 8])) +
          ((int) POPCNT64(fp1_32[ 9] & fp2_32[ 9])) +
          ((int) POPCNT64(fp1_32[10] & fp2_32[10])) +
          ((int) POPCNT64(fp1_32[11] & fp2_32[11])) +
          ((int) POPCNT64(fp1_32[12] & fp2_32[12])) +
          ((int) POPCNT64(fp1_32[13] & fp2_32[13])) +
          ((int) POPCNT64(fp1_32[14] & fp2_32[14])) +
          ((int) POPCNT64(fp1_32[15] & fp2_32[15])) +
          ((int) POPCNT64(fp1_32[16] & fp2_32[16])) +
          ((int) POPCNT64(fp1_32[17] & fp2_32[17])) +
          ((int) POPCNT64(fp1_32[18] & fp2_32[18])) +
          ((int) POPCNT64(fp1_32[19] & fp2_32[19])) +
          ((int) POPCNT64(fp1_32[20] & fp2_32[20])) +
          ((int) POPCNT64(fp1_32[21] & fp2_32[21])) +
          ((int) POPCNT64(fp1_32[22] & fp2_32[22])) +
          ((int) POPCNT64(fp1_32[23] & fp2_32[23])) +
          ((int) POPCNT64(fp1_32[24] & fp2_32[24])) +
          ((int) POPCNT64(fp1_32[25] & fp2_32[25])) +
          ((int) POPCNT64(fp1_32[26] & fp2_32[26])) +
          ((int) POPCNT64(fp1_32[27] & fp2_32[27])) +
          ((int) POPCNT64(fp1_32[28] & fp2_32[28])) +
          ((int) POPCNT64(fp1_32[29] & fp2_32[29])) +
          ((int) POPCNT64(fp1_32[30] & fp2_32[30])) +
          ((int) POPCNT32(fp1_32[31] & fp2_32[31])));
#else
  UNUSED(fp1);
  UNUSED(fp2);
  return 0;
#endif
}

/**** Multiples ****/

/** 1024 + 1024*n bits (popcount) **/
int
chemfp_popcount_popcnt_128_128(ssize_t size, const uint64_t *fp) {
  int bit_count = 0;
  int i;
  ssize_t rounded_size;
#if defined(_WIN64) || defined(__x86_64__)
  rounded_size = (size + 127) / 128 * 16;
  for (i=0; i<rounded_size; i+= 16, fp += 16) {
    bit_count +=  (((int) POPCNT64(fp[ 0])) +
                   ((int) POPCNT64(fp[ 1])) +
                   ((int) POPCNT64(fp[ 2])) +
                   ((int) POPCNT64(fp[ 3])) +
                   ((int) POPCNT64(fp[ 4])) +
                   ((int) POPCNT64(fp[ 5])) +
                   ((int) POPCNT64(fp[ 6])) +
                   ((int) POPCNT64(fp[ 7])) +
                   ((int) POPCNT64(fp[ 8])) +
                   ((int) POPCNT64(fp[ 9])) +
                   ((int) POPCNT64(fp[10])) +
                   ((int) POPCNT64(fp[11])) +
                   ((int) POPCNT64(fp[12])) +
                   ((int) POPCNT64(fp[13])) +
                   ((int) POPCNT64(fp[14])) +
                   ((int) POPCNT64(fp[15])));
  }

#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  rounded_size = (size + 127) / 128 * 32;
  for (i=0; i<rounded_size; i+= 32, fp_32 += 32) {
    bit_count +=  (((int) POPCNT32(fp_32[ 0])) +
                   ((int) POPCNT32(fp_32[ 1])) +
                   ((int) POPCNT32(fp_32[ 2])) +
                   ((int) POPCNT32(fp_32[ 3])) +
                   ((int) POPCNT32(fp_32[ 4])) +
                   ((int) POPCNT32(fp_32[ 5])) +
                   ((int) POPCNT32(fp_32[ 6])) +
                   ((int) POPCNT32(fp_32[ 7])) +
                   ((int) POPCNT32(fp_32[ 8])) +
                   ((int) POPCNT32(fp_32[ 9])) +
                   ((int) POPCNT32(fp_32[10])) +
                   ((int) POPCNT32(fp_32[11])) +
                   ((int) POPCNT32(fp_32[12])) +
                   ((int) POPCNT32(fp_32[13])) +
                   ((int) POPCNT32(fp_32[14])) +
                   ((int) POPCNT32(fp_32[15])) +
                   ((int) POPCNT32(fp_32[16])) +
                   ((int) POPCNT32(fp_32[17])) +
                   ((int) POPCNT32(fp_32[18])) +
                   ((int) POPCNT32(fp_32[19])) +
                   ((int) POPCNT32(fp_32[20])) +
                   ((int) POPCNT32(fp_32[21])) +
                   ((int) POPCNT32(fp_32[22])) +
                   ((int) POPCNT32(fp_32[23])) +
                   ((int) POPCNT32(fp_32[24])) +
                   ((int) POPCNT32(fp_32[25])) +
                   ((int) POPCNT32(fp_32[26])) +
                   ((int) POPCNT32(fp_32[27])) +
                   ((int) POPCNT32(fp_32[28])) +
                   ((int) POPCNT32(fp_32[29])) +
                   ((int) POPCNT32(fp_32[30])) +
                   ((int) POPCNT32(fp_32[31])));
  }
#else
  UNUSED(fp1);
  UNUSED(fp2);
  UNUSED(count);
  UNUSED(i);
  UNUSED(rounded_size);
#endif
  return bit_count;
}

/** 1024 + 1024*n bits (intersection) **/
int
chemfp_intersect_popcount_popcnt_128_128(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
  int bit_count = 0;
  int i;
  ssize_t rounded_size;
#if defined(_WIN64) || defined(__x86_64__)
  rounded_size = (size + 127) / 128 * 16;
  for (i=0; i<rounded_size; i += 16, fp1 += 16, fp2 += 16) {
    bit_count += (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
                  ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
                  ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
                  ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
                  ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
                  ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
                  ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
                  ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
                  ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
                  ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
                  ((int) POPCNT64(fp1[10] & fp2[10])) +
                  ((int) POPCNT64(fp1[11] & fp2[11])) +
                  ((int) POPCNT64(fp1[12] & fp2[12])) +
                  ((int) POPCNT64(fp1[13] & fp2[13])) +
                  ((int) POPCNT64(fp1[14] & fp2[14])) +
                  ((int) POPCNT64(fp1[15] & fp2[15])));
  }

#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  rounded_size = (size + 127) / 128 * 32;
  for (i=0; i<rounded_size; i+= 32, fp1_32 += 32, fp2_32 += 32) {
    bit_count += (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
                  ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
                  ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
                  ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
                  ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
                  ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
                  ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
                  ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
                  ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
                  ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
                  ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
                  ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
                  ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
                  ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
                  ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
                  ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
                  ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
                  ((int) POPCNT32(fp1_32[17] & fp2_32[17])) +
                  ((int) POPCNT32(fp1_32[18] & fp2_32[18])) +
                  ((int) POPCNT32(fp1_32[19] & fp2_32[19])) +
                  ((int) POPCNT32(fp1_32[20] & fp2_32[20])) +
                  ((int) POPCNT32(fp1_32[21] & fp2_32[21])) +
                  ((int) POPCNT32(fp1_32[22] & fp2_32[22])) +
                  ((int) POPCNT32(fp1_32[23] & fp2_32[23])) +
                  ((int) POPCNT32(fp1_32[24] & fp2_32[24])) +
                  ((int) POPCNT32(fp1_32[25] & fp2_32[25])) +
                  ((int) POPCNT32(fp1_32[26] & fp2_32[26])) +
                  ((int) POPCNT32(fp1_32[27] & fp2_32[27])) +
                  ((int) POPCNT32(fp1_32[28] & fp2_32[28])) +
                  ((int) POPCNT32(fp1_32[29] & fp2_32[29])) +
                  ((int) POPCNT32(fp1_32[30] & fp2_32[30])) +
                  ((int) POPCNT32(fp1_32[31] & fp2_32[31])));
  }
#else
  UNUSED(fp1);
  UNUSED(fp2);
  UNUSED(i);
  UNUSED(rounded_size);
#endif
  return bit_count;
}

/** 1024 + 8*i (intersect) **/
int
chemfp_popcount_popcnt_128_8(ssize_t size, const uint64_t *fp) {
  int bit_count = 0;
  int i;
  ssize_t rounded_size;
#if defined(_WIN64) || defined(__x86_64__)
  rounded_size = (size / 128) * 16;
  for (i=0; i<rounded_size; i+= 16, fp += 16) {
    bit_count +=  (((int) POPCNT64(fp[ 0])) +
                   ((int) POPCNT64(fp[ 1])) +
                   ((int) POPCNT64(fp[ 2])) +
                   ((int) POPCNT64(fp[ 3])) +
                   ((int) POPCNT64(fp[ 4])) +
                   ((int) POPCNT64(fp[ 5])) +
                   ((int) POPCNT64(fp[ 6])) +
                   ((int) POPCNT64(fp[ 7])) +
                   ((int) POPCNT64(fp[ 8])) +
                   ((int) POPCNT64(fp[ 9])) +
                   ((int) POPCNT64(fp[10])) +
                   ((int) POPCNT64(fp[11])) +
                   ((int) POPCNT64(fp[12])) +
                   ((int) POPCNT64(fp[13])) +
                   ((int) POPCNT64(fp[14])) +
                   ((int) POPCNT64(fp[15])));
  }
  switch ((size+7) / 8 - rounded_size) {
  case  0: break;
  case  1: bit_count += (
      ((int) POPCNT64(fp[ 0]))  );
      break;
      
  case  2: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1]))  );
      break;

  case  3: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2]))  );
      break;

  case  4: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3]))  );
      break;

  case  5: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4]))  );
      break;

  case  6: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5]))  );
      break;

  case  7: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6]))  );
      break;

  case  8: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6])) +
      ((int) POPCNT64(fp[ 7]))  );
      break;

  case  9: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6])) +
      ((int) POPCNT64(fp[ 7])) +
      ((int) POPCNT64(fp[ 8]))  );
      break;

  case 10: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6])) +
      ((int) POPCNT64(fp[ 7])) +
      ((int) POPCNT64(fp[ 8])) +
      ((int) POPCNT64(fp[ 9]))  );
      break;

  case 11: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6])) +
      ((int) POPCNT64(fp[ 7])) +
      ((int) POPCNT64(fp[ 8])) +
      ((int) POPCNT64(fp[ 9])) +
      ((int) POPCNT64(fp[10]))  );
      break;

  case 12: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6])) +
      ((int) POPCNT64(fp[ 7])) +
      ((int) POPCNT64(fp[ 8])) +
      ((int) POPCNT64(fp[ 9])) +
      ((int) POPCNT64(fp[10])) +
      ((int) POPCNT64(fp[11]))  );
      break;

  case 13: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6])) +
      ((int) POPCNT64(fp[ 7])) +
      ((int) POPCNT64(fp[ 8])) +
      ((int) POPCNT64(fp[ 9])) +
      ((int) POPCNT64(fp[10])) +
      ((int) POPCNT64(fp[11])) +
      ((int) POPCNT64(fp[12]))  );
      break;

  case 14: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6])) +
      ((int) POPCNT64(fp[ 7])) +
      ((int) POPCNT64(fp[ 8])) +
      ((int) POPCNT64(fp[ 9])) +
      ((int) POPCNT64(fp[10])) +
      ((int) POPCNT64(fp[11])) +
      ((int) POPCNT64(fp[12])) +
      ((int) POPCNT64(fp[13]))  );
      break;

  case 15: bit_count += (
      ((int) POPCNT64(fp[ 0])) +
      ((int) POPCNT64(fp[ 1])) +
      ((int) POPCNT64(fp[ 2])) +
      ((int) POPCNT64(fp[ 3])) +
      ((int) POPCNT64(fp[ 4])) +
      ((int) POPCNT64(fp[ 5])) +
      ((int) POPCNT64(fp[ 6])) +
      ((int) POPCNT64(fp[ 7])) +
      ((int) POPCNT64(fp[ 8])) +
      ((int) POPCNT64(fp[ 9])) +
      ((int) POPCNT64(fp[10])) +
      ((int) POPCNT64(fp[11])) +
      ((int) POPCNT64(fp[12])) +
      ((int) POPCNT64(fp[13])) +
      ((int) POPCNT64(fp[14]))  );
      break;
  }
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp_32 = (const uint32_t*) fp;
  rounded_size = (size + 127) / 128 * 32;
  for (i=0; i<rounded_size; i+= 32, fp_32 += 32) {
    bit_count +=  (((int) POPCNT32(fp_32[ 0])) +
                   ((int) POPCNT32(fp_32[ 1])) +
                   ((int) POPCNT32(fp_32[ 2])) +
                   ((int) POPCNT32(fp_32[ 3])) +
                   ((int) POPCNT32(fp_32[ 4])) +
                   ((int) POPCNT32(fp_32[ 5])) +
                   ((int) POPCNT32(fp_32[ 6])) +
                   ((int) POPCNT32(fp_32[ 7])) +
                   ((int) POPCNT32(fp_32[ 8])) +
                   ((int) POPCNT32(fp_32[ 9])) +
                   ((int) POPCNT32(fp_32[10])) +
                   ((int) POPCNT32(fp_32[11])) +
                   ((int) POPCNT32(fp_32[12])) +
                   ((int) POPCNT32(fp_32[13])) +
                   ((int) POPCNT32(fp_32[14])) +
                   ((int) POPCNT32(fp_32[15])) +
                   ((int) POPCNT32(fp_32[16])) +
                   ((int) POPCNT32(fp_32[17])) +
                   ((int) POPCNT32(fp_32[18])) +
                   ((int) POPCNT32(fp_32[19])) +
                   ((int) POPCNT32(fp_32[20])) +
                   ((int) POPCNT32(fp_32[21])) +
                   ((int) POPCNT32(fp_32[22])) +
                   ((int) POPCNT32(fp_32[23])) +
                   ((int) POPCNT32(fp_32[24])) +
                   ((int) POPCNT32(fp_32[25])) +
                   ((int) POPCNT32(fp_32[26])) +
                   ((int) POPCNT32(fp_32[27])) +
                   ((int) POPCNT32(fp_32[28])) +
                   ((int) POPCNT32(fp_32[29])) +
                   ((int) POPCNT32(fp_32[30])) +
                   ((int) POPCNT32(fp_32[31])));
  }
  switch ((size+7) / 8 - rounded_size) {
  case 0: break;
    
  case 1: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1]))   );
      break;
      
  case  2: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 4]))  );
      break;

  case  3: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 6]))  );
      break;

  case  4: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 8]))  );
      break;

  case  5: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[10]))  );
      break;

  case  6: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[12]))  );
      break;

  case  7: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[14]))  );
      break;

  case  8: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[13])) +
      ((int) POPCNT32(fp_32[14])) +
      ((int) POPCNT32(fp_32[16]))  );
      break;

  case  9: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[13])) +
      ((int) POPCNT32(fp_32[14])) +
      ((int) POPCNT32(fp_32[15])) +
      ((int) POPCNT32(fp_32[16])) +
      ((int) POPCNT32(fp_32[18]))  );
      break;

  case 10: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[13])) +
      ((int) POPCNT32(fp_32[14])) +
      ((int) POPCNT32(fp_32[15])) +
      ((int) POPCNT32(fp_32[16])) +
      ((int) POPCNT32(fp_32[17])) +
      ((int) POPCNT32(fp_32[18])) +
      ((int) POPCNT32(fp_32[20]))  );
      break;

  case 11: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[13])) +
      ((int) POPCNT32(fp_32[14])) +
      ((int) POPCNT32(fp_32[15])) +
      ((int) POPCNT32(fp_32[16])) +
      ((int) POPCNT32(fp_32[17])) +
      ((int) POPCNT32(fp_32[18])) +
      ((int) POPCNT32(fp_32[19])) +
      ((int) POPCNT32(fp_32[20])) +
      ((int) POPCNT32(fp_32[22]))  );
      break;

  case 12: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[13])) +
      ((int) POPCNT32(fp_32[14])) +
      ((int) POPCNT32(fp_32[15])) +
      ((int) POPCNT32(fp_32[16])) +
      ((int) POPCNT32(fp_32[17])) +
      ((int) POPCNT32(fp_32[18])) +
      ((int) POPCNT32(fp_32[19])) +
      ((int) POPCNT32(fp_32[20])) +
      ((int) POPCNT32(fp_32[21])) +
      ((int) POPCNT32(fp_32[22])) +
      ((int) POPCNT32(fp_32[24]))  );
      break;

  case 13: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[13])) +
      ((int) POPCNT32(fp_32[14])) +
      ((int) POPCNT32(fp_32[15])) +
      ((int) POPCNT32(fp_32[16])) +
      ((int) POPCNT32(fp_32[17])) +
      ((int) POPCNT32(fp_32[18])) +
      ((int) POPCNT32(fp_32[19])) +
      ((int) POPCNT32(fp_32[20])) +
      ((int) POPCNT32(fp_32[21])) +
      ((int) POPCNT32(fp_32[22])) +
      ((int) POPCNT32(fp_32[23])) +
      ((int) POPCNT32(fp_32[24])) +
      ((int) POPCNT32(fp_32[26]))  );
      break;

  case 14: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[13])) +
      ((int) POPCNT32(fp_32[14])) +
      ((int) POPCNT32(fp_32[15])) +
      ((int) POPCNT32(fp_32[16])) +
      ((int) POPCNT32(fp_32[17])) +
      ((int) POPCNT32(fp_32[18])) +
      ((int) POPCNT32(fp_32[19])) +
      ((int) POPCNT32(fp_32[20])) +
      ((int) POPCNT32(fp_32[21])) +
      ((int) POPCNT32(fp_32[22])) +
      ((int) POPCNT32(fp_32[23])) +
      ((int) POPCNT32(fp_32[24])) +
      ((int) POPCNT32(fp_32[25])) +
      ((int) POPCNT32(fp_32[26])) +
      ((int) POPCNT32(fp_32[28]))  );
      break;

  case 15: bit_count += (
      ((int) POPCNT32(fp_32[ 0])) +
      ((int) POPCNT32(fp_32[ 1])) +
      ((int) POPCNT32(fp_32[ 2])) +
      ((int) POPCNT32(fp_32[ 3])) +
      ((int) POPCNT32(fp_32[ 4])) +
      ((int) POPCNT32(fp_32[ 5])) +
      ((int) POPCNT32(fp_32[ 6])) +
      ((int) POPCNT32(fp_32[ 7])) +
      ((int) POPCNT32(fp_32[ 8])) +
      ((int) POPCNT32(fp_32[ 9])) +
      ((int) POPCNT32(fp_32[10])) +
      ((int) POPCNT32(fp_32[11])) +
      ((int) POPCNT32(fp_32[12])) +
      ((int) POPCNT32(fp_32[13])) +
      ((int) POPCNT32(fp_32[14])) +
      ((int) POPCNT32(fp_32[15])) +
      ((int) POPCNT32(fp_32[16])) +
      ((int) POPCNT32(fp_32[17])) +
      ((int) POPCNT32(fp_32[18])) +
      ((int) POPCNT32(fp_32[19])) +
      ((int) POPCNT32(fp_32[20])) +
      ((int) POPCNT32(fp_32[21])) +
      ((int) POPCNT32(fp_32[22])) +
      ((int) POPCNT32(fp_32[23])) +
      ((int) POPCNT32(fp_32[24])) +
      ((int) POPCNT32(fp_32[25])) +
      ((int) POPCNT32(fp_32[26])) +
      ((int) POPCNT32(fp_32[27])) +
      ((int) POPCNT32(fp_32[28])) +
      ((int) POPCNT32(fp_32[30]))  );
      break;    
    
  }
#else
  UNUSED(fp1);
  UNUSED(fp2);
  UNUSED(count);
  UNUSED(i);
  UNUSED(rounded_size);
#endif
  return bit_count;
}

/** 1024 + 8*i (popcount) **/
int
chemfp_intersect_popcount_popcnt_128_8(ssize_t size, const uint64_t *fp1, const uint64_t *fp2) {
  int bit_count = 0;
  int i;
  ssize_t rounded_size;
#if defined(_WIN64) || defined(__x86_64__)
  rounded_size = (size / 128) * 16;
  for (i=0; i<rounded_size; i += 16, fp1 += 16, fp2 += 16) {
    bit_count += (((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
                  ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
                  ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
                  ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
                  ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
                  ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
                  ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
                  ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
                  ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
                  ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
                  ((int) POPCNT64(fp1[10] & fp2[10])) +
                  ((int) POPCNT64(fp1[11] & fp2[11])) +
                  ((int) POPCNT64(fp1[12] & fp2[12])) +
                  ((int) POPCNT64(fp1[13] & fp2[13])) +
                  ((int) POPCNT64(fp1[14] & fp2[14])) +
                  ((int) POPCNT64(fp1[15] & fp2[15])));
  }
  switch ((size+7) / 8 - rounded_size) {
  case 0: break;
      
  case 1: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0]))  );
      break;
      
  case  2: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1]))  );
      break;

  case  3: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2]))  );
      break;

  case  4: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3]))  );
      break;

  case  5: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4]))  );
      break;

  case  6: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5]))  );
      break;

  case  7: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6]))  );
      break;

  case  8: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
      ((int) POPCNT64(fp1[ 7] & fp2[ 7]))  );
      break;

  case  9: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
      ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
      ((int) POPCNT64(fp1[ 8] & fp2[ 8]))  );
      break;

  case 10: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
      ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
      ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
      ((int) POPCNT64(fp1[ 9] & fp2[ 9]))  );
      break;

  case 11: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
      ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
      ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
      ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
      ((int) POPCNT64(fp1[10] & fp2[10]))  );
      break;

  case 12: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
      ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
      ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
      ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
      ((int) POPCNT64(fp1[10] & fp2[10])) +
      ((int) POPCNT64(fp1[11] & fp2[11]))  );
      break;

  case 13: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
      ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
      ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
      ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
      ((int) POPCNT64(fp1[10] & fp2[10])) +
      ((int) POPCNT64(fp1[11] & fp2[11])) +
      ((int) POPCNT64(fp1[12] & fp2[12]))  );
      break;

  case 14: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
      ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
      ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
      ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
      ((int) POPCNT64(fp1[10] & fp2[10])) +
      ((int) POPCNT64(fp1[11] & fp2[11])) +
      ((int) POPCNT64(fp1[12] & fp2[12])) +
      ((int) POPCNT64(fp1[13] & fp2[13]))  );
      break;

  case 15: bit_count += (
      ((int) POPCNT64(fp1[ 0] & fp2[ 0])) +
      ((int) POPCNT64(fp1[ 1] & fp2[ 1])) +
      ((int) POPCNT64(fp1[ 2] & fp2[ 2])) +
      ((int) POPCNT64(fp1[ 3] & fp2[ 3])) +
      ((int) POPCNT64(fp1[ 4] & fp2[ 4])) +
      ((int) POPCNT64(fp1[ 5] & fp2[ 5])) +
      ((int) POPCNT64(fp1[ 6] & fp2[ 6])) +
      ((int) POPCNT64(fp1[ 7] & fp2[ 7])) +
      ((int) POPCNT64(fp1[ 8] & fp2[ 8])) +
      ((int) POPCNT64(fp1[ 9] & fp2[ 9])) +
      ((int) POPCNT64(fp1[10] & fp2[10])) +
      ((int) POPCNT64(fp1[11] & fp2[11])) +
      ((int) POPCNT64(fp1[12] & fp2[12])) +
      ((int) POPCNT64(fp1[13] & fp2[13])) +
      ((int) POPCNT64(fp1[14] & fp2[14]))  );
      break;
  }
 
#elif defined(_WIN32) || defined(__i386__) || defined(__i386)
  const uint32_t* fp1_32 = (const uint32_t*) fp1;
  const uint32_t* fp2_32 = (const uint32_t*) fp2;
  rounded_size = (size + 127) / 128 * 32;
  for (i=0; i<rounded_size; i+= 32, fp1_32 += 32, fp2_32 += 32) {
    bit_count += (((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
                  ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
                  ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
                  ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
                  ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
                  ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
                  ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
                  ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
                  ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
                  ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
                  ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
                  ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
                  ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
                  ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
                  ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
                  ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
                  ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
                  ((int) POPCNT32(fp1_32[17] & fp2_32[17])) +
                  ((int) POPCNT32(fp1_32[18] & fp2_32[18])) +
                  ((int) POPCNT32(fp1_32[19] & fp2_32[19])) +
                  ((int) POPCNT32(fp1_32[20] & fp2_32[20])) +
                  ((int) POPCNT32(fp1_32[21] & fp2_32[21])) +
                  ((int) POPCNT32(fp1_32[22] & fp2_32[22])) +
                  ((int) POPCNT32(fp1_32[23] & fp2_32[23])) +
                  ((int) POPCNT32(fp1_32[24] & fp2_32[24])) +
                  ((int) POPCNT32(fp1_32[25] & fp2_32[25])) +
                  ((int) POPCNT32(fp1_32[26] & fp2_32[26])) +
                  ((int) POPCNT32(fp1_32[27] & fp2_32[27])) +
                  ((int) POPCNT32(fp1_32[28] & fp2_32[28])) +
                  ((int) POPCNT32(fp1_32[29] & fp2_32[29])) +
                  ((int) POPCNT32(fp1_32[30] & fp2_32[30])) +
                  ((int) POPCNT32(fp1_32[31] & fp2_32[31])));
  }
  switch ((size+7) / 8 - rounded_size) {
  case  0: break;
      
  case  1: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1]))   );
      break;
      
  case  2: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3]))  );
      break;

  case  3: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5]))  );
      break;

  case  4: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7]))  );
      break;

  case  5: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9]))  );
      break;

  case  6: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11]))  );
      break;

  case  7: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13]))  );
      break;

  case  8: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
      ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
      ((int) POPCNT32(fp1_32[15] & fp2_32[15]))  );
      break;

  case  9: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
      ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
      ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
      ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
      ((int) POPCNT32(fp1_32[17] & fp2_32[17]))  );
      break;

  case 10: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
      ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
      ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
      ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
      ((int) POPCNT32(fp1_32[17] & fp2_32[17])) +
      ((int) POPCNT32(fp1_32[18] & fp2_32[18])) +
      ((int) POPCNT32(fp1_32[19] & fp2_32[19]))  );
      break;

  case 11: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
      ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
      ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
      ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
      ((int) POPCNT32(fp1_32[17] & fp2_32[17])) +
      ((int) POPCNT32(fp1_32[18] & fp2_32[18])) +
      ((int) POPCNT32(fp1_32[19] & fp2_32[19])) +
      ((int) POPCNT32(fp1_32[20] & fp2_32[20])) +
      ((int) POPCNT32(fp1_32[21] & fp2_32[21]))  );
      break;

  case 12: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
      ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
      ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
      ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
      ((int) POPCNT32(fp1_32[17] & fp2_32[17])) +
      ((int) POPCNT32(fp1_32[18] & fp2_32[18])) +
      ((int) POPCNT32(fp1_32[19] & fp2_32[19])) +
      ((int) POPCNT32(fp1_32[20] & fp2_32[20])) +
      ((int) POPCNT32(fp1_32[21] & fp2_32[21])) +
      ((int) POPCNT32(fp1_32[22] & fp2_32[22])) +
      ((int) POPCNT32(fp1_32[23] & fp2_32[23]))  );
      break;

  case 13: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
      ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
      ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
      ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
      ((int) POPCNT32(fp1_32[17] & fp2_32[17])) +
      ((int) POPCNT32(fp1_32[18] & fp2_32[18])) +
      ((int) POPCNT32(fp1_32[19] & fp2_32[19])) +
      ((int) POPCNT32(fp1_32[20] & fp2_32[20])) +
      ((int) POPCNT32(fp1_32[21] & fp2_32[21])) +
      ((int) POPCNT32(fp1_32[22] & fp2_32[22])) +
      ((int) POPCNT32(fp1_32[23] & fp2_32[23])) +
      ((int) POPCNT32(fp1_32[24] & fp2_32[24])) +
      ((int) POPCNT32(fp1_32[25] & fp2_32[25]))  );
      break;

  case 14: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
      ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
      ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
      ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
      ((int) POPCNT32(fp1_32[17] & fp2_32[17])) +
      ((int) POPCNT32(fp1_32[18] & fp2_32[18])) +
      ((int) POPCNT32(fp1_32[19] & fp2_32[19])) +
      ((int) POPCNT32(fp1_32[20] & fp2_32[20])) +
      ((int) POPCNT32(fp1_32[21] & fp2_32[21])) +
      ((int) POPCNT32(fp1_32[22] & fp2_32[22])) +
      ((int) POPCNT32(fp1_32[23] & fp2_32[23])) +
      ((int) POPCNT32(fp1_32[24] & fp2_32[24])) +
      ((int) POPCNT32(fp1_32[25] & fp2_32[25])) +
      ((int) POPCNT32(fp1_32[26] & fp2_32[26])) +
      ((int) POPCNT32(fp1_32[27] & fp2_32[27]))  );
      break;

  case 15: bit_count += (
      ((int) POPCNT32(fp1_32[ 0] & fp2_32[ 0])) +
      ((int) POPCNT32(fp1_32[ 1] & fp2_32[ 1])) +
      ((int) POPCNT32(fp1_32[ 2] & fp2_32[ 2])) +
      ((int) POPCNT32(fp1_32[ 3] & fp2_32[ 3])) +
      ((int) POPCNT32(fp1_32[ 4] & fp2_32[ 4])) +
      ((int) POPCNT32(fp1_32[ 5] & fp2_32[ 5])) +
      ((int) POPCNT32(fp1_32[ 6] & fp2_32[ 6])) +
      ((int) POPCNT32(fp1_32[ 7] & fp2_32[ 7])) +
      ((int) POPCNT32(fp1_32[ 8] & fp2_32[ 8])) +
      ((int) POPCNT32(fp1_32[ 9] & fp2_32[ 9])) +
      ((int) POPCNT32(fp1_32[10] & fp2_32[10])) +
      ((int) POPCNT32(fp1_32[11] & fp2_32[11])) +
      ((int) POPCNT32(fp1_32[12] & fp2_32[12])) +
      ((int) POPCNT32(fp1_32[13] & fp2_32[13])) +
      ((int) POPCNT32(fp1_32[14] & fp2_32[14])) +
      ((int) POPCNT32(fp1_32[15] & fp2_32[15])) +
      ((int) POPCNT32(fp1_32[16] & fp2_32[16])) +
      ((int) POPCNT32(fp1_32[17] & fp2_32[17])) +
      ((int) POPCNT32(fp1_32[18] & fp2_32[18])) +
      ((int) POPCNT32(fp1_32[19] & fp2_32[19])) +
      ((int) POPCNT32(fp1_32[20] & fp2_32[20])) +
      ((int) POPCNT32(fp1_32[21] & fp2_32[21])) +
      ((int) POPCNT32(fp1_32[22] & fp2_32[22])) +
      ((int) POPCNT32(fp1_32[23] & fp2_32[23])) +
      ((int) POPCNT32(fp1_32[24] & fp2_32[24])) +
      ((int) POPCNT32(fp1_32[25] & fp2_32[25])) +
      ((int) POPCNT32(fp1_32[26] & fp2_32[26])) +
      ((int) POPCNT32(fp1_32[27] & fp2_32[27])) +
      ((int) POPCNT32(fp1_32[28] & fp2_32[28])) +
      ((int) POPCNT32(fp1_32[29] & fp2_32[29]))  );
      break;
  }
#else
  UNUSED(fp1);
  UNUSED(fp2);
  UNUSED(i);
  UNUSED(rounded_size);
#endif
  
  return bit_count;
}

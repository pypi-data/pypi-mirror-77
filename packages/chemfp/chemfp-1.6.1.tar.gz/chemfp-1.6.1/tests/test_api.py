from __future__ import absolute_import, with_statement, print_function

import os
import sys
import unittest2
import datetime
from cStringIO import StringIO
import tempfile
import gzip
import shutil
import itertools
import random

import chemfp
from chemfp import bitops, io

from chemfp.bitops import hex_encode_as_bytes, hex_decode

import support

try:
    import openbabel
    has_openbabel = True
except ImportError:
    has_openbabel = False

try:
    # I need to import 'oechem' to make sure I load the shared libries
    from openeye import oechem
    if not oechem.OEChemIsLicensed():
        raise ImportError
    from chemfp import openeye
    has_openeye = True
except ImportError:
    has_openeye = False
    openeye = None

try:
    from rdkit import Chem
    has_rdkit = True
except ImportError:
    has_rdkit = False

from support import fullpath, PUBCHEM_SDF, PUBCHEM_SDF_GZ


DBL_MIN = 2.2250738585072014e-308 # Assumes 64 bit doubles
assert DBL_MIN > 0.0

CHEBI_TARGETS = fullpath("chebi_rdmaccs.fps")
CHEBI_QUERIES = fullpath("chebi_queries.fps.gz")
MACCS_SMI = fullpath("maccs.smi")

# Backwards compatibility for Python 2.5
try:
    next
except NameError:
    def next(it):
        return it.next()

def _tmpdir(testcase):
    dirname = tempfile.mkdtemp()
    testcase.addCleanup(shutil.rmtree, dirname)
    return dirname


QUERY_ARENA = next(chemfp.open(CHEBI_QUERIES).iter_arenas(10))
        
class CommonReaderAPI(object):
    _open = None
    
    def _check_target_metadata(self, metadata):
        self.assertEqual(metadata.num_bits, 166)
        self.assertEqual(metadata.num_bytes, 21)
        self.assertEqual(metadata.software, "OEChem/1.7.4 (20100809)")
        self.assertEqual(metadata.type, "RDMACCS-OpenEye/1")
        self.assertEqual(metadata.sources, ["/Users/dalke/databases/ChEBI_lite.sdf.gz"])
        self.assertEqual(metadata.date, datetime.datetime(2011, 9, 16, 13, 49, 4))
        self.assertEqual(metadata.datestamp, "2011-09-16T13:49:04")
        self.assertEqual(metadata.aromaticity, "mmff")

    def _check_query_metadata(self, metadata):
        self.assertEqual(metadata.num_bits, 166)
        self.assertEqual(metadata.num_bytes, 21)
        self.assertEqual(metadata.software, "OEChem/1.7.4 (20100809)")
        self.assertEqual(metadata.type, "RDMACCS-OpenEye/1")
        self.assertEqual(metadata.sources, ["/Users/dalke/databases/ChEBI_lite.sdf.gz"])
        self.assertEqual(metadata.date, datetime.datetime(2011, 9, 16, 13, 28,43))
        self.assertEqual(metadata.datestamp, "2011-09-16T13:28:43")
        self.assertEqual(metadata.aromaticity, "openeye")
        
    
    def test_uncompressed_open(self):
        reader = self._open(CHEBI_TARGETS)
        self._check_target_metadata(reader.metadata)
        num = sum(1 for x in reader)
        self.assertEqual(num, 2000)

    def test_compressed_open(self):
        reader = self._open(CHEBI_QUERIES)
        self._check_query_metadata(reader.metadata)
        num = sum(1 for x in reader)
        self.assertEqual(num, 154)

    def test_iteration(self):
        assert self.hit_order is not sorted, "not appropriate for sorted arenas"
        reader = iter(self._open(CHEBI_TARGETS))
        fields = [next(reader) for i in range(5)]
        self.assertEqual(fields, 
                         [("CHEBI:776", hex_decode("00000000000000008200008490892dc00dc4a7d21e")),
                          ("CHEBI:1148", hex_decode("000000000000200080000002800002040c0482d608")),
                          ("CHEBI:1734", hex_decode("0000000000000221000800111601017000c1a3d21e")),
                          ("CHEBI:1895", hex_decode("00000000000000000000020000100000000400951e")),
                          ("CHEBI:2303", hex_decode("0000000002001021820a00011681015004cdb3d21e"))
                          ])
                          

      
    def test_iter_arenas_default_size(self):
        assert self.hit_order is not sorted, "not appropriate for sorted arenas"
        reader = self._open(CHEBI_TARGETS)
        count = 0
        for arena in reader.iter_arenas():
            self._check_target_metadata(arena.metadata)
            if count == 0:
                # Check the values of the first arena
                self.assertEqual(arena.ids[-5:],
                                  ['CHEBI:16316', 'CHEBI:16317', 'CHEBI:16318', 'CHEBI:16319', 'CHEBI:16320'])
                
            self.assertEqual(len(arena), 1000)  # There should be two of these
            count += 1
        self.assertEqual(count, 2)
        self.assertEqual(arena.ids[-5:],
                          ['CHEBI:17578', 'CHEBI:17579', 'CHEBI:17580', 'CHEBI:17581', 'CHEBI:17582'])

    def test_iter_arenas_select_size(self):
        assert self.hit_order is not sorted, "not appropriate for sorted arenas"
        reader = self._open(CHEBI_TARGETS)
        count = 0
        for arena in reader.iter_arenas(100):
            self._check_target_metadata(arena.metadata)
            if count == 0:
                self.assertEqual(arena.ids[-5:],
                                  ['CHEBI:5280', 'CHEBI:5445', 'CHEBI:5706', 'CHEBI:5722', 'CHEBI:5864'])
            self.assertEqual(len(arena), 100)
            count += 1
        self.assertEqual(count, 20)
        self.assertEqual(arena.ids[:5],
                          ['CHEBI:17457', 'CHEBI:17458', 'CHEBI:17459', 'CHEBI:17460', 'CHEBI:17464'])

    def test_read_from_file_object(self):
        f = StringIO("""\
#FPS1
#num-bits=8
F0\tsmall
""")
        reader = self._open(f)
        self.assertEqual(sum(1 for x in reader), 1)
        self.assertEqual(reader.metadata.num_bits, 8)

    def test_read_from_empty_file_object(self):
        f = StringIO("")
        reader = self._open(f)
        self.assertEqual(sum(1 for x in reader), 0)
        self.assertEqual(reader.metadata.num_bits, None)

    def test_read_from_header_only_file_object(self):
        f = StringIO("""\
#FPS1
#num_bits=100
""")
        reader = self._open(f)
        self.assertEqual(sum(1 for x in reader), 0)
        self.assertEqual(reader.metadata.num_bits, 100)


    #
    # Count tanimoto hits using a fingerprint
    # 

    def test_count_tanimoto_hits_fp_default(self):
        reader = self._open(CHEBI_TARGETS)
        num_hits = reader.count_tanimoto_hits_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"))
        self.assertEqual(num_hits, 176)

    def test_count_tanimoto_hits_fp_set_default(self):
        # This is set to the default value
        reader = self._open(CHEBI_TARGETS)
        num_hits = reader.count_tanimoto_hits_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                 threshold = 0.7)
        self.assertEqual(num_hits, 176)

    def test_count_tanimoto_hits_fp_set_threshold(self):
        reader = self._open(CHEBI_TARGETS)
        num_hits = reader.count_tanimoto_hits_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                 threshold = 0.8)
        self.assertEqual(num_hits, 108)

    def test_count_tanimoto_hits_fp_set_max_threshold(self):
        reader = self._open(CHEBI_TARGETS)
        num_hits = reader.count_tanimoto_hits_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                 threshold = 1.0)
        self.assertEqual(num_hits, 1)

    def test_count_tanimoto_hits_fp_set_min_threshold(self):
        reader = self._open(CHEBI_TARGETS)
        num_hits = reader.count_tanimoto_hits_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                 threshold = DBL_MIN)
        # It isn't 2000 since there are some scores of 0.0
        self.assertEqual(num_hits, 1993)

    def test_count_tanimoto_hits_fp_0(self):
        reader = self._open(CHEBI_TARGETS)
        num_hits = reader.count_tanimoto_hits_fp(hex_decode("000000000000000000000000000000000000000000"),
                                                 threshold = 1./1000)
        self.assertEqual(num_hits, 0)


    def test_count_tanimoto_hits_fp_threshold_range_error(self):
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            for x in reader.count_tanimoto_hits_fp(
                hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                threshold = 1.1):
                raise AssertionError("Should not happen!")
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            for x in reader.count_tanimoto_hits_fp(
                hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                threshold = -0.00001):
                raise AssertionError("Should not happen")

    #
    # Count tanimoto hits using an arena
    #

    def test_count_tanimoto_default(self):
        targets = self._open(CHEBI_TARGETS)
        counts = targets.count_tanimoto_hits_arena(QUERY_ARENA)
        self.assertSequenceEqual(counts, [4, 179, 40, 32, 1, 3, 28, 11, 46, 7])

    def test_count_tanimoto_set_default(self):
        targets = self._open(CHEBI_TARGETS)
        counts = targets.count_tanimoto_hits_arena(QUERY_ARENA, threshold=0.7)
        self.assertSequenceEqual(counts, [4, 179, 40, 32, 1, 3, 28, 11, 46, 7])

    def test_count_tanimoto_set_threshold(self):
        targets = self._open(CHEBI_TARGETS)
        counts = targets.count_tanimoto_hits_arena(QUERY_ARENA, threshold=0.9)
        self.assertSequenceEqual(counts, [0, 97, 7, 1, 0, 1, 1, 0, 1, 1])

    def test_count_tanimoto_hits_threshold_range_error(self):
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            for x in reader.count_tanimoto_hits_arena(QUERY_ARENA, threshold = 1.1):
                raise AssertionError("Shouldn't get here")
                                          
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            for x in reader.count_tanimoto_hits_arena(QUERY_ARENA, threshold = -0.00001):
                raise AssertionError("Shouldn't get here!")
        
        
    #
    # Threshold tanimoto search using a fingerprint
    # 

    def test_threshold_tanimoto_search_fp_default(self):
        reader = self._open(CHEBI_TARGETS)
        result = reader.threshold_tanimoto_search_fp(
            hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"))
        self.assertEqual(len(result), 176)
        hits = result.get_ids_and_scores()
        first_hits = [('CHEBI:3139', 0.72277227722772275), ('CHEBI:4821', 0.71134020618556704),
                      ('CHEBI:15345', 0.94505494505494503), ('CHEBI:15346', 0.92307692307692313),
                      ('CHEBI:15351', 0.96703296703296704), ('CHEBI:15371', 0.96703296703296704)]
        last_hits = [('CHEBI:17383', 0.72164948453608246), ('CHEBI:17422', 0.73913043478260865),
                     ('CHEBI:17439', 0.81000000000000005), ('CHEBI:17469', 0.72631578947368425),
                     ('CHEBI:17510', 0.70526315789473681), ('CHEBI:17552', 0.71578947368421053)]
        if self.hit_order is not sorted:
            self.assertEqual(hits[:6], first_hits)
            self.assertEqual(hits[-6:], last_hits)
        else:
            for x in first_hits + last_hits:
                self.assertIn(x, hits)


    def test_threshold_tanimoto_search_fp_set_default(self):
        # This is set to the default value
        reader = self._open(CHEBI_TARGETS)
        result = reader.threshold_tanimoto_search_fp(
            hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"), threshold = 0.7)
        self.assertEqual(len(result), 176)
        hits = result.get_ids_and_scores()
        first_hits = [('CHEBI:3139', 0.72277227722772275), ('CHEBI:4821', 0.71134020618556704),
                      ('CHEBI:15345', 0.94505494505494503), ('CHEBI:15346', 0.92307692307692313),
                      ('CHEBI:15351', 0.96703296703296704), ('CHEBI:15371', 0.96703296703296704)]
        last_hits = [('CHEBI:17383', 0.72164948453608246), ('CHEBI:17422', 0.73913043478260865),
                     ('CHEBI:17439', 0.81000000000000005), ('CHEBI:17469', 0.72631578947368425),
                     ('CHEBI:17510', 0.70526315789473681), ('CHEBI:17552', 0.71578947368421053)]
        if self.hit_order is not sorted:
            self.assertEqual(hits[:6], first_hits)
            self.assertEqual(hits[-6:], last_hits)
        else:
            for x in first_hits + last_hits:
                self.assertIn(x, hits)

    def test_threshold_tanimoto_search_fp_set_threshold(self):
        reader = self._open(CHEBI_TARGETS)
        result = reader.threshold_tanimoto_search_fp(
            hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"), threshold = 0.8)
        self.assertEqual(len(result), 108)
        hits = result.get_ids_and_scores()
        first_hits = [('CHEBI:15345', 0.94505494505494503), ('CHEBI:15346', 0.92307692307692313),
                      ('CHEBI:15351', 0.96703296703296704), ('CHEBI:15371', 0.96703296703296704),
                      ('CHEBI:15380', 0.92391304347826086), ('CHEBI:15448', 0.92391304347826086)]
        last_hits = [('CHEBI:15982', 0.81818181818181823), ('CHEBI:16304', 0.81000000000000005),
                     ('CHEBI:16625', 0.94565217391304346), ('CHEBI:17068', 0.90526315789473688),
                     ('CHEBI:17157', 0.94505494505494503), ('CHEBI:17439', 0.81000000000000005)]
        if self.hit_order is not sorted:
            self.assertEqual(hits[:6], first_hits)
            self.assertEqual(hits[-6:], last_hits)
        else:
            for x in first_hits + last_hits:
                self.assertIn(x, hits)

    def test_threshold_tanimoto_search_fp_set_max_threshold(self):
        reader = self._open(CHEBI_TARGETS)
        hits = reader.threshold_tanimoto_search_fp(
            hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"), threshold = 1.0)
        self.assertEqual(hits.get_ids_and_scores(), [('CHEBI:15523', 1.0)])

    def test_threshold_tanimoto_search_fp_set_min_threshold(self):
        reader = self._open(CHEBI_TARGETS)
        results = reader.threshold_tanimoto_search_fp(
            hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"), threshold = DBL_MIN)
        self.assertEqual(len(results), 1993)

    def test_threshold_tanimoto_search_fp_0_on_0(self):
        zeros = ("0000\tfirst\n"
                 "0010\tsecond\n"
                 "0000\tthird\n")
        f = StringIO(zeros)
        reader = self._open(f)
        result = reader.threshold_tanimoto_search_fp(hex_decode("0000"), threshold=0.0)
        hits = result.get_ids_and_scores()
        self.assertEqual(self.hit_order(hits),
                          self.hit_order([ ("first", 0.0), ("second", 0.0), ("third", 0.0) ]))

    def test_threshold_tanimoto_search_fp_0(self):
        reader = self._open(CHEBI_TARGETS)
        results = reader.threshold_tanimoto_search_fp(
            hex_decode("000000000000000000000000000000000000000000"), threshold = 1./1000)
        self.assertEqual(len(results), 0)

    def test_threshold_tanimoto_search_fp_threshold_range_error(self):
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            reader.threshold_tanimoto_search_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                threshold = 1.1)
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            reader.threshold_tanimoto_search_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                threshold = -0.00001)

    #
    # Threshold tanimoto search using an arena
    #

    def test_threshold_tanimoto_arena_default(self):
        targets = self._open(CHEBI_TARGETS)
        results = targets.threshold_tanimoto_search_arena(QUERY_ARENA)
        hits = [result.get_ids_and_scores() for result in results]
        self.assertEqual(map(len, results), [4, 179, 40, 32, 1, 3, 28, 11, 46, 7])
        self.assertEqual(list(hits[0]),
                         [('CHEBI:16148', 0.7142857142857143), ('CHEBI:17034', 0.8571428571428571),
                          ('CHEBI:17302', 0.8571428571428571), ('CHEBI:17539', 0.72222222222222221)])


    def test_threshold_tanimoto_arena_set_default(self):
        targets = self._open(CHEBI_TARGETS)
        results = targets.threshold_tanimoto_search_arena(QUERY_ARENA, threshold=0.7)
        self.assertEqual(map(len, results), [4, 179, 40, 32, 1, 3, 28, 11, 46, 7])
        hits = [result.get_ids_and_scores() for result in results]
        self.assertEqual(self.hit_order(list(hits[-1])),
                         self.hit_order([('CHEBI:15621', 0.8571428571428571), ('CHEBI:15882', 0.83333333333333337),
                                         ('CHEBI:16008', 0.80000000000000004), ('CHEBI:16193', 0.80000000000000004),
                                         ('CHEBI:16207', 1.0), ('CHEBI:17231', 0.76923076923076927),
                                         ('CHEBI:17450', 0.75)]))


    def test_threshold_tanimoto_arena_set_threshold(self):
        targets = self._open(CHEBI_TARGETS)
        results = targets.threshold_tanimoto_search_arena(QUERY_ARENA, threshold=0.9)
        self.assertEqual(map(len, results), [0, 97, 7, 1, 0, 1, 1, 0, 1, 1])
        hits = [result.get_ids_and_scores() for result in results]
        self.assertEqual(self.hit_order(list(hits[2])),
                         self.hit_order([('CHEBI:15895', 1.0), ('CHEBI:16165', 1.0),
                                         ('CHEBI:16292', 0.93333333333333335), ('CHEBI:16392', 0.93333333333333335),
                                         ('CHEBI:17100', 0.93333333333333335), ('CHEBI:17242', 0.90000000000000002),
                                         ('CHEBI:17464', 1.0)]))

    def test_threshold_tanimoto_search_0_on_0(self):
        zeros = ("0000\tfirst\n"
                 "0010\tsecond\n"
                 "0000\tthird\n")
        query_arena = next(chemfp.open(StringIO(zeros)).iter_arenas())
        self.assertEqual(query_arena.ids, ["first", "second", "third"])

        targets = self._open(StringIO(zeros))
        results = targets.threshold_tanimoto_search_arena(query_arena, threshold=0.0)
        self.assertEqual(map(len, results), [3, 3, 3])

        targets = self._open(StringIO(zeros))
        results = targets.threshold_tanimoto_search_arena(query_arena, threshold=0.000001)
        self.assertEqual(map(len, results), [0, 1, 0])
        

    def test_threshold_tanimoto_search_threshold_range_error(self):
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            for x in reader.threshold_tanimoto_search_arena(QUERY_ARENA, threshold = 1.1):
                raise AssertionError("should never get here")
                                          
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            for x in reader.threshold_tanimoto_search_arena(QUERY_ARENA, threshold = -0.00001):
                raise AssertionError("should never get here!")
        
        
    #
    # K-nearest tanimoto search using a fingerprint
    # 

    def test_knearest_tanimoto_search_fp_default(self):
        reader = self._open(CHEBI_TARGETS)
        result = reader.knearest_tanimoto_search_fp(
            hex_decode("00000000100410200290000b03a29241846163ee1f"))
        hits = result.get_ids_and_scores()
        self.assertEqual(hits, [('CHEBI:8069', 1.0),
                                ('CHEBI:6758', 0.78723404255319152),
                                ('CHEBI:7983', 0.73999999999999999)])

    def test_knearest_tanimoto_search_fp_set_default(self):
        # This is set to the default values
        reader = self._open(CHEBI_TARGETS)
        result = reader.knearest_tanimoto_search_fp(
            hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"), k = 3, threshold = 0.7)
        self.assertEqual(len(result), 3)
        hits = result.get_ids_and_scores()
        if hits[1][0] == "CHEBI:15483":
            self.assertEqual(hits, [('CHEBI:15523', 1.0), ('CHEBI:15483', 0.98913043478260865),
                                    ('CHEBI:15480', 0.98913043478260865)])
        else:
            self.assertEqual(hits, [('CHEBI:15523', 1.0), ('CHEBI:15480', 0.98913043478260865),
                                    ('CHEBI:15483', 0.98913043478260865)])
        
    def test_knearest_tanimoto_search_fp_set_knearest(self):
        reader = self._open(CHEBI_TARGETS)
        result = reader.knearest_tanimoto_search_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                    k = 5, threshold = 0.8)
        hits = result.get_ids_and_scores()
        expected = [('CHEBI:15523', 1.0), ('CHEBI:15483', 0.98913043478260865),
                    ('CHEBI:15480', 0.98913043478260865), ('CHEBI:15478', 0.98901098901098905),
                    ('CHEBI:15486', 0.97802197802197799)]
        if hits[1][0] == "CHEBI:15480" and hits[2][0] == "CHEBI:15483":
            expected[1], expected[2] = expected[2], expected[1]
        self.assertEqual(list(hits), expected)


    def test_knearest_tanimoto_search_fp_set_max_threshold(self):
        reader = self._open(CHEBI_TARGETS)
        result = reader.knearest_tanimoto_search_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                    threshold = 1.0)
        hits = result.get_ids_and_scores()
        self.assertEqual(hits, [('CHEBI:15523', 1.0)])

    def test_knearest_tanimoto_search_fp_set_knearest_1(self):
        reader = self._open(CHEBI_TARGETS)
        result = reader.knearest_tanimoto_search_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                                    k = 1)
        self.assertEqual(result.get_ids_and_scores(), [('CHEBI:15523', 1.0)])

    def test_knearest_tanimoto_search_fp_set_knearest_0(self):
        reader = self._open(CHEBI_TARGETS)
        result = reader.knearest_tanimoto_search_fp(
            hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"), k = 0)
        self.assertFalse(result)

    def test_knearest_tanimoto_search_fp_knearest_threshold_range_error(self):
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive"):
            reader.knearest_tanimoto_search_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                               threshold = 1.1)
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive"):
            reader.knearest_tanimoto_search_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                               threshold = -0.00001)

    def test_knearest_tanimoto_search_fp_knearest_k_range_error(self):
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "k must be non-negative") as e:
            reader.knearest_tanimoto_search_fp(hex_decode("000000102084322193de9fcfbffbbcfbdf7ffeff1f"),
                                               k = -1)

    #
    # K-nearest tanimoto search using an arena
    #

    def test_knearest_tanimoto_default(self):
        targets = self._open(CHEBI_TARGETS)
        results = targets.knearest_tanimoto_search_arena(QUERY_ARENA)
        self.assertEqual(map(len, results), [3, 3, 3, 3, 1, 3, 3, 3, 3, 3])
        hits = [result.get_ids_and_scores() for result in results]
        first_hits = hits[0]
        if first_hits[0][0] == 'CHEBI:17302':
            self.assertEqual(list(first_hits), [('CHEBI:17302', 0.8571428571428571),
                                                ('CHEBI:17034', 0.8571428571428571),
                                                ('CHEBI:17539', 0.72222222222222221)])
        else:
            self.assertEqual(list(first_hits), [('CHEBI:17034', 0.8571428571428571),
                                                ('CHEBI:17302', 0.8571428571428571),
                                                ('CHEBI:17539', 0.72222222222222221)])

    def test_knearest_tanimoto_set_default(self):
        targets = self._open(CHEBI_TARGETS)
        results = targets.knearest_tanimoto_search_arena(QUERY_ARENA, k=3, threshold=0.7)
        self.assertEqual(map(len, results), [3, 3, 3, 3, 1, 3, 3, 3, 3, 3])
        self.assertEqual(results[-1].get_ids_and_scores(),
                         [('CHEBI:16207', 1.0), ('CHEBI:15621', 0.8571428571428571),
                          ('CHEBI:15882', 0.83333333333333337)])

    def test_knearest_tanimoto_set_threshold(self):
        targets = self._open(CHEBI_TARGETS)
        results = targets.knearest_tanimoto_search_arena(QUERY_ARENA, threshold=0.8)
        self.assertEqual(map(len, results), [2, 3, 3, 3, 1, 1, 3, 3, 3, 3])
        self.assertEqual(results[6].get_ids_and_scores(),
                         [('CHEBI:16834', 0.90909090909090906), ('CHEBI:17061', 0.875),
                          ('CHEBI:16319', 0.84848484848484851)])

    def test_knearest_tanimoto_search_knearest_range_error(self):
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            for x in reader.knearest_tanimoto_search_arena(QUERY_ARENA, threshold = 1.1):
                raise AssertionError("What?!")
            
        reader = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "threshold must between 0.0 and 1.0, inclusive") as e:
            for x in reader.knearest_tanimoto_search_arena(QUERY_ARENA, threshold = -0.00001):
                raise AssertionError("What2?!")
        
    
class TestFPSReader(unittest2.TestCase, CommonReaderAPI):
    hit_order = staticmethod(lambda x: x)
    _open = staticmethod(chemfp.open)

    def test_row_iteration(self):
        reader = chemfp.open(CHEBI_TARGETS)
        num = sum(1 for x in reader.iter_rows())
        self.assertEqual(num, 2000)
        
        row_reader = chemfp.open(CHEBI_TARGETS).iter_rows()
        fields = [next(row_reader) for i in range(5)]
        self.assertEqual(fields,  [
            ['00000000000000008200008490892dc00dc4a7d21e', 'CHEBI:776'],
            ['000000000000200080000002800002040c0482d608', 'CHEBI:1148'],
            ['0000000000000221000800111601017000c1a3d21e', 'CHEBI:1734'],
            ['00000000000000000000020000100000000400951e', 'CHEBI:1895'],
            ['0000000002001021820a00011681015004cdb3d21e', 'CHEBI:2303']])

    def test_iter_blocks(self):
        reader = chemfp.open(CHEBI_TARGETS)
        line_counts = 0
        has_776 = False
        has_17582 = False
        for block in reader.iter_blocks():
            line_counts += block.count("\n")
            if "00000000000000008200008490892dc00dc4a7d21e\tCHEBI:776" in block:
                has_776 = True
            if "00000000020012008008000104000064844ca2521c\tCHEBI:17582" in block:
                has_17582 = True

        self.assertEqual(line_counts, 2000)
        self.assertTrue(has_776, "Missing CHEBI:776")
        self.assertTrue(has_17582, "Missing CHEBI:17582")

    def test_reiter_open_handle_arena_search(self):
        reader = chemfp.open(CHEBI_TARGETS)
        # The main goal is to prevent people from searching a
        # partially open file.  This reflects an implementation
        # problem; the iterator should be shared across all instances.
        it = iter(reader)
        arena = next(it)
        for method in (reader.threshold_tanimoto_search_arena,
                       reader.knearest_tanimoto_search_arena):
            with self.assertRaisesRegexp(TypeError, "FPS file is not at the start"):
                for x in method(arena):
                    break

    def test_reiter_open_handle_fp_search(self):
        reader = chemfp.open(CHEBI_TARGETS)
        # The main goal is to prevent people from searching a
        # partially open file.  This reflects an implementation
        # problem; the iterator should be shared across all instances.
        it = iter(reader)
        arena = next(it)
        fp = arena[0][1] # Get the fingerprint term
        
        for method in (reader.threshold_tanimoto_search_fp,
                       reader.knearest_tanimoto_search_fp):
            with self.assertRaisesRegexp(TypeError, "FPS file is not at the start"):
                for x in method(fp):
                    break
        
    def test_open_not_valid_object(self):
        with self.assertRaisesRegexp(ValueError, r"Unsupported source type \(1\+4j\)"):
            reader = self._open(1+4j)

    def test_date_extra_before(self):
        filename = support.get_tmpfile(self, "date_wrong_format.fps")
        with open(filename, "w") as f:
            f.write("#FPS1\n")
            f.write("#date=Q2010-08-09T10:11:12\n")
        with self.assertRaisesRegexp(ValueError, "The date must be in the form 'YYYY-DD-MMTHH:MM:SS'.*Q2010-08-09T10:11:12"):
            chemfp.open(filename)

    def test_date_wrong_format(self):
        filename = support.get_tmpfile(self, "date_wrong_format.fps")
        with open(filename, "w") as f:
            f.write("#FPS1\n")
            f.write("#date=next Tuesday\n")
        with self.assertRaisesRegexp(ValueError, "The date must be in the form 'YYYY-DD-MMTHH:MM:SS'.*next Tuesday"):
            chemfp.open(filename)
            
    def test_date_extra_after(self):
        filename = support.get_tmpfile(self, "date_wrong_format.fps")
        with open(filename, "w") as f:
            f.write("#FPS1\n")
            f.write("#date=2010-08-09T10:11:12 or so\n")
        with self.assertRaisesRegexp(ValueError, "Unconverted data remains after the date.*:12 or so"):
            chemfp.open(filename)

    def test_date_zulu(self):
        filename = support.get_tmpfile(self, "date_wrong_format.fps")
        with open(filename, "w") as f:
            f.write("#FPS1\n")
            f.write("#date=2010-08-09T10:11:12Z\n")
        with self.assertRaisesRegexp(ValueError, "The chemfp specification requires the date be in UTC without a timezone specifier.*2010-08-09T10:11:12Z"):
            chemfp.open(filename)

    def test_date_delta(self):
        filename = support.get_tmpfile(self, "date_wrong_format.fps")
        for delta in range(-15, 16):
            with open(filename, "w") as f:
                f.write("#FPS1\n")
                f.write("#date=2010-08-09T10:11:12%+03d\n" % (delta,))
            with self.assertRaisesRegexp(
                ValueError,
                "The chemfp specification requires the date be in UTC without a timezone specifier.*"
                "2010-08-09T10:11:12[+-][01][0-9]'"):
                chemfp.open(filename)


_cached_fingerprint_load = {}
class TestLoadFingerprints(unittest2.TestCase, CommonReaderAPI):
    hit_order = staticmethod(lambda x: x)
    # Hook to handle the common API
    def _open(self, name):
        try:
            return _cached_fingerprint_load[name]
        except KeyError:
            arena = chemfp.load_fingerprints(name, reorder=False)
            _cached_fingerprint_load[name] = arena
            return arena

    def test_slice_ids(self):
        fps = self._open(CHEBI_TARGETS)
        self.assertEqual(fps.ids[4:10], fps[4:10].ids)
        self.assertEqual(fps.ids[5:20][1:5], fps[6:10].ids)

    def test_slice_fingerprints(self):
        fps = self._open(CHEBI_TARGETS)
        self.assertEqual(fps[5:45][0], fps[5])
        self.assertEqual(fps[5:45][0], fps[5])
        self.assertEqual(fps[5:45][3:6][0], fps[8])

    def test_slice_negative(self):
        fps = self._open(CHEBI_TARGETS)
        self.assertEqual(fps[len(fps)-1], fps[-1])
        self.assertEqual(fps.ids[-2:], fps[-2:].ids)
        self.assertEqual(fps.ids[-2:], fps[-2:].ids)
        self.assertEqual(list(fps[-2:]), [fps[-2], fps[-1]])
        self.assertEqual(fps[-5:-2][-1], fps[-3])

    def test_slice_past_end(self):
        fps = self._open(CHEBI_TARGETS)
        self.assertSequenceEqual(fps[1995:], [
          ('CHEBI:17578', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x16'),
          ('CHEBI:17579', '\x00\x00\x00\x00\x00\x00\x02\x00\x02\n\x00\x00\x04\x88,\x80\x00\x105\x80\x14'),
          ('CHEBI:17580', '\x00\x00\x00\x00\x02\x00\x02\x00\x02\n\x00\x02\x84\x88,\x00\x08\x14\x94\x94\x08'),
          ('CHEBI:17581', '\x00\x00\x00\x00\x00\x000\x01\x80\x00\x02O\x030\x90d\x9c\x7f\xf3\xff\x1d'),
          ('CHEBI:17582', '\x00\x00\x00\x00\x02\x00\x12\x00\x80\x08\x00\x01\x04\x00\x00d\x84L\xa2R\x1c'),
            ])
        self.assertSequenceEqual(fps[2000:], [])

    def test_slice_errors(self):
        arena = self._open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(IndexError, "arena fingerprint index out of range"):
            arena[len(arena)]
        with self.assertRaisesRegexp(IndexError, "arena fingerprint index out of range"):
            arena[-len(arena)-1]
        with self.assertRaisesRegexp(IndexError, "arena slice step size must be 1"):
            arena[4:45:2]
        with self.assertRaisesRegexp(IndexError, "arena slice step size must be 1"):
            arena[45:5:-1]


    def test_search_in_slice(self):
        fps = self._open(CHEBI_TARGETS)
        for i, (id, fp) in enumerate(fps):
            subarena = fps[i:i+1]
            self.assertEqual(len(subarena), 1)
            self.assertEqual(subarena[0][0], id)
            self.assertEqual(subarena[0][1], fp)
            self.assertEqual(subarena.ids[0], id)

            results = subarena.threshold_tanimoto_search_arena(subarena)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].get_ids_and_scores(), [(id, 1.0)])
            hits = [result.get_ids_and_scores() for result in results]
            self.assertEqual(hits, [[(id, 1.0)]])

            results = subarena.knearest_tanimoto_search_arena(subarena)
            query_ids, hits = zip(*result)
            self.assertEqual(len(hits), 1)
            self.assertEqual(results[0].get_ids_and_scores(), [(id, 1.0)])
            hits = [result.get_ids_and_scores() for result in results]
            self.assertEqual(hits, [[(id, 1.0)]])

            counts = subarena.count_tanimoto_hits_arena(subarena)
            self.assertEqual(len(counts), 1)
            self.assertEqual(counts[0], 1)
            self.assertEqual(list(counts), [1])
        self.assertEqual(i, len(fps)-1)

    def test_missing_metatdata_size(self):
        pairs = [("first", hex_decode("1234")),
                 ("second", hex_decode("ABCD"))]
        # Not defined, but that's okay
        reader = chemfp.load_fingerprints(pairs, chemfp.Metadata(type="Blah!"))
        self.assertEqual(reader.metadata.num_bytes, None)
        data = list(reader)
        self.assertEqual(data, pairs)
    
    def test_read_from_id_fp_pairs_num_bytes(self):
        pairs = [("first", hex_decode("1234")),
                 ("second", hex_decode("ABCD"))]
        # Not defined, but that's okay
        reader = chemfp.load_fingerprints(pairs, chemfp.Metadata(type="Blah!"))
        self.assertEqual(reader.metadata.num_bytes, None)
        data = list(reader)
        self.assertEqual(data, pairs)

    def test_read_from_id_fp_pairs_num_bits(self):
        pairs = [("first", hex_decode("1234")),
                 ("second", hex_decode("ABCD"))]
        arena = chemfp.load_fingerprints(pairs, chemfp.Metadata(type="Blah!", num_bits=16))
        self.assertEqual(len(arena), 2)
        self.assertEqual(arena[0], ("first", hex_decode("1234")))
        self.assertEqual(arena[1], ("second", hex_decode("ABCD")))

    def test_declared_size_mismatch(self):
        pairs = [("first", hex_decode("1234"))]
        with self.assertRaisesRegexp(ValueError,
                                     "Fingerprint for id 'first' has 2 bytes "
                                     "while the metadata says it should have 4"):
            arena = chemfp.load_fingerprints(pairs, chemfp.Metadata(type="Blah!", num_bytes=4))

    def test_windows_newline_convention(self):
        with open(CHEBI_TARGETS, "rb") as f:
            content = f.read()
        self.assertNotIn(b"\r", content)
        expected_arena = chemfp.load_fingerprints(StringIO(content))
        
        content = content.replace(b"\n", b"\r\n")
        self.assertIn(b"\r", content)
        filename = support.get_tmpfile(self, "windows_newline.fps")
        with open(filename, "wb") as f:
            f.write(content)
        cr_arena = chemfp.load_fingerprints(filename)

        self.assertEqual(cr_arena.ids, expected_arena.ids)
        self.assertEqual(len(cr_arena), len(expected_arena))
        self.assertEqual(list(cr_arena), list(expected_arena))
        

# Use this to verify the other implementations
from chemfp.slow import SlowFingerprints
_cached_slow_fingerprint_load = {}
class TestSlowFingerprints(unittest2.TestCase, CommonReaderAPI):
    hit_order = staticmethod(lambda x: x)
    def _open(self, name):
        try:
            return _cached_slow_fingerprint_load[name]
        except KeyError:
            reader = chemfp.open(name)
            slow_arena = SlowFingerprints(reader.metadata, list(reader))
            _cached_slow_fingerprint_load[name] = slow_arena
            return slow_arena

_cached_ordered_fingerprint_load = {}
class TestLoadFingerprintsOrdered(unittest2.TestCase, CommonReaderAPI):
    hit_order = staticmethod(sorted)
    # Hook to handle the common API
    def _open(self, name):
        try:
            return _cached_ordered_fingerprint_load[name]
        except KeyError:
            arena = chemfp.load_fingerprints(name, reorder=True)
            _cached_ordered_fingerprint_load[name] = arena
            return arena

    def test_iteration(self):
        expected = [("CHEBI:776", hex_decode("00000000000000008200008490892dc00dc4a7d21e")),
                    ("CHEBI:1148", hex_decode("000000000000200080000002800002040c0482d608")),
                    ("CHEBI:1734", hex_decode("0000000000000221000800111601017000c1a3d21e")),
                    ("CHEBI:1895", hex_decode("00000000000000000000020000100000000400951e")),
                    ("CHEBI:2303", hex_decode("0000000002001021820a00011681015004cdb3d21e"))]
        found = []
        for x in self._open(CHEBI_TARGETS):
            try:
                found.append(expected.index(x))
            except ValueError:
                pass
        self.assertEqual(sorted(found), [0, 1, 2, 3, 4])
        

    def test_arena_is_ordered_by_popcount(self):
        arena = self._open(CHEBI_TARGETS)
        prev = 0
        for id, fp in arena:
            popcount = bitops.byte_popcount(fp)
            self.assertTrue(prev <= popcount, (prev, popcount))
            prev = popcount

    def test_iter_arenas_default_size(self):
        arena = self._open(CHEBI_TARGETS)
        ids = [id for (id, fp) in arena]
        for subarena in arena.iter_arenas():
            self.assertEqual(len(subarena), 1000)
            subids = [id for (id, fp) in subarena]
            self.assertEqual(ids[:1000], subids)
            del ids[:1000]
        self.assertFalse(ids)

    def test_iter_arenas_select_size(self):
        arena = self._open(CHEBI_TARGETS)
        ids = [id for (id, fp) in arena]
        prev = 0
        for subarena in arena.iter_arenas(100):
            self._check_target_metadata(subarena.metadata)
            self.assertEqual(len(subarena), 100)
            subids = []
            for id, fp in subarena:
                subids.append(id)
                popcount = bitops.byte_popcount(fp)
                self.assertTrue(prev <= popcount, (prev, popcount))
                prev = popcount
            
            self.assertEqual(ids[:100], subids)
            del ids[:100]

        self.assertFalse(ids)

    def test_iter_arenas_arena_size_None(self):
        arena = self._open(CHEBI_TARGETS)
        # use None to read all fingerprints into a single arena
        subarenas = list(arena.iter_arenas(None))
        self.assertEqual(len(subarenas), 1)
        self.assertEqual(len(subarenas[0]), 2000)

_expected_records = dict((rec[0], rec) for rec in QUERY_ARENA)
_expected_ids = set(_expected_records)

class TestArenaCopy(unittest2.TestCase):
    def _check_by_id(self, arena, id):
        # The identifier lookup is a bit tricky with copies.
        # This helps me feel a bit better.
        self.assertEqual(arena.get_by_id(id), _expected_records[id])
        self.assertEqual(arena.get_fingerprint_by_id(id), _expected_records[id][1])
        i = arena.get_index_by_id(id)
        self.assertNotEqual(i, None)
        self.assertEqual(arena[i], _expected_records[id])

        # And as long as I'm here, make sure I can look up a random id ..
        new_id = random.choice(arena.ids)
        self.assertEqual(arena.get_by_id(new_id), _expected_records[new_id])

        # .. and a record which doesn't exist
        missing_ids = _expected_ids - set(arena.ids)
        if missing_ids:
            missing_id = missing_ids.pop()
        else:
            missing_id = "spam"
        
        self.assertEqual(arena.get_by_id(missing_id), None)
        self.assertEqual(arena.get_fingerprint_by_id(missing_id), None)
        self.assertEqual(arena.get_index_by_id(missing_id), None)
        

    def _compare(self, arena1, arena2):
        self.assertEqual(len(arena1), len(arena2))
        for i in range(len(arena1)):
            self.assertEqual((i, arena1[i]), (i, arena2[i]))

    def _anti_compare(self, arena1, arena2):
        # These are supposed to be different, where the second is already ordered by popcount
        assert arena2.popcount_indices != "", "arena2 must be sorted!"
        self.assertEqual(len(arena1), len(arena2))
        values1 = list(arena1)
        values2 = list(arena2)
        self.assertNotEqual(values1, values2)
        indices = range(len(arena1))
        indices.sort(key = lambda i: (bitops.byte_popcount(values1[i][1]), i))
        ordered_values1 = [values1[i] for i in indices]
        self.assertEqual(ordered_values1, values2)
        
    def test_simple_copy_of_unordered_arena(self):
        # A copy of an unordered arena leaves things unordered
        arena1 = QUERY_ARENA.copy()
        self.assertEqual(arena1.popcount_indices, "") # internal API; make sure it's unsorted
        self._compare(QUERY_ARENA, arena1)
        # Do it again to make sure.
        arena2 = arena1.copy()
        self._compare(arena1, arena2)
        self._check_by_id(arena1, "CHEBI:17586")
        self._check_by_id(arena2, "CHEBI:17586")

    def test_reordered_copy_of_unordered_arena(self):
        arena1 = QUERY_ARENA.copy(reorder=True)
        self._anti_compare(QUERY_ARENA, arena1)
        self.assertNotEqual(arena1.popcount_indices, "") # internal API; make sure it's sorted
        # Do another copy. This triggers a different path through the code.
        arena2 = arena1.copy()
        self._compare(arena1, arena2)
        self.assertIs(arena1.popcount_indices, arena2.popcount_indices) # internal API; share popcounts
        self._check_by_id(arena1, "CHEBI:17586")
        self._check_by_id(arena2, "CHEBI:17586")

    def test_simple_copy_of_aligned_unordered_arena(self):
        arena1 = chemfp.load_fingerprints(iter(QUERY_ARENA), metadata=QUERY_ARENA.metadata,
                                          alignment=128, reorder=False)
        self.assertEqual(arena1.alignment, 128)
        self.assertEqual(arena1.start_padding + arena1.end_padding, 128-1)
        arena2 = arena1.copy(reorder=False)
        self._compare(arena1, arena2)
        arena3 = arena2.copy(reorder=True)
        self._anti_compare(arena1, arena3)
        self._check_by_id(arena1, "CHEBI:17586")
        self._check_by_id(arena3, "CHEBI:17586")

    def test_copy_of_reordered_arena_slice(self):
        arena1 = QUERY_ARENA.copy(reorder=True)
        arena2_slice = arena1[1:8]
        arena2_copy = arena2_slice.copy()
        self._compare(arena2_slice, arena2_copy)
        self._check_by_id(arena2_slice, "CHEBI:17587")
        self._check_by_id(arena2_copy, "CHEBI:17587")

    def test_copy_of_unordered_arena_slice(self):
        arena1 = QUERY_ARENA.copy(reorder=False)
        arena2_slice = arena1[1:8]
        arena2_copy = arena2_slice.copy()
        self._compare(arena2_slice, arena2_copy)
        self._check_by_id(arena2_slice, "CHEBI:17586")
        self._check_by_id(arena2_copy, "CHEBI:17586")

    def test_empty_input(self):
        arena1 = QUERY_ARENA[2:8][2:4][1:1]
        arena2 = arena1.copy()
        self._compare(arena1, arena2)

    ##### Work with indicies
    
    def test_select_all(self):
        arena1 = QUERY_ARENA.copy()
        arena2 = arena1.copy(indices=range(len(arena1)), reorder=False)
        self._compare(arena1, arena2)
        self._check_by_id(arena1, "CHEBI:17586")
        self._check_by_id(arena2, "CHEBI:17586")

    def test_select_all_reversed(self):
        arena1 = QUERY_ARENA.copy()
        arena2 = arena1.copy(indices=range(len(arena1)-1, -1, -1), reorder=False)
        self.assertEqual(arena1.ids, arena2.ids[::-1])
        self.assertEqual(list(arena1), list(reversed(arena2)))
        self._check_by_id(arena2, "CHEBI:17586")

    def test_subset_equals_slice(self):
        arena1 = QUERY_ARENA.copy(indices=range(2, 8), reorder=False)
        self._compare(arena1, QUERY_ARENA[2:8])
        self._check_by_id(arena1, "CHEBI:17589")

    def test_double_subset_equals_slice(self):
        arena1 = QUERY_ARENA.copy(indices=range(2, 8), reorder=False)
        arena2 = arena1.copy(indices=range(1, 3), reorder=False)
        self._compare(arena2, QUERY_ARENA[3:5])
        self._check_by_id(arena2, "CHEBI:17588")

    def test_negative_subset(self):
        arena1 = QUERY_ARENA.copy(indices=[-4, -3, -2], reorder=False)
        self._compare(arena1, QUERY_ARENA[6:9])
        self._check_by_id(arena1, "CHEBI:17592")

    def test_duplicate_indices(self):
        arena1 = QUERY_ARENA.copy(indices=[0, 0, 0], reorder=False)
        self.assertEqual(len(arena1), 3)
        self.assertEqual(arena1[0], arena1[1])
        self.assertEqual(arena1[0], arena1[2])
        self._check_by_id(arena1, "CHEBI:17585")

    def test_ordered_copy_with_indicies_from_unordered(self):
        arena1 = QUERY_ARENA.copy(indices=[3, 5, 9], reorder=True)
        self.assertNotEqual(arena1.popcount_indices, "")
        popcounts = [bitops.byte_popcount(fp) for (id, fp) in arena1]
        self.assertEqual(popcounts, sorted(popcounts))

        arena2 = chemfp.load_fingerprints((QUERY_ARENA[i] for i in [3, 5, 9]), QUERY_ARENA.metadata)
        self._compare(arena1, arena2)
        self._check_by_id(arena1, "CHEBI:17597")
        self._check_by_id(arena2, "CHEBI:17597")

    def test_unordered_copy_with_indicies_from_ordered(self):
        arena1 = QUERY_ARENA.copy(reorder=True)
        self.assertNotEqual(arena1.popcount_indices, "")
        arena2 = arena1.copy(indices=[2,3,6,7,9], reorder=False)
        self.assertEqual(arena2.popcount_indices, "")
        self._check_by_id(arena2, "CHEBI:17597")
            
    def test_ordered_copy_with_indicies_from_ordered(self):
        arena1 = QUERY_ARENA.copy(reorder=True)
        self.assertNotEqual(arena1.popcount_indices, "")
        arena2 = arena1.copy(indices=[2,3,6,7,9])
        self.assertNotEqual(arena2.popcount_indices, "")
        self.assertEqual(arena1[2], arena2[0])
        self.assertEqual(arena1[3], arena2[1])

        # make sure that reorder=True changes nothing
        arena2 = arena1.copy(indices=[2,3,6,7,9], reorder=True)
        self.assertNotEqual(arena2.popcount_indices, "")
        self.assertEqual(arena1[2], arena2[0])
        self.assertEqual(arena1[3], arena2[1])
            
        
    def test_empty_input_with_indices(self):
        arena1 = QUERY_ARENA.copy(indices=[])
        self._compare(arena1, QUERY_ARENA[8:7])

    def test_indices_out_of_range(self):
        with self.assertRaisesRegexp(IndexError, "arena fingerprint index 100 is out of range"):
            QUERY_ARENA.copy(indices=[100])
        with self.assertRaisesRegexp(IndexError, "arena fingerprint index 0 is out of range"):
            QUERY_ARENA[4:4].copy(indices=[0])

    def test_reorder_is_none_when_arena_is_unordered(self):
        arena1 = QUERY_ARENA.copy(reorder=None)
        self.assertEqual(arena1.popcount_indices, "")
        
    def test_reorder_is_none_when_arena_is_ordered(self):
        arena1 = QUERY_ARENA.copy(reorder=True)
        self.assertNotEqual(arena1.popcount_indices, "")
        arena2 = arena1.copy()
        self.assertNotEqual(arena2.popcount_indices, "")
        
        
        
        
# These tests use part of the private, internal API (the "_id_lookup").
# That's the only way I could figure out to make sure I'm caching correctly.
class TestArenaGetById(unittest2.TestCase):
    def test_get_by_id(self):
        arena = QUERY_ARENA.copy()
        assert arena._id_lookup is None
        record = arena.get_by_id("CHEBI:17586")
        self.assertEqual(record, ("CHEBI:17586",
                                  hex_decode("002000102084302197d69ecfbbf3b4ffdf6ffeff1f")))
        assert arena._id_lookup is not None

    def test_get_by_id_not_present(self):
        arena = QUERY_ARENA.copy()
        assert arena._id_lookup is None
        record = arena.get_by_id("spam")
        self.assertIs(record, None)
        assert arena._id_lookup is not None
        
    def test_get_index_by_id(self):
        arena = QUERY_ARENA.copy()
        assert arena._id_lookup is None
        index = arena.get_index_by_id("CHEBI:17586")
        self.assertEqual(index, 1)
        assert arena._id_lookup is not None

    def test_get_index_by_id_not_present(self):
        arena = QUERY_ARENA.copy()
        assert arena._id_lookup is None
        index = arena.get_index_by_id("spam")
        self.assertIs(index, None)
        assert arena._id_lookup is not None

    def test_get_fingerprint_by_id(self):
        arena = QUERY_ARENA.copy()
        assert arena._id_lookup is None
        fp = arena.get_fingerprint_by_id("CHEBI:17586")
        self.assertEqual(fp, hex_decode("002000102084302197d69ecfbbf3b4ffdf6ffeff1f"))
        assert arena._id_lookup is not None
        
    def test_get_fingerprint_by_id_not_present(self):
        arena = QUERY_ARENA.copy()
        assert arena._id_lookup is None
        fp = arena.get_fingerprint_by_id("spam")
        self.assertIs(fp, None)
        assert arena._id_lookup is not None

    def test_duplicate_id(self):
        arena = chemfp.load_fingerprints([("id1", "ABCD"),
                                          ("id2", "EFGH"),
                                          ("id3", "IJKL"),
                                          ("id2", "MNOP")],
                                          metadata = chemfp.Metadata(num_bytes=4),
                                          reorder=False)
        self.assertEqual(arena.get_fingerprint_by_id("id1"), "ABCD")
        self.assertEqual(arena.get_fingerprint_by_id("id3"), "IJKL")
        self.assertIn(arena.get_fingerprint_by_id("id2"), ("EFGH", "MNOP"))

        self.assertEqual(arena.get_index_by_id("id1"), 0)
        self.assertEqual(arena.get_index_by_id("id3"), 2)
        self.assertIn(arena.get_index_by_id("id2"), (1, 3))
        

_sample_arena = chemfp.load_fingerprints(
    [
        ("A", b"12345678"), # 29 bits
        ("B", b"13456780"), # 28 bits
        ("C", b"1456711~"), # 31 bits
        ("D", b"1567812z"), # 30 bits
        ], metadata=chemfp.Metadata(num_bytes=8), reorder=False)

class TestArenaSample(unittest2.TestCase):
    def test_sample_1_no_rng(self):
        ids = dict.fromkeys("ABCD", 0)
        for i in range(200):
            a = _sample_arena.sample(1)
            self.assertEqual(len(a), 1)
            ids[a.ids[0]] += 1
        # The odds of this failing are quite low
        self.assertGreater(ids["A"], 10)
        self.assertGreater(ids["B"], 10)
        self.assertGreater(ids["C"], 10)
        self.assertGreater(ids["D"], 10)

    def test_sample_1_fixed_key(self):
        ids = dict.fromkeys("ABCD", 0)
        for i in range(200):
            a = _sample_arena.sample(1, rng=34)
            self.assertEqual(len(a), 1)
            ids[a.ids[0]] += 1
        # All of the samples must go to one key
        self.assertEqual(sum(1 for v in ids.values() if v == 200), 1)
        self.assertEqual(sum(1 for v in ids.values() if v == 0), 3)
        
    def test_sample_1_python_rng(self):
        import random
        ids = dict.fromkeys("ABCD", 0)
        for i in range(200):
            a = _sample_arena.sample(1, rng=random.Random(34))
            self.assertEqual(len(a), 1)
            ids[a.ids[0]] += 1
        # All of the samples must go to one key
        self.assertEqual(sum(1 for v in ids.values() if v == 200), 1)
        self.assertEqual(sum(1 for v in ids.values() if v == 0), 3)

    def test_sample_uses_rng_as_generator_instead_of_hash(self):
        import random
        ids1 = _sample_arena.sample(4, rng=34).ids
        ids2 = _sample_arena.sample(4, rng=random.Random(34)).ids
        self.assertEqual(ids1, ids2)

    def test_sample_2_has_no_duplicates(self):
        for i in range(10):
            a = _sample_arena.sample(2)
            self.assertEqual(len(a), 2)
            id1, id2 = a.ids
            self.assertNotEqual(id1, id2)
            
            # also check that the fingerprints are reordered by default
            fp1 = a.get_fingerprint(0)
            fp2 = a.get_fingerprint(1)
            self.assertLess(
                bitops.byte_popcount(fp1),
                bitops.byte_popcount(fp2)
                )
        
    def test_sample_2_no_reorder(self):
        # ensure it isn't ordered
        for i, expected_popcount in enumerate((29, 28, 31, 30)):
            self.assertEqual(bitops.byte_popcount(_sample_arena.get_fingerprint(i)), expected_popcount)

        order_counts = [0, 0]
        for i in range(40):
            a = _sample_arena.sample(2, reorder=False)
            fp1 = a.get_fingerprint(0)
            fp2 = a.get_fingerprint(1)
            order_counts[bitops.byte_popcount(fp1) > bitops.byte_popcount(fp2)] += 1
        self.assertNotEqual(order_counts[0], 0)
        self.assertNotEqual(order_counts[1], 0)
        
    def test_sample_fractional_size(self):
        for i in range(10):
            a = _sample_arena.sample(0.75)
            self.assertEqual(len(a), 3)
            self.assertEqual(len(set(a.ids)), 3)
            
            a = _sample_arena.sample(0.25)
            self.assertEqual(len(a), 1)

    def test_empty_int(self):
        a = _sample_arena.sample(0)
        self.assertEqual(len(a), 0)
        self.assertFalse(a)
        
    def test_empty_float(self):
        a = _sample_arena.sample(0.0)
        self.assertEqual(len(a), 0)
        self.assertFalse(a)

    def test_all_int_reorder(self):
        a = _sample_arena.sample(4)
        self.assertEqual(len(a), 4)
        # the default reorders
        self.assertEqual(a.ids, ["B", "A", "D", "C"])

        # repeat with an explicit reorder
        a = _sample_arena.sample(4, reorder=True)
        self.assertEqual(len(a), 4)
        self.assertEqual(a.ids, ["B", "A", "D", "C"])
        
    def test_all_int_random_order(self):
        seen = set()
        for i in range(50):
            a = _sample_arena.sample(4, reorder=False)
            seen.add(tuple(a.ids))

        # the odds of seeing no more than 5 unique orderings is very low
        # (5./24) ** 50 = 8.7E-35
        self.assertGreater(len(seen), 5)

    def test_all_float_reorder(self):
        a = _sample_arena.sample(1.0)
        self.assertEqual(len(a), 4)
        # the default reorders
        self.assertEqual(a.ids, ["B", "A", "D", "C"])

    def test_int_size_out_of_bounds(self):
        for size in (-5, -2, -1, 5, 6):
            with self.assertRaisesRegexp(ValueError, "num_samples int value must be between 0 and 4, inclusive"):
                _sample_arena.sample(size)
            
    def test_float_size_out_of_bounds(self):
        for size in (-1.0, -0.001, 1.0001, 10.0, float("nan"), float("inf"), float("-inf")):
            with self.assertRaisesRegexp(ValueError, "num_samples float value must be between 0.0 and 1.0, inclusive"):
                _sample_arena.sample(size)
            
    def test_str_size(self):
        with self.assertRaisesRegexp(ValueError, "num_samples must be an integer or a float"):
            _sample_arena.sample("1")

    def test_reorder_None(self):
        with self.assertRaisesRegexp(NotImplementedError, "reorder=None is not supported"):
            _sample_arena.sample(1, reorder=None)

            
class TestArenaTrainTestSplit(unittest2.TestCase):
    def test_default(self):
        # 75/25 split
        train, test = _sample_arena.train_test_split()
        self.assertEqual(len(train), 3)
        self.assertEqual(len(test), 1)

    def test_with_train_size_int(self):
        for train_size in range(4):
            train, test = _sample_arena.train_test_split(train_size=train_size)
            self.assertEqual(len(train), train_size)
            self.assertEqual(len(test), 4-train_size)

    def test_with_test_size_int(self):
        for test_size in range(4):
            train, test = _sample_arena.train_test_split(test_size=test_size)
            self.assertEqual(len(train), 4-test_size)
            self.assertEqual(len(test), test_size)
            
    def test_with_train_size_float(self):
        for train_size_f in [0.0, 0.1, 0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8, 1.0]:
            train_size = int(4 * train_size_f)
            train, test = _sample_arena.train_test_split(train_size=train_size_f)
            self.assertEqual(len(train), train_size)
            self.assertEqual(len(test), 4-train_size)

    def test_with_test_size_float(self):
        for test_size_f in [0.0, 0.1, 0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8, 1.0]:
            test_size = int(4 * test_size_f)
            train, test = _sample_arena.train_test_split(test_size=test_size)
            self.assertEqual(len(train), 4-test_size)
            self.assertEqual(len(test), test_size)
            
    def test_with_both_sizes_int(self):
        for train_size, test_size in (
                (0, 0),
                (1, 1),
                (2, 1),
                (1, 2),
                (0, 3),
                (3, 0),
                (3, 1),
                ):
            train, test = _sample_arena.train_test_split(train_size=train_size, test_size=test_size)
            self.assertEqual(len(train), train_size)
            self.assertEqual(len(test), test_size)
    
    def test_with_both_sizes_float(self):
        for train_size_f, test_size_f in (
                (0.0,  0.0),
                (0.1,  0.8),
                (0.25, 0.25),
                (0.5,  0.25),
                (0.25, 0.5),
                (0,    0.75),
                (0.75, 0),
                (0.75, 0.25),
                ):
            train, test = _sample_arena.train_test_split(train_size=train_size_f, test_size=test_size_f)
            self.assertEqual(len(train), int(4*train_size_f))
            self.assertEqual(len(test), int(4*test_size_f))

    def test_out_of_range_test_sizes_int(self):
        for test_size in (-1, 5):
            with self.assertRaisesRegexp(ValueError, "test_size int must be between 0 and 4, inclusive"):
                _sample_arena.train_test_split(train_size=0, test_size=test_size)
            with self.assertRaisesRegexp(ValueError, "test_size int must be between 0 and 4, inclusive"):
                _sample_arena.train_test_split(train_size=None, test_size=test_size)
            
    def test_out_of_range_test_sizes_float(self):
        for test_size in (-1.0, -0.001, 1.001, 10.0, float("nan"), float("-inf"), float("inf")):
            with self.assertRaisesRegexp(ValueError, "test_size float must be between 0.0 and 1.0, inclusive"):
                _sample_arena.train_test_split(train_size=0, test_size=test_size)
            with self.assertRaisesRegexp(ValueError, "test_size float must be between 0.0 and 1.0, inclusive"):
                _sample_arena.train_test_split(train_size=None, test_size=test_size)

    def test_out_of_range_train_sizes_int(self):
        for train_size in (-1, 5):
            with self.assertRaisesRegexp(ValueError, "train_size int must be between 0 and 4, inclusive"):
                _sample_arena.train_test_split(train_size=train_size, test_size=0)
            with self.assertRaisesRegexp(ValueError, "train_size int must be between 0 and 4, inclusive"):
                _sample_arena.train_test_split(train_size=train_size, test_size=None)
            
    def test_out_of_range_train_sizes_float(self):
        for train_size in (-1.0, -0.001, 1.001, 10.0, float("nan"), float("-inf"), float("inf")):
            with self.assertRaisesRegexp(ValueError, "train_size float must be between 0.0 and 1.0, inclusive"):
                _sample_arena.train_test_split(train_size=train_size, test_size=0)
            with self.assertRaisesRegexp(ValueError, "train_size float must be between 0.0 and 1.0, inclusive"):
                _sample_arena.train_test_split(train_size=train_size, test_size=None)

    def test_train_size_str(self):
        with self.assertRaisesRegexp(ValueError, "train_size must be an integer, float, or None"):
            _sample_arena.train_test_split(train_size="1", test_size=None)
        with self.assertRaisesRegexp(ValueError, "train_size must be an integer, float, or None"):
            _sample_arena.train_test_split(train_size="1", test_size=0)
            
    def test_test_size_str(self):
        with self.assertRaisesRegexp(ValueError, "test_size must be an integer, float, or None"):
            _sample_arena.train_test_split(train_size=None, test_size="1")
        with self.assertRaisesRegexp(ValueError, "test_size must be an integer, float, or None"):
            _sample_arena.train_test_split(train_size=0, test_size="1")
            

    def test_sum_size_too_large(self):
        for train_size, test_size, needed_size in (
                (4, 4, 8),
                (1.0, 4, 8),
                (2, 3, 5),
                (2, 0.75, 5),
                (0.5, 0.75, 5),
                ):
            with self.assertRaisesRegexp(
                    ValueError,
                    "The sum of test_size and train_size requires %d samples, but only 4 fingerprints are available" %
                    (needed_size,)):
                _sample_arena.train_test_split(train_size=train_size, test_size=test_size)
            
    def test_default_rng(self):
        seen = set()
        for i in range(50):
            train, test = _sample_arena.train_test_split(2, 2)
            id1, id2 = train.ids
            id3, id4 = test.ids
            self.assertNotIn(id1, [id2, id3, id4])
            self.assertNotIn(id2, [id1, id3, id4])
            self.assertNotIn(id3, [id1, id2, id4])
            self.assertNotIn(id4, [id1, id2, id3])
            seen.add( (id1, id2, id3, id4) )
        self.assertGreater(len(seen), 5)

    def test_specified_rng_seed(self):
        seen = set()
        for i in range(50):
            train, test = _sample_arena.train_test_split(2, 2, rng=1234)
            id1, id2 = train.ids
            id3, id4 = test.ids
            self.assertNotIn(id1, [id2, id3, id4])
            self.assertNotIn(id2, [id1, id3, id4])
            self.assertNotIn(id3, [id1, id2, id4])
            self.assertNotIn(id4, [id1, id2, id3])
            seen.add( (id1, id2, id3, id4) )
        self.assertEqual(len(seen), 1)

    def test_specified_rng_obj(self):
        seen = set()
        import random
        for i in range(50):
            rng = random.Random(65)
            train, test = _sample_arena.train_test_split(2, 2, rng=rng)
            id1, id2 = train.ids
            id3, id4 = test.ids
            self.assertNotIn(id1, [id2, id3, id4])
            self.assertNotIn(id2, [id1, id3, id4])
            self.assertNotIn(id3, [id1, id2, id4])
            self.assertNotIn(id4, [id1, id2, id3])
            seen.add( (id1, id2, id3, id4) )
        self.assertEqual(len(seen), 1)
        
    def test_reorder_None(self):
        with self.assertRaisesRegexp(NotImplementedError, "reorder=None is not supported"):
            _sample_arena.sample(1, reorder=None)
        
SDF_IDS = ['9425004', '9425009', '9425012', '9425015', '9425018',
           '9425021', '9425030', '9425031', '9425032', '9425033',
           '9425034', '9425035', '9425036', '9425037', '9425040',
           '9425041', '9425042', '9425045', '9425046']

class ReadMoleculeFingerprints(object):
    def _read_ids(self, *args, **kwargs):
        reader = chemfp.read_molecule_fingerprints(*args, **kwargs)
        self.assertEqual(reader.metadata.num_bits, self.num_bits)
        ids = [id for (id, fp) in reader]
        self.assertEqual(len(fp), self.fp_size)
        return ids
        
    def test_read_simple(self):
        ids = self._read_ids(self.type, source=PUBCHEM_SDF)
        self.assertEqual(ids, SDF_IDS)

    def test_read_simple_compressed(self):
        ids = self._read_ids(self.type, source=PUBCHEM_SDF_GZ)
        self.assertEqual(ids, SDF_IDS)

    def test_read_missing_filename(self):
        with self.assertRaises(IOError):
            self._read_ids(self.type, "this_file_does_not_exist.sdf")

    def test_read_metadata(self):
        metadata = chemfp.Metadata(type=self.type)
        ids = self._read_ids(metadata, source=PUBCHEM_SDF_GZ)
        self.assertEqual(ids, SDF_IDS)

    def test_read_sdf_gz(self):
        ids = self._read_ids(self.type, source=PUBCHEM_SDF_GZ, format="sdf.gz")
        self.assertEqual(ids, SDF_IDS)

    def test_read_sdf(self):
        ids = self._read_ids(self.type, source=PUBCHEM_SDF, format="sdf")
        self.assertEqual(ids, SDF_IDS)

    def test_read_bad_format(self):
        with self.assertRaisesRegexp(ValueError, "does not support compression type 'xyzzy'"):
            self._read_ids(self.type, source=PUBCHEM_SDF, format="sdf.xyzzy")
            
    def test_read_bad_compression(self):
        with self.assertRaisesRegexp(ValueError, "does not support compression type 'Z'"):
            self._read_ids(self.type, source=PUBCHEM_SDF, format="sdf.Z")

    def test_read_bad_format_specification(self):
        with self.assertRaisesRegexp(ValueError, "does not support compression type '@'"):
            self._read_ids(self.type, source=PUBCHEM_SDF, format="sdf.@")

    def test_read_id_tag(self):
        ids = self._read_ids(self.type, source=PUBCHEM_SDF, id_tag = "PUBCHEM_MOLECULAR_FORMULA")
        self.assertEqual(ids, ["C16H16ClFN4O2", "C18H20N6O3", "C14H19N5O3", "C23H24N4O3", 
                                "C18H23N5O3S", "C19H21ClN4O4", "C18H31N6O4S+", "C18H30N6O4S",
                                "C16H20N4O2", "C19H21N5O3S", "C18H22N4O2", "C18H20ClN5O3",
                                "C16H20N8O2", "C15H17ClN6O3", "C19H21N5O4", "C17H19N5O4",
                                "C17H19N5O4", "C19H23N5O2S", "C15H17BrN4O3"])

# I decided to not check this. The failure is that you'll get a "can't find id" error. Oh well.
#    def test_read_invalid_id_tag(self):
#        self._read_ids(self.type, PUBCHEM_SDF, id_tag = "This\tis\ninvalid>")

    def test_read_smiles(self):
        # Need at least one test with some other format
        ids = self._read_ids(self.type, source=MACCS_SMI)
        self.assertEqual(ids, ["3->bit_2", "4->bit_3", "5->bit_4", "6->bit_5", 
                                "10->bit_9", "11->bit_10", "17->bit_16"] )

    def test_read_unknown_format(self):
        with self.assertRaisesRegexp(ValueError, "does not support the.*should_be_sdf_but_is_not' format"):
            self._read_ids(self.type, fullpath("pubchem.should_be_sdf_but_is_not"))

    def test_read_known_format(self):
        ids = self._read_ids(self.type, fullpath("pubchem.should_be_sdf_but_is_not"), "sdf")
        self.assertEqual(ids, SDF_IDS)

    ## def test_read_errors_strict(self):
    ##     with self.assertRaisesRegexp(chemfp.ParseError, "Missing title for record #1,.*missing_title.sdf"):
    ##         self._read_ids(self.type, fullpath("missing_title.sdf"), errors="strict")

    def test_read_errors_ignore(self):
        ids = self._read_ids(self.type, fullpath("missing_title.sdf"), errors="ignore")
        if self.toolkit in ("openbabel", "openeye"):
            self.assertEqual(ids, ["", "Good", ""])
        else:
            self.assertEqual(ids, ["", "Good", "\t"])

    ## def test_read_errors_report(self):
    ##     import sys
    ##     from cStringIO import StringIO
    ##     old_stderr = sys.stderr
    ##     sys.stderr = new_stderr = StringIO()
    ##     try:
    ##         ids = self._read_ids(self.type, fullpath("missing_title.sdf"), errors="report")
    ##     finally:
    ##         sys.stderr = old_stderr
    ##         errmsg = new_stderr.getvalue()
            
    ##     self.assertEqual(ids, ["Good"])
    ##     self.assertIn("ERROR: Missing title for record #1", errmsg)
    ##     self.assertNotIn("record #2", errmsg)
    ##     self.assertIn("ERROR: Missing title for record #3", errmsg)
    ##     self.assertIn("Skipping.\n", errmsg)

    ## def test_read_errors_wrong_setting(self):
    ##     with self.assertRaisesRegexp(ValueError, "'errors' value must be an ErrorHandler or one of 'ignore', 'log', 'report', 'strict'"):
    ##         self._read_ids(self.type, PUBCHEM_SDF, errors="this-is-not.a.valid! setting")
            
    def test_read_errors_wrong_setting(self):
        with self.assertRaisesRegexp(ValueError,
                                     "'errors' value must be an ErrorHandler or one of 'ignore', 'log', 'report', "
                                     "'strict', not 'this-is-not.a.valid! setting'"):
            self._read_ids(self.type, PUBCHEM_SDF, errors="this-is-not.a.valid! setting")

    
# Test classes for the different toolkits

class TestOpenBabelReadMoleculeFingerprints(unittest2.TestCase, ReadMoleculeFingerprints):
    toolkit = "openbabel"
    type = "OpenBabel-FP2/1"
    num_bits = 1021
    fp_size = 128

TestOpenBabelReadMoleculeFingerprints = (
  unittest2.skipUnless(has_openbabel, "Open Babel not available")(TestOpenBabelReadMoleculeFingerprints)
)

class TestOpenEyeReadMoleculeFingerprints(unittest2.TestCase, ReadMoleculeFingerprints):
    toolkit = "openeye"
    type = "OpenEye-Path/2"
    num_bits = 4096
    fp_size = 512

    # I haven't yet figured out how 'aromaticity' is exposed in the high-level interface
    # For now, test the toolkit-specific API
    def test_read_unknown_aromaticity(self):
        with self.assertRaisesRegexp(ValueError, "Unsupported aromaticity model 'smelly'"):
            openeye.read_structures(PUBCHEM_SDF, reader_args = {"aromaticity": "smelly"})

    def test_default_aromaticity(self):
        mol_reader = openeye.read_structures(PUBCHEM_SDF)
        default_smiles = [oechem.OECreateIsoSmiString(mol) for (id, mol) in mol_reader]

        mol_reader = openeye.read_structures(PUBCHEM_SDF, reader_args={"aromaticity": "openeye"})
        openeye_smiles = [oechem.OECreateIsoSmiString(mol) for (id, mol) in mol_reader]
        self.assertSequenceEqual(default_smiles, openeye_smiles)

        mol_reader = openeye.read_structures(PUBCHEM_SDF, reader_args={"aromaticity": "mdl"})
        mdl_smiles = [oechem.OECreateIsoSmiString(mol) for (id, mol) in mol_reader]
        for (smi1, smi2) in zip(default_smiles, mdl_smiles):
            if (smi1 == smi2):
                break
        else:
            raise AssertionError("MDL aromaticity model should not be the same as OpenEye's")
        
TestOpenEyeReadMoleculeFingerprints = (
  unittest2.skipUnless(has_openeye, "OpenEye not available")(TestOpenEyeReadMoleculeFingerprints)
)

class TestRDKitReadMoleculeFingerprints(unittest2.TestCase, ReadMoleculeFingerprints):
    toolkit = "rdkit"
    type = "RDKit-Fingerprint"
    num_bits = 2048
    fp_size = 256

    def test_read_from_compressed_input_using_default_type(self):
        from StringIO import StringIO
        f = StringIO("\x1f\x8b\x08\x00\xa9\\,O\x02\xff3042vt\xe3t\xccK)J-\xe7\x02\x00\xfe'\x16\x99\x0e\x00\x00\x00")
        f.name = "test.gz"
        values = list(chemfp.open(f))
        self.assertEqual(values, [("Andrew", hex_decode("0123AF"))])

TestRDKitReadMoleculeFingerprints = (
  unittest2.skipUnless(has_rdkit, "RDKit not available")(TestRDKitReadMoleculeFingerprints)
)

class ReadMoleculeFingerprintsErrors(unittest2.TestCase):
    def test_metadata_without_type(self):
        with self.assertRaisesRegexp(ValueError, "Missing fingerprint type information in metadata"):
            chemfp.read_molecule_fingerprints(chemfp.Metadata(num_bits=13))
    

# This also tests 'count_tanimoto_hits'
class TestFPSParser(unittest2.TestCase):
    def test_open_with_unknown_format(self):
        with self.assertRaisesRegexp(ValueError, "Unable to determine fingerprint format type from 'spam.pdf'"):
            chemfp.open("spam.pdf")
        with self.assertRaisesRegexp(ValueError, "Unsupported fingerprint format 'pdf'"):
            chemfp.open("spam.sdf", format="pdf")

    def test_fpb_failure(self):
        with self.assertRaisesRegexp(NotImplementedError, "fpb format support not implemented"):
            chemfp.open("spam.fpb")

    def test_base_case(self):
        values = list(chemfp.open(StringIO("ABCD\tfirst\n")))
        self.assertSequenceEqual(values, [("first", hex_decode("ABCD"))])
            
    def test_unsupported_whitespace(self):
        with self.assertRaisesRegexp(chemfp.ChemFPError, "Unsupported whitespace, line 1"):
            list(chemfp.open(StringIO("ABCD first\n")))

    def test_missing_id(self):
        with self.assertRaisesRegexp(chemfp.ChemFPError, "Missing id field, line 1"):
            list(chemfp.open(StringIO("ABCD\n")))
        with self.assertRaisesRegexp(chemfp.ChemFPError, "Missing id field, line 2"):
            list(chemfp.open(StringIO("0000\tXYZZY\nABCD\n")))

    def test_error_properties(self):
        from StringIO import StringIO
        f = StringIO("1234 first\n")
        f.name = "spam"
        try:
            list(chemfp.open(f))
            raise AssertionError("Should not get here")
        except chemfp.ChemFPError, err:
            self.assertEqual(str(err), "Unsupported whitespace, file 'spam', line 1")
            self.assertEqual(str(err), "Unsupported whitespace, file 'spam', line 1")
            self.assertEqual(err.location.lineno, 1)
            self.assertEqual(err.location.filename, "spam")

    def test_count_size_mismatch(self):
        query_arena = chemfp.load_fingerprints(StringIO("AB\tSmall\n"))
        targets = chemfp.open(StringIO("1234\tSpam\nABBA\tDancingQueen\n"))
        with self.assertRaisesRegexp(ValueError, "query_arena has 8 bits while target_reader has 16 bits"):
            chemfp.count_tanimoto_hits(query_arena, targets, 0.1)

    def test_count_size_changes(self):
        query_arena = chemfp.load_fingerprints(StringIO("ABCD\tSmall\n"))
        targets = chemfp.open(StringIO("1234\tSpam\nABBA\tDancingQueen\n" * 200 + "12\tNo-no!\n"))
        with self.assertRaisesRegexp(chemfp.ChemFPError, "Fingerprint is not the expected length, line 401"):
            list(chemfp.count_tanimoto_hits(query_arena, targets, 0.1))
    
    def test_count_size_bad_target_fps(self):
        query_arena = chemfp.load_fingerprints(StringIO("ABCD\tSmall\n"))
        targets = chemfp.open(StringIO("1234\tSpam\nABBA DancingQueen\n"))
        with self.assertRaisesRegexp(chemfp.ChemFPError, "Unsupported whitespace, line 2"):
            list(chemfp.count_tanimoto_hits(query_arena, targets, 0.1))

    def test_count_size_bad_query_fps(self):
        from StringIO import StringIO
        f = StringIO("DBAC\tLarge\nABCD Small\n")
        f.name = "query.fps"
        queries = chemfp.open(f)
        targets = chemfp.open(StringIO("1234\tSpam\nABBA\tDancingQueen\n"))
        with self.assertRaisesRegexp(chemfp.ChemFPError, "Unsupported whitespace.*'query.fps'.*line 2"):
            list(chemfp.count_tanimoto_hits(queries, targets, 0.1))

    def test_count_size_bad_fps_later_on(self):
        queries = chemfp.open(StringIO("ABCD\tSmall\n" * 200 + "AACE Oops.\n"))
        targets = chemfp.load_fingerprints(StringIO("1234\tSpam\nABBA\tDancingQueen\n"))
        results = chemfp.count_tanimoto_hits(queries, targets, 0.1)
        for i in range(10):
            results.next()
        with self.assertRaisesRegexp(chemfp.ChemFPError, "Unsupported whitespace.*line 201"):
            list(results)

    def test_empty_input(self):
        queries = chemfp.load_fingerprints([], chemfp.Metadata(num_bytes=16))
        targets = chemfp.load_fingerprints(StringIO("1234\tSpam\nABBA\tDancingQueen\n"))
        results = chemfp.count_tanimoto_hits(queries, targets, 0.34)
        for x in results:
            raise AssertionError("Should not get here")


class CountTanimotoHits(unittest2.TestCase):
    def test_with_initial_offset(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        it = targets.iter_arenas(10)
        # Skip the first arena and use only the second
        next(it)
        subarena = next(it)
        hits = list(chemfp.count_tanimoto_hits(subarena, subarena, 0.2, arena_size=3))
        self.assertEqual(hits, 
                         [("CHEBI:15343", 6), ("CHEBI:15858", 4), ("CHEBI:16007", 3),
                          ("CHEBI:16052", 4), ("CHEBI:16234", 7), ("CHEBI:16382", 4),
                          ("CHEBI:16716", 1), ("CHEBI:16842", 5), ("CHEBI:17051", 4),
                          ("CHEBI:17087", 4)])
        self.assertEqual(subarena.ids,
                         ["CHEBI:15343", "CHEBI:15858", "CHEBI:16007", "CHEBI:16052", "CHEBI:16234",
                          "CHEBI:16382", "CHEBI:16716", "CHEBI:16842", "CHEBI:17051", "CHEBI:17087"])
        self.assertEqual(len(subarena.arena_ids), len(targets))
        self.assertEqual(subarena.ids, targets.arena_ids[10:20])
        
            
    def test_with_large_input(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        for (query_id, count) in chemfp.count_tanimoto_hits(targets, targets, threshold=0.9,
                                                             arena_size=10):
            pass
        self.assertEqual(query_id, "CHEBI:16379")
        self.assertEqual(count, 5)
        

class ThresholdTanimotoSearch(unittest2.TestCase):
    def test_with_fps_reader_as_targets(self):
        queries = chemfp.open(CHEBI_QUERIES).iter_arenas(10).next()
        targets = chemfp.open(CHEBI_TARGETS)
        fps_results = chemfp.threshold_tanimoto_search(queries, targets)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(fps_results)
        results = list(fps_results)
        self.assertEqual(len(results), 10)
        query_id, result = results[0]
        self.assertEqual(query_id, "CHEBI:17585")
        self.assertEqual(len(result), 4)
        result.reorder("increasing-score")
        self.assertEqual(result.get_scores(),
                          [0.7142857142857143, 0.72222222222222221, 0.8571428571428571, 0.8571428571428571])
        self.assertEqual(result.get_ids(),
                          ['CHEBI:16148', 'CHEBI:17539', 'CHEBI:17034', 'CHEBI:17302'])

        query_id, result = results[3]
        self.assertEqual(query_id, "CHEBI:17588")
        self.assertEqual(len(result), 32)
        result.reorder("decreasing-score")
        expected_scores = [1.0, 0.88, 0.88, 0.88, 0.85185185185185186, 0.85185185185185186]
        expected_ids = ['CHEBI:17230', 'CHEBI:15356', 'CHEBI:16375', 'CHEBI:17561', 'CHEBI:15729', 'CHEBI:16176']
        self.assertEqual(result.get_scores()[:6], expected_scores)
        self.assertEqual(result.get_ids()[:6], expected_ids)
        self.assertEqual(result.get_ids_and_scores()[:6], zip(expected_ids, expected_scores))

    def test_with_arena_as_targets(self):
        queries = chemfp.load_fingerprints(CHEBI_QUERIES, reorder=False)[:10]
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        arena_results = chemfp.threshold_tanimoto_search(queries, targets)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(arena_results)
        results = list(arena_results)
        self.assertEqual(len(results), 10)
        query_id, result = results[0]
        self.assertEqual(query_id, "CHEBI:17585")
        self.assertEqual(len(result), 4)
        result.reorder("increasing-score")
        self.assertSequenceEqual(result.get_scores(),
                          [0.7142857142857143, 0.72222222222222221, 0.8571428571428571, 0.8571428571428571])
        self.assertEqual(result.get_ids(),
                          ['CHEBI:16148', 'CHEBI:17539', 'CHEBI:17034', 'CHEBI:17302'])

        query_id, result = results[3]
        self.assertEqual(query_id, "CHEBI:17588")
        self.assertEqual(len(result), 32)
        result.reorder("decreasing-score")
        expected_scores = [1.0, 0.88, 0.88, 0.88, 0.85185185185185186, 0.85185185185185186]
        expected_ids = ['CHEBI:17230', 'CHEBI:15356', 'CHEBI:16375', 'CHEBI:17561', 'CHEBI:15729', 'CHEBI:16176']
        self.assertSequenceEqual(result.get_scores()[:6], expected_scores)
        self.assertEqual(result.get_ids()[:6], expected_ids)
        self.assertEqual(result.get_ids_and_scores()[:6], zip(expected_ids, expected_scores))

    def test_with_different_parameters(self):
        queries = chemfp.load_fingerprints(CHEBI_QUERIES, reorder=False)[:10]
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        results = list(chemfp.threshold_tanimoto_search(queries, targets, threshold=0.8))

        query_id, result = results[0]
        result.reorder("increasing-score")
        self.assertEqual(query_id, "CHEBI:17585")
        self.assertSequenceEqual(result.get_scores(), [0.8571428571428571, 0.8571428571428571])
        self.assertEqual(result.get_ids(), ['CHEBI:17034', 'CHEBI:17302'])

    def test_with_initial_offset(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        it = targets.iter_arenas(10)
        # Skip the first arena and use only the second
        next(it)
        subarena = next(it)
        hits = list(chemfp.threshold_tanimoto_search(subarena, subarena, 0.2, arena_size=3))
        self.assertEqual([(query_id, len(hit)) for (query_id, hit) in hits],
                         [("CHEBI:15343", 6), ("CHEBI:15858", 4), ("CHEBI:16007", 3),
                          ("CHEBI:16052", 4), ("CHEBI:16234", 7), ("CHEBI:16382", 4),
                          ("CHEBI:16716", 1), ("CHEBI:16842", 5), ("CHEBI:17051", 4),
                          ("CHEBI:17087", 4)])
        self.assertEqual(subarena.ids,
                         ["CHEBI:15343", "CHEBI:15858", "CHEBI:16007", "CHEBI:16052", "CHEBI:16234",
                          "CHEBI:16382", "CHEBI:16716", "CHEBI:16842", "CHEBI:17051", "CHEBI:17087"])
        self.assertEqual(len(subarena.arena_ids), len(targets))
        self.assertEqual(subarena.ids, targets.arena_ids[10:20])
        

    def test_with_large_input(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        for (query_id, result) in chemfp.threshold_tanimoto_search(targets, targets, threshold=0.9):
            pass
        self.assertEqual(query_id, "CHEBI:16379")
        result.reorder("increasing-score")
        self.assertSequenceEqual(result.get_scores(),
                  [0.956989247311828, 0.96739130434782605, 0.97826086956521741, 0.97826086956521741, 1.0])
        self.assertSequenceEqual(result.get_ids(),
                  ["CHEBI:17439", "CHEBI:15982", "CHEBI:15852", "CHEBI:16304", "CHEBI:16379"])

    def test_with_empty_queries(self):
        targets = chemfp.load_fingerprints(CHEBI_QUERIES)
        queries = targets[len(targets):]
        for x in chemfp.threshold_tanimoto_search(queries, targets):
            raise AssertionError

class KNearestTanimotoSearch(unittest2.TestCase):
    def test_with_fps_reader_as_targets(self):
        queries = chemfp.open(CHEBI_QUERIES).iter_arenas(10).next()
        targets = chemfp.open(CHEBI_TARGETS)
        fps_results = chemfp.knearest_tanimoto_search(queries, targets)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(fps_results)
        results = list(fps_results)
        self.assertEqual(len(results), 10)
        query_id, result = results[0]
        self.assertEqual(query_id, "CHEBI:17585")
        self.assertEqual(len(result), 3)
        # The default is in decreasing score
        self.assertEqual(result.get_scores(),
                          [0.8571428571428571, 0.8571428571428571, 0.72222222222222221])
        self.assertEqual(result.get_ids(),
                          ['CHEBI:17302', 'CHEBI:17034', 'CHEBI:17539'])
        result.reorder("increasing-score")
        self.assertEqual(result.get_scores(),
                          [0.72222222222222221, 0.8571428571428571, 0.8571428571428571])
        self.assertEqual(result.get_ids(),
                          ['CHEBI:17539', 'CHEBI:17034', 'CHEBI:17302'])
        
        query_id, result = results[3]
        self.assertEqual(query_id, "CHEBI:17588")
        self.assertEqual(len(result), 3)
        expected_scores = [1.0, 0.88, 0.88]
        expected_ids = ['CHEBI:17230', 'CHEBI:15356', 'CHEBI:16375']
        self.assertEqual(result.get_scores(), expected_scores)
        self.assertEqual(result.get_ids(), expected_ids)
        self.assertEqual(result.get_ids_and_scores(), zip(expected_ids, expected_scores))

    def test_with_arena_as_targets(self):
        queries = chemfp.load_fingerprints(CHEBI_QUERIES, reorder=False)[:10]
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        arena_results = chemfp.knearest_tanimoto_search(queries, targets)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(arena_results)
        results = list(arena_results)
        self.assertEqual(len(results), 10)
        query_id, result = results[0]
        self.assertEqual(query_id, "CHEBI:17585")
        self.assertEqual(len(result), 3)

        # The default is in decreasing score
        self.assertSequenceEqual(result.get_scores(),
                                 [0.8571428571428571, 0.8571428571428571, 0.72222222222222221])
        self.assertEqual(result.get_ids()[2], 'CHEBI:17539')
        self.assertEqual(sorted(result.get_ids()),
                          sorted(['CHEBI:17302', 'CHEBI:17034', 'CHEBI:17539']))
        result.reorder("increasing-score")
        self.assertSequenceEqual(result.get_scores(),
                                 [0.72222222222222221, 0.8571428571428571, 0.8571428571428571])
        self.assertEqual(result.get_ids(),
                          ['CHEBI:17539', 'CHEBI:17034', 'CHEBI:17302'])

        query_id, result = results[3]
        self.assertEqual(query_id, "CHEBI:17588")
        self.assertEqual(len(result), 3)
        expected_scores = [1.0, 0.88, 0.88]
        expected_ids = ['CHEBI:17230', 'CHEBI:15356', 'CHEBI:16375']
        self.assertSequenceEqual(result.get_scores(), expected_scores)
        self.assertEqual(result.get_ids(), expected_ids)
        self.assertEqual(result.get_ids_and_scores(), zip(expected_ids, expected_scores))

    def test_with_different_parameters(self):
        queries = chemfp.load_fingerprints(CHEBI_QUERIES, reorder=False)[:10]
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        results = list(chemfp.knearest_tanimoto_search(queries, targets, k=8, threshold=0.3))

        query_id, result = results[0]
        result.reorder("increasing-score")
        self.assertEqual(query_id, "CHEBI:17585")
        self.assertSequenceEqual(result.get_scores(),
                   [0.61904761904761907, 0.66666666666666663, 0.66666666666666663, 0.66666666666666663,
                    0.7142857142857143, 0.72222222222222221, 0.8571428571428571, 0.8571428571428571])
                                                       
        self.assertEqual(result.get_ids(), ['CHEBI:15843', 'CHEBI:7896', 'CHEBI:15894', 'CHEBI:16759',
                                            'CHEBI:16148', 'CHEBI:17539', 'CHEBI:17034', 'CHEBI:17302'])

    def test_with_initial_offset(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        it = targets.iter_arenas(10)
        # Skip the first arena and use only the second
        next(it)
        subarena = next(it)
        hits = list(chemfp.knearest_tanimoto_search(subarena, subarena, k=5, threshold=0.2, arena_size=3))
        self.assertEqual([(query_id, len(hit)) for (query_id, hit) in hits],
                         [("CHEBI:15343", 5), ("CHEBI:15858", 4), ("CHEBI:16007", 3),
                          ("CHEBI:16052", 4), ("CHEBI:16234", 5), ("CHEBI:16382", 4),
                          ("CHEBI:16716", 1), ("CHEBI:16842", 5), ("CHEBI:17051", 4),
                          ("CHEBI:17087", 4)])
        self.assertEqual(subarena.ids,
                         ["CHEBI:15343", "CHEBI:15858", "CHEBI:16007", "CHEBI:16052", "CHEBI:16234",
                          "CHEBI:16382", "CHEBI:16716", "CHEBI:16842", "CHEBI:17051", "CHEBI:17087"])
        self.assertEqual(len(subarena.arena_ids), len(targets))
        self.assertEqual(subarena.ids, targets.arena_ids[10:20])

    def test_with_large_input(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS)
        for (query_id, result) in chemfp.knearest_tanimoto_search(targets, targets, threshold=0.9):
            pass
        self.assertEqual(query_id, "CHEBI:16379")
        result.reorder("increasing-score")
        self.assertSequenceEqual(result.get_scores(),
                  [0.97826086956521741, 0.97826086956521741, 1.0])
        self.assertSequenceEqual(result.get_ids(), ["CHEBI:15852", "CHEBI:16304", "CHEBI:16379"])

    def test_with_empty_queries(self):
        targets = chemfp.load_fingerprints(CHEBI_QUERIES)
        queries = targets[len(targets):]
        for x in chemfp.knearest_tanimoto_search(queries, targets):
            raise AssertionError
    

class TestCountSymmetric(unittest2.TestCase):
    def test_count_with_fps_reader(self):
        targets = chemfp.open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "`fingerprints` must be a FingerprintArena "
                                     "with pre-computed popcount indices"):
            chemfp.count_tanimoto_hits_symmetric(targets)

    def test_count_without_indices(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS, reorder=False)
        with self.assertRaisesRegexp(ValueError, "`fingerprints` must be a FingerprintArena "
                                     "with pre-computed popcount indices"):
            chemfp.count_tanimoto_hits_symmetric(targets)

    def test_count(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 200, 220), fps.metadata)
        results = chemfp.count_tanimoto_hits_symmetric(targets)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 20)
        self.assertSequenceEqual(results, [
            ('CHEBI:15399', 4), ('CHEBI:15400', 4), ('CHEBI:15404', 0), ('CHEBI:15385', 0),
            ('CHEBI:15386', 0), ('CHEBI:15388', 4), ('CHEBI:15389', 4), ('CHEBI:15392', 3),
            ('CHEBI:15396', 5), ('CHEBI:15397', 5), ('CHEBI:15402', 3), ('CHEBI:15403', 3),
            ('CHEBI:15387', 3), ('CHEBI:15398', 6), ('CHEBI:15393', 5), ('CHEBI:15394', 5),
            ('CHEBI:15401', 0), ('CHEBI:15390', 1), ('CHEBI:15391', 1), ('CHEBI:15395', 0)])
        
    def test_count_with_explicit_default_threshold(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 200, 220), fps.metadata)
        results = chemfp.count_tanimoto_hits_symmetric(targets, threshold=0.7)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 20)
        self.assertSequenceEqual(results, [
            ('CHEBI:15399', 4), ('CHEBI:15400', 4), ('CHEBI:15404', 0), ('CHEBI:15385', 0),
            ('CHEBI:15386', 0), ('CHEBI:15388', 4), ('CHEBI:15389', 4), ('CHEBI:15392', 3),
            ('CHEBI:15396', 5), ('CHEBI:15397', 5), ('CHEBI:15402', 3), ('CHEBI:15403', 3),
            ('CHEBI:15387', 3), ('CHEBI:15398', 6), ('CHEBI:15393', 5), ('CHEBI:15394', 5),
            ('CHEBI:15401', 0), ('CHEBI:15390', 1), ('CHEBI:15391', 1), ('CHEBI:15395', 0)])
            
    def test_count_with_different_threshold(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 300, 350), fps.metadata)
        results = chemfp.count_tanimoto_hits_symmetric(targets, threshold=0.95)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 50)
        self.assertSequenceEqual(results[:15], [
            ('CHEBI:15522', 28), ('CHEBI:15496', 40), ('CHEBI:15501', 40), ('CHEBI:15507', 40),
            ('CHEBI:15490', 29), ('CHEBI:15492', 29), ('CHEBI:15504', 29), ('CHEBI:15512', 41),
            ('CHEBI:15515', 35), ('CHEBI:15524', 29), ('CHEBI:15531', 29), ('CHEBI:15535', 29),
            ('CHEBI:15537', 35), ('CHEBI:15497', 27), ('CHEBI:15500', 31)])

class TestThresholdSymmetric(unittest2.TestCase):
    def test_search_with_fps_reader(self):
        targets = chemfp.open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "`fingerprints` must be a FingerprintArena "
                                     "with pre-computed popcount indices"):
            chemfp.threshold_tanimoto_search_symmetric(targets)

    def test_search_without_indices(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS, reorder=False)
        with self.assertRaisesRegexp(ValueError, "`fingerprints` must be a FingerprintArena "
                                     "with pre-computed popcount indices"):
            chemfp.threshold_tanimoto_search_symmetric(targets)

    def test_search(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 200, 220), fps.metadata)
        results = chemfp.threshold_tanimoto_search_symmetric(targets)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 20)
        self.assertSequenceEqual([(id, len(result)) for (id, result) in results], [
            ('CHEBI:15399', 4), ('CHEBI:15400', 4), ('CHEBI:15404', 0), ('CHEBI:15385', 0),
            ('CHEBI:15386', 0), ('CHEBI:15388', 4), ('CHEBI:15389', 4), ('CHEBI:15392', 3),
            ('CHEBI:15396', 5), ('CHEBI:15397', 5), ('CHEBI:15402', 3), ('CHEBI:15403', 3),
            ('CHEBI:15387', 3), ('CHEBI:15398', 6), ('CHEBI:15393', 5), ('CHEBI:15394', 5),
            ('CHEBI:15401', 0), ('CHEBI:15390', 1), ('CHEBI:15391', 1), ('CHEBI:15395', 0)])
        
    def test_search_with_explicit_defaults(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 200, 220), fps.metadata)
        results = chemfp.threshold_tanimoto_search_symmetric(targets, threshold=0.7)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 20)
        self.assertSequenceEqual([(id, len(result)) for (id, result) in results], [
            ('CHEBI:15399', 4), ('CHEBI:15400', 4), ('CHEBI:15404', 0), ('CHEBI:15385', 0),
            ('CHEBI:15386', 0), ('CHEBI:15388', 4), ('CHEBI:15389', 4), ('CHEBI:15392', 3),
            ('CHEBI:15396', 5), ('CHEBI:15397', 5), ('CHEBI:15402', 3), ('CHEBI:15403', 3),
            ('CHEBI:15387', 3), ('CHEBI:15398', 6), ('CHEBI:15393', 5), ('CHEBI:15394', 5),
            ('CHEBI:15401', 0), ('CHEBI:15390', 1), ('CHEBI:15391', 1), ('CHEBI:15395', 0)])
            
    def test_search_with_different_threshold(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 300, 350), fps.metadata)
        results = chemfp.threshold_tanimoto_search_symmetric(targets, threshold=0.95)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 50)
        self.assertSequenceEqual([(id, len(result)) for (id, result) in results[:15]], [
            ('CHEBI:15522', 28), ('CHEBI:15496', 40), ('CHEBI:15501', 40), ('CHEBI:15507', 40),
            ('CHEBI:15490', 29), ('CHEBI:15492', 29), ('CHEBI:15504', 29), ('CHEBI:15512', 41),
            ('CHEBI:15515', 35), ('CHEBI:15524', 29), ('CHEBI:15531', 29), ('CHEBI:15535', 29),
            ('CHEBI:15537', 35), ('CHEBI:15497', 27), ('CHEBI:15500', 31)])

class TestKNearestSymmetric(unittest2.TestCase):
    def test_search_with_fps_reader(self):
        targets = chemfp.open(CHEBI_TARGETS)
        with self.assertRaisesRegexp(ValueError, "`fingerprints` must be a FingerprintArena "
                                     "with pre-computed popcount indices"):
            chemfp.knearest_tanimoto_search_symmetric(targets)

    def test_search_without_indices(self):
        targets = chemfp.load_fingerprints(CHEBI_TARGETS, reorder=False)
        with self.assertRaisesRegexp(ValueError, "`fingerprints` must be a FingerprintArena "
                                     "with pre-computed popcount indices"):
            chemfp.knearest_tanimoto_search_symmetric(targets)

    def test_search(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 200, 220), fps.metadata)
        results = chemfp.knearest_tanimoto_search_symmetric(targets)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 20)
        self.assertSequenceEqual([(id, len(result)) for (id, result) in results], [
            ('CHEBI:15399', 3), ('CHEBI:15400', 3), ('CHEBI:15404', 0), ('CHEBI:15385', 0),
            ('CHEBI:15386', 0), ('CHEBI:15388', 3), ('CHEBI:15389', 3), ('CHEBI:15392', 3),
            ('CHEBI:15396', 3), ('CHEBI:15397', 3), ('CHEBI:15402', 3), ('CHEBI:15403', 3),
            ('CHEBI:15387', 3), ('CHEBI:15398', 3), ('CHEBI:15393', 3), ('CHEBI:15394', 3),
            ('CHEBI:15401', 0), ('CHEBI:15390', 1), ('CHEBI:15391', 1), ('CHEBI:15395', 0)])
        
    def test_search_with_explicit_defaults(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 200, 220), fps.metadata)
        results = chemfp.knearest_tanimoto_search_symmetric(targets, k=3, threshold=0.7)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 20)
        self.assertSequenceEqual([(id, len(result)) for (id, result) in results], [
            ('CHEBI:15399', 3), ('CHEBI:15400', 3), ('CHEBI:15404', 0), ('CHEBI:15385', 0),
            ('CHEBI:15386', 0), ('CHEBI:15388', 3), ('CHEBI:15389', 3), ('CHEBI:15392', 3),
            ('CHEBI:15396', 3), ('CHEBI:15397', 3), ('CHEBI:15402', 3), ('CHEBI:15403', 3),
            ('CHEBI:15387', 3), ('CHEBI:15398', 3), ('CHEBI:15393', 3), ('CHEBI:15394', 3),
            ('CHEBI:15401', 0), ('CHEBI:15390', 1), ('CHEBI:15391', 1), ('CHEBI:15395', 0)])
            
    def test_search_with_different_settings(self):
        # Work around a bug: cannot do the symmetric search on a subarena
        fps = chemfp.open(CHEBI_TARGETS)
        targets = chemfp.load_fingerprints(itertools.islice(fps, 300, 350), fps.metadata)
        results = chemfp.knearest_tanimoto_search_symmetric(targets, threshold=0.95, k=28)
        with self.assertRaisesRegexp(TypeError, ".*has no len.*"):
            len(results)
        results = list(results)
        self.assertEqual(len(results), 50)
        self.assertSequenceEqual([(id, len(result)) for (id, result) in results[:15]], [
            ('CHEBI:15522', 28), ('CHEBI:15496', 28), ('CHEBI:15501', 28), ('CHEBI:15507', 28),
            ('CHEBI:15490', 28), ('CHEBI:15492', 28), ('CHEBI:15504', 28), ('CHEBI:15512', 28),
            ('CHEBI:15515', 28), ('CHEBI:15524', 28), ('CHEBI:15531', 28), ('CHEBI:15535', 28),
            ('CHEBI:15537', 28), ('CHEBI:15497', 27), ('CHEBI:15500', 28)])



try:
    import bz2
    has_bz2 = True
except ImportError:
    has_bz2 = False

class TestSave(unittest2.TestCase):
    def test_save_to_fps(self):
        filename = os.path.join(_tmpdir(self), "output.fps")
        arena = chemfp.load_fingerprints(CHEBI_TARGETS, reorder=False)
        arena.save(filename)

        arena2 = chemfp.load_fingerprints(filename, reorder=False)
        self.assertEqual(arena.metadata.type, arena2.metadata.type)
        self.assertEqual(len(arena), len(arena2))

        arena_lines = open(CHEBI_TARGETS).readlines()
        arena2_lines = open(filename).readlines()
        self.assertSequenceEqual(arena_lines, arena2_lines)

    def test_save_to_file_object(self):
        arena = chemfp.load_fingerprints(CHEBI_TARGETS, reorder=False)
        f = StringIO()
        arena.save(f)
        s = f.getvalue()
        f.close()
        arena_lines = open(CHEBI_TARGETS, "rb").readlines()
        arena2_lines = s.splitlines(True)
        # the unittest difflib call can take a long time. Do a small test first.
        self.assertSequenceEqual(arena_lines[:10], arena2_lines[:10])
        self.assertSequenceEqual(arena_lines, arena2_lines)

    def test_save_to_fps_gz(self):
        filename = os.path.join(_tmpdir(self), "output.fps.gz")
        arena = chemfp.load_fingerprints(CHEBI_TARGETS, reorder=False)
        arena.save(filename)
        
        arena2 = chemfp.load_fingerprints(filename, reorder=False)
        self.assertEqual(arena.metadata.type, arena2.metadata.type)
        self.assertEqual(len(arena), len(arena2))

        arena_lines = open(CHEBI_TARGETS, "rb").readlines()
        arena2_lines = gzip.GzipFile(filename, "rb").readlines()
        # the unittest difflib call can take a long time. Do a small test first.
        self.assertSequenceEqual(arena_lines[:10], arena2_lines[:10])
        self.assertSequenceEqual(arena_lines, arena2_lines)

    def test_save_to_fps_bz2(self):
        filename = os.path.join(_tmpdir(self), "output.fps.bz2")
        arena = chemfp.load_fingerprints(CHEBI_TARGETS, reorder=False)
        arena.save(filename)
        
        arena2 = chemfp.load_fingerprints(filename, reorder=False)
        self.assertEqual(arena.metadata.type, arena2.metadata.type)
        self.assertEqual(len(arena), len(arena2))

        arena_lines = open(CHEBI_TARGETS, "rb").readlines()
        arena2_lines = bz2.BZ2File(filename, "rb").readlines()
        
        # the unittest difflib call can take a long time. Do a small test first.
        self.assertSequenceEqual(arena_lines[:10], arena2_lines[:10])
        self.assertSequenceEqual(arena_lines, arena2_lines)

    test_save_to_fps_bz2 = unittest2.skipUnless(has_bz2, "bz2 module not available")(test_save_to_fps_bz2)

    def test_save_id_with_tab(self):
        arena = chemfp.load_fingerprints([("A\tB", b"1234")], chemfp.Metadata(num_bytes=4))
        f = StringIO()
        with self.assertRaisesRegexp(ValueError, r"Fingerprint ids must not contain a tab: 'A\\tB' in record 1"):
            arena.save(f)

    def test_save_id_with_newline(self):
        arena = chemfp.load_fingerprints([("AB", b"1234"), ("C\nD", b"1324")], chemfp.Metadata(num_bytes=4))
        f = StringIO()
        with self.assertRaisesRegexp(ValueError,
                                     r"Fingerprint ids must not contain a newline: 'C\\nD' in record 2"):
            arena.save(f)

    def test_save_empty_id(self):
        arena = chemfp.load_fingerprints([("AB", b"1234"), ("", b"1324")], chemfp.Metadata(num_bytes=4))
        f = StringIO()
        with self.assertRaisesRegexp(ValueError,
                                     "Fingerprint ids must not be the empty string"):
            arena.save(f)


    def test_save_fps_to_file_object_from_fingerprint_iterator(self):
        fp_it = chemfp.FingerprintIterator(chemfp.Metadata(num_bytes=1),
                                           [("first", b"A"), ("second", b"B")])
        f = StringIO()
        fp_it.save(f)
        body = f.getvalue()
        self.assertIn(b"\n41\tfirst\n42\tsecond\n", body)

    def test_save_fps_fingerprint_iterator(self):
        fp_it = chemfp.FingerprintIterator(chemfp.Metadata(num_bytes=1),
                                           [("first", b"A"), ("second", b"B")])
        filename = support.get_tmpfile(self, "fp_iter_save.fps")
        fp_it.save(filename)
        with open(filename) as f:
            body = f.read()
        self.assertIn("\n41\tfirst\n42\tsecond\n", body)

    def test_save_fps_fingerprint_iterator_using_format(self):
        fp_it = chemfp.FingerprintIterator(chemfp.Metadata(num_bytes=1),
                                           [("first", b"A"), ("second", b"B")])
        filename = support.get_tmpfile(self, "fp_iter_save.fpb")
        fp_it.save(filename, format="fps.gz")
        f = gzip.GzipFile(filename)
        body = f.read()
        f.close()
        self.assertIn(b"\n41\tfirst\n42\tsecond\n", body)


# This is hard to test through the main() API since the main() API
# changes stdout / uses an alternate output.

class TestOpenCompression(unittest2.TestCase):
    def test_open_output(self):
        f, close = io.open_binary_output(None)
        self.assertIs(f, sys.stdout)
        f = StringIO()
        g, close = io.open_binary_output(f)
        self.assertIs(f, g)
        
    def test_open_compressed_output_uncompressed(self):
        outfile, close = io.open_compressed_output(None, None, None)
        self.assertIs(outfile, sys.stdout)
        filename = os.path.join(_tmpdir(self), "spam.out")
        f, close = io.open_compressed_output(filename, None, None)
        try:
            self.assertEqual(f.name, filename)
            f.write("Check that it's writeable.\n");
        finally:
            close()
        f = StringIO()
        g, close = io.open_compressed_output(f, None, None)
        self.assertIs(f, g)

    def test_open_compressed_output_gzip_stdout(self):
        old_stdout = sys.stdout
        sys.stdout = f = StringIO()
        try:
            g, close = io.open_compressed_output(None, "gz", None)
            g.write("Spam and eggs.")
            close()
        finally:
            sys.stdout = old_stdout
        t = gzip.GzipFile(fileobj=StringIO(f.getvalue())).read()
        self.assertEqual(t, "Spam and eggs.")
        
    def test_open_compressed_output_gzip_filename(self):
        filename = os.path.join(_tmpdir(self), "spam_gz")
        f, close = io.open_compressed_output(filename, "gz", None)
        try:
            if hasattr(f, "name"): # doesn't work before Python 2.7
                self.assertEqual(f.name, filename)
            f.write("Check that it's writeable.\n");
            close()
            f = gzip.GzipFile(filename)
            s = f.read()
            self.assertEqual(s, "Check that it's writeable.\n")
        finally:
            close()

    def test_open_compressed_output_gzip_filelike(self):
        f = StringIO()
        g, close = io.open_compressed_output(f, "gz", None)
        g.write("This is a test.\n")
        close()
        s = f.getvalue()
        t = gzip.GzipFile(fileobj=StringIO(s)).read()
        self.assertEqual(t, "This is a test.\n")


    ## def test_open_compressed_output_bzip_stdout(self):
    ##     # This cannot be tested from Python since the bz2 library only
    ##     # takes a filename.  The chemfp interface uses "/dev/stdout"
    ##     # as a hack, but that is not interceptable.
    ##     # I can't even check that I can connect to stdout since
    ##     # this emits a header
    ##     #g = io.open_compressed_output(None, "bz2", None)
        
    def test_open_compressed_output_bzip_filename(self):
        filename = os.path.join(_tmpdir(self), "spam_bz")
        f, close = io.open_compressed_output(filename, "bz2", None)
        try:
            self.assertEqual(f.name, filename)
            f.write("Check that it's writeable.\n");
            close()
            f = bz2.BZ2File(filename)
            s = f.read()
            self.assertEqual(s, "Check that it's writeable.\n")
        finally:
            close()
    test_open_compressed_output_bzip_filename = unittest2.skipUnless(has_bz2, "bz2 module not available")(
        test_open_compressed_output_bzip_filename)

    def test_open_compressed_output_bzip_filelike(self):
        with self.assertRaisesRegexp(ValueError,
                                     "Python's bz2 library does not support writing to a file object"):
            io.open_compressed_output(StringIO(), "bz2", None)
    test_open_compressed_output_bzip_filelike = unittest2.skipUnless(has_bz2, "bz2 module not available")(
        test_open_compressed_output_bzip_filelike)

    def test_open_compressed_output_xz(self):
        with self.assertRaisesRegexp(ValueError,
                                     "chemfp does not yet support xz compression"):
            io.open_compressed_output(StringIO(), "xz", None)

    def test_unsupported_compression(self):
        with self.assertRaisesRegexp(ValueError, "Unsupported compression type 'Z'"):
            io.open_compressed_output(StringIO(), "Z", None)

            ######

    def test_cannot_read_bzip_input_file(self):
        with self.assertRaisesRegexp(NotImplementedError,
                                     "bzip decompression from file-like objects is not supported"):
            io.open_compressed_input(StringIO(), "bz2", None)
    test_cannot_read_bzip_input_file = unittest2.skipUnless(has_bz2, "bz2 module not available")(
        test_cannot_read_bzip_input_file)
                    
            
            
    def test_cannot_read_xz_input_file(self):
        with self.assertRaisesRegexp(NotImplementedError, "xz decompression is not supported"):
            io.open_compressed_input(StringIO(), "xz", None)

    def test_unsupported_decompression(self):
        with self.assertRaisesRegexp(ValueError, "Unsupported compression type 'Z'"):
            io.open_compressed_output(StringIO(), "Z", None)

        with self.assertRaisesRegexp(ValueError, "Fred does not support compression type 'Z'"):
            io.open_compressed_output(StringIO(), "Z", "Fred")


if __name__ == "__main__":
    unittest2.main()


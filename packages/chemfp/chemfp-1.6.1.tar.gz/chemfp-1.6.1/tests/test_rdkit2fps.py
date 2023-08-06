from __future__ import with_statement
import sys
import unittest2
import tempfile
import shutil
import os
from cStringIO import StringIO
import tempfile

import support

from chemfp.bitops import hex_contains_bit, hex_encode, hex_union, hex_from_bitlist, hex_to_bitlist

try:
    import chemfp.rdkit
    has_rdkit = True
    skip_rdkit = False
except ImportError:
    has_rdkit = False
    skip_rdkit = True

    if not support.can_skip("rdkit"):
        skip_rdkit = False
        Chem = False
else:
    from rdkit import Chem

if has_rdkit:
    from chemfp.commandline import rdkit2fps

    runner = support.Runner(rdkit2fps.main)
else:
    runner = None

MACCS_SMI = support.fullpath("maccs.smi")
TRP_SDF = support.fullpath("tryptophan.sdf")
TRP = open(TRP_SDF).read()

class TestMACCS(unittest2.TestCase):
    def test_bitorder(self):
        result = runner.run_fps("--maccs166", 7, MACCS_SMI)
        # The fingerprints are constructed to test the first few bytes.
        self.assertEquals(result[0][:6], support.set_bit(2))
        self.assertEquals(result[1][:6], support.set_bit(3))
        self.assertEquals(result[2][:6], support.set_bit(4))
        self.assertEquals(result[3][:6], support.set_bit(5))
        self.assertEquals(result[4][:6], support.set_bit(9))
        self.assertEquals(result[5][:6], support.set_bit(10))
        self.assertEquals(result[6][:6], support.set_bit(16))
    def test_type(self):
        for line in runner.run("--maccs166", MACCS_SMI):
            if line.startswith("#type="):
                self.assertEquals(line, "#type=RDKit-MACCS166/" + chemfp.rdkit.MACCS_VERSION)
                return
        self.assertEquals("could not find", "#type line")

    @unittest2.skipIf(skip_rdkit or chemfp.rdkit.MACCS_VERSION != "1", "This version of RDKit does not implement RDKit-MACCS/1")
    def test_maccs1_key44(self):
        header, output = runner.run_split("--maccs", 7, source=MACCS_SMI)
        self.assertEqual(header[b"#type"], b"RDKit-MACCS166/1")
        hex_fp, id = output[0].split(b"\t")
        self.assertFalse(hex_contains_bit(hex_fp, 43))
        self.assertEqual(output[0], b"040000000000000000000000000000000000000000\t3->bit_2")

    @unittest2.skipIf(skip_rdkit or chemfp.rdkit.MACCS_VERSION != "2", "This version of RDKit does not implement RDKit-MACCS/2")
    def test_maccs2_key44(self):
        header, output = runner.run_split("--maccs", 7, source=MACCS_SMI)
        self.assertEqual(header[b"#type"], b"RDKit-MACCS166/2")
        hex_fp, id = output[0].split(b"\t")
        self.assertTrue(hex_contains_bit(hex_fp, 43))
        self.assertEqual(output[0], b"040000000008000000000000000000000000000000\t3->bit_2")
        
        
TestMACCS = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestMACCS)


def get_field_and_first(cmdline, field):
    result = runner.run(cmdline)
    field_value = None
    first = None
    for line in result:
        if line.startswith(field):
            field_value = line
        if not line.startswith("#"):
            first = line
            break
    return (field_value, first)

def _get_nonzero_values(values):
    nonzero_values = [value for value in values if set(value.split(b"\t")[0]) != {b"0"}]
    return nonzero_values

class FromAtomsMixin(object):
    def _run_fromatoms(self, fromAtoms):
        args = [self.typeflag, "--from-atoms", fromAtoms]
        header, fps = runner.run_split(args, 19)
        type_str = header[b"#type"].decode("ascii")
        indices = sorted(fromAtoms.split(","), key=int)
        expected_ending = u" fromAtoms=" + ",".join(indices)
        # Get the last term
        ending = type_str[type_str.rfind(" "):]
        self.assertEqual(ending, expected_ending)
        return fps
        
        
    def _run_fromatoms_exit(self, fromAtoms, expected_msg):
        args = [self.typeflag, "--from-atoms", fromAtoms]
        result = runner.run_exit(args)
        expected = "error: argument --from-atoms: " + expected_msg
        self.assertIn(expected_msg, result)
        
    def test_from_atoms_empty(self):
        self._run_fromatoms_exit(
            "", "must contain a comma-separated list of atom indices")
        
    def test_from_atoms_space(self):
        self._run_fromatoms_exit(
            "  ", "must contain a comma-separated list of atom indices")
        
    def test_from_atoms_not_a_number_A(self):
        self._run_fromatoms_exit(
            "A", "term 'A' must be a non-negative integer")
        
    def test_from_atoms_not_a_number_0xA(self):
        self._run_fromatoms_exit(
            "0xA", "term '0xA' must be a non-negative integer")
        
    def test_from_atoms_two_terms_first_bad(self):
        self._run_fromatoms_exit(
            "A,1", "term 'A' must be a non-negative integer")
        
    def test_from_atoms_two_terms_second_bad(self):
        self._run_fromatoms_exit(
            "1,A", "term 'A' must be a non-negative integer")
        
    def test_from_atoms_empty_field(self):
        self._run_fromatoms_exit(
            "1,A", "term 'A' must be a non-negative integer")
        
    def test_from_atoms_empty_field(self):
        self._run_fromatoms_exit(
            "1,,3", "term '' must be a non-negative integer")
        
    def test_from_atoms_negative_value(self):
        self._run_fromatoms_exit(
            "-3", "term '-3' must be a non-negative integer")
        
    def test_from_atoms_second_term_negative_value(self):
        self._run_fromatoms_exit(
            "2,-4,8", "term '-4' must be a non-negative integer")

    def test_from_atoms_0(self):
        values = self._run_fromatoms("0")
        self.assertEqual(values[0], self.from_atoms_0_0)

    def test_from_atoms_28(self):
        values = self._run_fromatoms("28")
        nonzero_values = _get_nonzero_values(values)
        self.assertEqual(len(nonzero_values), 3)
        self.assertEqual([v.split(b"\t")[1] for v in nonzero_values],
                         [v.split(b"\t")[1] for v in self.from_atoms_28]),
        self.assertEqual(nonzero_values[0], self.from_atoms_28[0])
        self.assertEqual(nonzero_values[1], self.from_atoms_28[1])
        self.assertEqual(nonzero_values[2], self.from_atoms_28[2])
        
    def test_from_atoms_29(self):
        values = self._run_fromatoms("29")
        nonzero_values = _get_nonzero_values(values)
        self.assertEqual(len(nonzero_values), 1)
        self.assertEqual(nonzero_values[0], self.from_atoms_29[0])

    def test_from_atoms_29_28(self):
        values = self._run_fromatoms("29,28")
        nonzero_values = _get_nonzero_values(values)
        self.assertEqual(len(nonzero_values), 3)
        hex_fp1, id1 = self.from_atoms_28[0].split(b"\t")
        hex_fp2, id2 = self.from_atoms_29[0].split(b"\t")
        self.assertEqual(id1, id2)
        union = hex_union(hex_fp1, hex_fp2)
        # It isn't always the union. The sparse dictionaries for 28
        # and 29 can have the same key, so the corresponding values
        # are added together. This increase may affect the code
        # which converts the sparse count fingerprint into a
        # hash fingerprint. The [28]+[29] fingerprint will always
        # be contained in the [28,29] fingerprint.
        if self.typeflag == "--pair":
            # For this one case, I need to add a few bits manually.
            union = hex_union(union, hex_from_bitlist([502, 757, 881, 1017, 1313, 1481, 1498, 1989], 2048))
            
        self.assertEqual(hex_to_bitlist(nonzero_values[0].split(b"\t")[0]),
                         hex_to_bitlist(union))
        self.assertEqual(nonzero_values[0],
                         union + b"\t" + id1)
        self.assertEqual(nonzero_values[1], self.from_atoms_28[1])
        self.assertEqual(nonzero_values[2], self.from_atoms_28[2])

    def test_from_atoms_29_50_100(self):
        values = self._run_fromatoms("29,50,100")
        nonzero_values = _get_nonzero_values(values)
        self.assertEqual(len(nonzero_values), 1)
        self.assertEqual(nonzero_values[0], self.from_atoms_29[0])
        
    def test_from_atoms_all_large(self):
        values = self._run_fromatoms("30,500,10000,36893488147419103232")
        nonzero_values = _get_nonzero_values(values)
        self.assertEqual(len(nonzero_values), 0)
        
        
if not skip_rdkit:
    RDKIT_TYPE = "RDKit-Fingerprint/" + chemfp.rdkit.RDK_VERSION + " "

    rdkit_fp = {
        "1": "32bb93145be9598dc6f22cbd1c781196e1733f7a53ed6f09e9e55e22bd3d3ac9e3be17f187fbcaefea8d2982ba7dab47ae1a3fd1aca52b48c70f540f964f79cd79afd9dc9871717341eaf7d7abe6febbc9bee9a971855ec7d960ecb2dacdbbb9b9b6d05f8ce9b7f4bc57fa7fa4573e95fe5a7dc918883f7fd9a3a825ef8e2fb2df944b94a2fb36c023cef883e967d9cf698fbb927cfe4fcbbaff71f7ada5ced97d5d679764bba6be8ff7d762f98d26bfbb3cb003647e1180966bc7eaffdad9a2ce47c6169bf679639e67e1bf50bd8bf30d3438dc877e67ba4e786fedfb831e56f34abc27bdfdce02c7aa57b36f761deb9d9bd5b2579df169ab0eae547515d2a7",
        "2": "058010878020000a791002c2b303b53ac0a1a2040a85300797005c1801000a48f13204307006108a2e8f55184096aa4a08403dcdfd290a026dc8e01302b994401649c20a52e316a5d5400690c4102cb211203113013044998d44065a644510845006ba8194b39f62151cc6ec3212cd105ac510f12540725089481a465e15280ecd57a94258871808979052027a51d59851d554460d0cc10028090b893460c800e00c0015012525443205e0000c220682d6d5a8004a2e4b22441c2cc100096180a2166266640232f1152a190042c103a34c022d49bc8046204324924b21b2682b51c7c0b32f43c100a2451312b7c4f81f7353ad4103108855016c442488b055a5",
        }[chemfp.rdkit.RDK_VERSION]

    assert len(rdkit_fp) == 2048 // 4


class TestRDKFingerprints(unittest2.TestCase, FromAtomsMixin):
    typeflag = "--RDK"
    from_atoms_0_0 = b"000010850000000000000000210200300000020000050004000040000000000041300000200200020002000840800000004000002000000020c08002001004000040020a00c0008010000080001000800000000000004018000000000000108000008080108000201004006802000000004000000000400000080802440420060043004200000000800000000000018810c40402090000000001000000008800000000000000014012010000080000000200000000000800400400000000000002102002200030401000000002010000080000001000000001001248000040200001800020410100004000000000100020010101000000000040002400201004\t9425004"
    from_atoms_28 = [
        b'02000008000000000000000080002001800000000200001006040000800000000000004040000000000400000001000000000008000040000800000000102000000200002000010000040000110000000000000000000000000000001110000000004001000000000004000200000000000800008000000000000000000100000400100000000000000010000000000000000000000000000000000200000201801000000000000002000000000000000000000000000000000000000000002000000000000000000000000000000000001040000000008000000020002000110000000000002000200000100200080000000041000000000004008008000000\t9425015',
        b'000000000010000000000080004001060000000000000000000000000000000400000000000000000000000000400000080000000000000000000000000000000000020001000000800800800000000000000000000000002800000000000c0000000000010100000400000004000000000000000000000080000000200000000000000000000000000000000080000000500400000000000004020000000000000000100000000000000000000100000000000000000100000000008000000000000000000000000004000000008000000001000000000400000800001000040000200000000000000080000001401008000000010000400000000000000000\t9425030',
        b'000000000010000000000080004001060000000000000000000000000000000400000000000000000000000000400000080000000000000000000000000000000000020001000000800800800000000000000000000000002800000000000c0000000000010100000400000004000000000000000000000080000000200000000000000000000000000000000080000000500400000000000004020000000000000000100000000000000000000100000000000000000100000000008000000000000000000000000004000000008000000001000000000400000800001000040000200000000000000080000001401008000000010000400000000000000000\t9425031']
    from_atoms_29 = [
        b'02000000000000000000000080000001800000000200000006000000000000000000004040000000000400000001000000000008000040000000000000102000000200002000010000000000110000000000000000000000000000001110000000000001000000000004000200000000000800000000000000000000000100000400000000000000000010000000000000000000000000000000000200000201800000000000000002000000000000000000000000000000000000000000002000000000000000000000000000000000000040000000000000000000002000010000000000002000000000000200080000000001000000000004000000000000\t9425015'
        ]
        
    def test_is_default(self):
        result = runner.run_fps("", 19)
        self.assertEquals(result[0], rdkit_fp + "\t9425004")
        self.assertNotEquals(result[1].split()[0], rdkit_fp)
        # All must have the same length (since the fp lengths and ids lengths are the same
        self.assertEquals(len(set(map(len, result))), 1, set(map(len, result)))

    def test_as_rdk(self):
        result = runner.run_fps("--RDK", 19)
        self.assertEquals(result[0], rdkit_fp + "\t9425004")
        self.assertNotEquals(result[1].split()[0], rdkit_fp)
        # All must have the same length (since the fp lengths and ids lengths are the same
        self.assertEquals(len(set(map(len, result))), 1, set(map(len, result)))

    def test_num_bits_default(self):
        result = runner.run_fps("--fpSize 2048", 19)
        self.assertEquals(result[0], rdkit_fp + "\t9425004")
        self.assertNotEquals(result[1].split()[0], rdkit_fp)

    def test_num_bits_16(self):
        field, first = get_field_and_first("--fpSize 16", "#num_bits=")
        self.assertEquals(field, "#num_bits=16")
        self.assertEquals(first, "ffff\t9425004")

    def test_num_bits_1(self):
        field, first = get_field_and_first("--fpSize 1", "#num_bits=")
        self.assertEquals(field, "#num_bits=1")
        self.assertEquals(first, "01\t9425004")

    def test_num_bits_2(self):
        field, first = get_field_and_first("--fpSize 2", "#num_bits=")
        self.assertEquals(field, "#num_bits=2")
        self.assertEquals(first, "03\t9425004")

    def test_num_bits_too_small(self):
        result = runner.run_exit("--fpSize 0")
        self.assertIn("fpSize must be 1 or greater", result)

    def test_bits_per_hash_default(self):
        field, first = get_field_and_first("--nBitsPerHash 2", "#type=")
        self.assertEquals(field,
  "#type=" + RDKIT_TYPE + "minPath=1 maxPath=7 fpSize=2048 nBitsPerHash=2 useHs=1")
        self.assertEquals(first.split()[0], rdkit_fp)

    def test_bits_per_hash(self):
        field, first = get_field_and_first("--nBitsPerHash 1", "#type")
        self.assertEquals(field,
  "#type=" + RDKIT_TYPE + "minPath=1 maxPath=7 fpSize=2048 nBitsPerHash=1 useHs=1")
        self.assertNotEquals(first.split()[0], rdkit_fp)

    def test_bits_per_hash_too_small(self):
        result = runner.run_exit("--nBitsPerHash 0")
        self.assertIn("nBitsPerHash must be 1 or greater", result)

    def test_min_path_default(self):
        field, first = get_field_and_first("--minPath 1", "#type")
        self.assertEquals(field,
  "#type=" + RDKIT_TYPE + "minPath=1 maxPath=7 fpSize=2048 nBitsPerHash=2 useHs=1")
        self.assertEquals(first.split()[0], rdkit_fp)

    def test_min_path_2(self):
        field, first = get_field_and_first("--minPath 2", "#type")
        self.assertEquals(field,
  "#type=" + RDKIT_TYPE + "minPath=2 maxPath=7 fpSize=2048 nBitsPerHash=2 useHs=1")
        self.assertNotEquals(first.split()[0], rdkit_fp)

    def test_min_path_too_small(self):
        result = runner.run_exit("--minPath 0")
        self.assertIn("minPath must be 1 or greater", result)

    def test_min_path_too_large(self):
        result = runner.run_exit("--minPath 5 --maxPath 4")
        self.assertIn("--minPath must not be greater than --maxPath", result)

    def test_max_path_default(self):
        field, first = get_field_and_first("--maxPath 7", "#type")
        self.assertEquals(field,
  "#type=" + RDKIT_TYPE + "minPath=1 maxPath=7 fpSize=2048 nBitsPerHash=2 useHs=1")
        self.assertEquals(first.split()[0], rdkit_fp)

    def test_max_path_6(self):
        field, first = get_field_and_first("--maxPath 6", "#type")
        self.assertEquals(field,
  "#type=" + RDKIT_TYPE + "minPath=1 maxPath=6 fpSize=2048 nBitsPerHash=2 useHs=1")
        self.assertNotEquals(first.split()[0], rdkit_fp)

#    def test_ignore_Hs(self):
#  I don't have a good test case for this... XXX

TestRDKFingerprints = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestRDKFingerprints)


_morgan1 = "00000080000200000010010000000040000000400000000000000000000000000000000200000000800000400040000400000000000000004200000000080000000000000000020000000000000000000004000000004008000000000002000000000000800000000800000100080800000000048000000000400000000000000081000002000000010000000000000001000020000000000000000000020000000000000100000020040800100000000000000000000000000000000000000000000000000000040000800000000000000008000000000408004000000000000000000000000100000002000000002000010000100000000000000000000000"

_morgan_radius3 = "00000080000200000110010000000040000100400000000000000000000000004000000201000000800000400040000401000000000000004200000000080000000000000000020000000000000000000004400000004008000000000002000000000000800000000800000100080800000000048000000000408000000000000081000002000000010020000000000001000020000000000002000000020080000000000100000020040800100000000000000000000000000000000000200000000040000000040000800000000000000008000000040408004000000000000000000000000100000002000000002800010000100000000000000000000000"

class TestRDKMorgan(unittest2.TestCase, FromAtomsMixin):
    typeflag = "--morgan"
    from_atoms_0_0 = b"00000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\t9425004"
    from_atoms_28 = [
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000\t9425015',
        b'00000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\t9425030',
        b'00000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\t9425031']
    from_atoms_29 = [
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000\t9425015'
        ]
    
    def test_as_morgan(self):
        result = runner.run_fps("--morgan", 19)
        self.assertEquals(result[0], _morgan1 + "\t9425004")
        self.assertNotEquals(result[1].split()[0], _morgan1)
        # All must have the same length (since the fp lengths and ids lengths are the same
        self.assertEquals(len(set(map(len, result))), 1, set(map(len, result)))
        
    def test_num_bits_default(self):
        result = runner.run_fps("--morgan --fpSize 2048", 19)
        self.assertEquals(result[0], _morgan1 + "\t9425004")
        self.assertNotEquals(result[1].split()[0], _morgan1)

    def test_num_bits_16(self):
        field, first = get_field_and_first("--morgan --fpSize 16", "#num_bits=")
        self.assertEquals(field, "#num_bits=16")
        self.assertEquals(first, "fbff\t9425004")

    def test_num_bits_1(self):
        field, first = get_field_and_first("--morgan --fpSize 1", "#num_bits=")
        self.assertEquals(field, "#num_bits=1")
        self.assertEquals(first, "01\t9425004")

    def test_num_bits_2(self):
        field, first = get_field_and_first("--morgan --fpSize 2", "#num_bits=")
        self.assertEquals(field, "#num_bits=2")
        self.assertEquals(first, "03\t9425004")

    def test_num_bits_too_small(self):
        result = runner.run_exit("--morgan --fpSize 0")
        self.assertIn("fpSize must be 1 or greater", result)

    def test_radius_default(self):
        result = runner.run_fps("--morgan --radius 2", 19)
        self.assertEquals(result[0], _morgan1 + "\t9425004")
        self.assertNotEquals(result[1].split()[0], _morgan1)

    def test_radius_3(self):
        result = runner.run_fps("--morgan --radius 3", 19)
        self.assertEquals(result[0], _morgan_radius3 + "\t9425004")
        self.assertNotEquals(result[1].split()[0], _morgan1)

    def test_radius_too_small(self):
        result = runner.run_exit("--morgan --radius -1")
        self.assertIn("radius must be 0 or greater", result)

    def test_default_use_options(self):
        field, first = get_field_and_first("--morgan --useFeatures 0 --useChirality 0 --useBondTypes 1",
                                      "#type")
        self.assertEquals(field,
                          "#type=RDKit-Morgan/1 radius=2 fpSize=2048 useFeatures=0 useChirality=0 useBondTypes=1")
        self.assertEquals(first, _morgan1 + "\t9425004")

    # This isn't a complete test of the different options. I don't think it's worth the effort
    def test_useChirality(self):
        field, first = get_field_and_first("--morgan --useFeatures 1 --useChirality 1 --useBondTypes 0",
                                           "#type=")
        self.assertEquals(field,
                          "#type=RDKit-Morgan/1 radius=2 fpSize=2048 useFeatures=1 useChirality=1 useBondTypes=0")
        self.assertNotEquals(first, _morgan1 + "\t9425004")
        
        
TestRDKMorgan = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestRDKMorgan)

_atom_pair_fingerprints = {
None: None,
"1": {"2048": "100000100008007000045020000008b0080220a4420084c000054010800300e02040000088c080010000800101404023000000100000000020000000004000a00002060400040800000000000002c00108000000000030009d00100002001001900080003081058010000400200209004000000000050b00800008084042060801000800000000010200030000000000040000000080000000000400000000021000708000100000600010008080200008000c8020000004040008000000600000000008000000100000000402000000400080300000600090004020000020000002008100000800000100020000000000000000000008100000000002000000",
       "128": "fd42febdfaddfff5ff05df3fe3c3fffb",
       "minLength": "dd02bebd328cbff5be055f3e6242ff32",
       "maxLength": "3042c000e8d1e141f101d02181c160cb",
       },

"2": {"2048": "0100070010000000101100000013010000000000001100000010000001001703100000000007000011000301000310001000000010000000003000110100731000310001300000000000101000033110100000010000001000037311000000370313033003010000000101070000130030000010330000000000170031001077000013301000000300003133030000300030133003000131011100100f000010000013010300000000030310310000000300101030000011033010077100100000300003000000000011000000000110000010000301000037300000000101000001303000000000003000000010000010000001100000073001100100101010",
       "128": "77f7fff7ff17017f7fffff7fff3fffff",
       "minLength": "71777f777317003377ffff37733fff77",
       "maxLength": "073033737f0001370100337f7f101077",
       },
}
if not (skip_rdkit or chemfp.rdkit.ATOM_PAIR_VERSION is None):
    _atom_pair_fps = _atom_pair_fingerprints[chemfp.rdkit.ATOM_PAIR_VERSION]
    PAIR_TYPE = "RDKit-AtomPair/" + chemfp.rdkit.ATOM_PAIR_VERSION + " "

class TestAtomPairFingerprinter(unittest2.TestCase, FromAtomsMixin):
    typeflag = "--pair"
    from_atoms_0_0 = b"00000000000000000000000000000000000000000000000000000000000001010000000000000000000000010000000010000000000000000000000001000000000000000000000000000000000000000000000000000010000000000000000100000010000100000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000030000000000010000000100000000000000000000000000000000110000000000301000000100000000000000000000000000000000000000000000000000000100000010000000000000010\t9425004"
    from_atoms_28 = [
        b'00000000000100000000000000000010000000000000000000000000000010000000000000000000000000001000000000000000000000000000100100003001000000000000000000000000000000000000000000000000000000000001100300000000000000000000000000000100000000000000000000000000000000110000000000000000000000000000100000000000000000000011001101000000000000000100000000000000000000000000000000000000000100030000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001000000000000\t9425015',
        b'00000000000000000000000011000000000000000000000000000000000000000000000000000000010000000300000000000000000000000000000000100000000000000000000000010000000100000000000000000000001000000000000000000000000000000030000100000000000000000000000000000000000000000000000000000000031000000100003000000000000000000000000000000000000000000000000000001003000001000000000000000000000000000000001000000000000000000001000000000000000000000000000000000000001000000000000000000000001000000000000000000000000000000100000000000001\t9425030',
        b'00000000000000000000000011000000000000000000000000000000000000000000000000000000010000000300000000000000000000000000000000100000000000000000000000010000000100000000000000000000001000000000000000000000000000000030000100000000000000000000000000000000000000000000000000000000031000000100003000000000000000000000000000000000000000000000000000001003000001000000000000000000000000000000001000000000000000000001000000000000000000000000000000000000001000000000000000000000001000000000000000000000000000000100000000000001\t9425031']
    from_atoms_29 = [
        b'00000000000000000000000000000000000000000000000000000010000003000000000000000000000000000000000100000000000000000000000000003000000000000000000000000000000100100000000000000000100000000000101000000000000000000000000000000100000000000000000000000110001001010000000010000000000000000000000000000000000000000000003000000000000000000100000000000000000000000000000000000000000100030000000000000000000000000000000000000000000000000000000011000000000000000000000010000000000000000000000000000000000000001000000010000000\t9425015'
        ]

    
    def test_pair_defaults(self):
        header, output = runner.run_split("--pair", 19)
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=2048 minLength=1 maxLength=30")
        self.assertEqual(output[0], _atom_pair_fps["2048"] + "\t9425004")
    def test_pair_explicit_defaults(self):
        header, output = runner.run_split("--pair --fpSize 2048 --minLength 1 --maxLength 30", 19)
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=2048 minLength=1 maxLength=30")
        self.assertEqual(output[0], _atom_pair_fps["2048"] + "\t9425004")
    def test_num_bits_128(self):
        header, output = runner.run_split("--pair --fpSize 128", 19)
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=128 minLength=1 maxLength=30")
        self.assertEqual(output[0], _atom_pair_fps["128"] + "\t9425004")
    def test_num_bits_error(self):
        errmsg = runner.run_exit("--pair --fpSize 0")
        self.assertIn("fpSize must be 1 or greater", errmsg)
        errmsg = runner.run_exit("--pair --fpSize 2.3")
        self.assertIn("fpSize must be 1 or greater", errmsg)
    def test_min_length(self):
        header, output = runner.run_split("--pair --fpSize 128 --minLength 4", 19)
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=128 minLength=4 maxLength=30")
        self.assertEqual(output[0], _atom_pair_fps["minLength"] + "\t9425004")
    def test_max_length(self):
        header, output = runner.run_split("--pair --fpSize 128 --maxLength 3", 19)
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=128 minLength=1 maxLength=3")
        self.assertEqual(output[0], _atom_pair_fps["maxLength"] + "\t9425004")
    def test_min_length_error(self):
        errmsg = runner.run_exit("--pair --minLength spam")
        self.assertIn("minLength must be 0 or greater", errmsg)
    def test_max_length_error(self):
        errmsg = runner.run_exit("--pair --maxLength -3")
        self.assertIn("maxLength must be 0 or greater", errmsg)
        errmsg = runner.run_exit("--pair --maxLength spam")
        self.assertIn("maxLength must be 0 or greater", errmsg)
    def test_invalid_min_max_lengths(self):
        errmsg = runner.run_exit("--pair --maxLength 0") # default minLength is 1
        self.assertIn("--minLength must not be greater than --maxLength", errmsg)
        errmsg = runner.run_exit("--pair --minLength 4 --maxLength 3")
        self.assertIn("--minLength must not be greater than --maxLength", errmsg)
    def test_valid_min_max_lengths(self):
        header, output = runner.run_split("--pair --minLength 0")
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=2048 minLength=0 maxLength=30")
        header, output = runner.run_split("--pair --minLength 0 --maxLength 0")
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=2048 minLength=0 maxLength=0")
        header, output = runner.run_split("--pair --minLength 5 --maxLength 5")
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=2048 minLength=5 maxLength=5")
        header, output = runner.run_split("--pair --minLength 6 --maxLength 8")
        self.assertEqual(header["#type"], PAIR_TYPE + "fpSize=2048 minLength=6 maxLength=8")


if skip_rdkit:
    TestAtomPairFingerprinter = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestAtomPairFingerprinter)
else:
    TestAtomPairFingerprinter = unittest2.skipIf(chemfp.rdkit.ATOM_PAIR_VERSION is None,
   "This version of RDKit has a broken GetHashedAtomPairFingerprintAsBitVect")(TestAtomPairFingerprinter)


_torsion_fingerprints = {
"1": {
    "2048": "000000010100000000000040800008000000000000000000000000000000000040004000000000000c0000000000000040000000003010000000000000000800000000000000000000000000000000000000000000100000000000000000000000000080000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000002000000000000000000000000000000000000002000000000000000000000000000000020200080000000000000100000000000000000000000000000800000000000008400000000000000000200000000000000000000020000000000000000010008000000000200000000",
    "128": "c2104083013018a42c008042c0000800",
    "targetSize": "1491150001c0f010648000086245052c",
    },
"2": {
    "2048": "00000000000003000000000001000000010000000000000000000000000000000000000000000000000000000000000700000010000000000010000000000000000000100000000000000000100000000000000000000100000000000001003000000000000000000000000000000000000000000000000000000000000000001000000100000000000000010000001000000000000000000000000000001000001100000000000000000000100000000000000000000000000000000000000000000001000000000000000000000000010000000000330000100100000010000000100000000000000000101000000000000001000000000030000000000000",
    "128": "13111033000037000070011131013037",
    "targetSize": "33037307030103730303131100331100",
      }
}
if not skip_rdkit:
    _torsion_fps = _torsion_fingerprints[chemfp.rdkit.TORSION_VERSION]
    TORSION_TYPE = "RDKit-Torsion/" + chemfp.rdkit.TORSION_VERSION + " "

class TestTorsionFingerprinter(unittest2.TestCase, FromAtomsMixin):
    typeflag = "--torsion"
    from_atoms_0_0 = b"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\t9425004"
    from_atoms_28 = [
        b'00100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\t9425015',
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\t9425030',
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\t9425031']
    from_atoms_29 = [
        b'00000000000003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\t9425015'
        ]
    
    def test_torsion_defaults(self):
        header, output = runner.run_split("--torsion", 19)
        self.assertEqual(header["#type"], TORSION_TYPE + "fpSize=2048 targetSize=4")
        self.assertEqual(output[0], _torsion_fps["2048"] + "\t9425004")
    def test_torsion_explicit_defaults(self):
        header, output = runner.run_split("--torsion --fpSize 2048 --targetSize 4", 19)
        self.assertEqual(header["#type"], TORSION_TYPE + "fpSize=2048 targetSize=4")
        self.assertEqual(output[0], _torsion_fps["2048"] + "\t9425004")
    def test_num_bits_128(self):        
        header, output = runner.run_split("--torsion --fpSize 128 --targetSize 4", 19)
        self.assertEqual(header["#type"], TORSION_TYPE + "fpSize=128 targetSize=4")
        self.assertEqual(output[0], _torsion_fps["128"] + "\t9425004")
    def test_num_bits_error(self):
        errmsg = runner.run_exit("--torsion --fpSize 0")
        self.assertIn("fpSize must be 1 or greater", errmsg)
        errmsg = runner.run_exit("--torsion --fpSize 2.3")
        self.assertIn("fpSize must be 1 or greater", errmsg)
    def test_target_size(self):
        header, output = runner.run_split("--torsion --fpSize 128 --targetSize 5", 19)
        self.assertEqual(header["#type"], TORSION_TYPE + "fpSize=128 targetSize=5")
        self.assertEqual(output[0], _torsion_fps["targetSize"] + "\t9425004")
    def test_target_size_error(self):
        errmsg = runner.run_exit("--torsion --fpSize 128 --targetSize -1")
        self.assertIn("targetSize must be 1 or greater", errmsg)
        errmsg = runner.run_exit("--torsion --fpSize 128 --targetSize spam")
        self.assertIn("targetSize must be 1 or greater", errmsg)
        errmsg = runner.run_exit("--torsion --fpSize 128 --targetSize 0")
        self.assertIn("targetSize must be 1 or greater", errmsg)

TestTorsionFingerprinter = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestTorsionFingerprinter)

# XXX

rdkit_pattern_1_values = [
b'0a0000089048610001000002801414408000280080200400000d000241001231284014280841000000218210080100002024002c01314c800000270400050200c180208040092008100b0800804640000020a009ca80984c0202204602001000300ea0f41012400086000000ab2840002c50010c80d00362ec1810444088004050000818500b4100104050021034001090301048224228410200000000420229000008100000034001809282803ce40850030000958210021800408810024009010a4065200150448011002160a640010010800042020a04b0080020100040000800220808910820100020c0084804000008000c014600700000000180080060\t9425004',
b'0a402008b048650081000002801414408000280080a00400000d000261801031284005080861000000018210080100002006402c0b714c8042202606000502004180208040092000000b0c00804640010022a009ca84984c02023046020410083006a2e41012400086000000ab2840000c50010c80d80360ec1850444088004050008018700b41001040504a1034001090301048224228410a00000400020029080008080101034001009086803ca408500300009182108218005009100a400d010220652101504480112020208648051000800040020a0cb0080020100040000800120a189100e0000020c8105804080008000c014222700000000100080062\t9425009',
b'0a4060089058610001000202821014408000280080200400000d1102610010312840040808410000000182100801000022240028013148801000260600050200c182208008092001000b08008046400000222009ca805c4c0202304602041000300622c410124000864000002b2840000c50010c80dc0360ec1810444008004050000018300b4100106050021034001090241048224a2c410240000000420029080008000000034011009082803ca40850430000d1c210001800400810124001010200652181504000110020288650058000800040020a04b0080020500040000800100808920820000000c0185804000008000c214200300000080186000062\t9425012',
b'0a080008b048610281001802811415000000280081200400008d000241041033284004080841000000018210080100002006402c03314c8040242684000502004180308048092000000b0800804640003020a009ca80d84c02222046020012003006a0f41012400006002000ab2940000c51010c80d48360ec185044408a004050000018500b41001060500a1234001090301048224238410a00000402020029000008081001034001009086803cac08500300409182100218005008100340090102006520015044801120202aa640011080800040020a04b00a0020100040000900120818910020000000c00a4804000008000c014220700000480140000060\t9425015',
b'8a00000891c8610081000002801414000000280080200400000d0002410410332840040a084100000001821008010000200640ac01314c800020268400050200c180208048092400000b0800804640001020a009ca80d84c020220460a0010003006a0e41012400006000000ab2940000c51010c80d40360ec181044c088004050000018500b41103060500a1034001090301048324228410a00000400020229000008000001034001009086a03ca40850030000918210021800400810024009010a00e52411504480112028288640011080800040020a04b0080020100040000900820818910822000000c00a4804000008000c214200700000080100000060\t9425018',
b'0a000008b04c610081000802811415400000280081200400000d000241041233284014280841000000018210080100002006402d01314c8000202784000502004180208048096008000b0800804640001020a009ca80d84c0202204622009000300ea0e41012410086000800ab2d40800c51010c80d00760ec1910444088004050000018500b41001060500a1034001090301048224238410a00000400020029000008080801034001009086843ce4085003000091821002180050081002400901024065200150448011202028a640011080800042020a04b00a0020100040000900320818910020000020c0085804000008000c0142207000000c0100000060\t9425021',
b'0a280200a14861028101d80281140500000028008120040000ac0002410410322040080a880100008000821000030000200640a403314c8040242684000d0200c180300048092000020b8802004640001420a4018a84584c0222204602401200300480f40812400006002000ab29000004010108a08003208c194046408a004000000018500b41003061500a9234001090341048220238400a00000482030221100008080011134000009006a034a408520340409182100218405018100340490508122524090044800160202a8a40011080008040001a04b0020020108040000b00120818810800000200800a4804010008000c014220748000080140802060\t9425030',
b'0a280200a14861028101d80281140500000028008120040000ac0002410410322040080a880100008000821000030000200640a403314c8040242684000d0200c180300048092000020b8802004640001420a4018a84584c0222204602401200300480f40812400006002000ab29000004010108a08003208c194046408a004000000018500b41003061500a9234001090341048220238400a00000482030221100008080011134000009006a034a408520340409182100218405018100340490508122524090044800160202a8a40011080008040001a04b0020020108040000b00120818810800000200800a4804010008000c014220748000080140802060\t9425031',
b'0a0000089048600001000000801014000000200000200400000d000241000031284004080041000000018210080100002004002c01310c8040002604000502004180208040092000000b0800804640000020a0094a80884c02022046000010003006206010124000040000002b2840000c50010c80d00360ec185044408800405000001810030100104050021034001080301048224228410200000000020029000008000000034001009082803ca40850030000918210021800400810024009000200612000504080110020208640010000800040020a04b0080020100040000000100808900020000000c0004804000008000c014200700000000140000060\t9425032',
b'0a400008b04c610081000802811415408001280081200400000d000241241033284004080841000000018210080100002006402d01714c8000202686020502004180208040096200000b08008246c0000022a00bca80d84c02023046120090003016a0e41012410086000080ab2d41800c51018c80dc0760ec1810444088004050000018700b41801060584a1034001090301048224a38510a00000c1002002b08000a080801034001209086803ca408500300009182100218005008100240090102006520015044801120202886400110008000c0020a04b00a0020100040000900020818910020000000c8084804000008400c214220700000000100000062\t9425033',
b'0a0000089048600001000000801014000000200080200400000d000241001231284004080041000000018210080100002004002c01310c8000002704000502004180208040092000000b0800804640000020a0094a80884c0202204600001000300ea0641012400004000000ab2840000c50010c80d00360ec181044408800405000001850034100104050021034001080301048224228410200000000020029000008000000034001009082803ca40850030000918210021800400810024009000200612000504480110020208640010000800040020a04b0080020100040000000320808900020000020c0004804000008000c014200700000000140000060\t9425034',
b'0a600008b048610081004002811415428000280081200400000d0002410410332860142a884100008001821008030000202640ac01314c904020268640050200c180208048092008000b0802804640001022a009ca84d84c02223046024010003006a0e41012400086000000ab2944000c51010c80dc0360ee185046408c004050000018700b41001060500a1034001090301048224238410a00000400420029080008080001034001009086a03ce40850030000918210021880500810025049050a4067200b50448011202428ae40011080800042020a04b0080020100040000900124818910820000000c00a4804010008000c614220700090080100002062\t9425035',
b'0a6040089048610081004002811414408001280081200400000d000241041033284004888841000080018211080300002026402c09314c80402026c600050200c180208048092000000b0802804640001022a009ca84584c02223046124010003006a0e41012400086000000ab2940808c51010c80d80361ec1850464088004250000018780b41001060580a5035001090341048224228412a000004004200290800080800010340110091868034a4085003000091c211021800400810026049050200652009584480112020288e40019080800040020a04b0080020100040000900120818910820002000c8084804010008000c014220700000080144000062\t9425036',
b'0a0001089048600081000002801414400001200080200400000d0042410010316840142a0841000000018210480100002004002c01314c8000002604000502004180208040092008000b08008046400000a0a009ca80184c02022046020010003006a0641012400486000000ab2840000c50010c80d00360ec1810444088004050000018500b4100104058021034001080301048224228400200000000020029000008000000034001009086a434e4085003020091821002180040081002400901024065200154448011002020a640010000800042020a04b0080020100040000800020818910020000000c80ac804000008000c014200700000001100000060\t9425037',
b'0a294008b048610281005802811415400000280081200400008d0082410410332940040a884100008001821008030000202640ac03314c804024268400050200c181308048092000000b0802804640001020a009ca84d84c02222046024012003006e0e41012400086002000ab2960000c51010c80d40360ec18d046408a004050000018508b41001460500a1234001090301048224238410a00000400420029000008080001034001009086a03ca4085003000091c210021800500810034049050a006520195044801120202a8e40011080800050020a04b00a00a0101040000900120818910820000000c00a4804010008000c214220700080080140000060\t9425040',
b'0a080008904c610281001002801414100000a810a020040000ad0002410410332840040a0841000002018210080100002006402d03314e804024268400050200c180308048096000000b080080464000102aa009ca80584c02022046024492003006a0e41012410006002100ab2d40800c51010c80d01760ee185044408e004052040018500b41001060500a103400909030106822422c400a000004000200a9008008080801034001009086a0bca40850030080918210021800400810034009010200652003504480112020a88640011080820040020a04b0080020100040000900120818910820000000c00a4804200008000c014220700011880100002060\t9425041',
b'0a080008904c610281001002801414100000a810a020040000ad0002410410332840040a0841000002018210080100002006402d03314e804024268400050200c180308048096000000b080080464000102aa009ca80584c02022046024492003006a0e41012410006002100ab2d40800c51010c80d01760ee185044408e004052040018500b41001060500a103400909030106822422c400a000004000200a9008008080801034001009086a0bca40850030080918210021800400810034009010200652003504480112020a88640011080820040020a04b0080020100040000900120818910820000000c00a4804200008000c014220700011880100002060\t9425042',
b'0a400008b048610081000002801414008000280080200400000d000241201031284004080841000000118210080100002006402c01314c8040202606020502004180208040092200000b0800824640000022a00bca80184c020230461b0010003016a0e41012400006000080ab2841000c50018c80d80360ec1850444088004050000018700b41801040504a5034001090301048224a28502a00200c1002002b08000a080001034001209086c03ca40850030000918210021800500810034209010200652201504480112020208640011000800040060a04b8080020100040000800120818914020000000c8004804000008400c014a20700200000100000162\t9425045',
b'0a000008904c610001000002801014c000002800c0200400000d000341001031284004080841000000018210080100002004002d01314c800000260420050220c180208040096010000b08108046c0000020a009ca80d84c0202204602009000302620e41012410086000000ab2840808c50010c80d40360ec1810444088004050000018500b4100106050021034001890305048224228410200000000020029002008000800034001009082803ca40850030000918210021800400810024009010200652001504080112020208640010000800040020a04b0080020100040000800020808900820000000c0004804000008000c214200700000000100000060\t9425046',
]

rdkit_pattern_2_values = [
b'0a0000089048610001000002801414000000280080200400002d040241001231284014280841000000218210080100002004002c03314c800000270400050200418020804009200810090800804640000120a009ca80984c0202204402001000301ea0f41012400006000000ab2840002c50010c80d00362ec1810044088004050000818520b4100104040021834003090301048224228410000000000020229001008000000430081009282803ce40850030000958210021800420810024008010a40652001504c8001002060a640012010800042020a04b04840201000c000080822080891002010002080884804000008000c014200700000000180080060\t9425004',
b'0a402008b048650081000002801414008000280080a00400002d040261801031284005080861000000018210080100002006402c0b31cc804220260600050200418020804009200000090c00804640010022a009ca84984c02023044020410083016a2e41012400006000000ab2840000c50010c80d80360ec1850044088004050008018700b41001040404a1034001090301048224228410800000400020029081008080101030081009086803ca408500300009182108218005009100a400c010220652101504c80012020208648053000800040020a0cb04800201000c0000800120a189100e000002088905804080008000c014222700000000100080062\t9425009',
b'0a4060089058610001000202821014008000280080200400002d15026100103128400408084100000001821008010000220400280131488210002606000502004182208008092001000908008046400000222009ca805c4c0202304402041000301622c410124000064000002b2840000c50012c80dc0360ed1810044008004050000018320b4100106040021034001090241048224a2c410040000000020029081008000000030091009082803ca40850430000d1c21002180042081012400001020065218150480001002028865005a000800040020a04b04840205000d000080810080892002000000080985804000008000c214200300000080182000062\t9425012',
b'0a080008b04861028100180281141500000028008120040000ad040241041033284004080841000000018210080100002006402c03314c804024268400050200418030804809200000090800804640003020a009ca80d84c02222044020012003006a0f41012400006002000ab2940000c51010c80d48360ec185004408a004050000018500b41001060400a1234001090301048224238410a00000402020029001008081001030081009086803cac0850030040918210021800500810034008010200652001504c800120202aa640013080800040020a04b04a00201000c0000900120818910020000000800a4804000008000c014220700000480140000060\t9425015',
b'8a00000891c8610081000002801414000000280080200400002d0403410410332840040a084100000001821008010000200640ac01314c800020268400050200418020804809240000090800804640001020a009ca80d84c020220440a0010003006a0e41012400006000000ab2940000c51010c80d40360ec181004c088004050000018500b41003060400a1034001090301048324228410800000400020229001008000001030081009086a03ca40850030000918210021800400810024008010a00e52411504c80012020288640013080800040020a04b04840201000c0000908830818910022000000800a4804000008000c214200700000080100000060\t9425018',
b'0a000008b04c610081000802811415000040280081200400002d040241041233284014284841000001018210080100002006402d01315c800060278400050200438020804809600800090800804640001060a009ca80d84c0202204422049000301ea0e41012610006000800ab2d40800c71010c80d00760ec1914044088004050010018d20b41001060400a50340010943031482242384108040004040300290011080808010300c1009086803ce40850030000d1821002180152081002400801024065200950cc8001202028a640013080800042020a04b04a40221000c0100908320c18910020000020c0885904000008000c0142207000000d0100000060\t9425021',
b'0a280200a14861028101d80281140500000028008120040000ac0402410410322040080a880100008000821000030000200640a403314c8040242684000d0200c18030004809200002098802004640001020a4018a84584c0222204602401204300480f40812400006002000ab29000004010108a08003208c194006408a004000000018500b41003061400a1234021090301048220238400a08000402030221100808080011130000009006a034a40852034040918210021840501810034048050812253409004c800160202a8a40011080008040001a04b00240201080c0000908120818810000000200800a4804010808000c014220748000080140802060\t9425030',
b'0a280200a14861028101d80281140500000028008120040000ac0402410410322040080a880100008000821000030000200640a403314c8040242684000d0200c18030004809200002098802004640001020a4018a84584c0222204602401204300480f40812400006002000ab29000004010108a08003208c194006408a004000000018500b41003061400a1234021090301048220238400a08000402030221100808080011130000009006a034a40852034040918210021840501810034048050812253409004c800160202a8a40011080008040001a04b00240201080c0000908120818810000000200800a4804010808000c014220748000080140802060\t9425031',
b'0a0000089048600001000000801014000000200000200400002d040241000031284004080041000000018210080100002004002c01310c804000260400050200418020804009200000090800804640000020a0094a80884c02022044000010003006206010124000040000002b2840000c50010c80d00360ec185004408800405000001810030100104040021034001080301048224228410000000000020029001008000000030081009082803ca40850030000918210021800400810024008000200612000504880010020208640012000800040020a04b04800201000c000000010080890002000000080004804000008000c014200700000000140000060\t9425032',
b'0a400008b04c610081000802811415008021280081200400002d040241241033284004080841000000018210080100002006402d01314c8000202686020502004180208040096200000908008246c0000022a00bca80d84c02023044120090003016a0e41012410006000080ab2d41800c51018c80dc0760ec1810044088004050000018700b41801060484a1034001090301048224a38510800000c1002002b08100a080801030081209086803ca40850030000918210021800500810024008010200652001504c800120202886400130008000c0020a04b04a01201000c0000900020818910020000000c8884804000008400c214220700000000100000062\t9425033',
b'0a0000089048600001000000801014000000200080200400002d040241001231284004080041000000018210080100002004002c01310c800000270400050200418020804009200000090800804640000020a0094a80884c0202204400001000300ea0641012400004000000ab2840000c50010c80d00360ec181004408800405000001850034100104040021034001080301048224228410000000000020029001008000000030081009082803ca40850030000918210021800400810024008000200612000504c80010020208640012000800040020a04b04800201000c000000032080890002000002080004804000008000c014200700000000140000060\t9425034',
b'0a600008b048610081004002811415008000280081200400002d0402410410332860142a884100008001821008030000200640ac01314c804020268640050200c18020804809200800090802804648001022a009ca84d84c02223046024010003016a0e41012400006000000ab2944020c51010c80dc0360ee185006408c004050000018720b41001060400a1034001090301048224278410800000400020029081008080001030081009086a03ce40850030000918210021880520810025048050a4067200b504c8001202428ae40013080800042020a04b04840201000c0000908124818910020000000808a4804010008000c614220700010080100002062\t9425035',
b'0a6040089048610081004002811414008009280081200400002d04024104103328440488c841000080018211080300002006402c09314c82406026c600050200c18020804809200000090802804640009022a009ca84585c0222b046124419003036a0e41012400047000000ab2940808c71010c91d80361ec18540640880042500000187a0b410010604a0a51350010943411482242285128040004040300290811080800010340d10091968034a4085003000091c21102180142081002604805020065200958cc80012020288e4001b080800040020a04b04840201000c004090812081891002000202088884804010008000c094220700000080140000062\t9425036',
b'0a0001089048600081000002801414000001200080200400006d0442410010316840142a0841000000018210480100002004002c01314c8000002604000502004180208040092008000908008046400000a0a009ca80184c02022044020010003016a0641012400406000000ab2840000c50010c80d00360ec1810044088004050000018500b410010404802103400108030104822422840000000000002002900100800000003008100b086a034e40850030200918210021800400810024008010240652001544c8001002020a640012000800042020a04b04800201000c0000800020818910020000000888ac804000008000c014200700000001100000060\t9425037',
b'0a294008b04861028100580283141500000028008120040000ad0482410410b32844040ac84100008001821008030000200644ac03314c804064268400050200c18130804809200000090802804640001020a009ca84d84c0222a04602441a003016e1e49012400006002000ab2960000c71010c81d40360ec18d406428a004050000018528b41001460400a13340010943011482242784109040004040300290011080800810300c1009096a03ca4085003202091c210021801520810034048050a0065201b50cc800120202a8e40017080800050020a04b04a40a01010c0000908120818910020000020808a4804010008000c294220700000080140010060\t9425040',
b'0a080008904c610281001002801414000000a810a020040000ad0402410410332840040a4841000002018210080100002006402d03314e804064268400050200418030804809600000090a0080465000102aa009ca80584c02022044024492003016a0e41012410016002100ab2d40800c71010c80d01760ee185404408e004052040018520b41001060400a10340090943010682242284008000404040200a90091080808010301c1009086a0bca4085003008091821002180142081003400801020065200350cc80012022a88640013080820040020a04b04840201000c0000b0a120858b10020000000c08a4804200008000c014221700011880100002060\t9425041',
b'0a080008904c610281001002801414000000a810a020040000ad0402410410332840040a4841000002018210080100002006402d03314e804064268400050200418030804809600000090a0080465000102aa009ca80584c02022044024492003016a0e41012410016002100ab2d40800c71010c80d01760ee185404408e004052040018520b41001060400a10340090943010682242284008000404040200a90091080808010301c1009086a0bca4085003008091821002180142081003400801020065200350cc80012022a88640013080820040020a04b04840201000c0000b0a120858b10020000000c08a4804200008000c014221700011880100002060\t9425042',
b'0a400008b04861008100000a801414008000280080200400002d040241201031284004084841000400118210080100002006402c01314c804020260602050200418020804009220000090800824640000022a00bca80984c020230441b0410003016a0e41012400106000080ab2841000c70018c80d80360ec1858044088004050000018720b41801040404a5034001094301248224a28502800200c1402002b08110a0800810300c1209086c03ca4085003000091821002180152081003420801020065220150cc80012020208640013000800040060a04b84840203000c000080812081891402000000088804804000008400c014a20700200000100000162\t9425045',
b'0a000008904c6100010000028010140000002800c0200400002d040341001031284004080841000000018210080100402004002d01314c8000002604200502004180208040096010000908108046c0000020b009ca80dc4c0202224402009000303620e41012410006000000ab2840808c50010c80d40360ec1810044088004050000018500b4100106040021034001890305048224228410000000000020029003008000800030081009082803ca40850030000918210021800400810024008010200652001504880010020208640012000800040020a04b04840201000c0000808020808900020000000c0804804000008000c214200700000000100000060\t9425046',
]

rdkit_pattern_4_values = [
b"0a0000089048610001008002801414000000280080a00400002d0402410012312a4014280841000000218210080100002004002c03314c800000270c00050200638820804009200810090800804640000120a009ca80984c0202204402001000301ea0f41012400006000000ab2840002c50010e80d00362ec1810044088004058020818720f411010404002183400309838104822422841000010000002022901d308000008430081009282803ee40850030000958210021800420810024008010a40652001504c8001002060a640012010800042020a04b04840201000c000080822080891002010002080884804000008000c01420070000000018a080060\t9425004",
b"0a402008b048650081008002801414008000280080a00400002d0402618010312a4005080861000000018210080100002006402c0b31cc804220260e00050200638820804009200000090c00804e40010022a009ca84984c02023044020410083016a2e41012400006000000ab2840000c50010e80d80360ec1850044088004058028018700f41101040404a103400109838104822422841080010040002002908d208080109030081009086803ea408500300009182108218005009100a400c010220652101504c80012020208648053000800040020a0cb04800201000c0000800120a189100e000002088905804080008000c01422270000000010a080062\t9425009",
b"0a4060089058610001008202821014008000280080a00400002d1502610010312a40040808410000000182100801000022040028013148821000260e00050200638a208008092001000908008046400000222009ca805c4c0202304402041000301622c410124000064000002b2840000c50012e80dc0360ed1810044008004050020018320f41101060400210340010982c1048224a2c41004010000002002908d208000008030091009082803ea40850430000d1c21002180042081012400001020065218150480001002028865005a000800040020a04b04840205000d000080810080892002000000080985804000008000c21420030000008018a000062\t9425012",
b"0a080008b048610281009802811415000000280081a0040000ad0402410410332a4004080841000000018210080100002006402c03314c804024268c00050200638830804809200000090800804e40003020a009ca80d84c02222044020012003006a0f41012400006002000ab2940000c51010e80d48360ec185004408a004058020018700f41101060400a1234001098381048224238410a0010040202002900d208081009030081009086803eac0850030040918210021800500810034008010200652001504c800120202aa640093080800040020a04b04a00201000c0000900120818910020080000800a480400000a000c01422070000048014a000060\t9425015",
b"8a00000891c8610081008002801414000000280080a00400002d0403410410332a40040a084100000001821008010000200640ac01314c800020268c00050200638820804809240000090800804e40001020a009ca80d84c020220440a0010003006a0e41012400006000000ab2940000c51010e80d40360ec181004c088004058020018700f41103060400a103400109838104832422841080010040002022902d208000009030081009086a03ea40850030000918210021800400810024008010a00e52411504c80012020288640013080800040020a04b04840201000c0000908830818910022000000800a4804000008000c21420070000008010a000060\t9425018",
b"0a000008b04c610081008802811415000040280081a00400002d0402410412332a4014284841000001018210080100002006402d01315c800060278c00050200638820804809600800090800804e40001060a009ca80d84c0202204422049000301ea0e41012610006000800ab2d40800c71010e80d00760ec1914044088004058030018f20f41101060400a503400109c38314822423841080410040403002901d3080808090300c1009086803ee40850030000d1821002180152081002400801024065200950cc8001202028a640013080800042020a04b04a40221000c0100908320c18910020000020c088590400000a000c0142207000000d010a000060\t9425021",
b"0a280200a14861028101d802811405000000280081a0040000ac0402410410322240080a880100008000821000030000200640a403314c804024268c000d0200e38830004809200002098802004e40001020a4018a84584c0222204602401204300480f40812400006002000ab2900000401010aa08003208c194006408a004008020018700f41103061400a1234021098381048220238400a0810040203022112ca08080019130000009006a036a40852034040918210021840501810034048050812253409004c800160202a8a40011080008040001a04b00240201080c0000908120818810000080200800a480401080a000c01422074800008014a802060\t9425030",
b"0a280200a14861028101d802811405000000280081a0040000ac0402410410322240080a880100008000821000030000200640a403314c804024268c000d0200e38830004809200002098802004e40001020a4018a84584c0222204602401204300480f40812400006002000ab2900000401010aa08003208c194006408a004008020018700f41103061400a1234021098381048220238400a0810040203022112ca08080019130000009006a036a40852034040918210021840501810034048050812253409004c800160202a8a40011080008040001a04b00240201080c0000908120818810000080200800a480401080a000c01422074800008014a802060\t9425031",
b"0a0000089048600001008000801014000000200000a00400002d0402410000312a4004080041000000018210080100002004002c01310c804000260c00050200638820804009200000090800804640000020a0094a80884c02022044000010003006206010124000040000002b2840000c50010e80d00360ec18500440880040500200183007011010404002103400108838104822422841000010000002002900d208000008030081009082803ea40850030000918210021800400810024008000200612000504880010020208640012000800040020a04b04800201000c000000010080890002000000080004804000008000c01420070000000014a000060\t9425032",
b"0a400008b04c610081008802811415008021280081a00400002d0402412410332a4004080841000000018210080100002006402d01314c800020268e02050200638820804009620000090800824ec0000022a00bca80d84c02023044120090003016a0e41012410006000080ab2d41800c51018e80dc0760ec1810044088004058020018700f41901060484a1034001098381048224a38510800100c1002002b0ad20a080809030081209086803ea40850030000918210021800500810024008010200652001504c800120202886400130008000c0020a04b04a01201000c0000900020818910020000000c888480400000a400c21422070000000010a000062\t9425033",
b"0a0000089048600001008000801014000000200080a00400002d0402410012312a4004080041000000018210080100002004002c01310c800000270c00050200638820804009200000090800804640000020a0094a80884c0202204400001000300ea0641012400004000000ab2840000c50010e80d00360ec18100440880040580200187007411010404002103400108838104822422841000010000002002900d208000008030081009082803ea40850030000918210021800400810024008000200612000504c80010020208640012000800040020a04b04800201000c000000032080890002000002080004804000008000c01420070000000014a000060\t9425034",
b"0a600008b04861008100c002811415008000280081a00400002d0402410410332a60142a884100008001821008030000200640ac01314c804020268e40050200e38820804809200800090802804e48001022a009ca84d84c02223046024010003016a0e41012400006000000ab2944020c51010e80dc0360ee185006408c004058020018720f41101060400a103400109838104822427841080010040002002909d208080009030081009086a03ee40850030000918210021880520810025048050a4067200b504c8001202428ae40013080800042020a04b04840201000c0000908124818910020000000808a4804010008000c61422070001008010a002062\t9425035",
b"0a604008904861008100c002811414008009280081a00400002d0402410410332a440488c841000080018211080300002006402c09314c82406026ce00050200e38820804809200000090802804e40009022a009ca84585c0222b046124419003036a0e41012400047000000ab2940808c71010e91d80361ec18540640880042580200187a0f411010604a0a513500109c3c114822422851280410040403002908d3080800090340d10091968036a4085003000091c21102180142081002604805020065200958cc80012020288e4001b080800040020a04b04840201000c004090812081891002000202088884804010008000c09422070000008014a000062\t9425036",
b"0a0001089048600081008002801414000001200080a00400006d0442410010316a40142a0841000000018210480100002004002c01314c800000260c00050200638820804009200800090800804e400000a0a009ca80184c02022044020010003016a0641012400406000000ab2840000c50010e80d00360ec1810044088004058020018700f411010404802103400108838104822422840000010000002002901d20800000803008100b086a036e40850030200918210021800400810024008010240652001544c8001002020a640012000800042020a04b04800201000c0000800020818910020000000888ac804000008000c01420070000000110a000060\t9425037",
b"0a294008b04861028100d802831415000000280081a0040000ad0482410410b32a44040ac84100008001821008030000200644ac03314c804064268c00050200e38930804809200000090802804e40001020a009ca84d84c0222a04602441a003016e1e49012400006002000ab2960000c71010e81d40360ec18d406428a004058020018728f41101460400a133400109c38114822427841090410040403002900d3080800890300c1009096a03ea4085003202091c210021801520810034048050a0065201b50cc800120202a8e40017080800050020a04b04a40a01010c0000908120818910020000020808a480401000a000c29422070000008014a010060\t9425040",
b"0a080008904c610281009002801414000000a810a0a0040000ad0402410410332a40040a4841000002018210080100002006402d03314e804064268c00050200638830804809600000090a00804e5000102aa009ca80584c02022044024492003016a0e41012410016002100ab2d40800c71010e80d01760ee185404408e00405a060018720f41101060400a103400909c3810682242284008001404040200a900d3080808090301c1009086a0bea4085003008091821002180142081003400801020065200350cc80012022a88640013080820040020a04b04840201000c0000b0a120858b10020000000c08a4804200008000c01422170001188010a002060\t9425041",
b"0a080008904c610281009002801414000000a810a0a0040000ad0402410410332a40040a4841000002018210080100002006402d03314e804064268c00050200638830804809600000090a00804e5000102aa009ca80584c02022044024492003016a0e41012410016002100ab2d40800c71010e80d01760ee185404408e00405a060018720f41101060400a103400909c3810682242284008001404040200a900d3080808090301c1009086a0bea4085003008091821002180142081003400801020065200350cc80012022a88640013080820040020a04b04840201000c0000b0a120858b10020000000c08a4804200008000c01422170001188010a002060\t9425042",
b"0a400008b04861008100800a801414008000280080a00400002d0402412010312a4004084841000400118210080100002006402c01314c804020260e02050200638820804009220000090800824e40000022a00bca80984c020230441b0410003016a0e41012400106000080ab2841000c70018e80d80360ec1858044088004058020018720f41901040404a503400109c381248224a28502800300c1402002b0ad30a0800890300c1209086c03ea4085003000091821002180152081003420801020065220150cc80012020208640013000800040060a04b84840203000c000080812081891402000000088804804000008400c014a2070020000010a000162\t9425045",
b"0a000008904c6100010080028010140000002800c0a00400002d0403410010312a4004080841000000018210080100402004002d01314c800000260c200502006388208040096010000908108046c0000020b009ca80dc4c0202224402009000303620e41012410006000000ab2840808c50010e80d40360ec1810044088004050020018700f411010604002103400189838504822422841000010000002002900f20c000808030081009082803ea40850030000918210021800400810024008010200652001504880010020208640012000800040020a04b04840201000c0000808020808900020000000c0804804000008000c21420070000000010a000060\t9425046",
]

if not skip_rdkit:
    rdkit_pattern_values = {
        None: None,
        "1": rdkit_pattern_1_values,
        "2": rdkit_pattern_2_values,
        "3": rdkit_pattern_2_values,
        "4": rdkit_pattern_4_values,
        }[chemfp.rdkit.PATTERN_VERSION]


class TestPatternFingerprinter(unittest2.TestCase):
    def test_pattern_defaults(self):
        header, output = runner.run_split("--pattern", 19)
        self.assertEqual(header[b"#type"], b"RDKit-Pattern/" + chemfp.rdkit.PATTERN_VERSION + b" fpSize=2048")
        self.assertEqual(output, rdkit_pattern_values)

    def test_pattern_explicit_defaults(self):
        header, output = runner.run_split("--pattern --fpSize 2048", 19)
        self.assertEqual(header[b"#type"], b"RDKit-Pattern/" + chemfp.rdkit.PATTERN_VERSION + b" fpSize=2048")
        self.assertEqual(output, rdkit_pattern_values)

    def test_num_bits_128(self):
        header, output = runner.run_split("--pattern --fpSize 128", 19)
        if chemfp.rdkit.PATTERN_VERSION == "1":
            self.assertEqual(output, [
                b'fffffffdfffffffffffffffffbfff679\t9425004',
                b'fffffffffbffffffff7ffefffbfffe7f\t9425009',
                b'fffffffdfbff7ffdff7ffffffffff67f\t9425012',
                b'fffffffdfbfffffffffffefffbffff7b\t9425015',
                b'ffffffffffffffffff7ffefffbfff67b\t9425018',
                b'fffffffdfbffffffff7ffffffffff7fb\t9425021',
                b'ffffffffffff7ffefffffefffbfff77b\t9425030',
                b'ffffffffffff7ffefffffefffbfff77b\t9425031',
                b'ffffbdfdfbfbffffff5ffefffbfff679\t9425032',
                b'fffffffffbffffffff7ffefffbfff7fb\t9425033',
                b'ffffbffdfbfbffffff5ffffffbfff679\t9425034',
                b'fffffffffbfffffffffffefffbfff77b\t9425035',
                b'fffffffdfbff7fffff7ffffffffff6fb\t9425036',
                b'fffffffffbfb7ffeff5ffefffffff679\t9425037',
                b'fffffffffbfffffffffffefffbfff77b\t9425040',
                b'fffffffffbff7ffefffffffffbfff6fb\t9425041',
                b'fffffffffbff7ffefffffffffbfff6fb\t9425042',
                b'fffffffffbff7ffeff7ffefffbfff77b\t9425045',
                b'fffffffdfbffffffff7ffefffbfff6f9\t9425046'])
        elif chemfp.rdkit.PATTERN_VERSION == "2":
            self.assertEqual(output, [
                b'fffffffdfffbffffff7ffffffbfff679\t9425004',
                b'fffffffffbffffffff7ffefffbfffe7f\t9425009',
                b'fffffffdfbff7fffff7ffffffbfff67f\t9425012',
                b'fffffffdfbfffffffffffefffbffff7b\t9425015',
                b'ffffffffffffffffff7ffefffbfff67b\t9425018',
                b'fffffffdfbffffffff7ffffffffff7fb\t9425021',
                b'ffffffffffff7ffefffffefffbfff77f\t9425030',
                b'ffffffffffff7ffefffffefffbfff77f\t9425031',
                b'ffffbdfdfbfbffffff7ffefffbfff679\t9425032',
                b'fffffffffbffffffff7ffffffbfff7fb\t9425033',
                b'ffffbffdfbfbffffff7ffffffbfff679\t9425034',
                b'fffffffffbfffffffffffefffbffff7b\t9425035',
                b'fffffffdfbff7fffff7fffffffffffff\t9425036',
                b'fffffffffbfb7ffeff7ffefffbfff679\t9425037',
                b'fffffffffbfffffffffffefffffffffb\t9425040',
                b'fffffffffbff7ffffffffffffffff6fb\t9425041',
                b'fffffffffbff7ffffffffffffffff6fb\t9425042',
                b'fffffffffbffffffff7ffefffffff77b\t9425045',
                b'fffffffdfbffffffff7ffefffbfff6f9\t9425046',
                ])
        elif chemfp.rdkit.PATTERN_VERSION == "3":
            self.assertEqual(output, [
                b'fffffffdfffbffffff7ffffffbfff679\t9425004',
                b'fffffffffbffffffff7ffefffbfffe7f\t9425009',
                b'fffffffdfbff7fffff7ffffffbfff67f\t9425012',
                b'fffffffdfbfffffffffffefffbffff7b\t9425015',
                b'ffffffffffffffffff7ffefffbfff67b\t9425018',
                b'fffffffdfbffffffff7ffffffffff7fb\t9425021',
                b'ffffffffffff7ffefffffefffbfff77f\t9425030',
                b'ffffffffffff7ffefffffefffbfff77f\t9425031',
                b'ffffbdfdfbfbffffff7ffefffbfff679\t9425032',
                b'fffffffffbffffffff7ffffffbfff7fb\t9425033',
                b'ffffbffdfbfbffffff7ffffffbfff679\t9425034',
                b'fffffffffbfffffffffffefffbffff7b\t9425035',
                b'fffffffdfbff7fffff7fffffffffffff\t9425036',
                b'fffffffffbfb7ffeff7ffefffbfff679\t9425037',
                b'fffffffffbfffffffffffefffffffffb\t9425040',
                b'fffffffffbff7ffffffffffffffff6fb\t9425041',
                b'fffffffffbff7ffffffffffffffff6fb\t9425042',
                b'fffffffffbffffffff7ffefffffff77b\t9425045',
                b'fffffffdfbffffffff7ffefffbfff6f9\t9425046',
                ])
        elif chemfp.rdkit.PATTERN_VERSION == "4":
            self.assertEqual(output, [
                b'ffffffffffffffffff7ffffffbfff679\t9425004',
                b'fffffffffbffffffff7ffefffbfffe7f\t9425009',
                b'fffffffffbff7fffff7ffffffbfff67f\t9425012',
                b'fffffffffbfffffffffffefffbffff7b\t9425015',
                b'ffffffffffffffffff7ffefffbfff67b\t9425018',
                b'fffffffffbffffffff7ffffffffff7fb\t9425021',
                b'ffffffffffff7ffefffffefffbfff77f\t9425030',
                b'ffffffffffff7ffefffffefffbfff77f\t9425031',
                b'ffffbdfffbffffffff7ffefffbfff679\t9425032',
                b'fffffffffbffffffff7ffffffbfff7fb\t9425033',
                b'ffffbffffbffffffff7ffffffbfff679\t9425034',
                b'fffffffffbfffffffffffefffbffff7b\t9425035',
                b'fffffffffbff7fffff7fffffffffffff\t9425036',
                b'fffffffffbff7ffeff7ffefffbfff679\t9425037',
                b'fffffffffbfffffffffffefffffffffb\t9425040',
                b'fffffffffbff7ffffffffffffffff6fb\t9425041',
                b'fffffffffbff7ffffffffffffffff6fb\t9425042',
                b'fffffffffbffffffff7ffefffffff77b\t9425045',
                b'fffffffffbffffffff7ffefffbfff6f9\t9425046',
                ])
        else:
            raise AssertionError("No test for %r" % (chemfp.rdkit.PATTERN_VERSION,))
            
                         
    def test_num_bits_error(self):
        errmsg = runner.run_exit("--pattern --fpSize 0")
        self.assertIn("fpSize must be 1 or greater", errmsg)
        errmsg = runner.run_exit("--pattern --fpSize 2.3")
        self.assertIn("fpSize must be 1 or greater", errmsg)
        errmsg = runner.run_exit("--pattern --fpSize -100")
        self.assertIn("fpSize must be 1 or greater", errmsg)
        

if skip_rdkit:
    TestPatternFingerprinter = unittest2.skipIf(1, "RDKit not installed")(TestPatternFingerprinter)
elif chemfp.rdkit.PATTERN_VERSION is None:
    TestPatternFingerprinter = unittest2.skipIf(1, "This RDKit does not support pattern fingerprints")(TestPatternFingerprinter)


class TestSubstructFingerprinter(unittest2.TestCase):
    def test_substruct_defaults(self):
        header, output = runner.run_split("--substruct", 19)
        self.assertEqual(header[b"#type"], "ChemFP-Substruct-RDKit/1".encode("ascii"))

TestSubstructFingerprinter = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestSubstructFingerprinter)

class TestRDMACCSFingerprinter(unittest2.TestCase):
    def test_rdmaccs_defaults(self):
        header, output = runner.run_split("--rdmaccs", 7, source=MACCS_SMI)
        self.assertEqual(header[b"#type"], b"RDMACCS-RDKit/2")
        hex_fp, id = output[0].split(b"\t")
        self.assertTrue(hex_contains_bit(hex_fp, 43))

    def test_rdmaccs1_key44(self):
        header, output = runner.run_split("--rdmaccs/1", 7, source=MACCS_SMI)
        self.assertEqual(header[b"#type"], b"RDMACCS-RDKit/1")
        hex_fp, id = output[0].split(b"\t")
        self.assertFalse(hex_contains_bit(hex_fp, 43))
        self.assertEqual(output[0], b"040000000000000000000000000000000000000000\t3->bit_2")

    def test_rdmaccs2_key44(self):
        header, output = runner.run_split("--rdmaccs/2", 7, source=MACCS_SMI)
        self.assertEqual(header[b"#type"], b"RDMACCS-RDKit/2")
        hex_fp, id = output[0].split(b"\t")
        self.assertTrue(hex_contains_bit(hex_fp, 43))
        self.assertEqual(output[0], b"040000000008000000000000000000000000000000\t3->bit_2")

    def test_both_flags_gives_error(self):
        result = runner.run_exit("--rdmaccs/1 --rdmaccs/2")
        self.assertIn("Cannot specify both --rdmaccs and --rdmaccs/1", result)
        result = runner.run_exit("--rdmaccs --rdmaccs/1")
        self.assertIn("Cannot specify both --rdmaccs and --rdmaccs/1", result)
        runner.run_split("--rdmaccs --rdmaccs/2", 7, source=MACCS_SMI)
        
        
TestRDMACCSFingerprinter = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestRDMACCSFingerprinter)

_avalon_fps = [
    b'a9a41744165240122932537310c2622410075362060021f29522355c0305047ca45e6ef3e6a8cba83c49a1aad65570601eb1c37c56549011ee25915b403204db\t9425004',
    b'a9b4d3ea1656c1562b3673c718c06767904557eb460061fa9522345c4309245de4566ff3e2aacb9838c9b1abd455f86827b3d77e56549011ef45951b50fe0ccb\t9425009',
    b'b9f5f3401656cb362976534b98c261b75241537a074061d295a2345e4309045dec5e7ef3f2eacbfa78e913abd455f0703fb3e3fc16549091fea7b21b40330ccb\t9425012',
    b'a9a41340165248122932534310c06064100553620e0021d2952274580309045ca4566ef3e2a88f983cc9b1aad455706026b1c37c56549011ee05911b403224c9\t9425015',
    b'a9a493401652c6922936534b10c0613410075766061061d29522345803a1045ca45e7ef3e2a88b88bcc9b5aad455f06076b1c37c56549811ee47b11b443204c9\t9425018',
    b'b9a4174096d2401a29325b7b10c263761087d363060021d6952a357c030304fcb45e6ef3e7a88ba83a6901aad4f57a601eb1d37c56d49015ee0591db403704cb\t9425021',
    b'11a0a0025470269e0a51539402813322808584c08c502b04402075d0130ae20c1c0804f3a29801812d6034229410400472808c020e000010e814811040212001\t9425030',
    b'11a0a0025470269e0a51539402813322808584c08c502304402075d0130ae20c1c0800f3a29801812c6034229410400472808c020e000010e814811040212001\t9425031',
    b'a9a41340165242122932534310c0602410055362060021d2952234580301045ca4566ef3e2a88b883849b1aad455706006b1c37c16549011ee05911b403204c9\t9425032',
    b'a9a49358165240da3932734b10c161bc12055be7060121d69522345a0f0d045cb45e7ef3f2ae8b983cc9b1aaf475f0e4b7b1c37e5654925def4595fb40330cc9\t9425033',
    b'a9a41740165240122932534310c2602410055362060021d29522345c0301045ca45e6ef3e2a88b883849a1aad455f0600eb1c37c56549011ee05911b403204cb\t9425034',
    b'b9a4936096d2441e29b357f311d36b36508753621614a1d6952235d8030914feac567ef3e6ac8ba83ef9b3aad455706037b1c37c565c9211fe65951b403724c9\t9425035',
    b'ebb613fc17d6727e3977734b18c073ad910553e2062871feb56a74dcc74924dca6d66efbe3bdbb99b849b5eedd55f3603fb1df7e1654f0b1ee97979b6a7bccc9\t9425036',
    b'a9a493401652401229b25b6310c4712410175362464221d285223458030104fca4567ef3e6a88ba83cc9b1eed455747026b1d37c56569011ef45b11b407324c9\t9425037',
    b'b9e693403672461e3b3a53c311c2717418055362061023d6953a75d80309c45ca6566ef7e3a88bc83ec9b5aad45579f006b1c37c5654b015ef45933b413384c9\t9425040',
    b'a9e673441652421a7bbe73cb11c1f7261005536e064061d2a53a75582709345cb6566ef3e3ac8bc93e4991ead575f8e436b1c37c56549115fe0591fb403326c9\t9425041',
    b'a9e673441652421a7bbe73cb11c1f7261005536e064061d2a53a75582709345cb6566ef3e3ac8bc93e4991ead575f8e436b1c37c56549115fe0591fb403326c9\t9425042',
    b'a9a59b681656c39af93a574b11c1696e180f57ef470061d2c52a3c582309145cfc5e7ef3e3aebb993949b7ead755786027f3c37c5656b035ef05dd9b763f0cc9\t9425045',
    b'a9a493401652401229b3534310c0713410075362260021d295223458070104dca4567ef7e2aa8b883cc9a1aad475f06016b1c37d16559015ee45915b403204cb\t9425046',
]

_other_avalon_fps = [
    b'24a436c776c84b222d7312fb52c262401e23c358540081b29527054f41050439\t9425004',
    b'64b4beeb76cc0b422b7612ef58c0ff469765d3ef5400a1829547850b514d2c4f\t9425009',
    b'64ac36c376c809462972126b58c2f1d41f61d3ec140081828507041f4101040b\t9425012',
    b'24a436c376c80b022df293eb50c060401621c348560081829507450b41010409\t9425015',
    b'24bcb6c3f6da8f822df617eb50c061501623c348541089c29547a50b45310409\t9425018',
    b'3cb436c3f7ca4b2a2b721afb54e26b5216a3d36954848186950f056f410704a9\t9425021',
    b'158800c3b6e8058b247137a01680730202858cc28e100000e814e5900103c209\t9425030',
    b'158800c3b6e8058b247137a01680730202858cc28e100000e814e5900103c209\t9425031',
    b'24a436c376c80b02297212eb50c060401621c348140081829507050b41010409\t9425032',
    b'35acb6d376ca0b4a3df232eb50e0e1d01721c3ee56018396954785cb41050c09\t9425033',
    b'24a436c376c80b02297212eb50c260401621c348540081829507050f41010409\t9425034',
    b'34a4b6e3f6ce0f2a2ff317fbd1d5635277a3c36a541c83c29567050b410534af\t9425035',
    b'66b63fef77cf3bca2977136f59c0f3c09725d7ca1428c1b6858f048f6b594c8d\t9425036',
    b'25e4b7c376c80ba22df21aef50c471501623d348540281828547050b415104a9\t9425037',
    b'34e6b6c777ea0f9a3ffb53eb51c279701e21c37a561083c6955f452b4101c449\t9425040',
    b'34e436c777ce0b8b3f7a72eb51e1fd461621c37e5400a1c6bd1f456b65011609\t9425041',
    b'34e436c777ce0b8b3f7a72eb51e1fd461621c37e5400a1c6bd1f456b65011609\t9425042',
    b'75bd3eebf7decb8be97236eb53c1694017f3c7df5500a1e6c50f9d9b773d1c0d\t9425045',
    b'24a4b6c776ca0b022df313eb50e070501623c369140181869547054b4511048f\t9425046',
]
    
class TestAvalonFingerprinter(unittest2.TestCase):
    def test_avalon_defaults(self):
        header, output = runner.run_split("--avalon", 19)
        self.assertEqual(header[b"#type"], b"RDKit-Avalon/1 fpSize=512 isQuery=0 bitFlags=15761407")
        self.assertEqual(output, _avalon_fps)
        
    def test_avalon_explicit_defaults(self):
        header, output = runner.run_split("--avalon --fpSize 512 --isQuery=0 --bitFlags=15761407", 19)
        self.assertEqual(header[b"#type"], b"RDKit-Avalon/1 fpSize=512 isQuery=0 bitFlags=15761407")
        self.assertEqual(output, _avalon_fps)

    def test_avalon_all_values_different(self):
        header, output = runner.run_split("--avalon --fpSize 256 --isQuery=1 --bitFlags=32767", 19)
        self.assertEqual(header[b"#type"], b"RDKit-Avalon/1 fpSize=256 isQuery=1 bitFlags=32767")
        self.assertEqual(output, _other_avalon_fps)
        

if skip_rdkit:
    TestAvalonFingerprinter = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestAvalonFingerprinter)
else:
    TestAvalonFingerprinter = unittest2.skipIf(not chemfp.rdkit.HAS_AVALON,
                                               "Avalon fingerprints not available")(TestAvalonFingerprinter)

@unittest2.skipIf(skip_rdkit, "RDKit not installed")
class TestIdAndErrors(unittest2.TestCase, support.TestIdAndErrors):
    _runner = runner
    toolkit = "rdkit"

@unittest2.skipIf(skip_rdkit, "RDKit not installed")
class TestIO(unittest2.TestCase, support.TestIO):
    _runner = runner

class TestBadStructureFiles(unittest2.TestCase):
    def setUp(self):
        self.dirname = tempfile.mkdtemp()
    def tearDown(self):
        shutil.rmtree(self.dirname)

    def _make_datafile(self, text, ext):
        filename = os.path.join(self.dirname, "input."+ext)
        with open(filename, "w") as f:
            f.write(text)
        return filename
    
    def test_blank_line_in_smiles(self):
        filename = self._make_datafile("C methane\n\nO water\n", "smi")
        msg = runner.run_exit(["--errors", "strict", filename])
        self.assertIn("Unexpected blank line", msg)
        self.assertIn(", line 2, record #2", msg)

    def test_bad_smiles(self):
        filename = self._make_datafile("C methane\nQ Q-ane\nO water\n", "smi")
        msg = runner.run_exit(["--errors", "strict", filename])
        self.assertIn("Cannot parse the SMILES 'Q'", msg)
        self.assertIn(", line 2", msg)

    def test_smiles_without_title(self):
        filename = self._make_datafile("C methane\nO water\n[235U]\n", "smi")
        msg = runner.run_exit(["--errors", "strict", filename])
        self.assertIn("Missing SMILES identifier (second column)", msg)
        self.assertIn(", line 3", msg)

    def test_sdf_with_bad_record(self):
        # Three records, second one is bad
        input = TRP + TRP.replace("32 28", "40 21") + TRP
        filename = self._make_datafile(input, "sdf")
        msg = runner.run_exit(["--errors", "strict", filename])
        self.assertIn("Could not parse molecule block", msg)
        self.assertIn(", line 70, record #2", msg)
        self.assertIn("input.sdf", msg)

    def test_sdf_with_bad_record_checking_id(self):
        # This tests a different code path than the previous
        input = TRP + TRP.replace("32 28", "40 21") + TRP
        filename = self._make_datafile(input, "sdf")
        msg = runner.run_exit(["--id-tag", "COMPND", "--errors", "strict", filename])
        self.assertIn("Could not parse molecule block", msg)
        self.assertIn(", line 70, record #2", msg)
        self.assertIn("input.sdf", msg)

    def test_sdf_with_missing_id(self):
        filename = self._make_datafile(TRP, "sdf")
        msg = runner.run_exit(["--id-tag", "SPAM", "--errors", "strict", filename])
        self.assertIn("Missing id tag 'SPAM'", msg)
        self.assertNotIn("for record #1", msg) # check that the old error message isn't present
        self.assertIn("line 1, record #1", msg)
        self.assertIn("input.sdf", msg)

    def test_ignore_errors(self):
        input = TRP + TRP.replace("32 28", "40 21") + TRP.replace("COMPND", "BLAH")
        filename = self._make_datafile(input, "sdf")
        header, output = runner.run_split(["--errors", "ignore", "--id-tag", "BLAH"], source=filename)
        self.assertEqual(len(output), 1)

    def test_unsupported_format(self):
        filename = self._make_datafile("Unknown", "xyzzy")
        result = runner.run_exit([filename])
        self.assertIn("RDKit does not support the 'xyzzy' format", result)
        
TestBadStructureFiles = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestBadStructureFiles)
        

# Some code to test the internal interface
class TestInternals(unittest2.TestCase):
    def test_make_rdk_fingerprinter(self):
        # Make sure that I can call with the defaults
        chemfp.rdkit.make_rdk_fingerprinter()
            
    def test_make_rdk_fingerprinter_bad_fpSize(self):
        with self.assertRaisesRegexp(ValueError, "fpSize must be positive"):
            chemfp.rdkit.make_rdk_fingerprinter(fpSize=0)
        with self.assertRaisesRegexp(ValueError, "fpSize must be positive"):
            chemfp.rdkit.make_rdk_fingerprinter(fpSize=-10)

    def test_make_rdk_fingerprinter_min_path(self):
        with self.assertRaisesRegexp(ValueError, "minPath must be positive"):
            chemfp.rdkit.make_rdk_fingerprinter(minPath=0)
        with self.assertRaisesRegexp(ValueError, "minPath must be positive"):
            chemfp.rdkit.make_rdk_fingerprinter(monPath=-3)

    def test_make_rdk_fingerprinter_max_path(self):
        chemfp.rdkit.make_rdk_fingerprinter(minPath=2, maxPath=2)
        with self.assertRaisesRegexp(ValueError, "maxPath must not be smaller than minPath"):
            chemfp.rdkit.make_rdk_fingerprinter(minPath=3, maxPath=2)

    def test_make_rdk_fingerprinter_min_path(self):
        with self.assertRaisesRegexp(ValueError, "nBitsPerHash must be positive"):
            chemfp.rdkit.make_rdk_fingerprinter(nBitsPerHash=0)
        with self.assertRaisesRegexp(ValueError, "nBitsPerHash must be positive"):
            chemfp.rdkit.make_rdk_fingerprinter(nBitsPerHash=-1)


    def test_make_morgan_fingerprinter(self):
        chemfp.rdkit.make_morgan_fingerprinter()
        
    def test_make_morgan_fingerprinter_bad_fpSize(self):
        with self.assertRaisesRegexp(ValueError, "fpSize must be positive"):
            chemfp.rdkit.make_morgan_fingerprinter(fpSize=0)
        with self.assertRaisesRegexp(ValueError, "fpSize must be positive"):
            chemfp.rdkit.make_morgan_fingerprinter(fpSize=-10)

    def test_make_morgan_fingerprinter_bad_radius(self):
        with self.assertRaisesRegexp(ValueError, "radius must be positive or zero"):
            chemfp.rdkit.make_morgan_fingerprinter(radius=-1)
        with self.assertRaisesRegexp(ValueError, "radius must be positive or zero"):
            chemfp.rdkit.make_morgan_fingerprinter(radius=-10)

    
TestInternals = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestInternals)

if not skip_rdkit and Chem is not None:
    TRP_MOL = Chem.MolFromMolBlock(TRP)

def bitvect_to_fp(bitvect, offset=0):
    data = [0] * ((len(bitvect)+7) // 8)
    for bitno in bitvect.GetOnBits():
        bitno += offset
        data[bitno//8] |= 1 << (bitno % 8)
    return hex_encode("".join(map(chr, data)))
        
class TestFingerprintDefaults(unittest2.TestCase):
    def test_rdkit_fingerprint(self):
        header, output = runner.run_split([], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(Chem.RDKFingerprint(TRP_MOL))
        self.assertEqual(got_fp, expected_fp)
    def test_maccs_fingerprint(self):
        from rdkit.Chem.MACCSkeys import GenMACCSKeys
        header, output = runner.run_split(["--maccs"], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(GenMACCSKeys(TRP_MOL), -1)
        self.assertEqual(got_fp, expected_fp)
    def test_morgan_fingerprint_r0(self):
        from rdkit.Chem import rdMolDescriptors
        header, output = runner.run_split(["--morgan", "--radius", "0"], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(rdMolDescriptors.GetMorganFingerprintAsBitVect(TRP_MOL, 0))
        self.assertEqual(got_fp, expected_fp)
    def test_morgan_fingerprint_r1(self):
        from rdkit.Chem import rdMolDescriptors
        header, output = runner.run_split(["--morgan", "--radius", "1"], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(rdMolDescriptors.GetMorganFingerprintAsBitVect(TRP_MOL, 1))
        self.assertEqual(got_fp, expected_fp)
    def test_morgan_fingerprint_r2(self):
        from rdkit.Chem import rdMolDescriptors
        header, output = runner.run_split(["--morgan", "--radius", "2"], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(rdMolDescriptors.GetMorganFingerprintAsBitVect(TRP_MOL, 2))
        self.assertEqual(got_fp, expected_fp)
    def test_torsion_fingerprint(self):
        from rdkit.Chem import rdMolDescriptors
        header, output = runner.run_split(["--torsion"], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(rdMolDescriptors.GetHashedTopologicalTorsionFingerprintAsBitVect(TRP_MOL))
        self.assertEqual(got_fp, expected_fp)
    def test_atom_pair_fingerprint(self):
        from rdkit.Chem import rdMolDescriptors
        header, output = runner.run_split(["--pairs"], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(rdMolDescriptors.GetHashedAtomPairFingerprintAsBitVect(TRP_MOL))
        self.assertEqual(got_fp, expected_fp)
    def test_pattern_fingerprint(self):
        header, output = runner.run_split(["--pattern"], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(Chem.PatternFingerprint(TRP_MOL))
        self.assertEqual(got_fp, expected_fp)

    @unittest2.skipIf(skip_rdkit or not chemfp.rdkit.HAS_AVALON, "RDKit not compiled for Avalon fingerprints")
    def test_avalon_fingerprint(self):
        from rdkit.Avalon import pyAvalonTools
        header, output = runner.run_split(["--avalon"], source=TRP_SDF)
        got_fp, id = output[0].split()
        expected_fp = bitvect_to_fp(pyAvalonTools.GetAvalonFP(TRP_MOL))
        self.assertEqual(got_fp, expected_fp)
        
TestFingerprintDefaults = unittest2.skipIf(skip_rdkit, "RDKit not installed")(TestFingerprintDefaults)

@unittest2.skipUnless(skip_rdkit, "RDKit installed - can't check for missing RDKit")
class TestMissingRDKitModule(unittest2.TestCase):
    def test_rdkit2fps(self):
        from chemfp import commandline
        try:
            commandline.run_rdkit2fps()
        except SystemExit as err:
            result = str(err)
            self.assertIn("Cannot run rdkit2fps: ", result)
            
            if "Library not loaded: libRDKitRDBoost" in result:
                pass
            else:
                self.assertIn(result, [
                    "Cannot run rdkit2fps: It appears that RDKit is not installed: No module named 'rdkit'",
                    "Cannot run rdkit2fps: It appears that RDKit is not installed: No module named rdkit.Chem",
                    ])
        else:
            self.assertTrue(0, "RDKit ran, but it's not installed?")

if __name__ == "__main__":
    unittest2.main()

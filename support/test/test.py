#!/usr/bin/env python

import unittest
import sys
import os
import subprocess
import RMF

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                      'scripts'))
os.chdir(TOPDIR)

class Tests(unittest.TestCase):
    def test_simple(self):
        """Test the simple modeling script"""
        p = subprocess.check_call([sys.executable, "pbc_simple.py"])
        self._check_rmf('pbc_simple.rmf', nframes=1001)

    def test_patches(self):
        """Test the patches modeling script"""
        p = subprocess.check_call([sys.executable, "pbc_patches.py"])
        self._check_rmf('pbc_patches.py.rmf', nframes=1001)

    def test_interacting_patches(self):
        """Test the interacting_patches modeling script"""
        p = subprocess.check_call([sys.executable,
                                   "pbc_interacting_patches.py"])
        self._check_rmf('pbc_interacting_patches.py.rmf', nframes=1001)

    def _check_rmf(self, fname, nframes):
        rh = RMF.open_rmf_file_read_only(fname)
        self.assertEqual(rh.get_number_of_frames(), nframes)


if __name__ == '__main__':
    unittest.main()

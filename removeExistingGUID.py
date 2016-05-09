#!/usr/bin/env python

import ROOT
import sys, os

def _run():
    inFile = sys.argv[1]

    # check if the input file is indeed a ROOT file
    _sanity_check(inFile, ".root", 1)

    # check for existing GUID and remove it
    fileHandle = ROOT.TFile.Open(inFile,"UPDATE")
    if fileHandle.Get('fileGUID;1'):
        print("ROOT calibration file already has a GUID assigned.")
        fileHandle.Delete('fileGUID;1')
        fileHandle.Write()
        print("Existing GUID was removed.")
    fileHandle.Close()

def _sanity_check(file_name, string_end, n):
   if not file_name.endswith(string_end):
       raise NameError("Input file does not match expected file format. It should be a ROOT file with file extension ", string_end)
       sys.exit(n)

if __name__ == '__main__':
    _run()

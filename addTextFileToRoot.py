#!/usr/bin/env python

"""
Add a text file to a ROOT file
"""

import ROOT
import sys
import argparse

def _run():
    args = _get_args()

    if args.input_file.endswith(".root"):
        print "ERROR: Input file should be text format, e.g. JSON or YAML."
        sys.exit(1)

    with open(args.input_file,'r') as fp:
        config_str = fp.read()
    root_file = args.root_file or args.input_file.rsplit(".",1)[0]+".root"

    outHandle = ROOT.TFile.Open(root_file,"RECREATE")
    for i in args.jet_collection:
        cal_dir_name = '{}/{}'.format(args.tagger, i)
        outHandle.mkdir(cal_dir_name)
        outHandle.cd(cal_dir_name)
        ROOT_str_name = ROOT.TObjString(str(config_str))
        ROOT_str_name.Write(args.entry_name)
        outHandle.Write()
    outHandle.Close()

def _get_args():
    help_input_file = "Input text file"
    help_jet_collection = "Jet collections for which the string will be added (default: %(default)s). Other jet collections like e.g. AntiKt10LCTopo or AntiKt3PV0 can be added as well. Just remember to include \
them in your job options later when you want to run Athena."
    d = '(default: %(default)s)'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", type=str,
                        help=help_input_file)
    parser.add_argument('-r', '--root-file', nargs='?')
    parser.add_argument('-t', '--tagger', default='DL1', help=d)
    parser.add_argument('-n', '--entry-name',
                        default="net_configuration", help=d)
    parser.add_argument("-jc", "--jet_collection", type=str, nargs='+',
                        default=["AntiKt4EMTopo", "AntiKt4LCTopo"],
                        help=help_jet_collection)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbosity", type=int, choices=[0,1],
                       help="increase output verbosity")
    group.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()
    if args.quiet:
        pass
    else:
        if args.verbosity == 1:
            print "The jet collections"
            for i in args.jet_collection:
                print "   ", i
            print "will be added to the ROOT calibration file."
        elif args.verbosity == 0:
            print "Jet collections:"
            for i in args.jet_collection:
                print "  ", i
    return args

if __name__ == '__main__':
    _run()

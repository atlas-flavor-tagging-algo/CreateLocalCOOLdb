import ROOT
import sys
import argparse

def _run():
    args = _get_args()

    if args.input_file.endswith(".root"):
        print "ERROR: Input file does not match expected format, should be any text format, e.g. JSON or YAML."
        sys.exit(1)

    with open(args.input_file,'r') as fp:
        config_str = fp.read()

    outHandle = ROOT.TFile.Open(args.input_file.rsplit(".",1)[0]+".root","RECREATE")
    for i in args.jet_collection:
        outHandle.mkdir("DL1/"+i)
        outHandle.cd("DL1/"+i)
        ROOT_str_name = ROOT.TObjString(str(config_str))
        ROOT_str_name.Write("net_configuration")
        outHandle.Write()
    outHandle.Close()

def _get_args():
    help_input_file = "Input file in JSON format using the same conventions as required by Dan's lightweight neural network client (default: %(default)s)."
    help_jet_collection = "Jet collections for which the string will be added (default: %(default)s). Other jet collections like e.g. AntiKt10LCTopo or AntiKt3PV0 can be added as well. Just remember to include \
them in your job options later when you want to run Athena."
    parser = argparse.ArgumentParser(description="Showcase the use of argparse on the test case of adding a NN configuration string to a ROOT file for different jet collections.")
    parser.add_argument("input_file", type=str, default="NNconfig.json",
                        help=help_input_file)
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

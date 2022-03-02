from bin.NtupleDataFormat import Ntuple
import sys

def main():
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    gen_weight = 0
    for event in ntuple:
        gen_weight += event.genweight()
    print "Total events       is: {}".format(event.nevents())
    print "genweight addition is: {}".format(gen_weight)

if __name__ == "__main__":
    main()

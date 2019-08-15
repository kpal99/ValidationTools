# import math
# import collections

import ROOT
import numpy as np
import pandas as pd
import root_numpy as rnp


class _Collection(object):
    """Adaptor class representing a collection of objects.

    Concrete collection classes should inherit from this class.

    """

    def __init__(self, tree, sizeBranch, objclass, prefix):
        """Constructor.

        Arguments:
        tree        -- TTree object
        sizeBranch  -- Name of the branch to be used in size()
        objclass    -- Class to be used for the objects in __getitem__()
        """
        super(_Collection, self).__init__()
        self._tree = tree
        self._sizeBranch = sizeBranch
        self._objclass = objclass
        self._prefix = prefix
    def size(self):
        """Number of objects in the collection."""
        return len(getattr(self._tree, self._sizeBranch))

    def __len__(self):
        """Number of objects in the collection."""
        return self.size()

    def __getitem__(self, index):
        """Get object 'index' in the collection."""
        return self._objclass(self._tree, index, self._prefix)

    def __iter__(self):
        """Returns generator for the objects."""
        for index in range(self.size()):
            yield self._objclass(self._tree, index, self._prefix)


class _Object(object):
    """Adaptor class representing a single object in a collection.

    The member variables of the object are obtained from the branches
    with common prefix and a given index.

    Concrete object classes should inherit from this class.
    """

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree   -- TTree object
        index  -- Index for this object
        prefix -- Prefix of the branchs
        """
        super(_Object, self).__init__()
        self._tree = tree
        self._index = int(index)
        self._prefix = prefix

    def __getattr__(self, attr):
        """Return object member variable.

        'attr' is translated as a branch in the TTree (<prefix>_<attr>).
        """
        self._checkIsValid()
        val = getattr(self._tree, self._prefix + "_" + attr)[self._index]
        return lambda: val

    def _checkIsValid(self):
        """Raise an exception if the object index is not valid."""
        if not self.isValid():
            raise Exception("%s is not valid" % self.__class__.__name__)

    def isValid(self):
        """Check if object index is valid."""
        return self._index != -1

    def index(self):
        """Return object index."""
        return self._index


##########
class Ntuple(object):
    """Class abstracting the whole ntuple/TTree.

    Main benefit is to provide nice interface for
    - iterating over events
    - querying whether attribute information exists

    Note that to iteratate over the evets with zip(), you should use
    itertools.izip() instead.
    """

    def __init__(self, fileName, tree="myana/mytree"):
        """Constructor.

        Arguments:
        fileName -- String for path to the ROOT file
        tree     -- Name of the TTree object inside the ROOT file (default: 'myana/mytree')
        """
        super(Ntuple, self).__init__()
        self._file = ROOT.TFile.Open(fileName)
        self._tree = self._file.Get(tree)
        self._entries = self._tree.GetEntriesFast()

    def file(self):
        return self._file

    def tree(self):
        return self._tree

    def nevents(self):
        return self._entries

    def __iter__(self):
        """Returns generator for iterating over TTree entries (events)

        Generator returns Event objects.

        """
        for jentry in range(self._entries):
            # get the next tree in the chain and verify
            ientry = self._tree.LoadTree(jentry)
            if ientry < 0:
                break
            # copy next entry into memory and verify
            nb = self._tree.GetEntry(jentry)
            if nb <= 0:
                continue

            yield Event(self._tree, jentry)

    def getEvent(self, index):
        """Returns Event for a given index"""
        ientry = self._tree.LoadTree(index)
        if ientry < 0:
            return None
        nb = self._tree.GetEntry(ientry)  # ientry or jentry?
        if nb <= 0:
            None

        return Event(self._tree, ientry)  # ientry of jentry?


##########
class Event(object):
    """Class abstracting a single event.

    Main benefit is to provide nice interface to get various objects
    or collections of objects.
    """

    def __init__(self, tree, entry):
        """Constructor.

        Arguments:
        tree  -- TTree object
        entry -- Entry number in the tree
        """
        super(Event, self).__init__()
        self._tree = tree
        self._entry = entry

    def entry(self):
        return self._entry

    def event(self):
        """Returns event number."""
        return self._tree.event

    def lumi(self):
        """Returns lumisection number."""
        return self._tree.lumi

    def run(self):
        """Returns run number."""
        return self._tree.run

    def eventId(self):
        """Returns (run, lumi, event) tuple."""
        return (self._tree.run, self._tree.lumi, self._tree.event)

    def eventIdStr(self):
        """Returns 'run:lumi:event' string."""
        return "%d:%d:%d" % self.eventId()

    def genparticles(self, prefix="genpart"):
        """Returns generator particles object."""
        return GenParticles(self._tree, prefix)
  
    def genjets(self, prefix="genjet"):
        """Returns GenJet object."""
        return GenJets(self._tree, prefix)

    def genjetsAK8(self, prefix="genjetAK8"):
        """Returns GenJetAK8 object."""
        return GenJetsAK8(self._tree, prefix)

    def electrons(self, prefix="elec"):
        """Returns electron object."""
        return Electrons(self._tree, prefix)

    def gammas(self, prefix="gamma"):
        """Returns photon object."""
        return Gammas(self._tree, prefix)

    def muons(self, prefix="muon"):
        """Returns muon object."""
        return Muons(self._tree, prefix)
    
    def jets(self, prefix="jet"):
        """Returns Jet object."""
        return Jets(self._tree, prefix)

    def jetsAK8(self, prefix="jetAK8"):
        """Returns JetAK8 object."""
        return JetsAK8(self._tree, prefix)

    def taus(self, prefix="tau"):
        """Returns Tau object."""
        return Taus(self._tree, prefix)

    def mets(self, prefix="met"):
        """Returns MET object."""
        return Mets(self._tree, prefix)


    def getDataFrame(self, prefix):
        branches = [br.GetName() for br in self._tree.GetListOfBranches() if br.GetName().startswith(prefix+'_')]
        names = ['_'.join(br.split('_')[1:]) for br in branches]
        nd_array = rnp.tree2array(self._tree, branches=branches, start=self._entry, stop=self._entry+1)
        df = pd.DataFrame()
        for idx in range(0, len(branches)):
            df[names[idx]] = nd_array[branches[idx]][0]
        return df

##########
class GenParticle(_Object):
    """Class representing a GenParticle."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the GenParticle
        prefix -- TBranch prefix
        """
        super(GenParticle, self).__init__(tree, index, prefix)


class GenParticles(_Collection):
    """Class presenting a collection of GenParticles."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(GenParticles, self).__init__(tree, prefix + "_pt", GenParticle, prefix)

##########
class GenJet(_Object):
    """Class representing a GenJet."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the GenJet
        prefix -- TBranch prefix
        """
        super(GenJet, self).__init__(tree, index, prefix)


class GenJets(_Collection):
    """Class presenting a collection of GenJets."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(GenJets, self).__init__(tree, prefix + "_pt", GenJet, prefix)

class GenJetAK8(_Object):
    """Class representing a GenJetAK8."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the GenJetAK8
        prefix -- TBranch prefix
        """
        super(GenJetAK8, self).__init__(tree, index, prefix)


class GenJetsAK8(_Collection):
    """Class presenting a collection of GenJetsAK8."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(GenJetsAK8, self).__init__(tree, prefix + "_pt", GenJetAK8, prefix)



##########
class Gamma(_Object):
    """Class representing a Gamma."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the Gamma
        prefix -- TBranch prefix
        """
        super(Gamma, self).__init__(tree, index, prefix)


class Gammas(_Collection):
    """Class presenting a collection of Gammas."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(Gammas, self).__init__(tree, prefix + "_pt", GenParticle, prefix)

##########
class Electron(_Object):
    """Class representing a Electron."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the Electron
        prefix -- TBranch prefix
        """
        super(Electron, self).__init__(tree, index, prefix)


class Electrons(_Collection):
    """Class presenting a collection of Electrons."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(Electrons, self).__init__(tree, prefix + "_pt", Electron, prefix)

##########
class Muon(_Object):
    """Class representing a Muon."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the GenParticle
        prefix -- TBranch prefix
        """
        super(Muon, self).__init__(tree, index, prefix)


class Muons(_Collection):
    """Class presenting a collection of Muons."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(Muons, self).__init__(tree, prefix + "_pt", Muon, prefix)

##########
class Tau(_Object):
    """Class representing a Tau."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the Tau
        prefix -- TBranch prefix
        """
        super(Tau, self).__init__(tree, index, prefix)


class Taus(_Collection):
    """Class presenting a collection of Taus."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(Taus, self).__init__(tree, prefix + "_pt", Tau, prefix)

##########
class Jet(_Object):
    """Class representing a Jet."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the Jet
        prefix -- TBranch prefix
        """
        super(Jet, self).__init__(tree, index, prefix)


class Jets(_Collection):
    """Class presenting a collection of Jets."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(Jets, self).__init__(tree, prefix + "_pt", Jet, prefix)


class JetAK8(_Object):
    """Class representing a JetAK8."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the JetAK8
        prefix -- TBranch prefix
        """
        super(JetAK8, self).__init__(tree, index, prefix)


class JetsAK8(_Collection):
    """Class presenting a collection of JetsAK8."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(JetsAK8, self).__init__(tree, prefix + "_pt", JetAK8, prefix)


##########
class Met(_Object):
    """Class representing a Met."""

    def __init__(self, tree, index, prefix):
        """Constructor.

        Arguments:
        tree  -- TTree object
        index -- Index of the Met
        prefix -- TBranch prefix
        """
        super(Met, self).__init__(tree, index, prefix)


class Mets(_Collection):
    """Class presenting a collection of Mets."""

    def __init__(self, tree, prefix):
        """Constructor.

        Arguments:
        tree -- TTree object
        prefix -- TBranch prefix
        """
        # self.prefix = prefix
        super(Mets, self).__init__(tree, prefix + "_pt", Met, prefix)


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
        return int(getattr(self._tree, self._sizeBranch).size())

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

    def __init__(self, fileName, tree="myana/"):
        """Constructor.

        Arguments:
        fileName -- String for path to the ROOT file
        tree     -- Name of the TTree object inside the ROOT file (default: 'ana/hgc')
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

    def genParticles(self, prefix="genpart"):
        """Returns generator particles object."""
        return GenParticles(self._tree, prefix)

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

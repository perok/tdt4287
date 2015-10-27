from algorithms.suffixtree.SuffixTree import SuffixTree
from algorithms.suffixtree.SuffixGrapher import Grapher

from contextlib import contextmanager
from timeit import default_timer
from timeit import timeit

@contextmanager
def elapsed_timer():
    """
    Timer from http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
    """
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

def create_gst_on_file(filename, gprint=False):
    """
    Opens a file and create a suffix tree on every string
    """
    st = SuffixTree()

    print "Opening file \"{0}\".".format(filename)
    time_start = timeit()

    with open(filename) as text_file:
        i = -1
        for line in text_file:
            st.add_string(line.strip())#.strip())
            i += 1

            if i % 100000 == 0:
                print "\tProcessed {0} elements".format(i)

    if gprint:
        g = Grapher(st)
        g.createGraphviz()

    print "Suffix tree for \"{0}\" complete in {1} seconds".format(filename, timeit() - time_start)

    return st

def generate_strings(filename):
    """
    Generator for each string seperated by "\n" in filename.
    """
    st = SuffixTree()

    with open(filename) as text_file:
        for line in text_file:
            yield line.strip()

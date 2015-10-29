#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A common strategy for reducing sequencing costs when sequencing multiple samples
# is to use a specific 3’ adapter sequence (barcode) per sample, mix all sample libraries
# and run a single sequencing reaction, and then use the sample-specific adapter
# sequence (barcode) to identify (de-multiplex) which sample any given sequence
# belongs to. The file Multiplexed.gz contains the results of such a multiplex
# sequencing experiment. Your tasks are (1) to identify the barcodes (3’ adapters) used
# and thereby how many samples were multiplexed, (2) identify how many sequences
# that were sequenced from each sample, and (3) identify the sequence length
# distribution within each sample. What is the most frequently occurring sequence
# within each sample?
from algorithms.suffixtree.SuffixTree import SuffixTree
import Utility

filename = "dataset/Multiplexed"
#suffix_tree = Utility.create_gst_on_file(filename, strip=True)

# suffix_tree = SuffixTree()
# suffix_tree.add_string("ABABC")
# suffix_tree.add_string("BABCABC")
# suffix_tree.add_string("ABCBABC")

#Utility.count_and_show_suffixes(suffix_tree)
#exit(0)
# Task 1
# TODO Identify 3' adapter barcodes
# TODO How many samples were multiplexed?
import re
longest = {}
total = 0
with open("dataset/task4_fake.txt") as text_file:
    for line in text_file:
        total += 1
        l = line.strip()
        count, label = l.split(": ")

        found = False

        if len(label) < 15:
            continue


        for eLabel, eCount in longest.iteritems():
            print label, "AGAINST", eLabel
            if len(label) == len(eLabel):
                ## Same length, cannot be equal
                print "Equal", label, eLabel
                continue
            elif len(label) > len(eLabel):
                if eLabel in label:
                    print label, "better than", eLabel
                    found = True
                    c = eCount if eCount > count else count
                    del longest[eLabel]
                    longest[label] = c
            else:
                if label in eLabel:
                    print eLabel, "better than", label
                    found = True
                    c = eCount if eCount > count else count
                    longest[eLabel] = c

        if not found:
            longest[label] = count

sortedSuffixes = sorted(longest.items(), key=lambda x: x[1])

for (key, value) in sortedSuffixes:
    print "{0}: {1}".format(value, key)

sortedSuffixes = sorted(longest.items(), key=lambda x: len(x[0]))
print "LENGTH SORT"
for (key, value) in sortedSuffixes:
    print "{0}:\t{1}".format(value, key)
print "{0} / {1}".format(len(longest), total)


# SECOND PASS
exit()
from itertools import izip_longest

best = {}
total = 0
for (label, count) in sortedSuffixes:
    total += 1

    found = False

    for eLabel, eCount in best.iteritems():
        print label, "AGAINST", eLabel

        # if len(label) == len(eLabel):
        #     ## Same length, cannot be equal
        #     print "Equal", label, eLabel
        #
        #     continue
        if len(label) > len(eLabel):
            print "Check", label[len(label) - len(eLabel) - 1:], eLabel
            err = sum(c1!=c2 for c1,c2 in izip_longest(label[len(label) - len(eLabel) - 1:], eLabel))
            print err
            if err < 3:
                found = True
                c = eCount if eCount > count else count
                del best[eLabel]
                best[label] = c
        elif len(label) < len(eLabel):
            err = sum(c1!=c2 for c1,c2 in izip_longest(eLabel[len(eLabel) - len(label) - 1:], label))
            print err
            if err < 3:
                found = True
                c = eCount if eCount > count else count
                best[eLabel] = c

    if not found:
        best[label] = count

sortedSuffixes = sorted(best.items(), key=lambda x: x[1])

for (key, value) in sortedSuffixes:
    print "{0}: {1}".format(value, key)

sortedSuffixes = sorted(longest.items(), key=lambda x: len(x[0]))
print "HAMMING FILTER"
for (key, value) in sortedSuffixes:
    print "{0}:\t{1}".format(value, key)
print "{0} / {1}".format(len(longest), total)

# Task 2
# TODO How many sequences for each barcode?



# Task 3
# TODO Sequence length distribution in each barcode sample
# TODO What is the most frequently occuring sequence within each sample?

try:
    from IPython import embed
except ImportError:
    print "Install IPython.. doh.. nut"
    exit(1)
embed()

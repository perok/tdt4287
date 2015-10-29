from algorithms.suffixtree.SuffixTree import SuffixTree

def hamming_distance(s1, s2):
    """
    Return the Hamming distance between equal-length sequences
    """
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

#Info for second task
adaptersequence = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"
filename = "s_3_sequence_1M.txt"
number_of_matches = 0
length_distribution = {}

#Init suffixtree
st = SuffixTree()

#Reverse adaptersequence to create prefixtree
reversed_adaptersequence = adaptersequence[::-1]
st.add_string(reversed_adaptersequence)

#Loop through the sequences in the file
f = open(filename, "r")
for line in f:
    #Remove whitespaces and reverse line
    line = line.strip()
    reversed_line = line[::-1]
    #Get longest suffix-prefix match for given string
    longest_match = st.find_prefixmatch_nr(reversed_line, st.root, 0.25)
    #Check number of matches
    length_match = len(longest_match)
    if length_match > 0:
        number_of_matches += 1
        if number_of_matches % 10000 == 0:
            print number_of_matches


    
print "Number of matches: " + str(number_of_matches)

from algorithms.suffixtree.SuffixTree import SuffixTree

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
    #Calculate number of mistakes allowed
    error_limit = len(reversed_line)*0.1
    #Get longest suffix-prefix match for given string
    longest_match = st.find_prefixmatch(reversed_line, st.root, error_limit)
    #Check number of matches
    length_match = len(longest_match)
    if length_match > 0:
        number_of_matches += 1
        print "Longest match found: " + longest_match[::-1]
        length_rest = len(reversed_line.replace(longest_match, '', 1))
    if length_rest in length_distribution:
        length_distribution[length_rest] += 1
    else:
        length_distribution[length_rest] = 1
    
print "Number of matches: " + str(number_of_matches)
print "Length distribution: "
print length_distribution
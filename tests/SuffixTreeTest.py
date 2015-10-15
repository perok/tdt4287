    def test_empty_string(self):
        st = SuffixTree('')
        assert st.find_substring('not there') is -1
        assert st.find_substring(''), -1)
        assert not st.has_substring('not there')
        assert not st.has_substring('')
        
    def test_repeated_string(self):
        st = SuffixTree("aaa")
        assert st.find_substring('a') is 0
        assert st.find_substring('aa') is 0
        assert st.find_substring('aaa') is 0
        assert st.find_substring('b') is -1
        assert st.has_substring('a')
        assert st.has_substring('aa')
        assert st.has_substring('aaa')
        
        assert not st.has_substring('aaaa')
        assert not st.has_substring('b')
        #case sensitive by default
        assert not st.has_substring('A')
        

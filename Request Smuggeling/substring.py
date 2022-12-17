

# uniqueChars(): converting str() into set() removes char duplication, resuting in len() differnces that can be measured
def uniqueChars(string):
    return len(set(string)) == len(string)

def bruteSolution(string):
    size = len(string)
    max_len = 0
    result_string = ""
    # Creating substrings

    for i in range(size):
        for j in range(i, size):
            # A substring is from i - j
            # String Slicing is also an O(M) complexity where M is substring size
            substring = string[i : j+1]

            if uniqueChars(substring):
                # substring contains only unique characters
                if(len(substring) > max_len):
                    result_string = substring
                    max_len = len(substring)

    print(result_string)

string = 'abcdabc'
bruteSolution(string)

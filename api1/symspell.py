import pkg_resources
from symspellpy import SymSpell, Verbosity

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
bigram_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)

# lookup suggestions for multi-word input strings (supports compound
# splitting & merging)
filePath="D:\BTP-2\\api1\\inputFinal.txt"
f = open(filePath).read()
file2=open("outputSymSpellPy.txt","w")

for sentence in f.split('.'):
    input_term = sentence
    # max edit distance per lookup (per single word, not per whole input string)
    suggestions = sym_spell.lookup_compound(input_term, max_edit_distance=2)
    # display suggestion term, edit distance, and term frequency
    for suggestion in suggestions:
        # for part in suggestion:
        part = str(suggestion.term)
        print(part)
        file2.write(part)
    file2.write('. ')
    
file2.close()
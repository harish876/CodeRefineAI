from collections import Counter
from nltk.util import ngrams

# 1. Import CrystalBLEU
from crystalbleu import corpus_bleu

# 2. Extract trivially shared n-grams
k = 500


# <tokenized_corpus> is a list of strings
# Extract all n-grams of length 1-4
all_ngrams = []
for n in range(1, 5):
    all_ngrams.extend(list(ngrams(tokenized_corpus, n)))
    
# Calculate frequencies of all n-grams
frequencies = Counter(all_ngrams)
trivially_shared_ngrams = dict(frequencies.most_common(k))

# 3. Calculate CrystalBLEU
reference = "def sum ( first , second ) :\n return second + first"
candidate = "def add ( a , b ) :\n return a + b"
crystalBLEU_score = corpus_bleu([reference], [candidate], ignoring=trivially_shared_ngrams)
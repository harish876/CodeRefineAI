from collections import Counter
from typing import List
from nltk.util import ngrams
import re
from pygments.lexers.python import PythonLexer
from crystalbleu import corpus_bleu,sentence_bleu


prediction = "def add ( a , b ) :\n return a + b"
reference = "def sum ( first , second ) :\n return second + first"
lexer = PythonLexer()
tokens = list(lexer.get_tokens(prediction))
print(tokens)

# 2. Extract trivially shared n-grams
k = 500

hypothesis1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
            'ensures', 'that', 'the', 'military', 'always',
           'obeys', 'the', 'commands', 'of', 'the', 'party']

hypothesis2 = ['It', 'is', 'to', 'insure', 'the', 'troops',
          'forever', 'hearing', 'the', 'activity', 'guidebook',
       'that', 'party', 'direct']

reference1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
           'ensures', 'that', 'the', 'military', 'will', 'forever',
          'heed', 'Party', 'commands']

reference2 = ['It', 'is', 'the', 'guiding', 'principle', 'which',
            'guarantees', 'the', 'military', 'forces', 'always',
            'being', 'under', 'the', 'command', 'of', 'the',
            'Party']

reference3 = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
             'army', 'always', 'to', 'heed', 'the', 'directions',
           'of', 'the', 'party']

crystalBLEU_score = sentence_bleu([reference1, reference2, reference3], hypothesis1)
print(f"CrystalBLEU score: {crystalBLEU_score}")
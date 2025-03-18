from codebleu import calc_codebleu

prediction = "def add ( a , b ) :\n return a + b"
reference = "def sum ( first , second ) :\n return second + first"

result = calc_codebleu(
    [reference], 
    [prediction], 
    lang="python",
    weights=(0.25, 0.25, 0.25, 0.25), 
    tokenizer=None)

print(result)
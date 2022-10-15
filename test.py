from search import TaiGiTranslator

test_cases = None

try:
    with open('chinese.txt', 'r', encoding='utf8') as f:
        test_cases = f.readlines()
        test_cases = [x.strip() for x in test_cases]
except Exception as e:
    print("Error:",  e)
    exit(1)

translator = TaiGiTranslator()
cands = translator.batch_translate(test_cases)
translator.close()

with open('taiwanese.txt', 'w', encoding='utf8') as f:
    for cand in cands:
        f.write(f'{cand[0]}\t{cand[1]}\n')

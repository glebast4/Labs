import re
def func(file):
    dict = {'0':'ноль','1':'один','2':'два','3':'три','4':'четыре','5':'пять','6':'шесть','7':'семь','8':'восемь','9':'девять'}
    with open(file) as f:
        while block := f.readline():
            for t in block.split():
                if re.match(r'^[1-9]\d*$', t) and all(int(t[i])%2 != int(t[i+1])%2 for i in range(len(t)-1)):
                    print(f'{t}: мин = {dict[min(t)]}, макс = {dict[max(t)]}')
func("input.txt")

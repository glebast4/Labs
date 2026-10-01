def func(file, bs = 1024):
    dict = {'0':'ноль','1':'один','2':'два','3':'три','4':'четыре','5':'пять','6':'шесть','7':'семь','8':'восемь','9':'девять'}
    b = ''
    with open(file) as f:
        while block := f.read(bs):
            b += block
            while ' ' in b:
                t, b = b.split(' ', 1)
                if t.isdigit() and t[0] != '0' and all(int(t[i])%2 != int(t[i+1])%2 for i in range(len(t)-1)):
                    print(f'{t}: мин = {dict[min(t)]}, макс = {dict[max(t)]}')
func("input.txt")

import re
path = "aricar"
f = open(path + '/' +'CheckMate 017.pdf.txt' , 'r', encoding='utf-8')
txt = f.read()
print(txt)
a = re.search('.*?' + '\s?' + 'Bevacizumab' + '\s?' , txt)
print(a)
# h = open('new_drug.txt', encoding='utf-8')
# res = h.read().splitlines()
# print(res)
# medcine = []
# reason = []
# num = 0
# for i in res:
#     a = re.search('.*?' + '\s?' + i + '\s?' + '.*?\.', txt, re.I | re.IGNORECASE)
#     if a:
#         print(i)
#         searchtxt = a
#         print(searchtxt.group())
#         medcine.append(i)
#         reason.append(searchtxt.group())
#     print('\r' + str(num / len(res) * 100) + '%', end='')
#     num += 1

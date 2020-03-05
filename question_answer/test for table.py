import re

path = "data"
f = open(path + '/' +'CASPIAN.pdf.txt' , 'r', encoding='utf-8')
txt = f.read()


# table = re.findall('.*?' + '\s' + 'table' + '\s?' + '.*?\.', txt, re.I | re.IGNORECASE)
# chart = re.findall('.*?' + '\s' + 'chart' + '\s?' + '.*?\.', txt, re.I | re.IGNORECASE)
# # b = re.findall('table'+ '\s?' + '.*?\.', txt, re.I | re.IGNORECASE)
#
# for i,j in enumerate(table):
#     print(i,j)
# for i,j in enumerate(chart):
#     print(i,j)

# table1 = re.findall('Table' + '\s?\d' + '.*?\n.*?\.', txt,re.DOTALL)
# table2 = re.findall('.*?\(Table' + '\s? ' + '.*?\)', txt,re.I)
figure2 = re.findall('.*?\(figure' + '\s? ' + '.*?\)', txt,re.I)
# print(table1)
# print(table2)
print(figure2)
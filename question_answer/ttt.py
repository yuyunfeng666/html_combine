from pdf_to_txt import get_content
import re

con = get_content('C:/Users/云峰/PycharmProjects/testhtml/static/Bauer2020_Article_BrainPenetrationOfLorlatinibCu.pdf')
#print(con)
table = re.findall('.*?\(.*?Table' + '\s' + '.*?\)', con)
#print(table)
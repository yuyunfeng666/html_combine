# -*- coding: utf-8 -*-
# @Time    : 2020/2/7 9:46
# @Author  : Yyf
# @FileName: tttttt.py
# @Software: PyCharm
import re
test='Early censoring (>10 weeks before data cutoff) occurred in  two (1%) of 268 patients for durvalumab plus platinum– ' \
     'etoposide compared with eight (3%) of 269 patients for  platinum–etoposide. Most of these cases (nine of ten)  wer' \
     'e because of withdrawal of consent. At the time of data cutoff, 226 (84%) of 268 patients in  the durvalumab plus ' \
     'platinum–etoposide group and  233 (87%) of 269 patients in the platinum–etoposide  group had disease progression ' \
     'or died. Although  progression-free survival could not be tested for sig- nificance within the multiple-testing ' \
     'procedure at the  time of the interim analysis because of the design of  the study, an HR of 0·78 (95% CI 0·65–0·94) ' \
     'for the  comparison was recorded (figure 2C)'
test2 = '. Grade 3 or  4 adverse events occurred in 163 (62%) patients in the  durvalumab plus platinum–etoposide group and  166 (62%) patients in the platinum–etoposide group and  adverse events leading to discontinuation occurred in  25 (9%) patients in each group. The most common  grade 3 or 4 adverse events were neutropenia and  anaemia. Deaths due to adverse events of any cause  occurred in 13 (5%) patients in the durvalumab plus  platinum–etoposide group and 15 (6%) patients in the  platinum–etoposide group (table 4)'
t3 = 'The median age of the patients was 63 years. Most patients were men, had an ECOG  performance-status score of 1, had stage IV cancer, and were current or former smokers  (Table 1, and Table S1 in the Supplementary Appendix)'

table = re.search('\(table\s([1-9]).*?\)',t3,re.I).group(1)
print(table)


def a() -> str:

    a_s = 's'
    b = 's'
    return a_s+b


print(a())

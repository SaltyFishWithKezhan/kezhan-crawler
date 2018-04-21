import re

str = '(239)'
str1 = ''

re_ret = re.match('.*\((\d*)\).*', str1)
if re_ret:
    print(re_ret.group(1))
else:
    print(12333333333333333)

import re

str = '啊啊啊239啊啊啊'
str1 = ''

re_ret = re.match('.*?(\d+).*', str)
if re_ret:
    print(re_ret.group(1))

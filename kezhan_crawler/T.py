import re

str = '(51少时诵诗书)'
str1 = ''

re_ret = re.match('\((\d*).*\)', str)
if re_ret:
    print(re_ret.group(1))


test = [1,2,3,4,5]
print(test[1:-1])

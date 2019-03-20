# -*- coding: utf-8 -*-
__author__ = 'JavaEdge'

import re

# 源字符串
# line = "13236519711"
line = "13sssssssss"

# 正则匹配规则
regex_str = "(1[34578][^1]{9})"

# 匹配结果
match_obj = re.match(regex_str, line)

if match_obj:
    print(match_obj.group(1))

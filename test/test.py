# -*- coding: utf-8 -*-
__author__ = 'JavaEdge'

import re

# 源字符串
line = "XXX出生于1997年"

# 正则匹配规则
regex_str = ".*?(\d+)年"

# 匹配结果
match_obj = re.match(regex_str, line)
if match_obj:
    print(match_obj.group(1))

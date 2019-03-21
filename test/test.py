# -*- coding: utf-8 -*-
__author__ = 'JavaEdge'

import re

# 源字符串
# line = "你好"
line = "study in 家里蹲大学"

# 正则匹配规则
regex_str = ".*?([\u4E00-\u9FA5]+大学)"

# 匹配结果
match_obj = re.match(regex_str, line)
if match_obj:
    print(match_obj.group(1))

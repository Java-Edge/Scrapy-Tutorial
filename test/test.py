# -*- coding: utf-8 -*-
__author__ = 'JavaEdge'

import re

# 源字符串
line = "你ss好"

# 正则匹配规则
regex_str = "(你\S好)"

# 匹配结果
match_obj = re.match(regex_str, line)

if match_obj:
    print(match_obj.group(1))

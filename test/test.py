# -*- coding: utf-8 -*-
__author__ = 'JavaEdge'

import re

# 源字符串
line = "XXX出生于1997年6月1日"
line = "XXX出生于1997/6/1"
line = "XXX出生于1997-6-1"
line = "XXX出生于1997-06-01"
line = "XXX出生于1997-06"


# 正则匹配规则
regex_str = ".*出生于(\d{4}[年/-]\d{1,2}([月/-]\d{1,2}|[月/-]$|$))"
# regex_str = ".*出生于(\d{4}[年/-]\d{1,2}[月/-](\d{1,2}|$))"

# 匹配结果
match_obj = re.match(regex_str, line)
if match_obj:
    print(match_obj.group(1))

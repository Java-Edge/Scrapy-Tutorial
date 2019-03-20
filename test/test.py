# -*- coding: utf-8 -*-
__author__ = 'JavaEdge'

import re

line = "JavaEdge1234"

# 普通判断
# if line == "JavaEdge1234"

regex_str = "^J.*4$"

if re.match(regex_str, line):
    print("yes")

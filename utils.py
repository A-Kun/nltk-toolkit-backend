# -*- coding: utf-8 -*-
# Andrew Wang (me@andrewwang.ca)

import random

def rand_dir_name():
    result = ''
    for i in range(10):
        result += chr(random.randint(97, 122))
    return result

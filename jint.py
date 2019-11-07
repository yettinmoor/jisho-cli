#!/usr/bin/env python

import os
import jisho


while True:
    try:
        input_ = input('jisho> ').split(' ')
        if input_ == ['clear']:
            os.system('tput reset')
        else:
            jisho.main(input_)
    except (KeyboardInterrupt, EOFError):
        exit(1)

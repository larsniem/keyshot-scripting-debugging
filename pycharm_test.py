# -*- coding: utf-8 -*-
# AUTHOR Anyone
# VERSION 1.0.0
# Hello World for debugging with PyCharm (2019.2.6)

################################################################################################
# Preprare debugging
################################################################################################
import sys, os
import pydevd

root = os.path.dirname(__file__)
sys.path.append(root)
os.chdir(root)
# Fix unmappable file/s issue
pydevd.mapping_patches = {"<string>": os.path.basename(__file__)}

################################################################################################

# Debugger will stop here because suspend is set to true.
pydevd.settrace('localhost', port=15678, stdoutToServer=True, stderrToServer=True, suspend=True)

try:
    print("Hello World!")
    print("Hello Breakpoint!")
    print("Hello World again!")
except Exception as e:
    print(e)
finally:
    pydevd.stoptrace()
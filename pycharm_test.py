# -*- coding: utf-8 -*-
# AUTHOR Anyone
# VERSION 1.0.0
# Hello World for debugging with PyCharm

# Prepare environment
import pydevd

# Debugger will stop here because suspend is set to true.
pydevd.settrace('localhost', port=15678, stdoutToServer=True, stderrToServer=True, suspend=True)

print("Hello World!")
print("Hello Breakpoint!")
print("Hello World again!")
# -*- coding: utf-8 -*-
# context.py
#
# author: Christopher S. Corley

import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import swindle
import swindle.scanner as scanner
import swindle.lexer as lexer
import swindle.types as types
import swindle.lexeme as lexeme
import swindle.parser as parser
import swindle.recognizer as recognizer
from swindle.types import Types

# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import swindle
import swindle.scanner as scanner
import swindle.lexer as lexer
import swindle.types as types
import swindle.lexeme as lexeme
from swindle.types import Types
from swindle.types import KEYWORDS
from swindle.types import PUNCTUATION
from swindle.types import LITERALS_PUNC

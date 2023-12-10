"""
This module contains functions
"""

import math


FUNCS = {
    # trignometric func
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,

    # inverse trignometric func
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,

    # hyperbolic func
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,

    # inverse hyperbolic func
    'asinh': math.asinh,
    'acosh': math.acosh,
    'atanh': math.atanh,

    # logrithmic
    'log10': math.log10,
    'log2': math.log2,
    'log': math.log,

    # common roots
    'sqrt': math.sqrt,
    'cbrt': math.cbrt,

    # common functions
    'floor': math.floor,
    'ceil': math.ceil,
    'round': round,
    'max': max,
    'min': min,
    'abs': abs,
    'avg': lambda *nums: sum(nums)/len(nums),

    # special functions
    'fact': math.factorial,
}

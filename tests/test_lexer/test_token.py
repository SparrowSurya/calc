"""
Tests for module calc.lexer.token
"""

import unittest
from dataclasses import FrozenInstanceError

from calc.lexer.token import TokenType, Token


class TestTokenTypes(unittest.TestCase):
    def test_tokentype_number(self):
        self.assertIn(TokenType.NUMBER, TokenType)

    def test_tokentype_operators(self):
        self.assertIn(TokenType.PLUS, TokenType)
        self.assertIn(TokenType.MINUS, TokenType)
        self.assertIn(TokenType.MUL, TokenType)
        self.assertIn(TokenType.DIV, TokenType)
        self.assertIn(TokenType.MOD, TokenType)
        self.assertIn(TokenType.POW, TokenType)

    def test_tokentype_identifier(self):
        self.assertIn(TokenType.NAME, TokenType)

    def test_tokentype_delimiters(self):
        self.assertIn(TokenType.LPAREN, TokenType)
        self.assertIn(TokenType.RPAREN, TokenType)
        self.assertIn(TokenType.COMMA, TokenType)


class TestToken(unittest.TestCase):
    def setUp(self):
        self.tokentype = TokenType.PLUS
        self.value = "+"
        self.index = 3

    def test_creation(self):
        t = Token(TokenType.LPAREN, "(", 3)

        self.assertEqual(t.type, TokenType.LPAREN)
        self.assertEqual(t.value, "(")
        self.assertEqual(t.index, 3)
        self.assertEqual(t.end, 4)
        self.assertEqual(len(t), 1)

    def test_has_attributes(self):
        t = Token(TokenType.NAME, "hello", 4)

        attrs = ("type", "value", "index", "end", "__len__", "__repr__")

        for attr in attrs:
            self.assertTrue(hasattr(t, attr))

    def test_fail_on_empty_value(self):
        with self.assertRaises(ValueError):
            Token(self.tokentype, "", self.index)

    def test_fail_on_invalid_index(self):
        with self.assertRaises(ValueError):
            Token(self.tokentype, "**", -1)

    def test_pass_on_index_0(self):
        t = Token(self.tokentype, "**", 0)
        self.assertEqual(t.index, 0)

    def test_is_immutable(self):
        t = Token(self.tokentype, self.value, self.index)

        new_values = {
            "type": self.tokentype,
            "value": self.value,
            "index": self.index,
        }

        for attr, value in new_values.items():
            with self.assertRaises(FrozenInstanceError):
                setattr(t, attr, value)

    def test_repr(self):
        t = Token(self.tokentype, self.value, self.index)
        repr_str = t.__repr__()

        self.assertIn(str(t.type).casefold(), repr_str.casefold())
        self.assertIn(str(t.value), repr_str)
        self.assertIn(str(t.index), repr_str)

    def test_should_use_tokentype(self):
        with self.assertRaises(TypeError):
            Token("PLUS", "+", 2)

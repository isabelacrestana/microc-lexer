from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Iterator


class TokenKind(enum.Enum):
    """Classe já implementada: nomes e números não devem ser alterados."""

    EOF = -1

    IDENTIFIER = 1
    INT_LITERAL = 2
    STRING_LITERAL = 3

    KW_INT = 10
    KW_BOOL = 11
    KW_VOID = 12
    KW_TRUE = 13
    KW_FALSE = 14
    KW_IF = 15
    KW_ELSE = 16
    KW_WHILE = 17
    KW_RETURN = 18
    KW_PRINT = 19

    PLUS = 20
    MINUS = 21
    STAR = 22
    SLASH = 23
    PERCENT = 24
    LESS = 25
    LESS_EQUAL = 26
    GREATER = 27
    GREATER_EQUAL = 28
    EQUAL_EQUAL = 29
    NOT_EQUAL = 30
    LOGICAL_AND = 31
    LOGICAL_OR = 32
    LOGICAL_NOT = 33
    ASSIGN = 34

    LEFT_PAREN = 40
    RIGHT_PAREN = 41
    LEFT_BRACE = 42
    RIGHT_BRACE = 43
    COMMA = 44
    SEMICOLON = 45


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    lexeme: str
    value: int | str | bool | None
    line: int
    column: int

    def __str__(self) -> str:
        return (
            f"<{self.kind.value}, {self.kind.name}, {self.lexeme!r}, "
            f"{self.value!r}, {self.line}, {self.column}>"
        )


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"erro léxico em {self.line}:{self.column}: {self.message}"


class Lexer:
    """Converte texto-fonte MicroC em uma sequência de tokens."""

    def __init__(self, source: str):
        self.source = source
        # TODO: inicialize aqui o estado exigido por sua estratégia.
        self.position = 0
        self.length = len(source)

        self.transition_table = {

            'start': {
                'alpha': self.state_identifier,
                'digit': self.state_number,
                '+': self.state_simple_token,
                '-': self.state_simple_token,
                '/': self.state_slash,
                '*': self.state_simple_token,
                '%': self.state_simple_token,
                '<': self.state_less,
                '>': self.state_greater,
                '=': self.state_assign,
                '!': self.state_not,
                '&': self.state_and,
                '|': self.state_or,
                '(': self.state_simple_token,
                ')': self.state_simple_token,
                '"': self.state_string,
                '{': self.state_simple_token,
                '}': self.state_simple_token,
                ',': self.state_simple_token,
                ';': self.state_simple_token,
                'whitespace': self.state_whitespace,
                'EOF': self.state_EOF,
                },

            'identifier':{
                'alpha': self.state_identifier,
                'digit': self.state_identifier,
                'EOF': self.state_accept_identifier,
                'default': self.state_accept_identifier,
            },

            'digit': {
                'digit': self.state_number,
                'alpha': self.state_invalid,
                'EOF': self.state_accept_number,
                'default': self.state_accept_number,
            },

            'slash':{
                '/': self.state_comment_line,
                '*': self.state_comment_block,
                'EOF': self.state_accept,
                'default': self.state_accept,
            },

            'assign': {
                '=': self.state_equal,
                'EOF': self.state_accept,
                'default': self.state_accept,
            },

            'less':{
                '=': self.state_less_equal,
                'EOF': self.state_accept,
                'default': self.state_accept,
            },

            'greater':{
                '=': self.state_greater_equal,
                'EOF': self.state_accept,
                'default': self.state_accept,
            },

            'NOT':{
                '=': self.state_not_equal,
                'EOF': self.state_accept,
                'default': self.state_accept
            },

            'AND':{
                '&': self.state_accept,
                'EOF': self.state_invalid,
                'default': self.state_invalid,
            },

            'OR':{
                '|': self.state_accept,
                'EOF': self.state_invalid,
                'default': self.state_invalid,
            }   
        }

        self.simple_tokens = {
            '+': TokenKind.PLUS,
            '-': TokenKind.MINUS,
            '*': TokenKind.STAR,
            '%': TokenKind.PERCENT,
            '(': TokenKind.LEFT_PAREN,
            ')': TokenKind.RIGHT_PAREN,
            '{': TokenKind.LEFT_BRACE,
            '}': TokenKind.RIGHT_BRACE,
            ',': TokenKind.COMMA,
            ';': TokenKind.SEMICOLON
        }

        self.keywords = {
            "int": TokenKind.KW_INT,
            "bool": TokenKind.KW_BOOL,
            "void": TokenKind.KW_VOID,
            "true": TokenKind.KW_TRUE,
            "false": TokenKind.KW_FALSE,
            "if": TokenKind.KW_IF,
            "else": TokenKind.KW_ELSE,
            "while": TokenKind.KW_WHILE,
            "return": TokenKind.KW_RETURN,
            "print": TokenKind.KW_PRINT
        }

    def state_simple_token(self) -> Token:
        inicial_line = self.line
        inicial_column = self.column

        char = self.source[self.position]

        self.column += 1
        self.position += 1

        kind = self.simple_tokens[char]

        return Token(kind, char, None, inicial_line, inicial_column)

    def state_whitespace(self) -> None:

        return None


    def tokens(self) -> Iterator[Token]:
        """Produza todos os tokens significativos e um único EOF ao final."""
        raise NotImplementedError("implemente o analisador léxico")
        yield  # mantém este método como gerador durante o desenvolvimento

    def scan(self) -> list[Token]:

        while self.position > len(self.source):

            char = self.source[self.position]

            if char.isspace():
                self.state_whitespace(self)
            
        return list(self.tokens())


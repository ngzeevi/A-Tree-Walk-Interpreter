from token_type import TokenType
from lox_token import Token
from error_handler import ErrorHandler

from typing import List, Optional


class Scanner:
    def __init__(self, source: str) -> None:
        self._source = source
        self._tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }
        self._error_handler = ErrorHandler()
        
    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()
        
        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens     
    
    def _scan_token(self) -> None:
        c = self._advance() 
        if c == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self._add_token(TokenType.COMMA)
        elif c == ".":
            self._add_token(TokenType.DOT)
        elif c == "-":
            self._add_token(TokenType.MINUS)
        elif c == "+":
            self._add_token(TokenType.PLUS)
        elif c == ";":
            self._add_token(TokenType.SEMICOLON)
        elif c == "*":
            self._add_token(TokenType.STAR)
        elif c == "!":
            self._add_token(TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG)
        elif c == "=":
            self._add_token(TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL)
        elif c == "<":
            self._add_token(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
        elif c == ">":
            self._add_token(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
        elif c == '/':
            if self._match('/'):
                while self._peek() != '\n' and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif c in [' ', '\r', '\t']:
            pass
        elif c == '\n':
            self._line += 1
        elif c == '"':
            self._string()
        else:
            if self._is_digit(c):
                self._number()
            elif self._is_alpha(c):
                self._identifier()
            else:
                self._error_handler.error(self._line, 'Unexpected character.')
    
    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)
    
    def _advance(self) -> str:
        self._current += 1
        return self._source[self._current - 1]
    
    def _add_token(self, tkn_type: TokenType, literal: Optional[object] = None) -> None:
        text = self._source[self._start:self._current]
        self._tokens.append(Token(tkn_type, text, literal, self._line))

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        
        if self._source[self._current] != expected:
            return False
        
        self._current += 1
        return True
    
    def _peek(self) -> str:
        if self._is_at_end():
            return '\0'
        return self._source[self._current]

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '\n':
                self._line += 1
            self._advance()
        
        if self._is_at_end():
            self._error_handler.error(self._line, 'Unterminated string.')
            return
        
        # The closing "
        self._advance()
        
        # Trim the surrounding quotes
        value = self._source[self._start + 1 : self._current - 1]
        self._add_token(TokenType.STRING, value)
        
    def _is_digit(self, c: str) -> bool:
        return c >= '0' and c <= '9'
        
    def _number(self) -> None:
        while self._is_digit(self._peek()):
            self._advance()
            
        # Look for a fractional part
        if self._peek() == '.' and self._is_digit(self._peek_next()):
            # Consume the '.'
            self._advance()
            
            while self._is_digit(self._peek()):
                self._advance()
            
        self._add_token(TokenType.NUMBER, float(self._source[self._start:self._current]))
        
    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return '\0'
        return self._source[self._current + 1]
        
    def _identifier(self) -> None:
        while self._is_alpha_numeric(self._peek()):
            self._advance()
        
        text = self._source[self._start : self._current]
        if text in self._keywords:
            self._add_token(self._keywords[text])
        else:
            self._add_token(TokenType.IDENTIFIER)
        
    def _is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"       
        
    def _is_alpha_numeric(self, c: str) -> bool:
        return self._is_alpha(c) or self._is_digit(c)
        

        
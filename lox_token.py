from token_type import TokenType

class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: str, line: str) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        
    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"

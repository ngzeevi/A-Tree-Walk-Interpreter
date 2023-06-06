import expr
from expr import Expr
from lox_token import Token
from token_type import TokenType


class AstPrinter(Expr):
    def __init__(self) -> None:
        pass
    
    def main(self) -> None:
        expression = expr.Binary(
            expr.Unary(
                Token(TokenType.MINUS, '-', None, 1),
                expr.Literal(123),
            ),
            Token(TokenType.STAR, '*', None, 1),
            expr.Grouping(expr.Literal(45.67)),
        )
        
        print(self._print_expr(expression))
    
    def _print_expr(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Expr) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)
        
    def visit_grouping_expr(self, expr: Expr) -> str:
        return self._parenthesize('group', expr.expression)
    
    def visit_literal_expr(self, expr: Expr) -> str:
        return str(expr.value)

    def visit_unary_expr(self, expr: Expr) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)
    
    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        builder = '(' + name
        
        for expr in exprs:
            builder += ' '
            builder += expr.accept(self)
            
        builder += ')'
        
        return builder

if __name__ == '__main__':
    a = AstPrinter()
    a.main()

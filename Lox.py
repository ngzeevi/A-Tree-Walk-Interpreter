import sys
import argparse

from scanner import Scanner
from error_handler import ErrorHandler


class Lox:
    def __init__(self) -> None:
        self._error_handler = ErrorHandler()
    
    def main(self) -> None:
        parser = argparse.ArgumentParser(description='Lox Interpreter')
        parser.add_argument('-s', required=False)
        args = parser.parse_args()
        
        if len(sys.argv) > 2:
            print("Usage: pylox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            self._run_file(args[1])
        else:
            self._run_prompt()
        
    def _run_file(self, path: str) -> None:
        with open(path, 'r') as f:
            self._run(f.read())
        
        if self._error_handler.had_error:
            sys.exit(65)
    
    def _run_prompt(self) -> None:
        while True:
            line = input('> ')
            if not line:
                break
            self._run(line)
            self._error_handler.had_error = False
            
    def _run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        
        for token in tokens:
            print(token)
        

if __name__ == '__main__':
    lox = Lox()
    lox.main()

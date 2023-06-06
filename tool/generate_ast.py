import sys
import argparse
from typing import List, TextIO


class GenerateAst:
    def __init__(self) -> None:
        self.tab = '    '
    
    def main(self) -> None:
        parser = argparse.ArgumentParser(description='Path')
        parser.add_argument('directory', default='../')
        args = parser.parse_args()
        
        if len(sys.argv) != 2:
            print(sys.argv)
            print("\nUsage: generate_ast <output directory>")
            sys.exit(64)
        
        output_dir = sys.argv[1]
        
        self._define_ast(output_dir, 'Expr', 
                         ['Binary   = left: Expr, operator: Token, right: Expr',
                          'Grouping = expression: Expr',
                          'Literal  = value: object',
                          'Unary    = operator: Token, right: Expr'])

    def _define_ast(self, output_dir: str, base_name: str, types: List[str]) -> None:
        path = output_dir + '/' + base_name.lower() + '.py'        
        with open(path, 'w+') as writer:  
            writer.write('from abc import ABC, abstractmethod\n\n')
            writer.write('from lox_token import Token\n\n\n')
            
            writer.write(f'class {base_name}:\n')
            writer.write(f'{self.tab}pass\n\n\n')
            
            self._define_visitor(writer, base_name, types)
            
            for ast_type in types:
                class_name = ast_type.split('=')[0].strip()
                fields = ast_type.split('=')[1].strip()
                self._define_type(writer, base_name, class_name, fields)
                
    def _define_type(self, writer: TextIO, base_name: str, class_name: str, field_list: str) -> None:
        writer.write(f'\nclass {class_name}({base_name}):\n')
        writer.write(f'{self.tab}def __init__(self')
        if field_list:
            writer.write(f', {field_list}):\n')
        else:
            writer.write('):\n')
            writer.write(f'{self.tab * 2}pass\n')
        
        fields = field_list.split(', ')     
        for field in fields:
            name = field.split(':')[0].strip()
            writer.write(f'{self.tab * 2}self.{name} = {name}\n')
        
        writer.write('\n')
        writer.write(f'{self.tab}def accept(self, visitor):\n')
        writer.write(f'{self.tab * 2}return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n\n')
        

    def _define_visitor(self, writer: TextIO, base_name: str, types: List[str]) -> None:
        writer.write(f'class {base_name}Visitor(ABC):\n')
        
        for ast_type in types:
            type_name = ast_type.split('=')[0].strip()
            writer.write(f'{self.tab}@abstractmethod\n')
            writer.write(f'{self.tab}def visit_{type_name.lower()}_{base_name.lower()} (self, {type_name.lower()}: {base_name}):\n')
            writer.write(f'{self.tab * 2}pass\n\n')
            

if __name__ == '__main__':      
    c = GenerateAst()
    c.main()

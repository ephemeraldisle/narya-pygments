from pygments.lexer import RegexLexer, words
from pygments.token import *

class NaryaLexer(RegexLexer):
    name = 'Narya'
    aliases = ['narya']
    filenames = ['*.narya']

    tokens = {
        'root': [
            # Whitespace and comments
            (r'\s+', Text.Whitespace),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            
            # Keywords
            (words((
                'if', 'else', 'while', 'for', 'foreach', 'match',
                'return', 'skip', 'exit', 'repeat', 'with', 'using',
                'danger', 'public', 'private', 'protected', 'print',
                'group', 'ring', 'do', 'core', 'inner', 'outer'
            ), prefix=r'\b', suffix=r'\b'), Keyword),
            
            # Types
            (words((
                'num', 'int', 'big int', 'uint', 'big uint',
                'float', 'big float', 'text', 'char', 'string',
                'bool', 'byte', 'List', 'Dictionary', 'Array', 'Set'
            ), prefix=r'\b', suffix=r'\b'), Keyword.Type),
            
            # Operators
            (r'[+\-*/^%=<>!]=?', Operator),
            (r'[&|]{1,2}', Operator),
            (r'\.\.\.?', Operator),  # Range operators
            
            # Literals
            (r'\d+\.\d+', Number.Float),
            (r'\d+', Number.Integer),
            (r'true|false', Keyword.Constant),
            (r'"[^"]*"', String),
            (r'\'[^\']*\'', String.Interpol),
            
            # Identifiers
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),
            
            # Punctuation
            (r'[\(\)\[\]\{\},:]', Punctuation),
        ]
    }

# Entry point for Pygments
def setup(app):
    return {'version': '0.1', 'parallel_read_safe': True}
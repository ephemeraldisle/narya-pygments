from pygments.lexer import RegexLexer, words, include, bygroups
from pygments.token import *
import re

class NaryaLexer(RegexLexer):
    name = 'Narya'
    aliases = ['narya']
    filenames = ['*.narya']

    # Built-in primitive types (camelCase)
    primitive_types = (
        'num', 'int', 'big int', 'uint', 'big uint',
        'float', 'big float', 'text', 'char', 'string',
        'bool', 'byte'
    )

    # Built-in collection types (PascalCase)
    collection_types = (
        'List', 'Dictionary', 'Array', 'Set'
    )

    # Language types (camelCase)
    language_types = (
        'group', 'object', 'obj', 'action', 'act',
        'enum', 'trait'
    )

    # All type keywords combined
    type_keywords = primitive_types + collection_types + language_types

    # Control flow keywords
    flow_keywords = (
        'if', 'else', 'while', 'for', 'foreach', 'in',
        'match', 'return', 'skip', 'exit', 'repeat',
        'with', 'using', 'danger', 'do', 'print',
        'try', 'catch'
    )
    
    # Memory management keywords
    memory_keywords = (
        'core', 'inner', 'outer'
    )
    
    # Access modifiers
    access_modifiers = (
        'public', 'private', 'viewable', 'protected'
    )

    # Other keywords
    other_keywords = (
        'new', 'const', 'generic', 'operator', 'Overload'
    )

    tokens = {
        'root': [
            # Whitespace (keep at top)
            (r'\s+', Text.Whitespace),
            
            # Comments
            (r'//.*$', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline_comment'),
            
            # Modifier combinations with mandatory spaces
            (r'\b(public|private|protected|viewable)(\s+)(act)\b',
             bygroups(Keyword.Namespace, Text.Whitespace, Keyword.Type)),
            
            # Memory modifier + access modifier + type
            (r'\b(core|inner|outer)(\s+)(public|private|protected|viewable)(\s+)(\*?)(\b(?:' + 
             '|'.join(type_keywords) + r')\b)(\??)',
             bygroups(Keyword.Namespace, Text.Whitespace, 
                     Keyword.Namespace, Text.Whitespace,
                     Operator, Keyword.Type, Operator)),
            
            # Access modifier + type
            (r'\b(public|private|protected|viewable)(\s+)(\*?)(\b(?:' + 
             '|'.join(type_keywords) + r')\b)(\??)(\s+)([A-Z][a-zA-Z0-9_]*)',
             bygroups(Keyword.Namespace, Text.Whitespace, 
                     Operator, Keyword.Type, Operator, Text.Whitespace, 
                     Name.Attribute)),

            # Group/Object declarations with mandatory space
            (r'\b(group|obj|trait|enum)(\s+)([A-Z][a-zA-Z0-9_]*)',
             bygroups(Keyword.Type, Text.Whitespace, Name.Class)),

            # Type usage (should come before method calls)
            (r'\b([A-Z][a-zA-Z0-9_]*)(?=\s+[a-z][a-zA-Z0-9_]*\b)',
             Name.Class),  # Type in variable 
            
            # Add this pattern before the existing method call patterns
            # Constructor declarations
            (r'\b(public|private|protected|viewable)(\s+)([A-Z][a-zA-Z0-9_]*)(\s*)(\()',
            bygroups(Keyword.Namespace, Text.Whitespace, Name.Class, Text.Whitespace, Punctuation)),

            # Modify the field reference pattern to also catch assignments
            # Field references including assignments
            (r'\b([A-Z][a-zA-Z0-9_]*)(\s*)(=)',
            bygroups(Name.Attribute, Text.Whitespace, Operator)),




            # Method calls via dot (preserve dot)
            (r'(\.)([A-Z][a-zA-Z0-9_]*)(\s*)(\()',
             bygroups(Punctuation, Name.Function, Text.Whitespace, Punctuation)),

            # Property/Field access via dot (preserve dot)
            (r'(\.)([A-Z][a-zA-Z0-9_]*)\b',
             bygroups(Punctuation, Name.Attribute)),

            # Constructor calls or type references
            (r'\b([A-Z][a-zA-Z0-9_]*)(\s*)(\()',
             bygroups(Name.Class, Text.Whitespace, Punctuation)),

            # Remaining capitalized identifiers are treated as types
            (r'\b[A-Z][a-zA-Z0-9_]*\b', Name.Class),

            # Other keywords
            (words(other_keywords, prefix=r'\b', suffix=r'\b'),
             Keyword),

            # Flow control keywords
            (words(flow_keywords, prefix=r'\b', suffix=r'\b'),
             Keyword),

            # Built-in primitive types
            (words(primitive_types, prefix=r'\b', suffix=r'\b'),
             Keyword.Type),

            # Collection types
            (words(collection_types, prefix=r'\b', suffix=r'\b'),
             Name.Class),

            # Constants
            (r'\b[A-Z][A-Z0-9_]+\b', Name.Constant),

            # Operators
            (r'[+\-*/^%]=?', Operator),
            (r'[&|]{1,2}', Operator),
            (r'\.\.\.?', Operator),
            (r'[=<>!]=?', Operator),
            (r'[\*\?^]', Operator),
            (r'<<|>>', Operator),
            (r'\^\^|~~', Operator),

            # Numbers
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'0b[01]+', Number.Bin),
            (r'0o[0-7]+', Number.Oct),
            (r'\b\d+\.\d+([eE][+-]?\d+)?\b', Number.Float),
            (r'\b\d+\b', Number.Integer),

            # Boolean literals
            (r'\b(true|false)\b', Keyword.Constant),

            # Regular strings
            (r'"[^"]*"', String.Double),

            # Interpolated strings
            (r'\'', String.Interpol, 'interpolated_string'),

            # Local variables (camelCase)
            (r'\b[a-z][a-zA-Z0-9_]*\b', Name.Variable),

            # Punctuation
            (r'[\(\)\[\]\{\},:]', Punctuation),
        ],
        
        'multiline_comment': [
            (r'[^*/]+', Comment.Multiline),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
        
        'interpolated_string': [
            # Complex interpolation with parentheses
            (r'\.\(', String.Interpol, 'interpolation_expression'),
            # Simple interpolation with preserved dot
            (r'(\.)([A-Z][a-zA-Z0-9_]*)',
             bygroups(Punctuation, Name.Attribute)),
            # Escaped dot
            (r'\.\.', String.Escape),
            # Regular text
            (r'[^\'\.]+', String.Interpol),
            # End of string
            (r'\'', String.Interpol, '#pop'),
        ],

        'interpolation_expression': [
            (r'\)', String.Interpol, '#pop'),
            include('root'),
        ],
    }
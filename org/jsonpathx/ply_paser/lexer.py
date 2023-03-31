import ply.lex as lex

class JsonPathXLexer(object):
    '''
        An LALR-parser for JsonPathX
    '''
    
    # List of token names.   This is always required
    tokens = [
        'NUMBER',
        'NAME',
        'SIGDOT',
        'DOUDOT',
        'ALLFLD',
        'COLON',
        'COMMA',
        'LBRACKET',
        'RBRACKET',
        'QUOTE',
        'QMARK',
        'AT',
        'EQUAL',
        'NOTEQ',
        'LESST',
        'NOTGT',
        'GREAT',
        'NOTLT',
        'LPARE',
        'RPARE'
    ]

    # Regular expression rules for simple tokens
    t_SIGDOT = r'\.'
    t_DOUDOT = r'\.\.'
    t_ALLFLD = r'\*'
    t_COLON = r'\:'
    t_COMMA = r'\,'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_QUOTE = r'\"'
    t_QMARK = r'\?'
    t_AT = r'\@'
    t_EQUAL = r'\=\='
    t_NOTEQ = r'\!\='
    t_LESST = r'\<'
    t_NOTGT = r'\<\='
    t_GREAT = r'\>'
    t_NOTLT = r'\>\='
    t_LPARE = r'\('
    t_RPARE = r'\)'

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t    

    # Define a rule so we can track line numbers
    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = 'NAME'
        return t

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = r' '

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: 
                 break
             print(tok)


if __name__ == "__main__":
    # Build the lexer and try it out
    lexer = JsonPathXLexer()
    lexer.build()           # Build the lexer
    lexer.test('movie[1:10]["person"]')     # Test it

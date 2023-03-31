import ply.yacc as yacc
# from org.jsonpathx.ply_paser.lexer import JsonPathLexer
# from . import JsonPathLexer
import lexer

class JsonPathXParser(object):
    '''
        An LALR-parser for JsonPathX
    '''

    def p_jsonx(self, p):
        '''
        jsonx : expression
            | empty
        '''
        p[0] = p[1]

    def p_expression(self, p):
        '''
        expression : NAME LBRACKET expression RBRACKET
                | NAME SIGDOT NAME
                | expression LBRACKET expression RBRACKET
                | expression SIGDOT NAME
                | AT LBRACKET expression RBRACKET
                | AT SIGDOT NAME
        '''
        p[0] = ('c', p[1], p[3])

    def p_expression_filter(self, p):
        '''
        expression : QMARK LPARE condition RPARE
        '''
        p[0] = p[3]


    def p_condition_equal(self, p):
        '''
        condition : expression EQUAL expression
        '''
        p[0] = ('=', p[1], p[3])

    def p_condition_notequal(self, p):
        '''
        condition : expression NOTEQ expression
        '''
        p[0] = ('!', p[1], p[3])

    def p_condition_less(self, p):
        '''
        condition : expression LESST expression
        '''
        p[0] = ('<', p[1], p[3])

    def p_condition_notgreater(self, p):
        '''
        condition : expression NOTGT expression
        '''
        p[0] = ('l', p[1], p[3])

    def p_condition_greater(self, p):
        '''
        condition : expression GREAT expression
        '''
        p[0] = ('>', p[1], p[3])

    def p_condition_notless(self, p):
        '''
        condition : expression NOTLT expression
        '''
        p[0] = ('g', p[1], p[3])



    def p_expression_dsearch(self, p):
        '''
        expression : NAME DOUDOT NAME
                | expression DOUDOT NAME
        '''
        p[0] = ('s', p[1], p[3])

    def p_expression_list(self, p):
        '''
        expression : NUMBER COMMA NUMBER
                | expression COMMA NUMBER
        '''
        try:
            p[1].append(p[3])
        except:
            p[1] = [p[1], p[3]]
        p[0] = p[1]

    def p_expression_all(self, p):
        '''
        expression : ALLFLD
        '''
        p[0] = '*'

    def p_expression_slice(self, p):
        '''
        expression : expression COLON expression
        '''
        p[0] = (':', p[1], p[3])

    def p_expression_name(self, p):
        '''
        expression : QUOTE NAME QUOTE
        '''
        p[0] = p[2]

    def p_expression_number(self, p):
        '''
        expression : NUMBER
        '''
        p[0] = p[1]

    def p_empty(self, p):
        '''
        empty : 
        '''
        p[0] = None

    def p_error(self, p):
        print("Syntax error in input!")

    def build(self, **kwargs):
        self.lexer = lexer.JsonPathXLexer()
        self.tokens = self.lexer.tokens
        self.lexer.build() 
        self.parser = yacc.yacc(module=self, **kwargs)
        

if __name__ == "__main__":
    # Build the parser and try it out
    json_path_parser = JsonPathXParser()
    json_path_parser.build()           # Build the parser
    result = json_path_parser.parser.parse('movie[1:10]["person"]')     # Test it
    print(result)
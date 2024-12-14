from enum import Enum

class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'
   # literals
    STRING = ""
    NUMBER = '1234567890'
    IDENTIFIER = 1
    # One or two character tokens
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='
    
    # Keywords
    AND = "and"
    CLASS = "class"
    FALSE = "false"
    TRUE = "true"
    ELSE = 'else'
    FUN = 'fun' 
    FOR = 'for'
    IF = "if" 
    NIL = '0' 
    OR = 'or' 
    PRINT = 'print'  
    RETURN = '1' 
    SUPER = 'super'
    THIS = 'this'  
    VAR = 'variable' 
    WHILE = 'while'
    # End of file
    EOF = "EOF"

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.token = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "and": "AND",
            "class": "CLASS",
            "else": "ELSE",
            "false": "FALSE",
            "for": "FOR",
            "fun": "FUN",
            "if": "IF",
            "nil": "NIL",
            "or": "OR",
            "print": "PRINT",
            "return": "RETURN",
            "super": "SUPER",
            "this": "THIS",
            "true": "TRUE",
            "var": "VAR",
            "while": "WHILE",
        }

    def advance(self):
        """Consume the next character and return it."""
        char = self.source[self.current]
        self.current += 1
        return char

    def peek(self):
        """Look at the next character without consuming it."""
        if self.is_at_end():
            return '\0'  
        return self.source[self.current]
    
    def peekNext(self):
        if (self.current +1 >= len(self.source)):
            return '\0'

        return self.source[self.current + 1]
    def is_at_end(self):
        return self.current >= len(self.source)
    def isDigit(self,c):
        return c >= '0' and c <= '99'


    def add_token(self,type:TokenType, literal=None):
        text = self.source[self.start:self.current]
        token = Token(type, text, literal, self.line)
        self.tokens.append(token)

    def match(self,expected:str):
        if (self.is_at_end()): return False
        if (self.source[self.current] != expected):
            return False
        
        self.current += 1
        return True
    
    def strings(self):
        while((self.peek() != '"') and not (self.is_at_end())):
            if (self.peek() == '\n'): self.line +=1
            self.advance()

        if (self.is_at_end()):
            self.reportError(self.line,'Unterminated string.')

        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING,value)
    def numbers(self):
        while (self.isDigit(self.peek())):
            self.advance()
        if (self.peek() == '.' and self.isDigit(self.peekNext())):
            self.advance()

            while (self.isDigit(self.peek())):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while (self.peek().isalnum()) :
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text,'IDENTIFIER')

        self.add_token(token_type)

    def scan_tokens(self):
        """Main loop to scan through the source and generate tokens."""
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append({"type": "EOF", "literal": None, "line": self.line})


    def scan_token(self,c:str):
        self.c = c
        if c == "(" :
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == '.': 
            self.add_token(TokenType.DOT)
        elif c == '-': 
            self.add_token(TokenType.MINUS)
        elif c == '+': 
            self.add_token(TokenType.PLUS) 
        elif c == ';': 
            self.add_token(TokenType.SEMICOLON)
        elif c == '*': self.add_token(TokenType.STAR)
        elif c == "=" :
            if self.match('=') : self.add_token(TokenType.EQUAL_EQUAL)
            else : self.add_token(TokenType.EQUAL)
        elif c == '!' :
            if self.match('='): self.add_token(TokenType.BANG_EQUAL)
            else: self.add_token(TokenType.BANG)
        elif c == '<' :
            if self.match('=') : self.add_token(TokenType.LESS_EQUAL)
            else : self.add_token(TokenType.LESS_THAN)
        elif c == '>' :
            if self.match('=') : self.add_token(TokenType.GREATER_EQUAL)
            else : self.add_token(TokenType.GREATER)
        elif c == '/' :
            if self.match('/') : 
                while((self.peek() != '\n') and not(self.is_at_end())):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == '"' :
            self.strings()
        elif c in {' ', '\r', '\t'}:
            return
        elif c == '\n' :
            self.line +=1
        elif (self.isDigit(c)): self.numbers()
        elif (c.isalpha()) : 
            self.identifier()
        else :
            self.reportError(self.line,"unexpected character")
    
    def reportError(self,line,message):
        print(f"[Line{line}] Error:{message}")

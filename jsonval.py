import re
import sys

class Token():
    def __init__(self, name, value, position):
        self.name = name
        self.value = value
        self.position = position

    def is_opening(self): 
        """
        Returns true if token is opening bracket

        >>> Token('open_square', '[', 0).is_opening()
        True

        >>> Token('close_square', ']', 0).is_opening()
        False

        >>> Token('number', '1', 0).is_opening()
        False
        """
        
        return self.name.startswith('open')
        
    def is_closing(self): 
        """
        Returns true if token is closing bracket

        >>> Token('open_square', '[', 0).is_closing()
        False
        
        >>> Token('close_square', ']', 0).is_closing()
        True

        >>> Token('number', '1', 0).is_closing()
        False
        """

        return self.name.startswith('close')
        
    def bracket_type(self): 
        """
        Returns the bracket type

        >>> Token('open_square', '[', 0).bracket_type()
        'square'
        
        >>> Token('close_curly', ']', 0).bracket_type()
        'curly'

        >>> Token('number', '1', 0).bracket_type()
        """

        if self.is_closing() or self.is_opening():
            return self.name.split('_')[1]
        else:
            return None

    def __repr__(self):
        """
        Returns representation of Token

        >>> Token('open_square', '[', 0)
        ('open_square', '[', 0)
        """
        
        return str((self.name, self.value, self.position))

def lex(src):
    """ 
    Returns a generator of (name, value, position) tuples for a simplified 
    JSON document.

    Examples:

    >>> next(lex('true'))
    ('boolean', 'true', 0)

    >>> next(lex('false'))
    ('boolean', 'false', 0)

    >>> next(lex('5'))
    ('number', '5', 0)

    >>> next(lex('3.14'))
    ('number', '3.14', 0)

    >>> next(lex('-1.61'))
    ('number', '-1.61', 0)

    >>> next(lex('"Hello"'))
    ('string', 'Hello', 0)

    >>> next(lex('{'))
    ('open_curly', '{', 0)

    >>> list(lex('[1, "2"]'))
    [('open_square', '[', 0), ('number', '1', 1), ('separator', ',', 2), ('string', '2', 4), ('close_square', ']', 7)]

    >>> list(lex('[1, --2]'))
    Traceback (most recent call last):
    ...
    ValueError: Unrecognized token starting at position 4
    """

    rules = [
        ('string', '\"(.*)\"'),
        ('boolean', '(true|false)'),
        ('assignment', '(:)'),
        ('open_square', '(\[)'),
        ('open_curly', '(\{)'),
        ('close_square', '(\])'),
        ('close_curly', '(\})'),
        ('separator', '(,)'),
        ('number', '(\-?[\d\.]+)'),
        (None, '(\s+)'),
    ]

    position = 0

    while position < len(src):
        for rule in rules:
            match = re.match(rule[1], src[position:]) 
        
            if match:
                if rule[0]:
                    yield Token(rule[0], match.group(1), position)
                position += len(match.group(0))
                break
        else:
            raise ValueError(f'Unrecognized token starting at position {position}')

def validate(doc):
    """
    Validates that a JSON document contains appropriately matched brackets
    and curly brackets.

    Returns nothing.

    Raises a ValueError on invalid documents

    >>> validate('')

    >>> validate('{}')
    
    >>> validate('[]')
    
    >>> validate('[{}]')
    
    >>> validate('[1,2,3]')
    
    >>> validate('{"numbers":[1,2,3]}')
    
    >>> validate('{')
    Traceback (most recent call last):
    ...
    ValueError: No closing token for ('open_curly', '{', 0)

    >>> validate('[')
    Traceback (most recent call last):
    ...
    ValueError: No closing token for ('open_square', '[', 0)

    >>> validate('["numbers":{1,2,3]}')
    Traceback (most recent call last):
    ...
    ValueError: No opening token for ('close_square', ']', 17)
    """

if __name__ == '__main__':
    validate(sys.stdin.read())

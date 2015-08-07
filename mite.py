import re

TOKEN_OPEN = '{{'
TOKEN_CLOSE = '}}'

FRAG_VAR = 0x00
FRAG_TEXT = 0x01

# This shit is for identifiers syntax validating
SYNTAX = re.compile(r'%s\s*([A-Za-z_]+[A-Za-z0-9_]*'
                   '(?:\.[A-Za-z_]+[A-Za-z0-9_]*)*)\s*%s'
                   '' % (TOKEN_OPEN, TOKEN_CLOSE))

# Regular expression used for splitting tokens
TOKEN = re.compile(r'(%s\s*[A-Za-z_]+[A-Za-z0-9_]*'
                   '(?:\.[A-Za-z_]+[A-Za-z0-9_]*)*\s*%s)'
                   '' % (TOKEN_OPEN, TOKEN_CLOSE))


def get(identifier, scopes):
    """ Returns the value of an identifier in the scope list. """
    identifier = identifier.split('.')
    keys = len(identifier)
    current = 0
    for scope in scopes:
        for key in identifier:
            if key in scope:
                scope = scope[key]
                current += 1
                if keys == current:
                    return str(scope)
            else:
                current = 0
                break
    return ''


def compile(template=''):
    """
    Returns a list of tuples.

    Each tuple has two informations:
    (`FRAG_VAR`, `identifier`)
    (`FRAG_TEXT`, `text`)
    """
    fragments = []
    tokens = filter(None, TOKEN.split(template))

    for token in tokens:
        var = SYNTAX.match(token)
        if var:
            fragments.append((FRAG_VAR, var.group(1)))
        else:
            fragments.append((FRAG_TEXT, token))
    return fragments


def render(template='', data={}, scopes=None, fragments=None):
    """
    Outputs the rendered template.
    """
    output = ''

    if not scopes:
        scopes = [data]

    if not fragments:
        fragments = compile(template)

    for frag, info in fragments:
        if frag == FRAG_VAR:
            output += get(info, scopes)
        else:
            output += info
    return output


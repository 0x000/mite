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


def resolve(identifier, context):
    for i in identifier.split('.'):
        context = context[i]
    return context


class Compiler:
    def __init__(self, source):
        self.fragments = filter(None, TOKEN.split(source))
        self.output = list(self.compile())

    def compile(self):
        """
        Returns a list of tuples.
        
        Each tuple has two information:
        (`FRAG_VAR`, `identifier`)
        (`FRAG_TEXT`, `text`)
        """
        for fragment in self.fragments:
            var = SYNTAX.match(fragment)
            if var:
                yield (FRAG_VAR, var.group(1))
            else:
                yield (FRAG_TEXT, fragment)
      
    def render(self, context, func=resolve):
        """ Returns joined rendered Fragments. """
        def render_all(self, context, func=resolve):
            for fragment in self.output:
                if fragment[0] == FRAG_VAR:
                    yield str(func(fragment[1], context))
                else:
                    yield fragment[1]
                    
        return ''.join(render_all(self, context, func))


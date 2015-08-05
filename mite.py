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


class Fragment:
    def __init__(self, raw):
        self.raw = raw

    def render(self, context, func=resolve):
        """ Must be overloaded. """
        pass


class Text(Fragment):
    def render(self, context, func=resolve):
        return self.raw

    @property
    def type(self):
        return FRAG_TEXT


class Var(Fragment):
    def __init__(self, raw):
        self.raw = raw
        self.identifier = SYNTAX.match(self.raw).group(1)

    def render(self, context, func=resolve):
        return str(func(self.identifier, context))

    @property
    def type(self):
        return FRAG_VAR


class Compiler:
    def __init__(self, source):
        self.fragments = filter(None, TOKEN.split(source))
        self.output = self.compile()

    def compile(self):
        """ Returns a list of Var or Text objects. """
        output = []
        for fragment in self.fragments:
            if SYNTAX.match(fragment):
                output.append(Var(fragment))
            else:
                output.append(Text(fragment))
        return output

    def render(self, context, func=resolve):
        """ Returns joined rendered Fragments. """
        def render_all(self, context, func=resolve):
            for fragment in self.output:
                yield fragment.render(context, func)

        return ''.join(render_all(self, context, func))


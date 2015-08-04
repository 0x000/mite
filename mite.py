import re

TOKEN_OPEN = '{{'
TOKEN_CLOSE = '}}'

FRAG_VAR = 0x00
FRAG_TEXT = 0x01

# This shit is for identifiers syntax validating
VAR_SYNTAX = (r'^%s\s*(([a-zA-Z]+[0-9]*[a-zA-Z]*)'
              '((\.?)(([a-zA-Z]+[0-9]*[a-zA-Z]*)))*)\s*%s$'
              '' % (TOKEN_OPEN, TOKEN_CLOSE))

VAR_REGEX = re.compile(VAR_SYNTAX)

# Valid identifiers are:
# {{ var    }}
# {{va0r.var0.var}}
# Non valid identifier are:
# {{ 123 }}
# {{ 12a }}
# {{ 1.a.b }}
# {{ 1a.b }}
# And so on...


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

    @property
    def type(self):
        """ Returns the Fragment type. Should be overloaded. """
        if VAR_REGEX.match(self.raw):
            return FRAG_VAR
        return FRAG_TEXT


class Text(Fragment):
    def render(self, context, func=resolve):
        return self.raw

    @property
    def type(self):
        return FRAG_TEXT


class Var(Fragment):
    def __init__(self, raw):
        self.raw = raw
        self.identifier = VAR_REGEX.match(self.raw).group(1)

    def render(self, context, func=resolve):
        return str(func(self.identifier, context))

    @property
    def type(self):
        return FRAG_VAR


CLASS_VAR = Var
CLASS_TEXT = Text


class Compiler:
    def __init__(self, source):
        regex = re.compile(r'(%s.*?%s)' % (TOKEN_OPEN, TOKEN_CLOSE))
        self.fragments = filter(None, regex.split(source))
        self.output = self.compile()

    def compile(self):
        """ Returns a list of Var or Text objects. """
        output = []
        for fragment in self.fragments:
            cls = CLASS_TEXT
            if Fragment(fragment).type == FRAG_VAR:
                cls = CLASS_VAR
            output.append(cls(fragment))
        return output

    def render(self, context, func=resolve):
        """ Returns joined rendered Fragments. """
        def render_all(self, context, func=resolve):
            for frag in self.output:
                yield frag.render(context, func)

        return ''.join(render_all(self, context, func))


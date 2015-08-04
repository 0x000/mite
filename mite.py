import re


TOKEN_OPEN = '{{'
TOKEN_CLOSE = '}}'

FRAG_VAR = 0x00
FRAG_TEXT = 0x01


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
        if re.match(r'^%s.*?%s$' % (TOKEN_OPEN, TOKEN_CLOSE), self.raw):
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
        self.identifier = self.clean_fragment()

    def clean_fragment(self):
        """ Returns raw fragment without tokens. """
        raw = self.raw
        raw = raw.replace(TOKEN_OPEN, '').replace(TOKEN_CLOSE, '')
        return raw.strip()

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


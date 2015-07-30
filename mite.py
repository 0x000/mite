import re

TOKEN_OPEN = '{{'
TOKEN_CLOSE = '}}'

FRAG_VAR = 0
FRAG_TEXT = 1

def resolve(identifier, context):
    for i in identifier.split('.'):
        context = context[i]
    return context


class Fragment:
    def __init__(self, raw):
        self.raw = raw

    def render(self, context):
        """ Returns the rendered string. """
        return ''

    @property
    def type(self):
        if self.raw.startswith(TOKEN_OPEN) and self.raw.endswith(TOKEN_CLOSE):
            return FRAG_VAR
        return FRAG_TEXT


class Text(Fragment):
    def render(self, context):
        return self.raw

    @property
    def type(self):
        return FRAG_TEXT


class Var(Fragment):
    def __init__(self, raw):
        self.raw = raw
        self.identifier = self.clean_fragment()

    def clean_fragment(self):
        raw = self.raw
        raw = raw.replace(TOKEN_OPEN, '').replace(TOKEN_CLOSE, '')
        return raw.strip()

    def render(self, context):
        return str(resolve(self.identifier, context))

    @property
    def type(self):
        return FRAG_VAR


class Compiler:
    def __init__(self, source):
        regex = re.compile(r'(%s.*?%s)' % (TOKEN_OPEN, TOKEN_CLOSE))
        self.fragments = filter(None, regex.split(source))
        self.output = self.compile()

    def compile(self):
        """ Returns a list of Var or Text objects. """
        output = []
        for frag in self.fragments:
            if Fragment(frag).type == FRAG_VAR:
                output.append(Var(frag))
            elif Fragment(frag).type == FRAG_TEXT:
                output.append(Text(frag))
        return output

    def _render_fragments(self, context):
        """ Yields rendered Fragments. """
        for frag in self.output:
            yield frag.render(context)

    def render(self, context):
        """ Returns joined rendered Fragments. """
        return ''.join(self._render_fragments(context))


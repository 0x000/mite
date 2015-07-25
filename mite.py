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
        self.clean = self.clean_fragment()

    def clean_fragment(self):
        """ Returns the cleaned fragment string. """
        clean = self.raw
        if self.type == FRAG_VAR:
            clean = clean.replace(TOKEN_OPEN, '').replace(TOKEN_CLOSE, '')
            return clean.strip()
        return clean

    def render(self, context):
        """ Returns the rendered string. """
        if self.type == FRAG_VAR:
            return str(resolve(self.clean, context))
        return self.raw

    @property
    def type(self):
        if self.raw.startswith(TOKEN_OPEN):
            return FRAG_VAR
        return FRAG_TEXT


class Compiler:
    def __init__(self, source):
        regex = re.compile(r'(%s.*?%s)' % (TOKEN_OPEN, TOKEN_CLOSE))
        self.fragments = filter(None, regex.split(source))
        self.output = self.compile()

    def compile(self):
        """ Returns a list of Fragment objects. """
        return [Fragment(frag) for frag in self.fragments]

    def _render_fragments(self, context):
        """ Yields rendered Fragments. """
        for frag in self.output:
            yield frag.render(context)

    def render(self, context):
        """ Returns joined rendered Fragments. """
        return ''.join(self._render_fragments(context))


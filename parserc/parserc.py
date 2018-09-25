from toolz import compose
from collections import namedtuple

Token = namedtuple('Token',
                   ('offset', 'lineno', 'colno', 'filename', 'type', 'value'))
_TokenView = namedtuple('_TokenView', ('offset', 'source'))


class TokenView(_TokenView):
    def split(self):
        if self.offset < len(self.source):
            offset = self.offset
            source = self.source
            yield source[offset]
            yield TokenView(offset + 1, source)
        else:
            yield


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, parse_fn):
        self.parse_fn = parse_fn

    def __call__(self, view):
        return self.parse_fn(view)

    def __add__(self, p):
        return Parser(both(self, p))

    def __truediv__(self, f):
        return Parser(trans(self, f))

    def __lshift__(self, p):
        return Parser(trans(both(self, p), lambda tp: tp[0]))

    def __rshift__(self, p):
        return Parser(trans(both(self, p), lambda tp: tp[1]))

    def __or__(self, p):
        return Parser(either(self, p))

    def __invert__(self):
        return Parser(not_of(self))

    def __mod__(self, f):
        return Parser(pred(self, f))

    def __getitem__(self, count):
        if isinstance(count, int):
            return Parser(rep(self, count, -1))
        elif isinstance(count, tuple) and len(count) is 2:
            least, most = count
            return Parser(rep(self, least, most))
        raise TypeError(count)


def report_error_location(view):
    token = view.source[view.offset]
    raise ParsingError(
        f"parsing error at line {token.lineno}, column {token.colno}, file {token.filename}"
    )


def run_parse(parser, view):
    result = parser(view)
    if result:
        ret, view = result
        if view.offset == len(view.source):
            return ret

        report_error_location(view)

    report_error_location(view)


def literal(f):
    def parse(view):
        it = view.split()
        token = next(it)
        if token and f(token):
            return token, next(it)

    return parse


def both(pa, pb):
    def parse(view):
        it = pa(view)
        if not it:
            return it
        ret1, view = it
        it = pb(view)
        if not it:
            return it
        ret2, view = it
        return (ret1, ret2), view

    return parse


def all_of(p_seq):
    def parse(view):
        seq = []
        append = seq.append
        for p in p_seq:
            it = p(view)
            if not it:
                return
            e, view = it
            append(e)
        return seq

    return parse


def either(pa, pb):
    def parse(view):
        it = pa(view)
        if it:
            return it
        it = pb(view)
        if it:
            return it

    return parse


def one_of(p_seq):
    def parse(view):
        for p in p_seq:
            it = p(view)
            if not it:
                continue
            return it

    return parse


def rep(p, at_least, at_most):
    def parse(view):
        now = 0
        seq = []
        append = seq.append
        while now != at_most:
            it = p(view)
            if not it:
                break
            ret, view = it
            append(ret)
            now += 1

        if at_least <= now:
            return (seq, view)

    return parse


def any_token(view):
    it = view.split()
    ret = next(it)
    if ret:
        return ret, next(it)


def not_of(pa):
    def parse(view):
        if pa(view):
            return
        it = view.split()
        ret = next(it)
        if ret:
            return ret, next(it)

    return parse


def trans(p, f):
    def parse(view):
        it = p(view)
        if not it:
            return it
        ret, view = it
        return f(ret), view

    return parse


def pred(p, f):
    def parse(view):
        it = p(view)
        if not it:
            return it
        ret, view = it
        if f(ret):
            return ret, view

    return parse


def pgen(p):
    def parse(view):
        it = p(view)
        if not it:
            return it
        ret, view = it
        return ret(view)

    return parse


def char_token_lex(text, filename="<unknown>"):
    lineno = 0
    colno = 0
    new = Token
    for offset, each in enumerate(text):
        if each == '\n':
            lineno += 1
            colno = 0
        else:
            colno += 1
        yield new(offset, lineno, colno, filename, "ch", each)


def char_token_lex_(text, filename="<unknown>"):
    return TokenView(0, tuple(char_token_lex(text, filename)))


if __name__ == '__main__':
    context = {'add': lambda a, b: a + b, 'mul': lambda a, b: a * b}

    match_str = lambda s: literal(lambda it: it.value == s)
    space = Parser(rep(match_str(' '), 0, -1))
    join_value = lambda tokens: ''.join(each.value for each in tokens)

    id = Parser(literal(lambda it: it.value.isidentifier()))
    num = Parser(literal(lambda it: it.value.isdecimal()))

    term = ((id[1, -1] / compose(lambda id: eval(id, context), join_value))
            | num[1, -1] / compose(int, join_value)) << space

    left_paren = Parser(match_str('(')) << space
    right_paren = Parser(match_str(')')) << space

    sexpr = Parser(None)

    sexpr.parse_fn = space >> (
        (left_paren >> rep(sexpr, 0, -1) << right_paren) /
        (lambda it: None if not it else it[0](*it[1:]))
        | term)

    def parse_lisp(text):
        tokens = char_token_lex_(text)
        print(run_parse(sexpr, tokens))

    while True:
        text = input('>>')
        if not text:
            break
        parse_lisp(text)

# =============================================================================
# >>(add 1 2)
# 3
#
# >>(add 3 5)
# 8
#
# >>(mul (add 2 3) (mul 8 9))
# 360
# =============================================================================

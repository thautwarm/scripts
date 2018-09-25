# -*- coding: utf-8 -*-

from parserc import char_token_lex_, both, either, rep, any_token, not_of, literal, trans, run_parse
tokens = char_token_lex_("12111")
one = trans(literal(lambda it: it.value == '1'), lambda it: int(it.value))
two = trans(literal(lambda it: it.value == '2'), lambda it: int(it.value))
print(run_parse(rep(either(one, two), 0, 10), tokens))



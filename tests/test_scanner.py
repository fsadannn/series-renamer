from typing import List

from series_renamer.scanner import Token, TokenType, tokenize
from series_renamer.utils import TPattern
from xeger import Xeger


def compare_results(tks: List[Token], tks1: List[Token]):
    return all(map(lambda x: x[0] == x[1], zip(tks, tks1)))


def sample(exp, limit=20):
    x = Xeger(limit=limit)
    return x.xeger(exp)


def test_tokens():
    n_test = 10
    for t_type in TokenType:
        if t_type.value._has_contains:
            continue

        if t_type is TokenType.Word:
            continue

        regex_exp = t_type.value._regex_exp

        if isinstance(regex_exp, TPattern):
            continue

        for _ in range(n_test):
            exp = sample(regex_exp)
            tks = tokenize(exp)
            result = [Token(exp, t_type, 1)]

            assert len(tks) == 1
            assert compare_results(tks, result)

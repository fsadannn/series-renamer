from typing import List

from series_renamer.scanner import Token, TokenType, epi, epin, tokenize
from xeger import Xeger


def compare_results(tks: List[Token], tks1: List[Token]):
    return all(map(lambda x: x[0] == x[1], zip(tks, tks1)))


def sample_epin():
    x = Xeger(limit=15)
    return x.xeger(epin)


def sample_epi():
    x = Xeger(limit=15)
    return x.xeger(epi)


def test_NumberedEpisode():
    n_test = 10
    for _ in range(n_test):
        exp = sample_epin()
        tks = tokenize(exp)
        result = [Token(exp, TokenType.NumberedEpisode)]
        assert len(tks) == 1
        assert compare_results(tks, result)


def test_EpisodeWord():
    n_test = 10
    for _ in range(n_test):
        exp = sample_epi()
        tks = tokenize(exp)
        result = [Token(exp, TokenType.EpisodeWord)]
        assert len(tks) == 1
        assert compare_results(tks, result)

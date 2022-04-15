import re
from enum import Enum
from typing import Container, List, Optional, Union
from xmlrpc.client import boolean

try:
    from .stopwords import stopwords
except ImportError:
    from stopwords import stopwords

dates_str = '[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4}|[0-9]{2,4}[/-][0-9]{1,2}[/-][0-9]{1,2}'

tokens_str = dates_str + r'|[a-zA-Z0-9!ñÑ\'áéíóúÁÉÍÓÚ@]+|\-|'
tokens_str += '|'.join([r'\{', r'\(', r'\['])
tokens_str += '|' + '|'.join([r'\}', r'\)', r'\]'])
tokens_expression = re.compile(tokens_str, re.I)

only_number = re.compile(r'(?<!\D)[0-9]+(?!\D)')

ordinal = re.compile(
    '1st|2nd|3rd|[1-9][0-9]?th|1ro|2do|3ro|[4-6]to|7mo|8vo|9no', re.I)

daysStr = ['lunes', 'martes', 'mi[eé]rcoles', 'jueves', 'viernes', 's[áa]bado', 'domingo',
           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days = re.compile('|'.join(daysStr), re.I)

dates = re.compile(dates_str)

resolution = re.compile(
    '1080p|720p|480p|1920[xX@]1080|1280[xX@]720|720[xX@]480')

codec = re.compile('[Xx]264|[xX]265')

epi = re.compile(
    'chapters?$|episodes?$|episodios?$|cap[ií]tulos?$|caps?$', re.I)
epin = re.compile(
    'chapters?[0-9]+|episodes?[0-9]+|episodios?[0-9]+|cap[ií]tulos?[0-9]+|caps?[0-9]+', re.I)

captemp = re.compile('([0-9]{1,3})[xX]([0-9]{1,4})', re.I)

seasonepi = re.compile('[Ss]([0-9]{1,3})[Ee]([0-9]{1,4})', re.I)

upperm = re.compile('[A-ZÁÉÍÓÚ].*?[A-ZÁÉÍÓÚ]')

letn = re.compile('[0-9][a-záéíóú]', re.I)

gopener = ['{', '(', '[']
gcloser = ['}', ')', ']']
grouping_d = dict(list(zip(gopener, gcloser)) + list(zip(gcloser, gopener)))
gopener = set(gopener)
gcloser = set(gcloser)

keep_joined = set(['kun', 'sama', 'chan', 'kai', 'senpai', 'man'])


class TokenTypeHelper:
    __slots__ = ('_regex_exp', '_has_contains')

    def __init__(self, regex_exp: Union[str, re.Pattern, Container]):
        if isinstance(regex_exp, str):
            self._regex_exp = re.compile(regex_exp)
            self._has_contains: boolean = False
        else:
            self._regex_exp = regex_exp
            self._has_contains: boolean = isinstance(regex_exp, Container)

    def match(self, text: str) -> Optional[re.Match]:
        if self._has_contains:
            return text in self

        return self._regex_exp.match(text)

    def __contains__(self, x):
        if not self._has_contains:
            raise TypeError(f'{self._regex_exp} is not a Container')
        return x in self._regex_exp


class TokenType(Enum):
    NumberedEpisode = TokenTypeHelper(epin)
    EpisodeWord = TokenTypeHelper(epi)
    SeasonEpisode = TokenTypeHelper(seasonepi)
    ScreenResolution = TokenTypeHelper(resolution)
    ChapterSeason = TokenTypeHelper(captemp)
    KeepJoined = TokenTypeHelper(keep_joined)
    StopWord = TokenTypeHelper(stopwords)
    GroupingOpen = TokenTypeHelper(gopener)
    GroupingClose = TokenTypeHelper(gcloser)
    Dash = TokenTypeHelper('-')
    Day = TokenTypeHelper(days)
    Date = TokenTypeHelper(dates)
    VideoCodec = TokenTypeHelper(codec)
    Ordinal = TokenTypeHelper(ordinal)
    NumberedWord = TokenTypeHelper(letn)
    Number = TokenTypeHelper(only_number)
    Word = TokenTypeHelper(r'[a-zA-Z0-9!ñÑ\'áéíóúÁÉÍÓÚ]')


class Token:
    __slots__ = ('_text', '_type')

    def __init__(self, expression: str, token_type: TokenType) -> None:
        self._text = expression
        self._type = token_type

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return self._type

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}< type={self.type} text="{self.text}" >'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Token):
            raise TypeError(f'Can not compare Token with {o.__class__}')

        return self.type == o.type and self.text == o.text


def make_token(text: str) -> Token:
    token_type: TokenType = TokenType.Word

    for t_type in TokenType:
        if t_type.value.match(text):
            token_type = t_type
            break

    return Token(text, token_type)


def tokenize(txt: str) -> List[Token]:
    tokens: List[Token] = []

    for i in map(lambda x: x.group().strip(), tokens_expression.finditer(txt)):
        token = make_token(i)
        tokens.append(token)

    return tokens


from xeger import Xeger


def sample():
    x = Xeger(limit=15)
    return x.xeger(resolution)


exp = 'i'
print(exp)
tks = tokenize(exp)
print(tks)

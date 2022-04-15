import re
from enum import Enum, auto
from typing import List

try:
    from .stopwords import stopwords
except ImportError:
    from stopwords import stopwords

tokens_str = r'[a-zA-Z0-9!ñÑ\'áéíóú]+|\-|'
tokens_str += '|'.join([r'\{', r'\(', r'\['])
tokens_str += '|' + '|'.join([r'\}', r'\)', r'\]'])
tokens_expression = re.compile(tokens_str, re.I)

only_number = re.compile(r'(?<!\D)[0-9]+(?!\D)')

ordinal = re.compile(
    '1st|2nd|3rd|[1-9][0-9?]th|1ro|2do|3ro|[4-6]to|7mo|8vo|9no', re.I)

daysStr = ['lunes', 'martes', 'mi[eé]rcoles', 'jueves', 'viernes', 's[áa]bado', 'domingo',
           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days = re.compile('|'.join(daysStr), re.I)

dates = re.compile(
    '[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4}|[0-9]{2,4}[/-][0-9]{1,2}[/-][0-9]{1,2}')

resolution = re.compile(
    '1080p|720p|480p|1920 *?[xX] *?1080|1280 *?[xX] *?720|720 *?[xX] *?480')

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
grouping_d = {i: j for i, j in list(
    zip(gopener, gcloser)) + list(zip(gcloser, gopener))}
gopener = set(gopener)
gcloser = set(gcloser)

keep_joined = set(['kun', 'sama', 'chan', 'kai', 'senpai', 'man'])


class TokenType(Enum):
    Word = auto()
    GroupingOpen = auto()
    GroupingClose = auto()
    Dash = auto()
    Day = auto()
    Date = auto()
    ScreenResolution = auto()
    VideoCodec = auto()
    KeepJoined = auto()
    Number = auto()
    Ordinal = auto()
    EpisodeWord = auto()
    NumberedEpisode = auto()
    StopWord = auto()
    ChapterSeason = auto()
    SeasonEpisode = auto()
    NumberedWord = auto()


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

    if epin.match(text):
        token_type = TokenType.NumberedEpisode
        return Token(text, token_type)

    if epi.match(text):
        token_type = TokenType.EpisodeWord
        return Token(text, token_type)

    if captemp.match(text):
        token_type = TokenType.ChapterSeason
        return Token(text, token_type)

    if seasonepi.match(text):
        token_type = TokenType.SeasonEpisode
        return Token(text, token_type)

    if text in keep_joined:
        token_type = TokenType.KeepJoined
        return Token(text, token_type)

    if text in stopwords:
        token_type = TokenType.StopWord
        return Token(text, token_type)

    if text in gopener:
        token_type = TokenType.GroupingOpen
        return Token(text, token_type)

    if text in gcloser:
        token_type = TokenType.GroupingClose
        return Token(text, token_type)

    if text == '-':
        token_type = TokenType.Dash
        return Token(text, token_type)

    if days.match(text):
        token_type = TokenType.Day
        return Token(text, token_type)

    if dates.match(text):
        token_type = TokenType.Date
        return Token(text, token_type)

    if resolution.match(text):
        token_type = TokenType.ScreenResolution
        return Token(text, token_type)

    if codec.match(text):
        token_type = TokenType.VideoCodec
        return Token(text, token_type)

    if ordinal.match(text):
        token_type = TokenType.Ordinal
        return Token(text, token_type)

    if letn.match(text):
        token_type = TokenType.NumberedWord
        return Token(text, token_type)

    if only_number.match(text):
        token_type = TokenType.Number
        return Token(text, token_type)

    return Token(text, token_type)


def tokenize(txt: str) -> List[Token]:
    tokens: List[Token] = []

    for i in map(lambda x: x.group().strip(), tokens_expression.finditer(txt)):
        token = make_token(i)
        tokens.append(token)

    return tokens

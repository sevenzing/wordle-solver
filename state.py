import typing
import logging

from letter import Letter, Yellow, Black, Green, Context


class State:
    FROM_STR_TO_LETTER_TYPE = {
        'Y': Yellow,
        'B': Black,
        'G': Green,
    }

    def __init__(self, words: typing.List[typing.List[Letter]]) -> None:
        self.words = words
        self._patch()

    def _patch(self):
        for word in self.words:
            for i, letter in enumerate(word):
                letter._patch(position=i, context=Context(words=self.words, my_word=word))

    def _is_possible(self, string: str) -> bool:
        string = string.upper()
        for word in self.words:
            for letter in word:
                if not letter.apply(string):
                    logging.info(f'word {string} is not ok since word {word} has letter {letter}')
                    return False
        return True

    def filter(self, options: typing.List[str]) -> typing.List[str]:
        possible_words = list(filter(lambda w: self._is_possible(w), options))
        return possible_words

    @classmethod
    def from_file(cls, path: str):
        with open(path, 'r',  encoding='utf-8') as f:
            lines = f.readlines()
            words = map(lambda x: zip(*x), map(str.split, lines))
            parsed_words = []
            for word in words:
                parsed_word = []
                for letter, _type in word:
                    _type_cls = cls.FROM_STR_TO_LETTER_TYPE[_type]
                    parsed_word.append(_type_cls(letter))
                parsed_words.append(parsed_word)
        return cls(parsed_words)

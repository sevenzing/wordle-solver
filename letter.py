"""
Represent one letter of wordle word
"""

import dataclasses
import typing


@dataclasses.dataclass
class Context:
    words: typing.List[typing.List['Letter']]
    my_word: typing.List['Letter']


@dataclasses.dataclass(eq=True)
class Letter:
    letter: str
    context: Context = dataclasses.field(compare=False, default=None)
    position: typing.Optional[int] = dataclasses.field(compare=False, default=None)
    _patched: bool = dataclasses.field(compare=False, init=False, default=False)


    def _patch(self, position: int, context: Context):
        self.position = position
        self.context = context
        self._patched = True

    def apply(self, word: str) -> bool:
        raise NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.letter}, pos={self.position})"

class Black(Letter):
    def apply(self, word: str) -> bool:
        total_yellow = self.context.my_word.count(Yellow(self.letter))
        total_green = self.context.my_word.count(Green(self.letter))
        if word.count(self.letter) != total_yellow + total_green:
            return False
        return True

class Green(Letter):
    def apply(self, word: str) -> bool:
        assert self._patched, f"{self} filter was not patched"
        return word[self.position] == self.letter

class Yellow(Letter):
    def apply(self, word: str) -> bool:
        assert self._patched, f"{self} filter was not patched"
        if word[self.position] == self.letter:
            return False
        
        total_yellow = self.context.my_word.count(Yellow(self.letter))
        total_green =  self.context.my_word.count(Green(self.letter))
        should_exists = total_yellow + total_green

        if word.count(self.letter) != should_exists:
            return False

        return True
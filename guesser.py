import collections
import logging

from state import State



class Guesser:
    def __init__(self,  path_to_words: str):
        with open(path_to_words, 'r',  encoding='utf-8') as f:
            self.words_from_path = list(map(str.strip, f.read().split()))
        self.letters_freq = collections.Counter(''.join(self.words_from_path))

    def guess(self, state: State):
        return sorted(state.filter(self.words_from_path), key=self._sort_by_letter_freq, reverse=True)

    def _sort_by_letter_freq(self, word: str):
        score = sum(map(lambda letter: self.letters_freq[letter], set(word)))
        return score


def one_guess(path_to_words, path_to_state):
    guesser = Guesser(path_to_words)
    state = State.from_file(path_to_state)
    possible = guesser.guess(state)
    return possible
    

import argparse
import pathlib

from guesser import one_guess

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--words', required=True, type=pathlib.Path)
    parser.add_argument('-s', '--state', required=True, type=pathlib.Path)
    args = parser.parse_args()

    options = one_guess(args.words, args.state)
    print(options[:5])

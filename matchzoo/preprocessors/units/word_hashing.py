import collections

import numpy as np

from .unit import Unit


class WordHashing(Unit):
    """
    Word-hashing layer for DSSM-based models.

    The input of :class:`WordHashingUnit` should be a list of word
    sub-letter list extracted from one document. The output of is
    the word-hashing representation of this document.

    :class:`NgramLetterUnit` and :class:`VocabularyUnit` are two
    essential prerequisite of :class:`WordHashingUnit`.

    Examples:
       >>> letters = [['#te', 'tes','est', 'st#'], ['oov']]
       >>> word_hashing = WordHashing(
       ...     term_index={'': 0,'st#': 1, '#te': 2, 'est': 3, 'tes': 4})
       >>> hashing = word_hashing.transform(letters)
       >>> hashing[0]
       [0.0, 1.0, 1.0, 1.0, 1.0, 0.0]
       >>> hashing[1]
       [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    """

    def __init__(
        self,
        term_index: dict,
    ):
        """
        Class initialization.

        :param term_index: term-index mapping generated by
            :class:`VocabularyUnit`.
        :param dim_triletter: dimensionality of tri_leltters.
        """
        self._term_index = term_index

    def transform(self, input_: list) -> list:
        """
        Transform list of :attr:`letters` into word hashing layer.

        :param input_: list of `tri_letters` generated by
            :class:`NgramLetterUnit`.
        :return: Word hashing representation of `tri-letters`.
        """
        if any([isinstance(elem, list) for elem in input_]):
            # The input shape for CDSSM is
            # [[word1 ngram, ngram], [word2, ngram, ngram], ...].
            hashing = np.zeros((len(input_), len(self._term_index) + 1))
            for idx, word in enumerate(input_):
                counted_letters = collections.Counter(word)
                for key, value in counted_letters.items():
                    letter_id = self._term_index.get(key, 0)
                    hashing[idx, letter_id] = value
        else:
            # The input shape for DSSM model [ngram, ngram, ...].
            hashing = np.zeros((len(self._term_index) + 1))
            counted_letters = collections.Counter(input_)
            ''' Ben's doubt [Resolved] self._term_index is a dictionary of ngrams.'''
            for key, value in counted_letters.items():
                letter_id = self._term_index.get(key, 0)
                hashing[letter_id] = value

        return hashing.tolist()

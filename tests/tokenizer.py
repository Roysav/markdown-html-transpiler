import unittest
from md_html import tokenizer
from itertools import takewhile


class TestIndividualRules(unittest.TestCase):
    def test_underline_should_tokenize(self):
        self.assertEqual(tokenizer.Underline.tokenize('__  __', 0),
                         tokenizer.Token(tokenizer.OPEN_UNDERLINE, 0, 2, '__'))
        self.assertEqual(tokenizer.Underline.tokenize('__  __', 4),
                         tokenizer.Token(tokenizer.CLOSE_UNDERLINE, 4, 6, '__'))

    def test_bold_should_tokenize(self):
        self.assertEqual(tokenizer.Bold.tokenize('**  **', 0), tokenizer.Token(tokenizer.OPEN_BOLD, 0, 2, '**'))
        self.assertEqual(tokenizer.Bold.tokenize('**  **', 4), tokenizer.Token(tokenizer.CLOSE_BOLD, 4, 6, '**'))

    def test_headline_should_tokenize(self):
        self.assertEqual(tokenizer.Token(tokenizer.HEADLINE, 0, 2, '# '), tokenizer.Headline.tokenize('#  ', 0))
        self.assertEqual(tokenizer.Token(tokenizer.HEADLINE, 0, 3, '## '), tokenizer.Headline.tokenize('##  ', 0))
        self.assertEqual(tokenizer.Token(tokenizer.HEADLINE, 0, 4, '### '), tokenizer.Headline.tokenize('###  ', 0))


class TestTokenizer(unittest.TestCase):
    def test_sequence_underline(self):
        code = '**h**'
        expected = [
            tokenizer.Token(tokenizer.OPEN_BOLD, 0, 2, '**'),
            tokenizer.Token(tokenizer.CONTENT, 2, 3, 'h'),
            tokenizer.Token(tokenizer.CLOSE_BOLD, 3, 5, '**')
        ]
        actual = []
        tokens = tokenizer.Tokenizer(code)
        while tokens.current is not None:
            actual.append(tokens.current)
            next(tokens)
        self.assertEqual(expected, actual)

    def test_sequence_bold(self):
        code = '__h__'
        expected = [
            tokenizer.Token(tokenizer.OPEN_UNDERLINE, 0, 2, '__'),
            tokenizer.Token(tokenizer.CONTENT, 2, 3, 'h'),
            tokenizer.Token(tokenizer.CLOSE_UNDERLINE, 3, 5, '__')
        ]
        actual = []
        tokens = tokenizer.Tokenizer(code)
        while tokens.current is not None:
            actual.append(tokens.current)
            next(tokens)
        self.assertEqual(expected, actual)

    def test_sequence_headline(self):
        code = '# h'
        expected = [
            tokenizer.Token(tokenizer.HEADLINE, 0, 2, '# '),
            tokenizer.Token(tokenizer.CONTENT, 2, 3, 'h')
        ]
        actual = []
        tokens = tokenizer.Tokenizer(code)
        while tokens.current is not None:
            actual.append(tokens.current)
            next(tokens)

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

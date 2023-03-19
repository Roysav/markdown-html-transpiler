import unittest
from md_html import tokenizer


class TestIndividualRules(unittest.TestCase):
    def test_underline_should_tokenize(self):
        self.assertEqual(tokenizer.Underline.tokenize('__  __', 0), tokenizer.Token(tokenizer.OPEN_UNDERLINE, 0, 2, '__'))
        self.assertEqual(tokenizer.Underline.tokenize('__  __', 4), tokenizer.Token(tokenizer.CLOSE_UNDERLINE, 4, 6, '__'))


if __name__ == '__main__':
    unittest.main()

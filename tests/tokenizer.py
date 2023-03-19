import unittest
from md_html import tokenizer


class TestIndividualRules(unittest.TestCase):
    def test_underline_should_tokenize(self):
        self.assertEqual(tokenizer.Underline.tokenize('__  __', 0), tokenizer.Token(tokenizer.OPEN_UNDERLINE, 0, 2, '__'))
        self.assertEqual(tokenizer.Underline.tokenize('__  __', 4), tokenizer.Token(tokenizer.CLOSE_UNDERLINE, 4, 6, '__'))

    def test_bold_should_tokenize(self):
        self.assertEqual(tokenizer.Bold.tokenize('**  **', 0), tokenizer.Token(tokenizer.OPEN_BOLD, 0, 2, '**'))
        self.assertEqual(tokenizer.Bold.tokenize('**  **', 4), tokenizer.Token(tokenizer.CLOSE_BOLD, 4, 6, '**'))

    def test_headline_should_tokenize(self):
        self.assertEqual(tokenizer.Token(tokenizer.HEADLINE, 0, 2, '# '), tokenizer.Headline.tokenize('#  ', 0))
        self.assertEqual(tokenizer.Token(tokenizer.HEADLINE, 0, 3, '## '), tokenizer.Headline.tokenize('##  ', 0))
        self.assertEqual(tokenizer.Token(tokenizer.HEADLINE, 0, 4, '### '), tokenizer.Headline.tokenize('###  ', 0))

if __name__ == '__main__':
    unittest.main()

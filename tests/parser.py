import unittest
from md_html import parser
import dominate
from dominate import tags
from bs4 import BeautifulSoup


class TestParser(unittest.TestCase):
    def test_content(self):
        cases = [
            'hello world',
            '<div>injected tag</div>'
        ]
        for case in cases:
            with self.subTest(case=case):
                expected = tags.span(case)
                actual = parser.Parser(case).content()
                expected_soup = BeautifulSoup(expected.render(), 'html.parser')
                actual_soup = BeautifulSoup(actual.render(), 'html.parser')
                self.assertEqual(expected_soup.text, actual_soup.text)
                self.assertEqual(expected_soup.find().name, actual_soup.find().name)

    def test_underline(self):
        text = 'hello world'
        code = f'__{text}__'
        expected = tags.u(tags.p(text))
        actual = parser.Parser(code).underline()
        expected_soup = BeautifulSoup(expected.render(), 'html.parser')
        actual_soup = BeautifulSoup(actual.render(), 'html.parser')
        self.assertEqual(expected_soup.text, actual_soup.text)
        self.assertEqual(expected_soup.find().name, actual_soup.find().name)

    def test_headline(self):
        text = 'hello world'
        code = f'# {text}'
        p = parser.Parser(code)
        expected = tags.h1(tags.p(text))
        actual = p.headline()
        expected_soup = BeautifulSoup(expected.render(), 'html.parser')
        actual_soup = BeautifulSoup(actual.render(), 'html.parser')
        self.assertEqual(expected_soup.text.strip(), actual_soup.text.strip())
        self.assertEqual(expected_soup.find().name, actual_soup.find().name)

    def test_paragraph(self):
        text = 'hello world'
        expected = tags.p(tags.span(tags.span(text)))
        actual = parser.Parser(text).paragraph()
        expected_soup = BeautifulSoup(expected.render(), 'html.parser')
        actual_soup = BeautifulSoup(actual.render(), 'html.parser')
        self.assertEqual(expected_soup.text, actual_soup.text)
        self.assertEqual(expected_soup.find().name, actual_soup.find().name)

if __name__ == "__main__":
    unittest.main()

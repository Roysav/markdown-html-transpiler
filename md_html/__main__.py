import pathlib
import argparse
from . import parser


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('path', type=pathlib.Path)



path = arg_parser.parse_args().path
with path.open() as f:
    code = f.read()
    p = parser.Parser(code)
    doc = p.document()
    print(doc.render())

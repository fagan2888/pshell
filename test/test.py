import unittest
import sys
from os.path import dirname, realpath
src = dirname(dirname(realpath(__file__))) + "/src"
print(src)
sys.path.insert(0, src)
from pshell import *

class test_python_fn_cmd(unittest.TestCase):
    def test_zero_argument(self):
        u = shell(lambda: 1234)
        self.assertEqual('1234', u.run())
    def test_one_argument(self):
        u = shell(lambda x: str(x) + 'abc')(123)
        self.assertEqual("123abc", u.run())

unittest.main()

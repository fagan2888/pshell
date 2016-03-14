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
    def test_multiple_args(self):
        u = shell(lambda x, y: str(x) + 'abc' + str(y))(2, 3)
        self.assertEqual('2abc3', u.run())
        u = shell(lambda x, y, z: str(x) + 'abc' + str(y) + 'def' + str(z))(2, 3, 4)
        self.assertEqual('2abc3def4', u.run())
    def test_named_params(self):
        u = shell(lambda x=0, y=0: str(x) + 'abc' + str(y))(x=2, y=3)
        self.assertEqual('2abc3', u.run())
        u = shell(lambda x=0, y=0: str(x) + 'abc' + str(y))(y=3, x=2)
        self.assertEqual('2abc3', u.run())
    def test_hybrid(self):
        u = shell(lambda z, x=0, y=0: str(x) + 'abc' + str(y) + 'def' + str(z))(5, x=2, y=3)
        self.assertEqual('2abc3def5', u.run())
    def test_curry(self):
        u = shell(lambda x, y: str(x + y))(2)(3)
        self.assertEqual('5', u.run())
    def test_multiple_curry(self):
        u = shell(lambda a,b,c,d,e,f,g: "{a} {b} {c} {d} {e} {f} {g}".format(**locals()))(1,2,3)(4)(5,6)(7)
        self.assertEqual('1 2 3 4 5 6 7', u.run())
    def test_curry_nonpositional(self):
        testfn = lambda a=1,b=2,c=3,d=4,e=5,f=6,g=7: "{a} {b} {c} {d} {e} {f} {g}".format(**locals())
        u = shell(testfn)(c=1,d=2,a=3)(b=4)(g=5,e=6)(f=7)
        self.assertEqual('3 4 1 2 6 7 5', u.run())
        u = shell(testfn)(c=1,d=2,a=3)(b=4)
        self.assertEqual('3 4 1 2 5 6 7', u.run())
        u = shell(testfn)(c=1,d=2,a=3)(b=4)(a=4,d='abc',g=2)
        self.assertEqual('4 4 1 abc 5 6 2', u.run())
    def test_curry_hybrid(self):
        testfn = lambda a,b,c,d=4,e=5,f=6,g=7: "{a} {b} {c} {d} {e} {f} {g}".format(**locals())
        u = shell(testfn)(1,d=2)(3, 4)(g=5,e=6)(f=7)
        self.assertEqual('1 3 4 2 6 7 5', u.run())
    def test_extra_positional(self):
        u = shell(lambda: 1234)
        self.assertRaises(TypeError, u(1234).run)
        u = shell(lambda x: x)
        self.assertRaises(TypeError, u(1234, 23).run)
    def test_extra_nonpositional(self):
        u = shell(lambda: 1234)
        self.assertRaises(TypeError, u(x=1234).run)
        u = shell(lambda y=2: 1234)
        self.assertRaises(TypeError, u(x=1234).run)
unittest.main()

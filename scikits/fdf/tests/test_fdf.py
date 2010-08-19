import unittest

import scikits.fdf as fdf

import numpy as np

def tsin01(fdf):
    return fdf.sin()
#

def fun1(fun, x, eps):
    x = fdf.variable(x)
    b = fun(x+eps)
    a = fun(x)
    return ((b-a)/eps).f/((a+b)/2).df - 1
#

def fun2(fun, x, eps):
    x = fdf.variable(x)
    b = fun(x+eps)
    a = fun(x)
    return ((b-a)/eps).f - ((a+b)/2).df
#

def t1(fun, x, eps, err):
    tf = abs(fun1(fun, x, eps))
    if (tf > err).any():
        print tf
        return False
    #
    else:
        return True
    #
#

def t2(fun, x, eps, err):
    tf = abs(fun2(fun, x, eps))
    if (tf > err).any():
        print tf
        return False
    #
    else:
        return True
    #
#

class TestBibi(unittest.TestCase):

    def test_OK(self):
        self.assertTrue(True)
    #

    def test_adda(self):
        self.assertTrue(t1(lambda fdf:fdf+(10*fdf), [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_addb(self):
        self.assertTrue(t1(lambda fdf:2+fdf, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_addc(self):
        self.assertTrue(t1(lambda fdf:fdf+2, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_suba(self):
        self.assertTrue(t1(lambda fdf:fdf-(10*fdf), [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_subb(self):
        self.assertTrue(t1(lambda fdf:2-fdf, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_subc(self):
        self.assertTrue(t1(lambda fdf:fdf-2, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_neg(self):
        self.assertTrue(t1(lambda fdf:-fdf, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_mula(self):
        self.assertTrue(t1(lambda fdf:fdf*(10*fdf), [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_mulb(self):
        self.assertTrue(t1(lambda fdf:2*fdf, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_mulc(self):
        self.assertTrue(t1(lambda fdf:fdf*2, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_inv(self):
        self.assertTrue(t1(lambda fdf:fdf.inv(), [0.1, 0.2, 1.0], 1e-5,1e-8))
    def test_diva(self):
        self.assertTrue(t1(lambda fdf:fdf/(fdf*fdf), [0.1, 0.2, 1.0], 1e-5,1e-8))
    def test_divb(self):
        self.assertTrue(t1(lambda fdf:2/fdf, [0.1, 0.2, 1.0], 1e-5,1e-8))
    def test_divc(self):
        self.assertTrue(t1(lambda fdf:fdf/2, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_powa(self):
        self.assertTrue(t1(lambda fdf:fdf**(10*fdf), [0.1, 0.2, 1.0], 1e-5,1e-8))
    def test_powb(self):
        self.assertTrue(t1(lambda fdf:2**fdf, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_powc(self):
        self.assertTrue(t1(lambda fdf:fdf**2, [0.1, 0.2, 1.0], 1e-5,1e-10))
    def test_sqrt(self):
        self.assertTrue(t1(lambda fdf:fdf.sqrt(), [0.1, 0.2, 1.0], 1e-5,1e-9))
    def test_sqrt0(self):
        self.assertTrue(t2(lambda fdf:fdf.sqrt(), [0.01], 1e-5,1e-6))
    def test_square(self):
        self.assertTrue(t1(lambda fdf:fdf.square(), [0.1, 0.2, 1.0], 1e-5,1e-9))
    def test_sin(self):
        self.assertTrue(t1(lambda fdf:fdf.sin(), [0.0, 0.1, 0.2, 1.0], 1e-5,1e-9))
    def test_cos(self):
        self.assertTrue(t1(lambda fdf:fdf.cos(), [0.1, 0.2, 1.0], 1e-5,1e-9))
    def test_cos0(self):
        self.assertTrue(t1(lambda fdf:fdf.cos(), [0.0, np.pi], 1e-5,1e-7))        
    def test_exp(self):
        self.assertTrue(t1(lambda fdf:fdf.exp(), [0.1, 0.2, 1.0], 1e-5,1e-9))
    def test_log(self):
        self.assertTrue(t1(lambda fdf:fdf.exp(), [0.1, 0.2, 1.0], 1e-5,1e-9))


if __name__ == '__main__':
    unittest.main()

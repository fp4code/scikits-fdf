# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import scikits.sqrts as sqrts

class Fdf:

    """
from  scikits.fdf import Fdf
import numpy as np

v = np.array([1,2,3])
v = np.array([1,2,3j])
a = Fdf.variable(v)

print(a)
print(a+a)
print(a+a-2*a)
print(a*a/a - a)
print(Fdf.sqrt(a**2) - a)
print(Fdf.square(a) - a**2)
print(Fdf.square(Fdf.sin(a)) + Fdf.square(Fdf.cos(a)))
print(Fdf.exp(Fdf.log(a)))
s,c = Fdf.sincos(a) ; print(s**2 + c**2)


# newton:
s = np.array([1,2,3,1j,-2])
r = np.array([1,1,1,1,1j])
print(r)
for i in xrange(10):
    r = Fdf.newton_step(lambda z: Fdf.variable(z)**2 - Fdf.constant(s), r)
    print(np.max(np.abs(np.sqrt(s)-r)))
#

s = np.array([1,2,3,1j,-2])
r = np.array([1,1,1,1,1j])
(r,err) = Fdf.newton_ten_steps(lambda z: Fdf.variable(z)**2 - Fdf.constant(s), r)
print (r,err)

"""

    def __init__(self,f,df):
        """Construct a Fdf from the value of a function and the value of its derivative"""
        self.f,self.df = f,df
    #

    def __str__(self):
        return '(' + self.f.__str__() + ', ' + self.df.__str__() + ')'
    #

    def __repr__(self):
        return 'Fdf(' + self.f.__repr__() + ', ' + self.df.__repr__() + ')'

    def __add__(self,a):
        if isinstance(a,Fdf):
            return Fdf(self.f + a.f, self.df + a.df)
        #
        else:
            return Fdf(self.f + a, self.df)
        #
    #

    def __radd__(self,a):
        if isinstance(a,Fdf):
            return Fdf(a.f + self.f, a.df + self.df)
        #
        else:
            return Fdf(a + self.f, self.df)
        #
    #

    def __sub__(self,a):
        if isinstance(a,Fdf):
            return Fdf(self.f - a.f, self.df - a.df)
        #
        else:
            return Fdf(self.f - a, self.df)
        #
    #

    def __rsub__(self,a):
        if isinstance(a,Fdf):
            return Fdf(a.f - self.f, a.df - self.df)
        #
        else:
            return Fdf(a - self.f, -self.df)
        #
    #

    def __neg__(self):
        return Fdf(-self.f, -self.df)
    #

    def __mul__(self,a):
        if isinstance(a,Fdf):
            return Fdf(self.f * a.f, self.f * a.df + self.df * a.f)
        #
        else:
            return Fdf(self.f * a, self.df * a)            
        #
    #

    def __rmul__(self,a):
        if isinstance(a,Fdf):
            return Fdf(a.f * self.f, a.df * self.f + a.f * self.df)
        #
        else:
            return Fdf(a * self.f, a * self.df)            
        #
    #

    def inv(self):
        return Fdf(1.0 / self.f, - self.df / (self.f**2))
    #

    def __truediv__(self,a):
        if isinstance(a,Fdf):
            return self * Fdf.inv(a)
        #
        else:
            return self * (1.0 / a)
        #
    #

    __div__ = __truediv__

    def __rtruediv__(self,a):
        return a * self.inv()
    #

    __rdiv__ = __rtruediv__

    def __pow__(self,a):
        if isinstance(a,Fdf):
            spa = self.f**a.f
            return Fdf(spa, (a.df * np.log(self.f) + a.f * self.df / self.f) * spa)
        #
        else :
            spa = self.f**a
            return Fdf(spa, (a * self.df / self.f) * spa)
        #
    #

    def __rpow__(self,a):
        if isinstance(a,Fdf):
            aps = a.f**self.f
            return Fdf(aps, (self.df * np.log(a.f) + self.f * a.df / a.f) * aps)
        #
        else :
            aps = a**self.f
            return Fdf(aps, (self.df * np.log(a)) * aps)
        #
    #

    def __getitem__(self,i):
        return Fdf(self.f.__getitem__(i),self.df.__getitem__(i))
    #
#

def variable(x):
    """Constructs a Fdf variable from its value. The derivative is 1"""
    if not np.isscalar(x):
        x = np.asarray(x)
    #
    return Fdf(x,np.ones_like(x))
#

def constant(x):
    """Constructs a Fdf constant from its value. The derivative is 0"""
    if not np.isscalar(x):
        x = np.asarray(x)
    #
    return Fdf(x,np.zeros_like(x))
#

def sqrt(v, funsqrt = np.sqrt):
    s = funsqrt(v.f)
    return Fdf(s,0.5*v.df/s)
#
Fdf.sqrt = sqrt
    
class Sqrt_near:
    def __init__(self, value):
        self.near = sqrts.Nearest(value)
    #
    def sqrt(self,_fdf):
        s = self.near.sqrt(_fdf.f)
        return Fdf(s,0.5*_fdf.df/s)
    #
#   

def square(v):
    return Fdf(np.square(v.f),2*v.df*v.f)
#
Fdf.square = square

def sin(v):
    return Fdf(np.sin(v.f),v.df*np.cos(v.f))
#
Fdf.sin = sin

def cos(v):
    return Fdf(np.cos(v.f),-v.df*np.sin(v.f))
#
Fdf.cos = cos

def sincos(v):
    s = np.sin(v.f)
    c = np.cos(v.f)
    return Fdf(s,v.df*c),Fdf(c,-v.df*s)
#
Fdf.sincos = sincos

def exp(v):
    e = np.exp(v.f)
    return Fdf(e,v.df*e)
#
Fdf.exp = exp

def expi(v):
    e = np.exp(1j*v.f)
    return Fdf(e,1j*v.df*e)
#
Fdf.expi = expi

def log(v):
    return Fdf(np.log(v.f), v.df/v.f)
#
Fdf.log = log

def newton_step(fun_fdf, r):
    fdf = fun_fdf(r)
    return (r - fdf.f/fdf.df)
#

def newton_ten_steps(fun_fdf, r):
    for i in xrange(10):
        r = Fdf.newton_step(fun_fdf, r)
    #
    rn = Fdf.newton_step(fun_fdf, r) 
    return (rn, np.abs(rn - r))
#


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

    @staticmethod
    def variable(x):
        """Constructs a Fdf variable from its value. The derivative is 1"""
        return Fdf(x,np.ones_like(x))
    #

    @staticmethod
    def constant(x):
        """Constructs a Fdf constant from its value. The derivative is 0"""
        return Fdf(x,np.zeros_like(x))
    #

    def __str__(self):
        return '('+self.f.__str__()+','+self.df.__str__()+')'
    #

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
            return Fdf(self.f - a.f, self.df)
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

    def __div__(self,a):
        if isinstance(a,Fdf):
            return self * Fdf.inv(a)
        #
        else:
            return self * (1.0 / a)
        #
    #

    def __rdiv__(self,a):
        return self.inv() * a
    #

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

    def sqrt(self, funsqrt = np.sqrt):
        s = funsqrt(self.f)
        return Fdf(s,0.5*self.df/s)
    #
    
    class Sqrt_near:
        def __init__(self, value):
            self.near = sqrts.Near(value)
        #
        def sqrt(self,fdf):
            s = self.sqrt(fdf.f)
            return Fdf(s,0.5*fdf.df/s)
        #
    #

    def square(self):
        return Fdf(np.square(self.f),2*self.df*self.f)
    #

    def sin(self):
        return Fdf(np.sin(self.f),self.df*np.cos(self.f))
    #

    def cos(self):
        return Fdf(np.cos(self.f),-self.df*np.sin(self.f))
    #

    def sincos(self):
        s = np.sin(self.f)
        c = np.cos(self.f)
        return Fdf(s,self.df*c),Fdf(c,-self.df*s)
    #

    def exp(self):
        e = np.exp(self.f)
        return Fdf(e,self.df*e)
    #

    def expi(self):
        e = np.exp(1j*self.f)
        return Fdf(e,1j*self.df*e)
    #

    def log(self):
        return Fdf(np.log(self.f), self.df/self.f)
    #

    @staticmethod
    def newton_step(fun_fdf, r):
        fdf = fun_fdf(r)
        return (r - fdf.f/fdf.df)
    #

    @staticmethod
    def newton_ten_steps(fun_fdf, r):
        for i in xrange(10):
            r = Fdf.newton_step(fun_fdf, r)
        #
        rn = Fdf.newton_step(fun_fdf, r) 
        return (rn, np.abs(rn - r))

    def __getitem__(self,i):
        return Fdf(self.f.__getitem__(i),self.df.__getitem__(i))

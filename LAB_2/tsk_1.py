import math


class Complex():
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __add__(self, other):
        # +
        return Complex(self.real + other.real, self.imaginary + other.imaginary)


    def __sub__(self, other):
        # -
        return Complex(self.real - other.real, self.imaginary - other.imaginary)


    def __mul__(self, other):
        # *
        real = self.real * other.real - self.imaginary * other.imaginary
        imaginary = self.real * other.imaginary + self.imaginary * other.real
        return Complex(real, imaginary)


    def __truediv__(self, other):
        # /
        denominator = other.real**2 + other.imaginary**2
        real = (self.real * other.real + self.imaginary * other.imaginary) / denominator
        imaginary = (self.imaginary * other.real - self.real * other.imaginary) / denominator
        return Complex(real, imaginary)

   
    def __abs__(self):
        # || 
        return math.sqrt(self.real**2 + self.imaginary**2)
    
    
    def __str__(self):
        # print 
        if self.imaginary >= 0:
            return f"{self.real} + {self.imaginary}i"
        else:
            return f"{self.real} - {abs(self.imaginary)}i"
        

a = Complex(10, 25)
b = Complex(31, 42)

print(a)
print(b)
print(a+b, a-b, a*b, a/b)
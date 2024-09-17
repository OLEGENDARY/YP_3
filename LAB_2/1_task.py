class Complex:
    def __init__(self, real=0.0, imag=0.0):
        self.real = real
        self.imag = imag

    def __repr__(self):
        return f"Complex({self.real}, {self.imag})"

    def __str__(self):
        if self.imag >= 0:
            return f"{self.real} + {self.imag}j"
        else:
            return f"{self.real} - {-self.imag}j"

    def __add__(self, other):
        #+
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        #-
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        #*
        real = self.real * other.real - self.imag * other.imag
        imag = self.real * other.imag + self.imag * other.real
        return Complex(real, imag)

    def __truediv__(self, other):
        #/
        denom = other.real**2 + other.imag**2
        real = (self.real * other.real + self.imag * other.imag) / denom
        imag = (self.imag * other.real - self.real * other.imag) / denom
        return Complex(real, imag)

    def __abs__(self):
        #abs
        return (self.real**2 + self.imag**2)**0.5

    def __eq__(self, other):
        #==
        return self.real == other.real and self.imag == other.imag


#Пример
a = Complex(1, 2)
b = Complex(3, -4)

print(f"a: {a}",
      f"b: {b}", 
      sep='\n', end='\n\n')

print(f"a + b = {a + b}", 
      f"a - b = {a - b}", 
      f"a * b = {a * b}", 
      f"a / b = {a / b}",
      sep='\n', end='\n\n')

print(f"|a| = {abs(a)}", 
      f"|b| = {abs(b)}",
      sep='\n', end='\n\n')
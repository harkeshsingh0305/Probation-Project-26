import numpy as np

a = np.random.randint(1,20,10)
b = np.random.randint(1,20,10)

print("First Array :",a)
print("Second Array :",b)

print("Sum :",a+b)
print("Sub :",a-b)
print("Product :",a*b)
print("Division :",a/b)

print("Square of every element :",a**2)

print("Dot Product :",np.dot(a,b))

print("Sorted Second Array :",np.sort(b))
import numpy as np

a = np.random.randint(1,20,9).reshape(3,3)

print(a)

b = a[0,:]
print("First Row :",b)

c = a[:,0]
print("First Column :",c)

d = a[1:2,1:2]
print("2,2 Element :",d)

e = a[0:2,0:2]
print("Sub Array :",e)

a[1:2,1:2] = 99
print("Modified Array :",a)


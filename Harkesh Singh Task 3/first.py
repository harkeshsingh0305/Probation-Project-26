import numpy as np

a = np.random.randint(1,100,10)
print(a)

print("Maximum Element :",np.max(a))

print("Minimum Element :",np.min(a))


print("Mean :",np.mean(a))
print("Sum :",np.sum(a))

print("Max Value Index :",np.argmax(a))
print("Min Value Index :",np.argmin(a))

print("Sorted :",np.sort(a))

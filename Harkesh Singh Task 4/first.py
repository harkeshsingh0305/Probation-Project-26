import numpy as np
import pandas as pd

a = pd.Series(np.random.randint(1,101,10))
print(a)

print("First 5 Elements :\n",a.head())
print("Last Five elements :\n",a.tail())

print("Maximum Value :",a.max())
print("Minimum Value :",a.min())

print("Mean Of Series :",a.mean())

print("List :",a.tolist())
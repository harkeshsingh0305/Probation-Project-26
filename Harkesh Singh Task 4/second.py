import numpy as np
import pandas as pd

students = {
    'Name':['Adi','Babby','Candy', 'Dior', 'Ena'],
    'Age':[20,21,19,22,20],
    'Marks':[85,90,75,95,88]
}
a = pd.DataFrame(students)


print(a)

print("First Three Row :\n",a.head(3))

print("Name Column :\n",a['Name'])

b = a[a['Marks']>85]
print("Marks greater than 85:\n",b)

a['Grade']=['B','A','C','A','B']
print(a)

c = a.drop("Age",axis=1)
print(c)
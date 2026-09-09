import numpy as np
import pandas as pd

Students = {
    "Name":["Adi","Ani","Anu","Anju","Aryan","Bila","Sita","Ram","Bheem","Arjun"],
    "Maths":np.random.randint(50,101,10),
    "Science":np.random.randint(50,101,10),
    "English":np.random.randint(50,101,10)
}

a = pd.DataFrame(Students)
print(a)

b = a[["Maths","Science","English"]].mean()
print("Mean :",b)

a["Total"] = a["Maths"] + a["Science"] + a['English']
print("Topper :",a.loc[a["Total"].idxmax()])



a["Result"]=a["Total"].apply(lambda x:"Pass" if x>=150 else "Fail")
print(a)

print("Sorted By Total Marks :",a.sort_values("Total",ascending=False))




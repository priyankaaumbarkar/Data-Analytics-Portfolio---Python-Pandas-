import pandas as pd
df=pd.DataFrame({

    "name":["Priyanka","Vaishali","Divya","Vaishnavi"],
    "marks":[99,89,67,87],
    "dept":["computer","civil","AI","ML"]
})

print("Original Date:\n",df)

print("\nSubset(marks>50):\n",df[df["marks"]>50])

print("\nsorted by marks(ascending):\n",df.sort_values("marks"))

print("\nsorted by marks(descending):\n",df.sort_values("marks",ascending=False))

print("\nGrouping(Average marks by department):\n",
df.groupby("dept")["marks"].mean())

print("\nmean=",df["marks"].mean())
print("\nmedian=",df["marks"].median())
print(df["marks"].mode())
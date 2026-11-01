import pandas as pd

data = pd.read_csv("dataset/reviews.csv", nrows=5)
print(data.columns)
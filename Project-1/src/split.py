import pandas as pd
from sklearn.model_selection import train_test_split

file_path= "/Users/akshayrao/dev/mlops/Project-1/artifacts"

df = pd.read_csv(f"{file_path}/Hotel_Reservations.csv")

train_df, test_df = train_test_split(df, test_size=0.2, random_state=108)

train_df.to_csv(f"{file_path}/train.csv", index=False)
test_df.to_csv(f"{file_path}/test.csv", index=False)

print("✅ CSVs saved: train.csv and test.csv")
import pandas as pd

path = "data/raw/telco_customer_churn.csv"
df = pd.read_csv(path)

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nChurn distribution:")
print(df["Churn"].value_counts(dropna=False))
print("\nTotalCharges type:", df["TotalCharges"].dtype)
print("Blank TotalCharges:", df["TotalCharges"].isna().sum())
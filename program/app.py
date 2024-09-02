import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('files/Transactions/July.csv')

# Display the DataFrame

print(df)

amount = df.groupby(['Category'])
print("this is amount",amount)
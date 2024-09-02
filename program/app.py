import pandas as pd
from datetime import datetime


def get_month_now():
    # Get the current date and time
    now = datetime.now()
    # Convert to month's name
    month_name = now.strftime('%B')

    return month_name


# Read the CSV file into a DataFrame
df = pd.read_csv('files/Transactions/July.csv')


def generate_summary():
    #Group the data frame according to the category
    categorized_transaction = df.groupby('Category')

    #initializing a dictionary to store the summary
    summary = {}

    for category, details in categorized_transaction:
        #convert the amount data type and sum up for each category
        summary[category] = details['Amount'].convert_dtypes().sum()

    return summary

print("Summary of ", get_month_now())
print(generate_summary())
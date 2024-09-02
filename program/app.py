import pandas as pd
from module.file_generation import generate_bar_chart, create_summary_pdf
from module.utils import get_month_now

def is_csv_file(file_path):
    # Check if the file path ends with '.csv'
    if file_path.lower().endswith('.csv'):
        return True
    return False


def generate_summary(df):
    #Group the data frame according to the category
    categorized_transaction = df.groupby('Category')

    #initializing a dictionary to store the summary
    summary = {}

    for category, details in categorized_transaction:
        #convert the amount data type and sum up for each category
        summary[category] = details['Amount'].convert_dtypes().sum()

    return summary




def main():
    file_path_entered = input("ENTER the full file path of the transaction csv \n")
    print(file_path_entered)

    #check if it is a csv
    if is_csv_file(file_path_entered):
        try:
            df = pd.read_csv(file_path_entered)
        except ExceptionGroup as error:
            print("Reading CSV ERROR")

    print("Summary of ", get_month_now())



    # Separate rows where 'category' is 'income'
    income_df = df[df['Category'] == 'Income']

    # Separate rows where 'category' is not 'income'
    expenses_df = df[df['Category'] != 'Income']

    summary = generate_summary(expenses_df)
    generate_bar_chart(summary)
    print(summary)
    print(create_summary_pdf(summary))

main()
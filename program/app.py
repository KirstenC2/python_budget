import pandas as pd
from module.file_generation import generate_bar_chart, create_summary_pdf
from module.utils import get_today_month_name, count_csv_files
import os


def is_csv_file(file_path):
    # Check if the file path ends with '.csv'
    if file_path.lower().endswith('.csv'):
        return True
    return False



def store_csv_to_dataframe(file_name_list, file_directory):
    print(file_name_list)
    monthly_data={}
    #iterate each file in the list
    for file in file_name_list:
        
        file_path = file_directory+'/'+file
        
        #clearing file extension for naming generated folders
        file_name_without_ext = str(file).split('.')[0]

        #check if it is a csv
        if is_csv_file(file_path):
            try:
                monthly_data[file_name_without_ext] = pd.read_csv(file_path)
            except ExceptionGroup as error:
                print("Reading CSV ERROR")

    return monthly_data

def get_expense_summary(data):
    annual_summary = {}
    for month in data.keys():

        print("----------------------------------------------")
        # expenses_df = csv_data[month] #data type : pandas dataframe
        # print("data type", type(expenses_df))


        # category_df = csv_data[month]['Category'] #data type: pandas series
        # print("data type", type(category_df))
        
        #Sum up all expenses based on category

        #data type: pandas series
        summary_expenses = data[month].groupby('Category')['Amount'].sum()
        annual_summary[month]=summary_expenses

    return annual_summary
    

def main():
    file_directory = 'Files/Transactions'
    file_count, file_name_list = count_csv_files(file_directory)

    print("You have ",file_count,'csv files in Transaction folder')
    print("----------------------------------")

    #iterating each csv files in the folder 
    csv_data = store_csv_to_dataframe(file_name_list,file_directory)
    monthly_distribution = get_expense_summary(csv_data)

    generate_bar_chart(monthly_distribution) #sending dictionary to generate bar chart
    

    print("----------------------------------")
        

    # #get the summary from dataframe (data in csv dile)
    # summary = generate_summary(expenses_df)
    # #then use the summary data ( sum of each category expense) to generate bar chart
    # 

    # create_summary_pdf(summary)

main()
import pandas as pd
from module.file_processor import *
from module.utils import get_today_month_name, count_csv_files
import os
from datetime import datetime


def raw_data_process(file_name_list, file_directory):
    """
    - checking is it csv files
    - reading csv to dataframe
    - splitting off income and expenses

    args:
    file_name_list
    file_directory(string) : 

    
    """
    monthly_data={}
    #iterate each file in the list
    for file in file_name_list:

        file_path = file_directory+'/'+file
        
        #clearing file extension for naming generated folders
        month = str(file).split('.')[0] #file name without extension

        #check if it is a csv
        if is_csv_file(file_path):
            try:
                # Read the CSV file into a DataFrame
                all_data = pd.read_csv(file_path)
                
                # Separate rows where Category is 'Income' into a new DataFrame
                df_income = all_data[all_data["Category"] == "Income"]
                
                # Check if there are no income rows
                if len(df_income) == 0:
                    print(file, "no income, add zero income...")
                    
                    # Create a new row for zero income as a DataFrame
                    zero_income = pd.DataFrame([{
                        "Date": "",
                        "Notes": "No income entry",
                        "Category": "Income",
                        "Amount": 0
                    }])
                    
                    # Concatenate the new row with the original DataFrame
                    all_data = pd.concat([all_data, zero_income], ignore_index=True)
                    df_income = all_data[all_data["Category"] == "Income"]
                # Separate rows where Category is not 'Income' into another DataFrame
                df_expenses = all_data[all_data["Category"] != "Income"]

                # Store the expenses DataFrame in the monthly_data dictionary
                monthly_data[month] = {"expenses": df_expenses,"income":df_income}


            except ExceptionGroup as error:
                print("Reading CSV ERROR")

    return monthly_data

def get_total_of_each_group(data):
    """
    category here
    = F&B, Mobile, Entertainment, ....

    args:
    data(dataframe)
    - data(month) each months contains two series: income and expenses

    return:
    ttl (dict type)
    - total of each category such as F&B, Entertainment, mobile, ....
    """
    ttl = {}
    for month in data.keys():
        if len(data[month]["income"]) != 0:
            ttl_income = data[month]["income"].groupby('Category')['Amount'].sum()
        
        ttl_expenses = data[month]["expenses"].groupby('Category')['Amount'].sum()
        
        ttl[month]={"expenses": ttl_expenses,"income": ttl_income}



    return ttl
    
def calculate_monthly_total(monthly_data):
    """
    Calculating total expenses of each month.
    
    Args:
    - monthly_data (dict): storing month's different expenses value

    Returns:
    - monthly_total (dict): monthly total value
        {key:value}
        {"July": 123.00}

    """
    monthly_total = {}

    # category here: income, expense
    for category in monthly_data.keys():
        #sum up all amount for expense/ income
        
        monthly_total[category] = monthly_data[category].values.sum()
        

    return monthly_total # dictionary data type

def main():

    # folder_path = input('Enter the folder path where contains all the csv files: \n \n > ')
    file_directory = 'Files/Transactions'
    file_count, file_name_list = count_csv_files(file_directory)
    print("You have ",file_count,'csv files in Transaction folder')

    #Data Processing (Monthly Transactions from different csv files)
    data = raw_data_process(file_name_list,file_directory)
    monthly_distribution_in_dict = get_total_of_each_group(data) #returned dictionary
    print("This is the monthly budget and finance details")
    print(monthly_distribution_in_dict)
    print("----------------------------------------------")
    #Calculation of Monthly total income expenses
    annual_summary = {}
    for month in monthly_distribution_in_dict.keys():
        ExpenseIncomeMonthlySeries = pd.Series(calculate_monthly_total(monthly_distribution_in_dict[month]))
        annual_summary[month] = ExpenseIncomeMonthlySeries
    print("Monthly expenses and incomes summary")
    print(annual_summary)

    # Summary file generating process
    # saving_status = save_summary_to_csv(annual_summary)
    # if(saving_status == True):
    #     print("Saved Successfully")
    # else:
    #     print("Failed in saving file")
    




main()
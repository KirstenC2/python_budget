import pandas as pd
from module.file_processor import generate_bar_chart, is_csv_file
from module.utils import get_today_month_name, count_csv_files
import os

def raw_data_process(file_name_list, file_directory):
    """
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

def get_expense_summary(data):
    """
    args:
    data(dataframe)
    - data(month) each months contains two series: income and expenses

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


    file_directory = 'Files/Transactions'
    file_count, file_name_list = count_csv_files(file_directory)
    print("You have ",file_count,'csv files in Transaction folder')

    #iterating each csv files in the folder 
    data = raw_data_process(file_name_list,file_directory)
    

    monthly_distribution = get_expense_summary(data)

    for month in monthly_distribution.keys():
        print("Summary of ",month)
        print(calculate_monthly_total(monthly_distribution[month]))
    # # monthly_distribution #-- this is series
    
    # print("calculating monthly total expenses")
    # 
    #generate_bar_chart(monthly_distribution) #sending dictionary to generate bar chart



    # create_summary_pdf(summary)

main()
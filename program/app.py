import pandas as pd
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

from tabulate import tabulate

def get_month_now():
    # Get the current date and time
    now = datetime.now()
    # Convert to month's name
    month_name = now.strftime('%B')

    return month_name


def generate_summary(df):
    #Group the data frame according to the category
    categorized_transaction = df.groupby('Category')

    #initializing a dictionary to store the summary
    summary = {}

    for category, details in categorized_transaction:
        #convert the amount data type and sum up for each category
        summary[category] = details['Amount'].convert_dtypes().sum()

    return summary


def is_csv_file(file_path):
    # Check if the file path ends with '.csv'
    if file_path.lower().endswith('.csv'):
        return True
    return False

def generate_bar_chart(data):

    month = get_month_now()
    directory = 'C:/Users/User/Desktop/Python_Budget/Files'
    file_path = os.path.join(directory, f'{month}_bar.png')

    # Unpack data into two lists: categories and values
    categories = list(data.keys())
    values = list(data.values())

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(categories, values, color='blue')

    # Add titles and labels
    plt.title('Bar Chart')
    plt.xlabel('Categories')
    plt.ylabel('Values')

    # Save the chart as a PNG image
    plt.savefig(file_path)
    plt.close()



def create_summary_pdf(summary_text):
    month = get_month_now()

    directory = 'C:/Users/User/Desktop/Python_Budget/Files'
    file_path = os.path.join(directory, f'{month}.pdf')
    chart_path = os.path.join(directory,f'{month}_bar.png')

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Create a PDF canvas object
    c = canvas.Canvas(file_path, pagesize=letter)
    
    # Define the title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 750, f"Report of {month}")

    # Add the summary text
    c.setFont("Helvetica", 12)
    text_object = c.beginText(72, 380)  # Starting position for the text
    
    # Convert dictionary to a string (e.g., formatted as key-value pairs)
    if isinstance(summary_text, dict):
        summary_lines = [f"{key}: {value}" for key, value in summary_text.items()]
        summary_string = "\n".join(summary_lines)
    else:
        summary_string = str(summary_text)

    # Split the summary string into lines and add to the text object
    lines = summary_string.split('\n')
    for line in lines:
        text_object.textLine(line)
    
    #put in chart
    c.drawImage(chart_path, 42, 430, width=540, height=300) 
    #put in Summary subtitle
    c.drawString(72, 400, f"Summary of {month}",2,0.2)
    #load in expenses data 
    c.drawText(text_object)
    
    # Save the PDF
    c.save()
    print(f"PDF created at {file_path}")


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
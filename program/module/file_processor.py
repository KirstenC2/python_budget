from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from module.utils import get_today_month_name
import os
from datetime import datetime

def generate_bar_chart(data):
    directory = 'Files/Reports/Charts'
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists

    # Iterate over the data
    for month, month_data in data.items():
        if isinstance(month_data, np.ndarray):
            if month_data.ndim == 2 and month_data.shape[1] == 2:
                categories = month_data[:, 0]
                values = month_data[:, 1]
            else:
                print(f"Data for {month} is not in the expected format.")
                continue
        elif isinstance(month_data, pd.Series):
            categories = month_data.index
            values = month_data.values
        elif isinstance(month_data, dict):
            categories = list(month_data.keys())
            values = list(month_data.values())
        else:
            print(f"Data for {month} is not in the expected format.")
            continue
        
        file_path = os.path.join(directory, f'{month}_bar.png')
        
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 10))
        
        # Plot the bar chart
        ax.bar(categories, values, color='blue')
        ax.set_title(f'{month} Expenses Bar Chart')
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        
        # Save the chart as a PNG image
        plt.savefig(file_path)
        plt.close()
        
        print(f"Bar chart with table saved for {month} at {file_path}")

        
def is_csv_file(file_path):
    # Check if the file path ends with '.csv'
    if file_path.lower().endswith('.csv'):
        return True
    return False

def create_summary_pdf(summary_text):
    month = get_today_month_name()

    directory = 'Files/Reports'
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


def save_summary_to_csv(monthly_summary_value):
    """
    args: 
    monthly_summary_value(dict type)

    return: 
    boolean
    """
    try:
        annual_summary_df = pd.DataFrame(monthly_summary_value)
        current_year = str(datetime.now().year)
        annual_summary_df.to_csv('Files/Reports/Summary/'+ current_year + ".csv")
        return True
    except ExceptionGroup as error:
        print(error)
        return False
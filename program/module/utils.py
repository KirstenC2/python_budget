from datetime import datetime
import os

def get_today_month_name():
    # Get the current date and time
    now = datetime.now()
    # Convert to month's name
    month_name = now.strftime('%B')

    return month_name


def count_csv_files(directory):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter the list to include only .csv files
    csv_files = [file for file in files if file.endswith('.csv')]
    
    # Extract the base filenames (without directory paths)
    csv_files_names = [os.path.basename(file) for file in csv_files]

    # Count the number of CSV files
    csv_count = len(csv_files)
    
    return csv_count, csv_files_names
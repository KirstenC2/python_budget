from datetime import datetime

def get_month_now():
    # Get the current date and time
    now = datetime.now()
    # Convert to month's name
    month_name = now.strftime('%B')

    return month_name
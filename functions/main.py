from flask import Flask, render_template
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

# def format_date(date):
#     return date.strftime("%A, %B %d, %Y").replace(',', ', ').replace(' 0', ' ')

# def get_schedule_for_date(schedule_df, date, sheet_name):
#     formatted_date = format_date(date)
#     try:
#         return schedule_df[schedule_df[sheet_name]['Date'] == formatted_date]
#     except KeyError as e:
#         return f"KeyError: {e}. Please check the column names in the Excel sheet."
    
# def format_class_info(schedule_df, sheet_name):
#     class_info = schedule_df.applymap(lambda x: x if pd.notna(x) else "")
    
#     classes_2d = []
#     for row in class_info.values:
#         row_classes = []
#         for room, subject in zip(class_info.columns, row):
#             room_name = f"{room[0]} ({room[1]})" if isinstance(room, tuple) and len(room) == 2 else str(room)
#             room_name = room_name.replace(f'{sheet_name} ', '')
#             row_classes.append(subject if subject else "No Class")
#             print('mano',row_classes)
#         classes_2d.append(row_classes)
#     return classes_2d

# def get_schedule(schedule_file):
#     # Read the Excel file, skipping the first two header rows
#     schedule_df = pd.read_excel(schedule_file, header=[0, 1])

#     # Replace NaN values with blank spaces
#     schedule_df = schedule_df.fillna('--')

#     # Dates
#     today = datetime.now()
#     tomorrow = today + timedelta(days=1)
#     sheet_name = 'PGP 28 Term-I Class Schedule'

#     # Get schedules for today and tomorrow
#     today_schedule = get_schedule_for_date(schedule_df, today, sheet_name)
#     tomorrow_schedule = get_schedule_for_date(schedule_df, tomorrow, sheet_name)

#     if isinstance(today_schedule, str):
#         return today_schedule  # Return the error message if KeyError occurred

#     if isinstance(tomorrow_schedule, str):
#         return tomorrow_schedule  # Return the error message if KeyError occurred

#     # Format class information
#     classes_today_2d = format_class_info(today_schedule, sheet_name)
#     classes_tomorrow_2d = format_class_info(tomorrow_schedule, sheet_name)

#     return format_date(today), format_date(tomorrow), classes_today_2d, classes_tomorrow_2d

# Function to determine the classes for the current day
def classes_for_today(schedule_file):
    # Read the Excel file, skipping the first two header rows
    schedule_df = pd.read_excel(schedule_file, header=[0, 1])

    # Replace NaN values with blank spaces
    schedule_df = schedule_df.fillna('--')
    
    # Get today's date in the same format as the schedule
    today = datetime.now().strftime("%A, %B %d, %Y").replace(',', ', ')

    # Handling Windows systems where %-d might not be supported
    if '%-d' not in datetime.now().strftime("%A, %B %d, %Y"):
        today = datetime.now().strftime("%A, %B %d, %Y").replace(' 0', ' ')

    # Tomorrow date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d, %Y").replace(',', ', ').replace(' 0', ' ')

    # Filter the dataframe for today's date
    try:
        today_schedule = schedule_df[schedule_df['PGP 28 Term-I Class Schedule']['Date'] == today]
    except KeyError as e:
        return f"KeyError: {e}. Please check the column names in the Excel sheet."

    # Filter the dataframe for tomorrow's date
    try:
        tomorrow_schedule = schedule_df[schedule_df['PGP 28 Term-I Class Schedule']['Date'] == tomorrow]
    except KeyError as e:
        return f"KeyError: {e}. Please check the column names in the Excel sheet."
    
        
    class_details = today_schedule.iloc[:, :]
    class_info = class_details.applymap(lambda x: x if pd.notna(x) else "")

    class_details_tomorrow = tomorrow_schedule.iloc[:, :]
    class_info_tomorrow = class_details_tomorrow.applymap(lambda x: x if pd.notna(x) else "")

    # Initialize an empty list to hold all rows
    classes_today_2d = []
    classes_tomorrow_2d = []

    for row in class_info.values:
        # Initialize an empty list to hold the formatted room-subject pairs for this row
        row_classes = []
    
        # Iterate over the columns (rooms) and corresponding subjects in the current row
        for room, subject in zip(class_info.columns, row):
            # Assuming room is a tuple with two values
            if isinstance(room, tuple) and len(room) == 2:
                room_name = f"{room[0]} ({room[1]})"
            else:
                room_name = str(room)
            
            room_name = room_name.replace('PGP 28 Term-I Class Schedule ', '')
            # Format the room-subject pair and append to the row_classes list
            if subject:
                row_classes.append(f"{subject}")
            else:
                row_classes.append(f"No Class")
    
        # Append the row_classes list to the main classes_today_2d list
        classes_today_2d.append(row_classes)

    for row in class_info_tomorrow.values:
        # Initialize an empty list to hold the formatted room-subject pairs for this row
        row_classes = []
    
        print(class_info_tomorrow)
        # Iterate over the columns (rooms) and corresponding subjects in the current row
        for room, subject in zip(class_info_tomorrow.columns, row):
            # Assuming room is a tuple with two values
            if isinstance(room, tuple) and len(room) == 2:
                room_name = f"{room[0]} ({room[1]})"
            else:
                room_name = str(room)
            
            room_name = room_name.replace('PGP 28 Term-I Class Schedule ', '')
            # Format the room-subject pair and append to the row_classes list
            if subject:
                row_classes.append(f"{subject}")
            else:
                row_classes.append(f"No Class")
    
        # Append the row_classes list to the main classes_today_2d list
        classes_tomorrow_2d.append(row_classes)

    return today,tomorrow,classes_today_2d,classes_tomorrow_2d


@app.route('/')
def index():
    today, tomorrow, schedule, tomorrow_schedule = classes_for_today('PGP 28 Term I Schedule.xlsx')
    return render_template('index.html', today=today, tomorrow=tomorrow, schedule=schedule, tomorrow_schedule=tomorrow_schedule)

if __name__ == '__main__':
    app.run(debug=True)

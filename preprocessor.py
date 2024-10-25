import re
import pandas as pd

def preprocess(data):
    # Updated pattern for date and time format with two-digit year
    pattern = r'\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame with messages and corresponding dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime format with two-digit year
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract user and message content
    users = []
    messages = []
    for message in df['user_message']:
        # Splitting based on the first occurrence of ': ' which indicates user and message split
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 1:  # If the message has a username
            users.append(entry[1])  # First part after split is user
            messages.append(" ".join(entry[2:]))  # The remaining part is the message
        else:
            # System notifications or group messages without a specific user
            users.append('group_notification')
            messages.append(entry[0])

    # Add user and message columns, drop user_message
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Additional date and time-based columns
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create a 'period' column indicating hour ranges (e.g., 23-00, 00-1)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour + 1}")
        else:
            period.append(f"{hour}-{hour + 1}")
    df['period'] = period

    return df

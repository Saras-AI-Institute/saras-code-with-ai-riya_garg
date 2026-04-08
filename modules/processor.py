import pandas as pd


def load_data():
    """
    Load the health data CSV file, handle missing values, convert the 'date' column, 
    and return the cleaned DataFrame.
    """
    # Step 1: Read the CSV file into a pandas DataFrame
    data = pd.read_csv('data/health_data.csv')

    # Step 2: Fill missing steps with the median value of steps
    if 'steps' in data.columns:
        median_steps = data['steps'].median()
        data['steps'].fillna(median_steps, inplace=True)

    # Step 3: Fill missing sleep_hours with 7.0
    if 'sleep_hours' in data.columns:
        data['sleep_hours'].fillna(7.0, inplace=True)

    # Step 4: Fill missing heart_rate_bpm with 68
    if 'heart_rate_bpm' in data.columns:
        data['heart_rate_bpm'].fillna(68, inplace=True)

    # Step 5: Fill other columns with their median values
    for column in data.columns:
        if column not in ['steps', 'sleep_hours', 'heart_rate_bpm', 'date']:
            median_value = data[column].median()
            data[column].fillna(median_value, inplace=True)

    # Step 6: Convert the 'date' column to datetime objects
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])

    # Step 7: Return the cleaned DataFrame
    return data

def calculate_recovery_score(df):
    """
    Calculate a recovery score for each entry in the DataFrame based on sleep hours, heart rate, and steps.
    Adds a new column 'Recovery_score' to the DataFrame with a score between 0 and 100.
    """
    # Initialize the recovery score to 0
    df['Recovery_score'] = 0

    # Iterate over each row to calculate the recovery score
    for index, row in df.iterrows():
        score = 50  # Start with a base score of 50

        # Adjust score based on sleep_hours
        if row['sleep_hours'] >= 7:
            score += 20  # Good sleep boosts score
        elif row['sleep_hours'] < 6:
            score -= 20  # Poor sleep reduces score

        # Adjust score based on heart_rate_bpm
        if row['heart_rate_bpm'] <= 60:
            score += 20  # Lower heart rate improves recovery
        elif row['heart_rate_bpm'] >= 90:
            score -= 10  # Higher heart rate slightly reduces recovery

        # Adjust score based on Steps
        if row['steps'] >= 12000:
            score -= 5  # High activity can add strain, reduces score slightly

        # Ensure the score stays within 0 to 100
        score = max(0, min(100, score))

        df.at[index, 'Recovery_score'] = score

    return df


def process_data():
    """
    Process the data by loading it and calculating the recovery score.
    This will return the processed DataFrame.
    """
    df = load_data()  # Call load_data to get the cleaned DataFrame
    df = calculate_recovery_score(df)  # Add Recovery Score
    return df  # Return the processed DataFrame


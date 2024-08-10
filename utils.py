import pandas as pd
import numpy as np

def fetch_medal_tally(df, year, country):
    """
    Fetches the medal tally based on the specified year and country.

    Parameters:
    - df (DataFrame): DataFrame containing Olympic data.
    - year (str or int): Year filter ('Overall' or specific year).
    - country (str): Country filter ('Overall' or specific country).

    Returns:
    - DataFrame: Medal tally DataFrame sorted by total medals.
    """
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def country_year_list(df):
    """
    Retrieves unique years and countries from the DataFrame.

    Parameters:
    - df (DataFrame): DataFrame containing Olympic data.

    Returns:
    - tuple: Lists of unique years and countries.
    """
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries

def data_over_time(df, col):
    """
    Computes the count of unique values over time for a specified column.

    Parameters:
    - df (DataFrame): DataFrame containing Olympic data.
    - col (str): Column name to analyze over time.

    Returns:
    - DataFrame: Count of unique values over time.
    """
    data_over_time_df = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(by='Year')
    return data_over_time_df



def most_successful(df, sport):
    """
    Computes the top successful athletes in a specific sport or overall.

    Parameters:
    - df (DataFrame): DataFrame containing Olympic data.
    - sport (str): Sport name ('Overall' or specific sport).

    Returns:
    - DataFrame: Top successful athletes in the sport.
    """
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals by athlete name
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']

    # Merge with original DataFrame to get additional athlete details
    successful_df = pd.merge(medal_counts.head(15), df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

    return successful_df
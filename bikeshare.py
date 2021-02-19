import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june','all']
days = ['monday', 'muesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']
month_day=['month', 'day', 'both', 'none']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """    
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city or washington). HINT: Use a while loop to handle invalid inputs  
    print('Would you like to see data for : ')
    city_list = []
    for cities in CITY_DATA:
        city_list.append(cities)        
        print('              ==> {}    '.format(cities.title()))        
    city = input().lower()
    while city not in(CITY_DATA.keys()):
        print('ERROR... Would you like to see data for   ')
        for cities in CITY_DATA:
            city_list.append(cities)            
            print('                                            ==>  {}'.format(cities.title()))
        city = input('              choose one city :').lower()
    print('You have chosen the ',city.upper(),' city. If thats not what you want to do, restart the program now.')
    


    # get user input for filter type (month, day or both).    
    print('Would you like to filter the data by :')
    month_day_list = []
    for month_days in month_day:
        month_day_list.append(month_days)        
        print('              ==> {}    '.format(month_days.title()))
    filter = input().lower()
    while filter not in month_day:
        print('ERROR ..... provided invalid filter, Would you like to filter the data by :')        
        for month_days in month_day:
            month_day_list.append(month_days)            
            print('              ==> {}    '.format(month_days.title()))
        filter = input().lower()
    
    # get user input for month (january', 'february', 'march', 'april', 'may', 'june')    
    if filter == 'month' or filter == 'both':        
        print("Which month ? :")
        month_list = []
        for monthss in months:
            month_list.append(monthss)        
            print('              ==> {}    '.format(monthss.title()))
        month = input().lower()
        while month not in months:
            print("ERROR.....,You provided invalid month, please you have to make a choice between : ")
            for monthss in months:
                month_list.append(monthss)            
                print('              ==> {}    '.format(monthss.title()))
            month = input('Which month ? : ').lower()
            print('You have chosen the ',month.upper(),' city. If thats not what you want to do, restart the program now.')
    else:
        month = 'all'


    # get user input for day of week (all, monday, tuesday, ... sunday)    
    if filter == 'day' or filter == 'both':
        print('Which day ?:')
        day_list = []
        for dayss in days:
            day_list.append(dayss)        
            print('              ==> {}    '.format(dayss.title()))       
        day = input().lower()
        while day not in days:
            print("ERROR ...,You provided invalid day, please you have to make a choice between : ")
            day_list = []
            for dayss in days:
                day_list.append(dayss)            
                print('              ==> {}    '.format(dayss.title()))            
            day = input('Which day ? : ').lower()
            print('You have chosen the ',day.upper(),' . If thats not what you want to do, restart the program now.')
    else:
        day = 'all'

        #Separation line
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting the month and day of the week from the start time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month
    if month != 'all':
        # use the index of the list of months to get the corresponding int by starting with 1
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    month = df['month'].mode()[0]
    print(f'The most common month is: {months[month-1]}')

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    print(f'The most common day of week is: {day}')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f'The most common start hour is: {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'The most popular start station is: {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'The most popular end station is: {popular_end_station}')

    # display most frequent combination of start station and end station trip
    popular_trip = df['Start Station'] + ' to ' + df['End Station']
    print(f'The most popular trip is: from {popular_trip.mode()[0]}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    from datetime import timedelta as td
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days =  total_travel_duration.days
    hours = total_travel_duration.seconds // (60*60)
    minutes = total_travel_duration.seconds % (60*60) // 60
    seconds = total_travel_duration.seconds % (60*60) % 60
    print(f'Total travel time is: {days} days {hours} hours {minutes} minutes {seconds} seconds')

    # display mean travel time
    average_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    days =  average_travel_duration.days
    hours = average_travel_duration.seconds // (60*60)
    minutes = average_travel_duration.seconds % (60*60) // 60
    seconds = average_travel_duration.seconds % (60*60) % 60
    print(f'Average travel time is: {days} days {hours} hours {minutes} minutes {seconds} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users info."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    print('\n\n')

    # Display counts of gender
    print('\nCalculating User counts of each gender...\n')
    if 'Gender' in(df.columns):
        print(df['Gender'].value_counts())
        print('\n\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in(df.columns):
        year = df['Birth Year'].fillna(0).astype('int64')
        print(f'earliest, most recent, most common year of birth (only available for NYC and Chicago): {year.min()}\nmost recent is: {year.max()}\n most comon birth year is: {year.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Ask the user if he wants to display the raw data and print 5 rows at time"""
    raw = input("\nWould you like to diplay raw data ?'yes' to display data, any key to contunue :\n")
    if raw.lower() == 'yes':
        count = 0
        while True:
            print(df.iloc[count: count+5])
            count += 5
            ask = input('Next 5 raws? yes or no :')
            if ask.lower() != 'yes':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input("\nWould you like to restart? Enter 'yes' to restart, any key to stop .\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

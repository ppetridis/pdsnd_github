import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago','new york city','washington']
    city = ''
    while city not in cities:
        city = input("Would you like to see data from Chicago, New York City or Washington?\n").lower()
        if city not in cities:
            print("That's not one of the options - check your city name and try again!\n")
    # TO DO: get user input for month (all, january, february, ... , june)
    month_or_day = input("Would you like to filter the data by month, day, or neither?\n").lower()
    month = 'all'
    day = 'all'
    if month_or_day == 'month':
        months = ['january','february','march','april','may','june']
        month = ''
        while month not in months:
            month = input("Which month's data would you like to see? Please choose a month between January and June:\n").lower()
            if month not in months:
                print("You may have spelled it wrong or picked a month outside the range. Try again!\n")
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    elif month_or_day == 'day':
        while True:
            day = input("Which day's data would you like to see? Please type the full day name:\n").lower()
            days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
            if day in days:
                break
            else:
                print("You may have spelled it wrong or written it incorrectly. Try again!\n")

    print (city, ' ', month, ' ', day)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common travel month is: {}".format(popular_month))
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common travel day of the week is: {}".format(popular_day))
    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most common hour to start travel is: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + " - and - " + df['End Station']
    popular_station_combo = df['Station Combo'].mode()[0]
    print("The most commonly used station combo is: {}".format(popular_station_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['travel_time'] = df['End Time'] - df['Start Time']
    # TO DO: display total travel time
    total_travel_time = df['travel_time'].sum()
    total_trip_duration = df['Trip Duration'].sum()
    print("The total travel time is: {} seconds - or - {}".format(total_trip_duration, total_travel_time))
    # TO DO: display mean travel time
    mean_travel_time = df['travel_time'].mean()
    mean_trip_duration = df['Trip Duration'].mean()
    print("The average travel time is: {} seconds - or - {}".format(mean_trip_duration, mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The different types of users are:\n{}\n".format(user_types))
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print("The number of people in each gender is:\n{}\n".format(genders))
    else:
        print("Washington doesn't have any gender data!")
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        print("The earliest birth year is: {}".format(earliest_birth))
        latest_birth = int(df['Birth Year'].max())
        print("The most recent birth year is: {}".format(latest_birth))
        common_year = int(df['Birth Year'].mode()[0])
        print("The most common birth year is: {}".format(common_year))
    else:
        print("Washington doesn't have any birth year data!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw user data in groups of 5"""

    i = 0
    raw_data = input('\nWould you like to see raw user data? Enter yes or no.\n').lower()

    while True:
        if raw_data.lower() != 'yes':
            break
        print(df[i:i+5])
        raw_data = input('\nWould you like to see more raw user data? Enter yes or no.\n').lower()
        i +=5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

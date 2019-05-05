import time
import pandas as pd
import numpy as np
import calendar
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns


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
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    stop = True #used the stop variable to be able to break out of the nested loops.

    while stop:
        user_choice = str(input('\nEnter the city you would like to analyze: Chicago, New York City or Washington.\n').title())
        if user_choice.lower() not in CITY_DATA.keys():
            print('\nInvalid city name, enter a valid city name!\n')
            continue
        else:
            print('You chose {}, if this is correct, continue, otherwise exit the program.'.format(user_choice))
            while stop:
                keep_going = str(input('\nWould you like to continue yes or no? ').title())
                if  keep_going == 'No':
                    print('\nExiting the program now.\n\nGood bye!')
                    raise SystemExit #used SystemExit to terminate the program after choosing the city.
                elif keep_going != 'Yes':  # Used this conditional to handle any typing error that the user may input.
                    print('\nYou must enter \'yes\' to continue or \'no\' to end the program!')
                    continue
                elif keep_going == 'Yes':
                    print('\nYou chose to continue!')
                    while stop:
                        user_input = str(input('\nPlease, choose how you would like to filter the data, by \'month\', \'day\', \'both\'; or \'none\' to see all available data?\n').title())
                        if user_input not in ['Month', 'Day', 'Both', 'None']:
                            print('\nPlease choose a valid filter!')
                        if user_input == 'None':
                            city = user_choice
                            month = 'all'
                            day = 'all'
                            print('\nRendering data with no filters...')
                            stop = False
                        elif user_input == 'Month':
                            city = user_choice
                            day = 'all'
                            print('\nYou chose a monthly filter!')
                            while stop:
                                month = str(input('\nEnter the month you would like to analyze, choose from the following:\n{}\n'.format(', '.join(list(calendar.month_name)[1:7]))).title())
                                if month not in list(calendar.month_name)[1:7]:
                                    print('\nInvalid input, please enter a valid month!')
                                    continue
                                else:
                                    print('\nAnalizing all {} data for {}...'.format(month, city))
                                    stop = False
                        elif user_input == 'Day':
                            city = user_choice
                            month = 'all'
                            print('\nYou chose a daily filter!')
                            while stop:
                                day = str(input('\nEnter the day of the week you would like to analyze, choose from the following:\n{}\n'.format(', '.join(list(calendar.day_name)))).title())
                                if day.lower() != 'all' and day not in list(calendar.day_name):
                                    print('\nInvalid input, enter a valid day of the week!')
                                    continue
                                else:
                                    print('\nAnalizing data for {} on {}s...'.format(city,day))
                                    stop = False
                        elif user_input == 'Both':
                            city = user_choice
                            print('Please enter the day of the week and the month you would like to analize!')
                            while stop:
                                month = str(input('\nEnter the month you would like to analyze first, choose form the following:\n{}\n'.format(', '.join(list(calendar.month_name)[1:7]))).title())
                                if month not in list(calendar.month_name)[1:7]:
                                    print('\nInvalid input, please enter a valid month!')
                                    continue
                                elif keep_going == 'Yes':
                                    while stop:
                                        day = str(input('\nEnter the day of the week you would like to analyze, choose from the following:\n{}\n'.format(', '.join(list(calendar.day_name)))).title())
                                        if day.lower() != 'all' and day not in list(calendar.day_name):
                                            print('\nInvalid input, enter a valid day of the week!')
                                            continue
                                        else:
                                            print('\nAnalizing data for {} during {}, on a {}...'.format(city, month, day))
                                            stop = False



    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('-'*40)
    return city.lower(), month.lower(), day


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
    df['day_of_week'] = df['Start Time'].dt.weekday_name


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


    # display the most common month


    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]


    popular_month = df['month'].value_counts().argmax()

    popular_day = df['day_of_week'].mode()[0]

    '''I decided to use the std to determine if all items in the column were the same
    in order to only diplay relevant information according to the filters chosen,
    for instance if all days are the same only diplay hour and month, or if all months
    are the same only display hour and day'''

    std_m = df['month'].std()
    std_d = df['Start Time'].dt.weekday.std()

    while True:
        m = std_m
        d = std_d
        if m == 0 and d == 0:
            print("The most popular hour to travel was {}.".format(popular_hour))
            break

        elif m > 0 and d > 0:
            print("The most popular month to travel was {}.".format(list(calendar.month_name)[popular_month]))
            print('\nThe most popular day to travel was {}.'.format(popular_day))
            print("\nThe most popular hour to travel was {}.".format(popular_hour))
            break

        elif m == 0:
            print('The most popular day to travel was {}.'.format(popular_day))
            print("\nThe most popular hour to travel was {}.".format(popular_hour))
            break

        else:
            print("The most popular month to travel was {}.".format(list(calendar.month_name)[popular_month]))
            print("\nThe most popular hour to travel was {}.".format(popular_hour))
            break


    # display the most common day of week

    # display the most common start hour


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].value_counts().argmax()
    print('Most people like to start their ride on, {}.'.format(most_common_start))


    # display most commonly used end station
    most_common_end = df['End Station'].value_counts().argmax()
    print('\nMost people like to end their ride on, {}.'.format(most_common_end))


    # display most frequent combination of start station and end station trip
    most_popular_combo = df.groupby(['Start Station', 'End Station']).size().argmax()
    print('\nThe most popular trip, begins at {}.'.format(' and finishes at '.join(most_popular_combo)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #I decided to display the time in a format that was more easier for any user to understand
    tota_travel = df['Trip Duration'].sum()
    print('Total travel time was, {}'.format(str(dt.timedelta(seconds=tota_travel))))


    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('\nAverage travel time was, {}'.format(str(dt.timedelta(seconds=mean_travel))))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print("The breakdown of user by category is:\n{}".format(user_types))


    # Display counts of gender


    if 'Gender' not in df.columns:
        print('\nSorry no available gender data for this city!')
    else:
        gender_type = df['Gender'].value_counts().to_frame()
        birth_years_min = df['Birth Year'].min()
        birth_years_max = df['Birth Year'].max()
        birth_years_common = df['Birth Year'].value_counts().argmax()
        print("\nThe breakdown of user by gender is:\n{}".format(gender_type))
        print("\nThe earliest recorded birth year for our users was: {}".format(str(birth_years_min)[:-2]))
        print("\nThe most recent recorded birth year for our users was: {}".format(str(birth_years_max)[:-2]))
        print("\nThe most common recorded birth year for our users was: {}".format(str(birth_years_common)[:-2]))


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

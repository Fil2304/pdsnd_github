import time
import pandas as pd
import numpy as np

"""  Here are all of the lists or dictionaries that will be used in the program!  """
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ['january','february','march','april','may','june','all']
day_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
decision_list = ['month','day','both']


#this function check if the given string inculdes any number, which is importannt for the initial user input
def hasNumbers(InputString):
    return any(char.isdigit() for char in InputString)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City, or Washington?: ')
            if (hasNumbers(city) or CITY_DATA.get(city.lower()) == None):
                raise ValueError
            print('It looks like you want to hear about {}! If that is not true, restart the program now!'.format(city.title()))
            break
        except ValueError:
            print('This is not a valid city, please check your input and try it again!')
        except KeyboardInterrupt:
            print('\nNo Input was taken! Try again!')



        # get user input on how they want to filter the data (which month, day and whether he wants to filter at all) and cover all possible exceptions that could happen
    while True:
        try:
            decision = input("Would you like to filter the data by month, day, both or not at all? Type 'none' for no time filter: ")
            month = None
            day = None

            if (decision == None or decision.lower() == 'none'):
                break

            if (hasNumbers(decision)):
                raise ValueError

            if (decision.lower() not in decision_list):
                raise ValueError

            if (decision.lower() == 'month' or decision.lower() == 'both'):
                while True:
                    try:
                        # get user input for month (all, january, february, ... , june)
                        month = input("Which month? January, February, March, April, May, or June? Or type 'all' to apply no month filter: ")
                        if (hasNumbers(month)):
                            raise ValueError
                        if (month.lower() not in month_list):
                            raise ValueError
                        break
                    except ValueError:
                        print('This is not a valid month, please check your input and try it again!')
                    except KeyboardInterrupt:
                        print('\nNo Input was taken!')
                        break

            if (decision.lower() == 'day' or decision.lower() == 'both'):
                while True:
                    try:
                        # get user input for day of week (all, monday, tuesday, ... sunday)
                        day = input("Which day? Type the full weekday name, f.e. 'Monday' or type 'all' to apply no day filter: ")
                        if (hasNumbers(day)):
                            raise ValueError
                        if (day.lower() not in day_list):
                            raise ValueError
                        break
                    except ValueError:
                        print('This is not a valid weekday, please check your input and try it again!')
                    except KeyboardInterrupt:
                        print('\nNo Input was taken!')
                        break

            break
        except ValueError:
            print('This is not a valid option to choose from, please check your input and try it again!')
        except KeyboardInterrupt:
            print('\nNo Input was taken!')
            break


    print('Just one moment... data is loading')
    print('And done! These are the results of your filters')
    print('-'*40)

    return city, month, day



def load_data(city, month = None, day = None):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter (optional since city is the only
              mandatory variable for the program, that's why the default is set to None)
        (str) day - name of the day of week to filter by, or "all" to apply no day filter (optional since city is the only
              mandatory variable for the program, that's why the default is set to None)
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    if month is None:
        #if the user does not want it, dont filter
        pass
    else:
        df['month'] = df['Start Time'].dt.month
        # if he does, filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            month = month_list.index(month.lower())+1
            # filter by month to create the new dataframe
            df = df[df['month'] == month]
            df.pop('month')

    if day is None:
        #if the user does not want it, dont filter
        pass
    else:
        # if he does, filter by day of week if applicable
        if day != 'all':
            df['day_of_week'] = df['Start Time'].dt.day_name()
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
            df.pop('day_of_week')

    return df
"""  Here start all of the functions, that calculate statistics or output the raw data!  """

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['common_month'] = df['Start Time'].dt.month_name()
    common_month = df['common_month'].mode()[0]
    print('The most common month is: ' + common_month )
    df.pop('common_month')

    # display the most common day of week
    df['common_day_of_week'] = df['Start Time'].dt.day_name()
    common_day_of_week = df['common_day_of_week'].mode()[0]
    print('The most common day of the week is:', common_day_of_week)
    df.pop('common_day_of_week')

    # display the most common start hour
    df['common_hour'] = df['Start Time'].dt.hour
    common_hour = df['common_hour'].mode()[0]
    print('The most common start hour is:', common_hour)
    df.pop('common_hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most commonly used end station is:', common_end)

    # display most frequent combination of start station and end station trip
    common_combination = ('From ' + df['Start Station'] + ' to the ' + df['End Station']).mode()[0]
    print('The most frequent combination of start station and end station trip is:\n', common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total traveltime: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Avg traveltime: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n', user_types)

    # Display counts of gender and if there is no such column in the DataFrame, it notifys the user
    try:
        gender = df['Gender'].value_counts()
        print('Counts of gender:\n',gender)
    except:
        print('No gender data available')

    # Display earliest, most recent, and most common year of birth and if there is no such column in the DataFrame, it notifys the user
    try:
        year1 = df['Birth Year'].min()
        year2 = df['Birth Year'].max()
        year3 = df['Birth Year'].mode()[0]
        print('The earliest year of birth:', year1)
        print('The most recent year of birth:', year2)
        print('The most common year of birth:', year3)
    except:
        print('No birth data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """This function prompt the user whether they would like want to see the raw data (basically the whole DataFrame,
    without the extra columns for the analysis, they already have been popped out). If the user answers 'yes,' then
    the script should print 5 rows of the data at a time, then ask the user if they would like to see 5 more rows of
    the data. The script should continue prompting and printing the next 5 rows at a time until the user chooses 'no,
    ' they do not want any more raw data to be displayed."""

    df = df.rename (columns = {'Unnamed: 0': 'ID'})
    n = 5
    while True:
        try:
            #get user input, whether he wants the raw data or not and also covering any possible exceptions that coudl arise
            decision = input("Would you like to view individual trip data? Type 'yes' or 'no': ")
            if (decision.lower() != 'no' and decision.lower() != 'yes'):
                raise ValueError
            if decision.lower() == 'no':
                break
            if decision.lower() == 'yes':
                print(df.head(n))
                while True:
                    try:
                        #getting user input if he wants even more raw data (the next 5 rows of the DataFrame) or not and again covering all possible exceptions
                        decision_cont = input("Would you want to see more individual trip data? Type 'yes' or 'no': ")
                        if (decision_cont.lower() != 'no' and decision_cont.lower() != 'yes'):
                            raise ValueError
                        if (decision_cont.lower() == 'no'):
                            break
                        else:
                            print(df.iloc[n:(n+5)])
                            n += 5
                    except ValueError:
                        print('This is not a valid answer (yes or no) to choose from, please check your input and try it again!!')
                    except KeyboardInterrupt:
                        print('\nNo Input was taken!')
                        break
                break
        except ValueError:
                print('This is not a valid answer (yes or no) to choose from, please check your input and try it again!')
        except KeyboardInterrupt:
                print('\nNo Input was taken!')
                break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank you for using the bikesharing database to gather some knowledge and I hope it could help you out, Goodbye!')
            break


if __name__ == "__main__":
	main()

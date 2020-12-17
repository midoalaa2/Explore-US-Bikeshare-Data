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
    city_list = ["chicago", "new york city", "washington"]
    city = 5
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while city not in range(len(city_list)+1) :
        try:
            city = int(input("Would you like to see data for :- \n1-Chicago \n2-New York city \n3-Washington \n..... :  "))
            if city in range(len(city_list)+1) :
                city = city_list[city-1]
                break
        except:
            print("please select one from cities beloww")
    # get user input for month (all, january, february, ... , june)
    months_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = 10
    while month not in range(len(months_list)) :
        try:
            month = int(input(" Which month Type month number \n0-all \n1-January \n2-February \n3-March \n4-April \n5-May  \n6-June \n..... : "))
            if month in range(len(months_list)) :
                month = months_list[month]
                break
        except:
            print("please choose number from 0 to 6")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list= ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = 10
    while day not in range(len(day_list)) :
        try:
            day = int(input("Which day Type day number \n0-all \n1-Monday \n2-Tuesday \n3-Wednesday \n4-Thursday \n5-Friday \n6-Saturday \n7-Sunday \n..... :  "))
            if day in range(len(day_list)):
                day = day_list[day]
                break
        except:
            print("please choose number from 0 to 7")
                
    
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
    # data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    while True:
        try:
            inp = str(input("Would you like to see sample raw data ? yes or no : ")).lower()
            if inp == "yes" :
                print(df.sample(5))
            else:
                break
        except:
            print("Loading....")

    # the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], format ='%Y%m%d %H:%M:%S')

    #  month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'], format ='%Y%m%d %H:%M:%S')
    # the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month :', popular_month)


    # the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Start Hour:', popular_day_of_week)

    # the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station : ', popular_start_station)
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station : ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " /// " + df['End Station']
    combination_station = df['combination'].mode()[0]
    print("most frequent combination of start station and end station trip : ", combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df["Trip Duration"].sum()
    print("total travel time : {} sec".format(total_time))


    # display mean travel time
    mean = df["Trip Duration"].mean()
    print("mean is : {} sec".format(mean))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_typs = df["User Type"].value_counts()
    print("counts of user types : \n",user_typs)

    # Display counts of gender
    if 'Gender' in df :
        gender = df["Gender"].value_counts()
        print("counts of gender :\n",gender)
    else:
        print("there is no Gender data in selected city")

    #  Display earliest, most recent, and most common year of birth
    if "Birth Year" in df :
        earliest = df["Birth Year"].min()
        recent = df["Birth Year"].max()
        common = df["Birth Year"].mode()[0]
        print("The earliest year of birth is : {}\nThe most recent year of birth is : {}\nThe most common year of birth is : {}".format(earliest,recent,common))
    else:
        print("There is no Birth Year data in selected city")


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

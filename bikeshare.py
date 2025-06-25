import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def month_filter():
    """
    Asks user to specify a month to analyze.

    Takes a user input of a month name to filter data, while checking for correct user input.

    Args:
        none, no arguments are passed to this function as it prompts user for input.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter.
    """
    month_dict = { 'jan': 'january',
                   'feb': 'february',
                   'mar': 'march',
                   'apr': 'april',
                   'may': 'may',
                   'jun': 'june' }

    # get user input for month (all, january, february, ... , june)
    while True:
        month_input = input("\nPlease enter a month to analyze (at least the first 3 letters are necessary i.e. Jan, Feb, etc.):\n").lower()
        try:
            month_three = month_input[:3]
            if month_three in month_dict:
                month = month_dict[month_three]
                break
            else:
                print("Sorry only the first 6 months of data are available for the year. Please enter a different month.")
        except:
            print("Invalid input. Please try again.")

    return month


def day_filter():
    """
    Asks user to specify a day to analyze.

    Takes a user input of a day name to filter data, while checking for correct user input.

    Args:
        none, no arguments are passed to this function as it prompts user for input.

    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    day_dict = { 'mon': 'monday',
                 'tue': 'tuesday',
                 'wed': 'wednesday',
                 'thu': 'thursday',
                 'fri': 'friday',
                 'sat': 'saturday',
                 'sun': 'sunday' }

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = input("\nPlease enter a day of the week to analyze (at least the first 3 letter):\n").lower()
        try:
            day_three = day_input[:3]
            if day_three in day_dict:
                day = day_dict[day_three]
                break
            else:
                print("Invalid day of the week. Please try again.")
        except:
            print("Invalid input. Please try again")

    return day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Args:
        none, no arguments are passed to this function as it prompts user for input.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_input = input("\nWhich city would you like to analyze, Chicago, New York City, or Washington?\n").lower()
        try:
            city = city_input
            if city in ["chicago","new york city","washington"]:
                break
            else:
                print("That's an invalid city. Please try again.")
        except:
            print("Invalid input. Please try again.")  


    #determine whether to filter the data
    while True:
        filter_input = input("\nWould you like to filter the data by month, day, both, or not at all? Enter 'none' for no filters.\n").lower()
        try:
            how_to_filter = filter_input[:1]
            if how_to_filter in ["m","d","b","n"]:
                break
            else:
                print("Invalid input, please enter another filter.")
        except:
            print("Invalid input, please try another filter.")
    
    #depending on how user wants to filter data, calls one or both of month_filter() and day_filter() function(s).
    if how_to_filter == "b":
        month = month_filter()
        day = day_filter()
    elif how_to_filter == "m":
        month = month_filter()
        day = "all"
    elif how_to_filter == "d":
        month = "all"
        day = day_filter()
    else:
        month = "all"
        day = "all"    

    print("\nYou have entered the following to filter the data:\nCity: {}\nMonth: {}\nDay: {}\n".format(city, month, day))
    
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

    # load the csv file corresponding to the specified city
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

    # display the most common month
    if len(df['month'].value_counts()) > 1:
        most_common_month = df['month'].mode()[0]
        month_count = df['month'].value_counts().get(most_common_month, 0)
        print("The most trips occurred during the month of {} with {} trips.\n".format(most_common_month, month_count))
    else:
        print("The data is already filtered to {}.\n".format(calendar.month_name[df['month'].mode()[0]]))

    # display the most common day of week
    if len(df['day_of_week'].value_counts()) > 1:
        most_common_day = df['day_of_week'].mode()[0]
        day_count = df['day_of_week'].value_counts().get(most_common_day, 0)
        print("The most trips occurred on {}s with {} trips.\n".format(most_common_day, day_count))
    else:
        print("The data is already filtered to {}.\n".format(df['day_of_week'].mode()[0]))


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    hour_count = df['hour'].value_counts().get(most_common_hour, 0)

    if most_common_hour == 0:
        hour_standard = 12
        hour_suffix = "am"
    elif 1 <= most_common_hour <= 11:
        hour_standard = most_common_hour
        hour_suffix = "am"
    elif most_common_hour == 12:
        hour_standard = 12
        hour_suffix = "pm"
    else:
        hour_standard = most_common_hour - 12
        hour_suffix = "pm"

    print("The most bike trips began during the {}{} hour with {} trips.\n".format(hour_standard, hour_suffix, hour_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    start_count = df['Start Station'].value_counts().get(popular_start_station, 0)
    print("The most commonly used starting station is {} with {} trips starting there.\n".format(popular_start_station, start_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    end_count = df['End Station'].value_counts().get(popular_end_station, 0)
    print("The most commonly used ending station is {} with {} trips ending there.\n".format(popular_end_station, end_count))

    # display most frequent combination of start station and end station trip
    df['start_end_combo'] = list(zip(df['Start Station'], df['End Station']))
    most_freq_combo = df['start_end_combo'].mode()[0]
    combo_count = df['start_end_combo'].value_counts().get(most_freq_combo, 0)
    print("The most frequent combination of start and end stations is {} to {}, with {} trips.\n".format(most_freq_combo[0], most_freq_combo[1], combo_count))

    df.drop('start_end_combo', axis=1, inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum().round(decimals=0)
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    print("Total travel time was {} hours, {} minutes, and {} seconds.\n".format(hours, minutes, seconds))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean().round(decimals=0)
    minutes, seconds = divmod(mean_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    print("The average travel time per trip was {} hours, {} minutes, and {} seconds.\n".format(hours, minutes, seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of bike trips by user type:")
    print(df['User Type'].fillna('Unknown').value_counts(dropna=False))


    # Display counts of gender
    print("\nNumber of bike trips by user's gender (gender is only known for subscribers):")
    try:
        print(df['Gender'].fillna('Unknown').value_counts(dropna=False))
    except:
        print("Gender data is not available for {}".format(city.title()))


    # Display earliest, most recent, and most common year of birth
    print("\nSubscriber age-related usage (birth year is only known for substribers):")
    try:
        print("The oldest user was born in {}.".format(df['Birth Year'].min()))
        print("The youngest user was born in {}.".format(df['Birth Year'].max()))
        print("The most common birth year was {}.".format(df['Birth Year'].mode()[0]))
    except:
        print("Age-related data is not available for {}".format(city.title()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_dataframe(df, num_rows=5):
    """
    Displays the raw data to the terminal, asking for user input to continue.
    
    Args:
        df: The DataFrame to print.
        num_rows (int): The number of rows of the DataFrame to print at a time.
    """
    total_rows = len(df)
    start_index = 0

    while start_index < total_rows:
        end_index = min(start_index + num_rows, total_rows)
        print(df.iloc[start_index:end_index])

        if end_index < total_rows:
            user_input = input("Press Enter to see more rows, or 'q' to quit: ")
            if user_input =='q':
                break
        start_index += num_rows



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data = input('\nWould you like to see the raw trip data? Enter yes or no.\n')
        if raw_data.lower() == 'yes':
            print_dataframe(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np

#Store all the needed information into separate data structures
cities = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ('all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')
weekdays = ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

#Get filters from user and validate them
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). Allowing just 1 city
    while True:
        city = str(input("\nWhat city do you want to analyze? Choose 1 from chicago, new york city, or washington? \n")).lower()
        if city in cities:
            break    
        else:
            print("\nThe city you entered does not match - chicago, new york city, or washington. Please enter a valid city \n")
    
    #for month and day, the user can enter ALL in which case there are no filters
    #we are not proactively checking if ALL comes along with another month, but in the load_data function we ignore filters if we see ALL in the list
   
    # get user input for month (all, january, february, ... , june). Allowing multiple/all months
    while True:
        month = str(input("\nWhich months do you want to analyze? Use commas to separate them and provide the full month names. Provide 'all' if you dont             want to filter by months \n")).lower()
        if ',' in month:
            month_list = [m.strip() for m in month.split(',')] #split the multiple options into a separate list
            if list(filter(lambda x: x in months, month_list)) == month_list:
                break
            else:
                print("\nOne of the months you entered does not exist. Please enter valid months \n")
        else:
            if month in months:
                break
            else:
                print("\nThe month you entered does not exist. Please enter a valid month \n")

    # get user input for day of week (all, monday, tuesday, ... sunday). Allowing multiple/all days
    while True:
        day = str(input("\nWhich days do you want to analyze? Use commas to separate them and provide the full day names. Provide 'all' if you dont                         want to filter by days \n")).lower()
        if ',' in day:
            day_list = [d.strip() for d in day.split(',')]  #split the multiple options into a separate list
            if list(filter(lambda x: x in weekdays, day_list)) == day_list:
                break
            else:
                print("\n One of the days you entered does not exist. Please enter valid days \n")
        else:
            if day in weekdays:
                break
            else:
                print("\n The day you entered does not exist. Please enter a valid day \n")

    print('-'*80)
    
    return city, month, day

#writing function to change month numbers to month text
def month_change(row):
    if row['Month'] == 1:
        return 'january'
    elif row['Month'] == 2:
        return 'february' 
    elif row['Month'] == 3:
        return 'march' 
    elif row['Month'] == 4:
        return 'april' 
    elif row['Month'] == 5:
        return 'may' 
    elif row['Month'] == 6:
        return 'june' 
    elif row['Month'] == 7:
        return 'july' 
    elif row['Month'] == 8:
        return 'august' 
    elif row['Month'] == 9:
        return 'september' 
    elif row['Month'] == 10:
        return 'october' 
    elif row['Month'] == 11:
        return 'november' 
    else:
        return 'december' 

#filter and load the dataset into a new dataframe
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
    print("\n Loading the data for your filters. Hang tight! This might take around 30 seconds")
    start_time = time.time()

    # filter for city
    df = pd.read_csv(cities[city.lower()]) #we are allowing just 1 city, so can read directly
    
    # creating derived columns to compute stats below
    #for full transparency, I used a fellow programmer's github code here for the below 5 statements - https://github.com/decarvalhohenrique/programming-for-data-science-nanodegree/blob/master/2nd-project/bikeshare.py
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Month_Text'] = df.apply(month_change, axis=1) #apaplying this function to convert month number to actual month values
    
    # filter according to month
    if 'all' in month: #if there is ALL, we need not filter
        pass #do nothing
    elif ',' in month: #multiple months without ALL
        #print(list(month.split(",")))
        df = df[df['Month_Text'].isin(i.strip().lower() for i in list(month.split(",")))]
    else: #single month
        df = df[df['Month_Text'] == month.lower()]

    # filter according to day
    if 'all' in day: #if there is ALL, we need not filter
        pass #do nothing
    elif ',' in day: #multiple days without ALL
        #print(list(day.split(",")))
        df = df[df['Weekday'].isin(i.strip().title() for i in list(day.split(",")))]
    else: #single day
        df = df[df['Weekday'] == day.title()]

    print("\nThis took %s seconds.".format((time.time() - start_time)))
    print('-'*80)
    
    #prints to check that filters are working as expected
    print(df.head())
    print(df['Month_Text'].value_counts())
    print(df['Weekday'].value_counts())
    
    return df

#calculating first set of statistics based on times of travel
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month_Text'].mode()[0]
    print('\nThe month with the most travels is {}'.format(most_common_month))

    # display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('The day with the most travels is {}'.format(most_common_day))
    
    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The hour with the most travels is {}'.format(most_common_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

#calculating second set of statistics based on station details
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common end station is {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +  df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print("The most common start-end combination is {}".format(most_common_start_end_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

#calculating third set of statistics based on duration details
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in d, h, m
    total_travel = df['Trip Duration'].sum()
    total_travel = (str(int(total_travel//86400)) + 
                         'd ' +
                         str(int((total_travel % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel % 86400) % 3600)//60)) +
                         'm ')
    print('The total travel time is {}'.format(total_travel))

    # display mean travel time in minutes and seconds
    mean_travel = df['Trip Duration'].mean()
    mean_travel = (str(int(mean_travel//60)) + 'm ' +
                        str(int(mean_travel % 60)) + 's')
    print("The mean travel time is {}".format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

#calculating fourth set of statistics based on user stats
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

# Display counts of user types
    user_types = df['User Type'].value_counts().to_string() #converts to a good tabular format
    print("The distribution for user types is shown below:")
    print(user_types)

    # Display counts of gender
    try:
        gender_dist = df['Gender'].value_counts().to_string()  #converts to a good tabular format
        print("\nThe distribution for gender is shown below:")
        print(gender_dist)
    except KeyError:
        print("\nNo gender data available for chosen city")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nEarliest year of birth is {}".format(earliest_birth_year))
        latest_birth_year = str(int(df['Birth Year'].max()))
        print("Latest year of birth is {}".format(latest_birth_year))
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("Most common year of birth is {}".format(most_common_birth_year))
    except:
        print("\nNo birth information available for chosen city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

#function to print raw data
def raw_data_print(df, marker = 0): #setting marker to the 0th position
    """Display 5 line of sorted raw data each time."""

    # displays 5 lines of raw data at a time
    while True:
        for i in range(marker, len(df.index)):
            print("\n")
            print(df.iloc[marker:marker+5].to_string())
            print("\n")
            marker += 5 #increase by 5 each time
            
            choice = str(input("\nDo you want to keep printing raw data? Say yes for printing. Say anything else to proceed to statistics\n")).lower()
            if choice == 'yes':
                continue
            else:
                break
        break

#function to get things rolling!
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        raw_data_choice = str(input("\nDo you want to see the raw data before printing statistics? Say yes to print raw data. Say anything else to proceed with calculating statistics\n")).lower()
        if raw_data_choice == 'yes':
            raw_data_print(df)
        else:
            pass
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

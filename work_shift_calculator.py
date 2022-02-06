"""
LICENCING
Copyright (c) 2021, Jack Allen, [JackEAllen](https://github.com/JackEAllen)

All rights reserved under the GNU GENERAL PUBLIC LICENSE Version 3 or later.

A small script to calculate time spent working in a given time period.
This script was made to make my life easier when working from home as
my brain is usually too tired to do simple maths at hte ed of the day
to track time spent working

This script uses 24 hour time format.

This Script is licensed under the GNU General Public License v3.0
copyright (c) 2021, Jack Allen JackEAllen
"""

# Dependencies
import sys
import datetime
import re
from time import time

import utils

class WorkShiftCalculator:
    """
    A class to calculate time spent working in a given time period.
    """
    def __init__(self):
        """
        Initialise the class with start and end time.
        """
        self.start_time = self.convert_input_to_datetime("start time")
        self.lunch_break = self.convert_input_to_datetime("lunch break")
        self.end_time = self.convert_input_to_datetime("end time")

    def calc_time_without_break(self) -> datetime.datetime:
        """
        Calculate the time spent working in a given time period.
        @return: The time spent working in a given time period.
        """

        time_spent_working_without_lunch_break = self.end_time - self.start_time
        return time_spent_working_without_lunch_break

    def extract_lunch_break_time_to_minutes(self) -> int:
        """
        Extract the lunch break time to minutes.
        @return: The lunch break time in minutes.
        """
        lunch = datetime.datetime.strptime(str(self.lunch_break), '%Y-%m-%d %H:%M:%S').time()
        hour, minute, _ = str(lunch).split(":")

        lunch_break_time_in_minutes = (int(hour) * 60) + (int(minute))
        return lunch_break_time_in_minutes

    def calc_time_with_lunch_break(self) -> datetime.datetime:
        """
        Calculate the time spent working in a given time period without lunch break.
        @return: The time spent working in a given time period without lunch break.
        """
        lunch = self.extract_lunch_break_time_to_minutes()
        time_spent_working = self.calc_time_without_break() - datetime.timedelta(minutes=lunch)
        return time_spent_working


    def surplus_time(self) -> datetime.datetime:
        """
        Calculate the surplus time worked in a given time period compared to 07:30:00.
        @return: The surplus time worked in a given time period.
        """
        time_spent_working_with_lunch_break = self.calc_time_with_lunch_break()
        surplus_time = time_spent_working_with_lunch_break - datetime.timedelta(hours=7, minutes=30)
        if surplus_time.days < 0:
            return '-' + str(datetime.timedelta() - surplus_time)
        return surplus_time

    def calculate_total_surplus_time(self) -> datetime.datetime.time:
        """
        Calculate the total surplus time.
        @return: The total surplus time.
        """

        previous_surplus = utils.get_most_recent_surplus_time_value_from_csv("time_spent_working.csv")
        time_delta_surplus = datetime.datetime.combine(datetime.date.min, previous_surplus) - datetime.datetime.min
        total_surplus = time_delta_surplus + self.surplus_time()
        return total_surplus

    @staticmethod
    def convert_input_to_datetime(booking: str) -> datetime.datetime:
        """
        Convert the input time to datetime format.
        @param input_time: The input time to be converted.
        @return: The input time in datetime format.
        """
        pattern = re.compile("^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$")

        input_time = input(f"Enter the {booking} in 24 hour format (HH:MM): ")
        if not re.match(pattern, input_time):
            print("Error! Only integers 1-9 allowed!")
            sys.exit()
        time = datetime.datetime.strptime(input_time, '%H:%M')
        return time

    def get_current_date(self) -> datetime.datetime:
        """
        Get the current date.
        @return: The current date.
        """
        return datetime.date.today()

    def format_data(self) -> str:
        """
        Format the data to be written to the csv file.
        @return: The formatted data.
        """
        time_spent_working_with_lunch_break = self.calc_time_with_lunch_break()
        surplus_time = self.surplus_time()
        time_spent_working_without_lunch_break = self.calc_time_without_break()
        time_spent_working_with_lunch_break = self.calc_time_with_lunch_break()
        time_data = [self.start_time, self.lunch_break, self.end_time, time_spent_working_without_lunch_break, time_spent_working_with_lunch_break, surplus_time, self.calculate_total_surplus_time()]
        formatted_data = ', '.join(map(str, time_data))
        return formatted_data
        # return time_data


    def create_dictionary(self) -> dict:
        """
        Create a dictionary with the data to be written to the csv file.
        @return: The dictionary.
        """
        date = self.get_current_date()
        dictionary = {"Date": date, 
        "start": self.start_time.time(), 
        "Lunch": self.lunch_break.time(), 
        "end": self.end_time.time(),
        "Time without Lunch": self.calc_time_without_break(),
        "Time With Lunch": self.calc_time_with_lunch_break(),
        "Surplus Time": self.surplus_time(),
        "Total Surplus": self.calculate_total_surplus_time()}
        return dictionary



def main():
    """
    The main function of the script.
    """

    workshift = WorkShiftCalculator()
    # print("Previous Surplus Time: " + str(utils.get_most_recent_surplus_time_value_from_csv("time_spent_working.csv")))
    print(f"Start Time: {workshift.start_time.time()}")
    print(f"Lunch Break: {workshift.lunch_break.time()}")
    print(f"End Time: {workshift.end_time.time()}")
    print(f"Time worked excluding break: {workshift.calc_time_without_break()}")
    print(f"Time worked including break: {workshift.calc_time_with_lunch_break()}")
    print(f"Surplus time: {workshift.surplus_time()}")
    print(f"Total Surplus time: {workshift.calculate_total_surplus_time()}")

    utils.write_dictionary_to_csv("time_spent_working.csv", workshift.create_dictionary())


if __name__ == "__main__":
    main()

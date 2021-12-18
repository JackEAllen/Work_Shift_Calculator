"""
LICENCING
Copyright (c) 2021, Jack Allen, [JackEAllen](https://github.com/JackEAllen)

All rights reserved under the GNU GENERAL PUBLIC LICENSE Version 3 or later.

Main file for the project.
"""

from work_shift_calculator import WorkShiftCalculator


def main():
    """
    Main function.
    """
    workshift = WorkShiftCalculator()
    print("------------------------------------")
    print(f"Start Time: {workshift.start_time.time()}")
    print(f"Lunch Break: {workshift.lunch_break.time()}")
    print(f"End Time: {workshift.end_time.time()}")
    print("------------------------------------")
    print(f"Time worked excluding break: {workshift.calc_time_without_break()}")
    print(f"Time worked including break: {workshift.calc_time_with_lunch_break()}")

if __name__ == "__main__":
    main()

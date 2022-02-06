"""
Utility functions for the project.
"""

# Dependencies
import csv
import datetime

def list_dictionary_keys(dictionary: dict) -> list:
	"""
	Get the keys of a dictionary as a list of strings.
	@param dictionary: The dictionary to get the keys from.
	@return: The keys of the dictionary as a list of strings.
	"""

	keys = []
	for key in dictionary.keys():
		keys.append(str(key))
	return keys

def create_csv_file(file_name: str):
	"""
	Create a csv file.
	@param file_name: The name of the file.
	"""

	with open(file_name, 'w', newline='') as csv_file:
		csvwriter = csv.writer(csv_file)
		csvwriter.writerow(["Date", "Time", "Surplus Time"])

# A function to write a dictionary to a csv file.
def write_dictionary_to_csv(file_name: str, dictionary: dict):
	"""
	Write a dictionary to a csv file.
	@param file_name: The name of the file.
	@param dictionary: The dictionary to write.
	"""

	headers = list_dictionary_keys(dictionary)
	data = [dictionary]

	if check_if_file_exists(file_name):
		with open(file_name, 'a') as f:
			writer = csv.DictWriter(f, fieldnames=headers)
			writer.writerows(data)
	else:
		with open(file_name, 'w', newline='') as csv_file:
			csvwriter = csv.DictWriter(csv_file, fieldnames=headers)
			csvwriter.writeheader()

			for d in data:
				csvwriter.writerow(d)


def check_if_file_exists(file_name: str) -> bool:
	"""
	Check if a file exists.
	@param file_name: The name of the file.
	@return: True if the file exists, false if not.
	"""

	try:
		with open(file_name, 'r') as f:
			return True
	except FileNotFoundError:
		return False

# FUnction to convert string HH:MM:SS to time object.
def convert_string_to_time(time_string: str) -> datetime.time:
	"""
	Convert a string to a time object.
	@param time_string: The string to convert.
	@return: The time object.
	"""

	time = datetime.datetime.strptime(time_string, '%H:%M:%S').time()
	return time


def get_most_recent_surplus_time_value_from_csv(file_name: str) -> int:
	"""
	Get the most recent surplus time value from a csv file.
	@param file_name: The name of the file.
	@return: The most recent surplus time value.
	"""

	if check_if_file_exists(file_name):
		with open(file_name, "r", encoding="utf-8", errors="ignore") as scraped:
			if len(list(scraped)) > 1:
				final_line = scraped.readlines()[-1].split(",")[-1].strip()
				return convert_string_to_time(final_line)
			else: 
				no_time = "00:00:00"
				return convert_string_to_time(no_time)
	else:
		no_time = "00:00:00"
		return convert_string_to_time(no_time)
		
		
# 		writer = csv.writer(csv_file)
# 		for key, value in dictionary.items():
# 			writer.writerow([key, value])

# 	data = [
#     {'name': 'Pat', 'age': 78},
#     {'name': 'Nancy', 'age': 23},
# ]

# headers = ['name', 'age']

# with open('outputdata.csv', 'w') as outfile:
#     mywriter = csv.DictWriter(outfile, fieldnames=headers)
#     mywriter.writeheader()

#     for d in data:
#         mywriter.writerow(d)


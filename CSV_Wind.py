# Matthew Buzalsky, Colby Connolly
# Read csv data and write to new file

import csv

'''

Notes:

1. Run this program after using the ReadSerial_Wind_Proj file
2. Enter in the file name of the newly created csv file without the .csv
3. A new file will be created that is purely based on per minute data

'''

data_list = []

# Input file name

file_name = input("Please input the name of the csv file (without .csv): ")

# New file name

new_name = file_name + ".csv"


if __name__ == "__main__":

    # Read raw data file

    with open(new_name, "r") as data_file:

        # Print each line of data

        wind_file = csv.reader(data_file)

        # Skip headers

        next(wind_file, None)

        for row in wind_file:
            
            # Check for the first timestamp

            new_list = row[0].split(":")

            if new_list[2] == "00":

                # Add to list

                data_list.append(row)
            
            else:
                pass

    # Write to new csv file

    with open("Lab4_Anemometer_Data.csv", "w", newline = "") as new_file:
        new_wind_file = csv.writer(new_file, delimiter = ",")

        # Write headers

        new_wind_file.writerow(["Time Stamp", "Voltage (V)", "Wind Speed (m/s)"])

        # Write each line to the csv file

        for element in data_list:
            new_wind_file.writerow(element)

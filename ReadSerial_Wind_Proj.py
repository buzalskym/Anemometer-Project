# Matthew Buzalsky, Colby Connolly
# Introduction to Renewable Energy
# Read serial from Arduino

'''

Notes: 

1. Make sure the commands to print the output of the voltage and wind are defined as such in the Arduino program:

Serial.print("Voltage: ");
Serial.print(sensor_voltage);

Serial.print(", Wind: ");
Serial.println(wind_speed);

Change the variable names (wind_speed, sensor_voltage) to the names used in your program

2. Once the Arduino program is set, upload the Arduino code to the board and open the Serial Monitor.
Exit (click x) out of the Arduino Serial Monitor after a couple of seconds.

3. Once ready, run the python script by pressing run. 

You will see different COM ports being used on your computer, choose the one that has Arduino Uno.
If the port is COM10 for example, enter in 10.

4. Also note that the baud rate for Arduino is 9600, so enter that in as well.

5. The data will be printed in the output terminal. When done reading data from python, hold the letter Q on the keyboard
and the data will be exported to a csv file. The csv file will be located in the file path where this python file is stored 
on your computer.

'''

import csv
import numpy as np
import serial.tools.list_ports
import keyboard
from datetime import datetime

# Voltage list

vol_list = []

# Wind list

wind_list = []

# Time data

time_data = []

# List available COM ports

avail_ports = serial.tools.list_ports.comports()

def write_to_file(final_data):
    # Record file time
    file_time = datetime.now()
    file_time_string = file_time.strftime("%m-%d-%Y_%H;%M;%S")

    # File name
    file_string = "Anemometer_" + file_time_string + ".csv"

    # Write data

    try:
        with open(file_string, "w", newline = "") as data_file:
            data_write = csv.writer(data_file, delimiter = ",")

            # Write headers

            data_write.writerow(["Time Stamp", "Voltage (V)", "Wind Speed (m/s)"])

            # Write to each row of excel file

            for element in final_data:
                data_write.writerow([element[0], element[1], element[2]])

    except: # Error with file writing
        print("There were problems writing to the CSV file!")


if __name__ == "__main__":

    # Print out COM ports in use

    for element in avail_ports:
        print(str(element))

    # Open COM Port

    user_input = input("Please enter in the COM Port Number: ")

    port_number = "COM" + user_input
    baud_rate = int(input("Please enter in the baud rate: "))

    serial_mon = serial.Serial(port_number, baud_rate)

    while True:
        # Bytes in the buffer

        if serial_mon.in_waiting:
            if keyboard.is_pressed('q'): # End program
                break
            else:
                # Record time stamp
                current_time = datetime.now()
                current_time_string = current_time.strftime("%H:%M:%S")

                # Read line
                pos_output = serial_mon.readline()
                new_string = str(pos_output.decode('utf-8').rstrip('\n'))

                time_string = str(current_time_string) + ", " + new_string
                print(time_string)

                # Record data
                new_string = time_string.split(", ")

                # Append time stamp, voltage, and wind

                if len(new_string) == 3:
                    # Data isn't the correct length
                    if len(new_string[0]) < 8 or len(new_string[1]) < 13 or len(new_string[2]) < 10: 
                        pass
                    else:
                        time_data.append(new_string[0])
                        vol_list.append(float(new_string[1][9:]))
                        wind_list.append(float(new_string[2][6:]))
                else: # List doesn't contain three elements
                    pass

    
    # Set matrix
                
    data_set = [time_data, vol_list, wind_list]
    
    # Import into numpy

    new_data = np.array(data_set)
    final_data = new_data.T
    
    # Write to CSV

    write_to_file(final_data)
class AlarmEvent:
    def __init__(self, timestamp, sensortype, location, status, duration_seconds):
        # Setting up the alarm details
        self.timestamp = timestamp
        self.sensortype = sensortype
        self.location = location
        self.status = status
        # Convert to int so we can do math/logic on it later
        self.duration_seconds = int(duration_seconds)

    def __str__(self):
        # Makes it easy to print the object in a readable format
        return f"AlarmEvent(timestamp={self.timestamp}, sensortype={self.sensortype}, location={self.location}, status={self.status}, duration_seconds={self.duration_seconds})"
    

def parse_logs(filepath):
    # Create an empty list to store our alarm objects
    alarms = []
    # Open the file and read it line by line
    with open(filepath, 'r') as file:
        lines = file.readlines()
        data_lines = lines[1:]  # Skip the first line because it's just the header
        
        for line in data_lines:
            # Clean up the line and split the values by comma
            clean_line = line.strip()
            row_data = clean_line.split(',')
            
            # Put the data into named variables for better readability
            timestamp = row_data[0]
            sensortype = row_data[1]
            location = row_data[2]
            status = row_data[3]
            duration_seconds = row_data[4]

            # Create an object and add it to our list
            alarm = AlarmEvent(timestamp, sensortype, location, status, duration_seconds)
            alarms.append(alarm)

    return alarms


# Define where the data file is
file_path = "secom_alarms.csv"

# Load the data from the CSV file
all_alarms = parse_logs(file_path)

# Let us know how many records were imported
print(f"Successfully loaded {len(all_alarms)} alarms.")

# Just showing the first one to make sure it worked
print("First alarm record:", all_alarms[0])


def filter_alarms(alarms_list):
    # This list will only contain the real, valid alarms
    valid_alarms = [] 

    for alarm in alarms_list:
        
        # Check if it's a "cat" false alarm (motion < 3s)
        if alarm.sensortype == 'motion' and alarm.duration_seconds < 3:
            continue 
            
        # Check if it's a "glitch" false alarm (door < 3s)
        elif alarm.sensortype == 'door' and alarm.duration_seconds < 3:
            continue
            
        # Check if the sensor was offline (invalid)
        elif alarm.status == 'offline':
            continue
            
        # If it passes all checks, it's a real alarm, so add it to the list
        else:
            valid_alarms.append(alarm)
            
    # Return the clean, filtered list
    return valid_alarms


# Run our filter function to remove the junk data
valid_alarms = filter_alarms(all_alarms)

# Print a simple report to the terminal
print("-" * 30)
print(f"REPORT: Cleaned Alarm Log")
print(f"Original records: {len(all_alarms)}")
print(f"False alarms removed: {len(all_alarms) - len(valid_alarms)}")
print(f"Valid alarms remaining: {len(valid_alarms)}")
print("-" * 30)

# Save the filtered results into a new clean CSV file
with open('valid_alarms_report.csv', 'w') as f:
    f.write("timestamp,sensor_type,location,status,duration_seconds\n")
    for alarm in valid_alarms:
        f.write(f"{alarm.timestamp},{alarm.sensortype},{alarm.location},{alarm.status},{alarm.duration_seconds}\n")

print("Valid alarms have been saved to 'valid_alarms_report.csv'.")
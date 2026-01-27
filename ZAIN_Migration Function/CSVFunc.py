import csv
import pandas as pd


def dict_to_csv(history_session_time):#ewmaresult, ):
    with open('sessionTime.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # Write history_session_time dictionary
        writer.writerow(['previous_SSID , next_SSID', 'History_SessionTime'])
        for (previous_ssid, next_ssid), session_times in history_session_time.items():
            print("previous_ssid__INSIDE 11 CSVFUNC", previous_ssid)
            for session_time in session_times:
                writer.writerow([(previous_ssid, next_ssid)] + [session_time])
                print("previous_ssid__INSIDE 22 CSVFUNC", previous_ssid)

def dataframe_to_csv(dataframe, filename):
    # Convert the 'WMA' column to strings
    dataframe['WMA'] = dataframe['WMA'].apply(lambda x: ', '.join(map(str, x)))

    # Save the DataFrame to a CSV file
    dataframe.to_csv(filename, index=False)


def monitoring_output_to_csv(linked_previous_ssids, csv_filename):
    # Create empty lists to store the data
    next_ssid_list = []
    linked_previous_ssids_list = []
    previous_ssid_list = []
    wma_values_list = []
    smallest_previous_ssid_list = []
    smallest_wma_value_list = []

    # Iterate through linked_previous_ssids dictionary
    for next_ssid, data in linked_previous_ssids.items():
        next_ssid_list.append(next_ssid)
        linked_previous_ssids_list.append(', '.join(data['previous_ssids']))
        smallest_previous_ssid_list.append(data['smallest_previous_ssid'])
        smallest_wma_value_list.append(data['smallest_wma_value'])

        # Iterate through the WMA arrays for each previous_ssid
        for previous_ssid, wma_values in data['wma_data'].items():
            previous_ssid_list.append(previous_ssid)
            wma_values_list.append(', '.join(map(str, wma_values)))

    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'Next SSID': next_ssid_list,
        'Linked Previous SSIDs': linked_previous_ssids_list,
        'Previous SSID': previous_ssid_list,
        'WMA Values': wma_values_list,
        'Smallest Previous SSID': smallest_previous_ssid_list,
        'Smallest WMA Value': smallest_wma_value_list
    })

    # Save the DataFrame to a CSV file
    df.to_csv(csv_filename, index=False)


def LinkedPreviousSSID_Dict_to_csv(dictionary, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['next_ssid', 'min_previous_ssid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for next_ssid, data in dictionary.items():
            writer.writerow({'next_ssid': next_ssid, 'min_previous_ssid': data.get('smallest_previous_ssid', '')})

def save_state_dict_to_csv(self, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['MAC Address', 'Last Timestamp', 'Current Timestamp'])
        # Write data
        for mac_address, timestamps in self.state_dict.items():
            writer.writerow([mac_address, timestamps['last_timestamp'], timestamps['current_timestamp']])
    print(f"State dictionary saved to {filename}")
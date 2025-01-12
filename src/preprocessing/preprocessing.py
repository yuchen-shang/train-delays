import os
import pandas as pd


def prepropressing_pipeline(data):
    selected_data = select_columns(data)
    passenger_train_data = select_passenger_train_companies(selected_data)
    renamed_df = rename_columns(passenger_train_data)
    output_df = convert_datetime(renamed_df)

    return output_df


def select_columns(data):
    columns_to_keep = [
        'PLANNED_ORIGIN_WTT_DATETIME',
        'INCIDENT_START_DATETIME',
        'INCIDENT_END_DATETIME',
        'EVENT_DATETIME',
        'PFPI_MINUTES',
        'PLANNED_ORIGIN_LOCATION_CODE',
        'PLANNED_DEST_LOCATION_CODE',
        'START_STANOX',
        'TOC_CODE',
        'INCIDENT_REASON',
        'EVENT_TYPE'
    ]
    selected_df = data[columns_to_keep]

    return selected_df


def select_passenger_train_companies(data):
    passenger_train_companies = [
        "E1", "EA", "EB", "EC", "ED", "EF",
        "EH", "EI", "EJ", "EK", "EM", "ES",
        "ET", "EX", "HA", "HB", "HG", "HH",
        "HI", "HJ", "HL", "HT", "HU", "HX", "HY"
    ]

    passenger_train_data = data[data['TOC_CODE']
                                .isin(passenger_train_companies)]

    passenger_train_data.reset_index(inplace=True, drop=True)
    return passenger_train_data


def rename_columns(data):
    rename = {
        'PLANNED_ORIGIN_LOCATION_CODE': 'ORIGIN_STANOX',
        'PLANNED_DEST_LOCATION_CODE': 'DESTINATION_STANOX',
        'START_STANOX': 'EVENT_STANOX',
        'PLANNED_ORIGIN_WTT_DATETIME': 'JOURNEY_ORIGIN_DATETIME',
        'TOC_CODE': 'TOC',
        'PFPI_MINUTES': 'DELAY_MINUTES'
    }
    renamed_df = data.rename(rename, axis=1)
    return renamed_df


def convert_datetime(data):
    datetime_columns = [
        'JOURNEY_ORIGIN_DATETIME', 
        'INCIDENT_START_DATETIME',
        'INCIDENT_END_DATETIME',
        'EVENT_DATETIME'
    ]

    for column in datetime_columns:
        data[column] = pd.to_datetime(data[column], format='mixed')

    data.insert(
        3,
        'INCIDENT_DURATION',
        data['INCIDENT_END_DATETIME']-data['INCIDENT_START_DATETIME']
    )

    data.drop('INCIDENT_END_DATETIME', axis=1, inplace=True)

    return data


if __name__ == "__main__":
    # Directory paths
    raw_data_dir = 'data/raw'
    interim_data_dir = 'data/interim'

    # Get a list of raw data files
    raw_data_files = sorted(os.listdir(raw_data_dir))

    # Iterate over the raw data files
    for filename in raw_data_files:
        if filename.startswith('raw_delays_') and filename.endswith('.csv'):
            # Get the number from the filename
            file_number = filename.split('_')[-1].split('.')[0]

            # Load the raw data file
            file_path = os.path.join(raw_data_dir, filename)
            raw_data = pd.read_csv(file_path)

            # Preprocess the data
            preprocessed_data = prepropressing_pipeline(raw_data)

            # Save the preprocessed data as CSV
            output_filename = f'preprocessed_{file_number}.csv'
            output_path = os.path.join(interim_data_dir, output_filename)
            preprocessed_data.to_csv(output_path, index=False)

            print(f'{filename} completed, output saved as {output_filename}')

#!/bin/bash

BASE_URL="https://sacuksprodnrdigital0001.blob.core.windows.net/historic-delay-attribution/2022-23/"
OUTPUT_DIR="data/raw"

# Loop through the file range from P01 to P13
for ((i=1; i<=13; i++))
do
    # Format the file number with leading zero if necessary
    file_number=$(printf "%02d" $i)

    # Construct the URL for the current file
    url="${BASE_URL}All-delays-2022-23-P${file_number}.zip"

    # Download the file using wget
    wget "$url" -P "$OUTPUT_DIR"

    # Unzip the downloaded file to the raw directory
    unzip -j "$OUTPUT_DIR/All-delays-2022-23-P${file_number}.zip" -d "$OUTPUT_DIR"

    if [ "$i" -lt 10 ]; then
        # Move the file for i==1 with different structure
        mv "$OUTPUT_DIR/Transparency page 202223_P${file_number}.csv" "$OUTPUT_DIR/raw_delays_${file_number}.csv"
    else
        # Rename the unzipped file to raw_delays_n.csv
        mv "$OUTPUT_DIR/All-delays-2022-23-P${file_number}.csv" "$OUTPUT_DIR/raw_delays_${file_number}.csv"
        rm "$OUTPUT_DIR/._All-delays-2022-23-P${file_number}.csv"
    fi

    # Remove the downloaded zip file
    rm "$OUTPUT_DIR/All-Delays-2022-23-P${file_number}.zip"

done

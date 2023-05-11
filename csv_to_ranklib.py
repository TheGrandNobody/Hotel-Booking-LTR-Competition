import csv
import sys

def convert_csv_to_ranklib(input_csv, output_ranklib):
    # Open input CSV file for reading and output RankLib file for writing
    with open(input_csv, 'r') as csvfile, open(output_ranklib, 'w') as ranklibfile:
        # Create a CSV reader
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header row

        # Iterate through each row in the CSV file
        for row in reader:
            # Extract the relevance label, query ID, and feature values from the row
            relevance_label = row[0]
            query_id = row[1]
            features = row[2:]

            # Start building the RankLib line with the relevance label and query ID
            ranklib_line = f"{relevance_label} qid:{query_id}"

            # Add the feature values to the RankLib line with their indices
            for i, feature_value in enumerate(features, start=1):
                ranklib_line += f" {i}:{feature_value}"
            ranklib_line += '\n'

            # Write the RankLib line to the output file
            ranklibfile.write(ranklib_line)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python csv_to_ranklib.py <input_csv> <output_ranklib>")
        sys.exit(1)

    # Get the input CSV file path and output RankLib file path from the command-line arguments
    input_csv = sys.argv[1]
    output_ranklib = sys.argv[2]

    # Call the convert_csv_to_ranklib function to perform the conversion
    convert_csv_to_ranklib(input_csv, output_ranklib)

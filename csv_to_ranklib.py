import csv
import sys

def remove_leading_zeroes(value: str) -> str:
    """ Removes leading zeroes from numbers in a string.

    Args:
        value (str): The numerical value to remove leading zeroes from.

    Returns:
        str: The value with leading zeroes removed.
    """
    try:
        # Try to convert the value to a number and then back to a string
        return str(float(value)) if '.' in value else str(int(value))
    except ValueError:
        # If the value cannot be converted to a number, return it unchanged
        return value

def assign_relevance_label(booking_bool: str, click_bool: str) -> str:
    """ 

    Args:
        booking_bool (str): The booking_bool value for the row.
        click_bool (str): The click_bool value for the row.

    Returns:
        str: The relevance label for the row.
    """
    # Assign relevance labels based on booking_bool and click_bool values
    if booking_bool == '1':
        return '5'
    elif click_bool == '1':
        return '1'
    else:
        return '0'

def convert_csv_to_ranklib(input_csv: str, output_ranklib: str) -> None:
    """ Converts a csv data file to a RankLib file.

    Args:
        input_csv (str): The path to the input CSV file.
        output_ranklib (str): The name of the output RankLib file.
    """
    # Open input CSV file for reading and output RankLib file for writing
    with open(input_csv, 'r') as csvfile, open(output_ranklib, 'w') as ranklibfile:
        # Create a CSV reader with a dictionary interface
        reader = csv.DictReader(csvfile)
        # Iterate through each row in the CSV file
        for row in reader:
            # Extract the search ID, booking_bool, and click_bool values from the row
            srch_id = row['srch_id']
            booking_bool = row['booking_bool']
            click_bool = row['click_bool']

            # Assign a relevance label based on the booking_bool and click_bool values
            relevance_label = assign_relevance_label(booking_bool, click_bool)

            # Start building the RankLib line with the relevance label and query ID
            ranklib_line = f"{relevance_label} qid:{srch_id}"

            # Add the feature values to the RankLib line with their indices
            feature_idx = 1
            for key, value in row.items():
                if key not in ['srch_id', 'booking_bool', 'click_bool']:
                    ranklib_line += f" {feature_idx}:{remove_leading_zeroes(value)}"
                    feature_idx += 1
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

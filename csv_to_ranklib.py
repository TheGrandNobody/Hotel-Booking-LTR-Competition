import sys, csv

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

            # Create a copy of the row dictionary and remove the query id
            features = dict(row)
            del features['srch_id']

            if output_ranklib == 'temp.txt':
                # Assign a relevance label based on the booking_bool and click_bool values
                relevance_label = assign_relevance_label(row['booking_bool'], row['click_bool'])
                # Start building the RankLib line with the relevance label and query ID
                ranklib_line = f"{relevance_label} qid:{srch_id}"
                del features['booking_bool']
                del features['click_bool']
                del features['position']
            else:
                ranklib_line = f"0 qid:{srch_id}"

            # Create a string for the features in the format "index:value", removing leading zeros from the feature values
            features_str = ' '.join(f'{i+1}:{remove_leading_zeroes(v)}' for i, (k, v) in enumerate(features.items()))

            # Write the RankLib line to the output file
            ranklibfile.write(f"{ranklib_line} {features_str}\n")

def split_data(input_file: str, output_train: str, output_valid: str, valid_ratio: float) -> None:
    """ Split a dataset in RankLib format into a training and validation file based on a given percentage.

    Args:
        input_file (str): The name of the input dataset in RankLib format.
        output_train (str): The name of the output training file.
        output_valid (str): The name of the output validation file.
        valid_ratio (float): The percentage of the dataset we would like to use as validation data.
    """
    # Open the input file and read all the lines
    with open(input_file, 'r') as datafile:
        lines = datafile.readlines()

    # Calculate the number of lines for the validation set
    valid_size = int(len(lines) * valid_ratio)

    # Split the lines into validation and training sets
    valid_lines = lines[:valid_size]
    train_lines = lines[valid_size:]

    # Write the training lines into the output training file
    with open(output_train, 'w') as trainfile:
        trainfile.writelines(train_lines)

    # Write the validation lines into the output validation file
    with open(output_valid, 'w') as validfile:
        validfile.writelines(valid_lines)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python csv_to_ranklib.py <input_csv> <output_ranklib>")
        sys.exit(1)

    # Get the input CSV file path and output RankLib file path from the command-line arguments
    input_csv = sys.argv[1]
    output_ranklib = sys.argv[2]

    # Convert the input CSV file to a RankLib file
    convert_csv_to_ranklib(input_csv, "temp.txt" if output_ranklib == 'train.txt' else output_ranklib)
    
    if output_ranklib == 'train.txt':
        # Take a random 10% sample of the train file and turn it into a validation file
        split_data('temp.txt', output_ranklib, 'valid.txt', 0.1)

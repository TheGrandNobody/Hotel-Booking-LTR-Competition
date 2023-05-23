import sys, csv, random

def assign_relevance_label(booking_bool: str, click_bool: str) -> str:
    """Assigns a relevance label based on booking_bool and click_bool values.

    Args:
        booking_bool (str): A string indicating if a booking was made.
        click_bool (str): A string indicating if a click was made.

    Returns:
        str: A relevance label. '5' if a booking was made, '1' if a click was made, and '0' otherwise.
    """
    if booking_bool == '1':
        return '5'
    elif click_bool == '1':
        return '1'
    else:
        return '0'

def convert_csv_to_ranklib(input_csv: str, output_ranklib: str, batch_size=1000) -> None:
    """Converts a csv data file to a RankLib file.

    Args:
        input_csv (str): The path to the input CSV file.
        output_ranklib (str): The name of the output RankLib file.
        batch_size (int): The number of lines to write at once.
    """
    # Open the input CSV file for reading and the output RankLib file for writing
    with open(input_csv, 'r') as csvfile, open(output_ranklib, 'w') as ranklibfile:
        
        # Create a CSV reader with a dictionary interface
        reader = csv.DictReader(csvfile)

        # Initialize a list to store the RankLib lines
        batch = []
        
        # Iterate through each row in the CSV file
        for row in reader:

            # Extract the search ID from the row and create a dictionary of the remaining features
            srch_id = row['srch_id']
            features = dict(row)
            del features['srch_id']

            # If we're creating the temporary RankLib file, assign a relevance label based on the booking_bool and click_bool values
            if output_ranklib == 'temp.txt':
                relevance_label = assign_relevance_label(row['booking_bool'], row['click_bool'])
                ranklib_line = f"{relevance_label} qid:{srch_id}"
                del features['booking_bool']
                del features['click_bool']
                del features['position']
            else:
                ranklib_line = f"0 qid:{srch_id}"

            # Create a string for the features in the format "index:value"
            features_str = ' '.join(f'{i+1}:{v}' for i, (k, v) in enumerate(features.items()))

            # Add the RankLib line to the batch
            batch.append(f"{ranklib_line} {features_str}\n")

            # If the batch has reached the specified size, write the lines to the output file and clear the batch
            if len(batch) >= batch_size:
                ranklibfile.writelines(batch)
                batch = []

        # If there are any remaining lines in the batch, write them to the output file
        if batch:
            ranklibfile.writelines(batch)



def split_data(input_file: str, output_train: str, output_valid: str, valid_ratio: float, batch_size=1000) -> None:
    """ 
    Split a dataset in RankLib format into a training and validation file based on a given percentage.

    Args:
        input_file (str): The name of the input dataset in RankLib format.
        output_train (str): The name of the output training file.
        output_valid (str): The name of the output validation file.
        valid_ratio (float): The percentage of the dataset we would like to use as validation data.
        batch_size (int): The number of lines to write at once.
    """

    # Open the input file and read all the lines
    with open(input_file, 'r') as datafile:
        lines = datafile.readlines()

    # Calculate the total number of lines and the number of lines for the validation set
    total_size = len(lines)
    valid_size = int(total_size * valid_ratio)

    # Generate a set of random indices for the validation set
    valid_indices = set(random.sample(range(total_size), valid_size))

    # Initialize the batches for the training and validation sets
    train_batch, valid_batch = [], []

    # Open the output files for writing
    with open(output_train, 'w') as trainfile, open(output_valid, 'w') as validfile:

        # Iterate over the lines with their indices
        for i, line in enumerate(lines):

            # If the current index is in the validation indices, add the line to the validation batch
            if i in valid_indices:
                valid_batch.append(line)

                # If the validation batch has reached the specified size, write it to the validation file and clear the batch
                if len(valid_batch) >= batch_size:
                    validfile.writelines(valid_batch)
                    valid_batch = []
            else:
                # If the current index is not in the validation indices, add the line to the training batch
                train_batch.append(line)

                # If the training batch has reached the specified size, write it to the training file and clear the batch
                if len(train_batch) >= batch_size:
                    trainfile.writelines(train_batch)
                    train_batch = []

        # If there are any remaining lines in the validation batch, write them to the validation file
        if valid_batch:
            validfile.writelines(valid_batch)

        # If there are any remaining lines in the training batch, write them to the training file
        if train_batch:
            trainfile.writelines(train_batch)


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
        # Take a n% sample of the train file and turn it into a validation file
        split_data('temp.txt', output_ranklib, 'valid.txt', 0.1)
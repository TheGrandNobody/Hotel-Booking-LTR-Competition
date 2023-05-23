import pandas as pd

# Function to extract the prop_id from the features
def extract_prop_id(features):
    for feature in features.split():
        index, value = feature.split(':')
        if index == '2':
            return int(value)
    return None

# Load the scores
scores_data = pd.read_csv('score.txt', sep='\t', header=None, names=['srch_id', 'doc_id', 'score'])

# Convert the scores to float
scores_data['score'] = scores_data['score'].astype(float)

# Load the test data
test_data = []
with open('test.txt', 'r') as f:
    for line in f:
        line = line.strip().split(' ', 2)
        srch_id = int(line[1].split(':')[1])
        features = line[2]
        prop_id = extract_prop_id(features)
        test_data.append([srch_id, prop_id, features])

test_data = pd.DataFrame(test_data, columns=['srch_id', 'prop_id', 'features'])

# Create a dictionary of grouped rows by srch_id
grouped_test_data = test_data.groupby('srch_id')

# Initialize an empty list to hold the correct prop_ids
correct_prop_ids = []

# Loop over the scores_data DataFrame
for index, row in scores_data.iterrows():
    srch_id = row['srch_id']
    doc_id = row['doc_id']
    group = grouped_test_data.get_group(srch_id)
    prop_id = group.iloc[int(doc_id)]['prop_id']
    correct_prop_ids.append(prop_id)

# Add the correct prop_ids to the scores_data DataFrame
scores_data['prop_id'] = correct_prop_ids

# Sort by srch_id and score
scores_data.sort_values(by=['srch_id', 'score'], ascending=[True, False], inplace=True)

# Save the sorted data to a CSV file, dropping the redundant doc_id column
scores_data[['srch_id', 'prop_id']].to_csv('output.csv', index=False)
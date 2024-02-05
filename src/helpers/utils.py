import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def prepare_train_examples(train_filepath: str)-> pd.DataFrame:
    train = pd.read_csv(train_filepath)
    train['examples'] = "Question: " + train['Question Text'] + ", Answer: " + train['Question Answer'] + ", Filename: " + train['Reference Document'] + ", Paragraph(s) Number: " + train['Paragraph(s) Number'] + ", Keywords: " + train['Keywords']
    train[['examples']].to_csv("src/data/train_examples.csv", index=False)
    return train['examples'][0: 4]

def prepare_context_data(folder_path: str):
    # Initialize an empty list to store DataFrames
    dfs = []

    for file in os.listdir(folder_path):
        for i in range(1, 7):
            if str(i) in file:
                # Create a DataFrame for each i with the format book_i
                df = pd.read_excel(os.path.join(folder_path, file))
                df.columns = ['paragraph', 'content']
                df['filename'] = f"TG Booklet {i}"
                dfs.append(df)

    # Concatenate all the DataFrames into one
    merged_df = pd.concat(dfs, ignore_index=True)

    # Create the 'context' column
    merged_df['context'] = (
        "Filename: " + merged_df['filename'] +
        ", Paragraph(s) Number: " + merged_df['paragraph'].astype('str') +
        ", Content: " + merged_df['content']
    )

    return merged_df[['context']]

def load_test_data(test_filepath: str):
    df_test = pd.read_csv(test_filepath)
    return df_test


def prepare_submit_files(df: pd.DataFrame):
# Assuming your DataFrame is named 'df'
    df['Target'] =  df['answer']
    df['Reference Document'] = df['filename']
    df['Paragraph(s) Number'] = df['paragraph']
    df['Keywords'] = df['keywords']

    # Selecting and renaming the columns
    result_df = df[['ID', 'Target', 'Reference Document', 'Paragraph(s) Number', 'Keywords']].rename(columns={'ID': 'ID'})
    new_result_df = pd.DataFrame(columns=['ID', 'Target'])

    for index, row in result_df.iterrows():
        new_row = {
            'ID': row['ID'] + '_question_answer',
            'Target': row['Target']
        }
        new_result_df = new_result_df.append(new_row, ignore_index=True)

        new_row = {
            'ID': row['ID'] + '_reference_document',
            'Target': row['Reference Document']
        }
        new_result_df = new_result_df.append(new_row, ignore_index=True)

        new_row = {
            'ID': row['ID'] + '_paragraph(s)_number',
            'Target': row['Paragraph(s) Number']
        }
        new_result_df = new_result_df.append(new_row, ignore_index=True)

        new_row = {
            'ID': row['ID'] + '_keywords',
            'Target': row['Keywords']
        }
        new_result_df = new_result_df.append(new_row, ignore_index=True)

    return new_result_df.fillna(0)

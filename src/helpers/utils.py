import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def prepare_train_examples(train_filepath: str)-> pd.DataFrame:
    train = pd.read_csv(train_filepath)
    train['examples'] = "Question: " + train['Question Text'] + ", Answer: " + train['Question Answer'] + ", Filename: " + train['Reference Document'] + ", Paragraph(s) Number: " + train['Paragraph(s) Number'] + ", Keywords: " + train['Keywords']
    return train['examples'][0: 15]

def prepare_context_data(folder_path: str):
    # Initialize an empty list to store DataFrames
    dfs = []

    for file in os.listdir(folder_path):
        for i in range(1, 7):
            if str(i) in file:
                # Create a DataFrame for each i with the format book_i
                df = pd.read_csv(os.path.join(folder_path, file))
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






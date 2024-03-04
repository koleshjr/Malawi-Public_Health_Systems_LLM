import os
import pandas as pd
import re
import warnings
from langchain.docstore.document import Document
warnings.filterwarnings("ignore")

def prepare_train_examples(train_filepath: str)-> pd.DataFrame:
    train = pd.read_csv(train_filepath)
    train['examples'] = "Question: " + train['Question Text'] + ", Answer: " + train['Question Answer'] + ", Filename: " + train['Reference Document'] + ", Paragraph(s) Number: " + train['Paragraph(s) Number'] + ", Keywords: " + train['Keywords']
    train[['examples']].to_csv("src/data/train_examples.csv", index=False)
    return train['examples'][0: 4]



def extract_booklet_number(filename: str) -> str:
    match = re.search(r'TG Booklet \d+', filename)
    if match:
        return match.group()
    else:
        return ""

def prepare_context_data(folder_path: str):
    # Initialize an empty list to store DataFrames
    dfs = []

    for file in os.listdir(folder_path):
        booklet_number = extract_booklet_number(file)
        if booklet_number:
            print(booklet_number)
            # Create a DataFrame for each file with the format book_i
            df = pd.read_excel(os.path.join(folder_path, file))
            df.columns = ['paragraph', 'content']
            df['filename'] = booklet_number
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
def split_content(content, max_words=1000):
    """
    Splits the content into chunks of approximately `max_words` words each.
    """
    content = str(content)
    words = content.split()
    num_words = len(words)
    num_chunks = (num_words + max_words - 1) // max_words  # Ceiling division to calculate number of chunks

    chunks = []
    for i in range(num_chunks):
        start_index = i * max_words
        end_index = min((i + 1) * max_words, num_words)
        chunk = " ".join(words[start_index:end_index])
        chunks.append(chunk)

    return chunks

def process_csv(folder_path, csv_file):
    """
    Reads the CSV file, processes content, and creates Document objects.
    """
    documents = []
    booklet_number = extract_booklet_number(csv_file)
    if booklet_number:
        print(booklet_number)
        # Create a DataFrame for each file with the format book_i
        df = pd.read_excel(os.path.join(folder_path, csv_file))
        df.columns = ['paragraph', 'content']
        df['filename'] = booklet_number

        # Assuming you have a CSV reader (e.g., using pandas)
        for index, row in df.iterrows():
            content = row["content"]
            paragraph_number = row["paragraph"]
            filename = row['filename']

            if len(str(content).split()) > 1000:    
                # Split content into chunks
                content_chunks = split_content(content, max_words=1000)
                for i, chunk in enumerate(content_chunks):
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            "source": filename,
                            "paragraph": paragraph_number,
                        }
                    )
                    documents.append(doc)
            else:
                # No need to split
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": filename,
                        "paragraph": paragraph_number,
                    }
                )
                documents.append(doc)

    return documents



def prepare_docs_list(folder_path: str):
    # Initialize an empty list to store DataFrames
    docs_all = []

    for file in os.listdir(folder_path):
        docs = process_csv(folder_path=folder_path, csv_file=file)
        docs_all.extend(docs)
    
    return docs_all

# Define the function to extract information
def extract_info(column):
    try:
        column_value = column  # Access the string element from the list
        answer = column_value.split('[/INST] ')[-1].split(',\n\n')[0]
        filename = column_value.split(',\n\n')[1]
        paragraph = column_value.split(',\n\n')[2]
        keywords = column_value.split(',\n\n')[3]
        keywords = keywords.replace(' </s>', '')
        keywords = keywords.replace('</s>', '')
        return answer, filename, paragraph, keywords
    except Exception as e:
        print(f"Error: {e}")
        return " ", " ", " ", " "


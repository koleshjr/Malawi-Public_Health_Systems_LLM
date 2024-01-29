class Config:
  # data configs
  folder_path = "src/data/"
  test_filepath = "src/competition_data/Test.csv"
  submission_filepath = "src/competition_data/SampleSubmission.csv"
  train_filepath = "src/competition_data/Train.csv"

  # unify instruct template
  malawi_template = """
    You are a very helpful assistant for question answering tasks.
    Use the pieces of retrieved context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    You can also use the examples to get a better understading of how you are supposed to answer the question.


    Query: 
        {query}
    Retrieved Contexts:
        {context}
    Examples:
        {examples}

    Output format: Answer the user query \n{format_instructions}
   
   










"""

  


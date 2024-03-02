class Config:
  # data configs
  folder_path = "src/data/"
  test_filepath = "src/competition_data/Test.csv"
  test_filepath_with_rag = "src/output/test_with_rag.csv"
  submission_filepath = "src/competition_data/SampleSubmission.csv"
  train_filepath = "src/competition_data/Train.csv"

  # unify instruct template
  malawi_template = """
    You are a very helpful assistant for question answering tasks.
    Use the pieces of retrieved context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Question: 
        {query}
    Rely on these retrieved contexts to answer the question. Don't try to make up an answer if the context doesn't contain the answer.
        {context}
    Examples to show how to answer the question:
        "Question": Is HMIS an abbreviation mentioned in the TG, and what does it stand for?
        helpful answer:
                Answer: Health Management Information System,
                Filename: TG Booklet 6,
                Paragraph: 106,
                Keywords: Health Management Information System",


        "Question": When should problems with reporting be addressed and solutions developed?
        helpful answer:
                Answer: Problems with reporting should be addressed as soon as they are identified through monitoring, and solutions should be developed immediately to correct poor performance and improve data quality and reporting.,
                Filename: TG Booklet 4,
                Paragraph: 241-244,
                Keywords: Problem Addressing, Reporting Issues, Solution Development, Monitoring, Poor Performance Correction, Data Quality Improvement",
                

        "Question": How do the attack rates among different age groups compare in Bacterial Meningitis, Chikungunya, and Buruli Ulcer?
        helpful answer:
                Answer: Attack rates are highest among children aged less than 15 years in Bacterial Meningitis, while the text does not provide specific information on age-related attack rates for Chikungunya and Buruli Ulcer.,
                Filename: TG Booklet 6,
                Paragraph: 142, 154,
                Keywords: Attack Rates: Bacterial Meningitis, Chikungunya, BU",

    Now your turn to answer the question and you must provide the answer in this format\n{format_instructions}


"""

  


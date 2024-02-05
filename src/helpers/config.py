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

    Question: 
        {query}
    Rely on these retrieved contexts to answer the question. Don't try to make up an answer if the context doesn't contain the answer.
        {context}
    Examples to show how to answer the question:
    1. "Question": Is HMIS an abbreviation mentioned in the TG, and what does it stand for?
        helpful answer:
                answer: Health Management Information System,
                filename: TG Booklet 6,
                paragraph: 106,
                keywords: Health Management Information System",


    2. "Question": When should problems with reporting be addressed and solutions developed?
        helpful answer:
                answer: Problems with reporting should be addressed as soon as they are identified through monitoring, and solutions should be developed immediately to correct poor performance and improve data quality and reporting.,
                filename: TG Booklet 4,
                paragraph: 241-244,
                keywords: Problem Addressing, Reporting Issues, Solution Development, Monitoring, Poor Performance Correction, Data Quality Improvement",
                

    3. "Question": How do the attack rates among different age groups compare in Bacterial Meningitis, Chikungunya, and Buruli Ulcer?
        helpful answer:
                answer: Attack rates are highest among children aged less than 15 years in Bacterial Meningitis, while the text does not provide specific information on age-related attack rates for Chikungunya and Buruli Ulcer.,
                filename: TG Booklet 6,
                paragraph: 142, 154,
                keywords: Attack Rates: Bacterial Meningitis, Chikungunya, BU",

    Important Rules to follow:
        1. Filename can only be TG Booklet 1, TG Booklet 2, TG Booklet 3, TG Booklet 4, TG Booklet 5 or TG Booklet 6 
        2. Answer can only be found within one of the booklets not multiple
        2. Paragraph answers should be in either of these formats:
            129 - if the answer is in a single paragraph for example in example 1
            129-132 - if the answer spans multiple paragraphs that are sequential for example in example 2
            134, 154 - if the answer is in multiple non-sequential paragraphs for example in example 3

    Now your turn to answer the question and you must provide the answer in this format\n{format_instructions}. Don't add any additional information.


"""

  


class Config:
  # data configs
  folder_path = "src/data/"
  test_filepath = "src/competition_data/Test.csv"
  submission_filepath = "src/competition_data/SampleSubmission.csv"
  train_filepath = "src/competition_data/Train.csv"

  # unify instruct template
  malawi_template = """
    You are a very helpful assistant for question answering tasks. 👍
    Use the pieces of retrieved context to answer the question at the end while following the below rules enclosed in dollar signs

        $$$
        - Filename can only be TG Booklet 1, TG Booklet 2, TG Booklet 3, TG Booklet 4, TG Booklet 5 or TG Booklet 6 
        - Answer can only be found within one of the booklets not multiple
        - Paragraph answers should be in either of these formats:
            -single paragraph e.g:
                129 - if the answer is in a single paragraph for example in example 1
            
            -multiple paragaraphs that follow each other e.g:
                129-132 - if the answer spans multiple paragraphs that are sequential for example in example 2

            -multiple paragraphs that do not follow each other e.g:
                134, 154 - if the answer is in multiple non-sequential paragraphs for example in example 3
        $$$
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Please Please pay attention to how you should answer the paragraph from the above rules

    *Question:*
        {query}

    *Context:*
        {context}
 
    *Answer Format:*
        answer: "answer to the question",
        filename: "TG Booklet  where the answer is found",
        paragraph: "paragraph number or numbers where the answer is found",
        keywords: "important keywords that support the answer"

    *Some examples of how to answer the question are:*

    - *Question:* Is HMIS an abbreviation mentioned in the TG, and what does it stand for?
        *Answer:*
            answer: Health Management Information System,
            filename: TG Booklet 6,
            paragraph: 106,
            keywords: Health Management Information System

    - *Question:* When should problems with reporting be addressed and solutions developed?
        *Answer:*
            answer: Problems with reporting should be addressed as soon as they are identified through monitoring, and solutions should be developed immediately to correct poor performance and improve data quality and reporting.,
            filename: TG Booklet 4,
            paragraph: 241-244,
            keywords: Problem Addressing, Reporting Issues, Solution Development, Monitoring, Poor Performance Correction, Data Quality Improvement

    - *Question:* How do the attack rates among different age groups compare in Bacterial Meningitis, Chikungunya, and Buruli Ulcer?
        *Answer:*
            answer: Attack rates are highest among children aged less than 15 years in Bacterial Meningitis, while the text does not provide specific information on age-related attack rates for Chikungunya and Buruli Ulcer.,
            filename: TG Booklet 6,
            paragraph: 142, 154,
            keywords: Attack Rates: Bacterial Meningitis, Chikungunya, BU


    Now it's your turn to answer the question and you must provide the answer in this format\n{format_instructions}. Don't add any additional information.


"""

  


import scrapy
import pandas as pd
import os

class MonSpider(scrapy.Spider):
    name = 'mon_spider'
    start_urls = ['https://almofiid.com/%D8%A7%D8%B3%D8%A6%D9%84%D8%A9-%D8%AF%D9%8A%D9%86%D9%8A%D8%A9-%D8%A7%D8%B3%D9%84%D8%A7%D9%85%D9%8A%D8%A9-%D9%84%D9%84%D9%85%D8%B3%D8%A7%D8%A8%D9%82%D8%A7%D8%AA-%D9%88%D8%A7%D8%AC%D8%A7%D8%A8%D8%AA/#google_vignette']

    def parse(self, response):
        data = []

        # Use the provided XPath for selecting the list containing questions and answers
        question_list = response.xpath('/html/body/div[1]/div/div/div[2]/div/div/article/div[1]/div[1]/ul[3]')

        for question_li in question_list.xpath('li'):
            # Extract the question text
            question_text = question_li.xpath('strong[contains(text(), "السؤال")]/following-sibling::text()').get()

            # Extract the options and answer
            options_and_answer = question_li.xpath('strong[contains(text(), "الإجابة")]/following-sibling::text()').getall()
        
            answer = options_and_answer[-1].strip() if options_and_answer else None

            data.append({
                'question': question_text.strip() if question_text else None,
                'answer': answer,
            })

            # Add print statements for debugging
            print(f'Question: {question_text}, Answer: {answer}')

        # Check if any data is extracted
        if data:
            # Convert the data to a pandas DataFrame
            df = pd.DataFrame(data)

            # Specify the directory where you want to save the CSV file
            output_directory = 'C:\\Users\\DELL\\Documents\\MBD\\S3\\Deep Learning MBD 2023\\Project\\Angular app'

            # Ensure the directory exists; create it if necessary
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Save the DataFrame to a CSV file in the specified directory
            csv_file_path = os.path.join(output_directory, 'out_data.csv')
            df.to_csv(csv_file_path, encoding='utf-8-sig', index=False)

            self.log(f'Data saved to {csv_file_path} file.')
        else:
            self.log('No data extracted.')

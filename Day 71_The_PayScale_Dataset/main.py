import os
import pandas
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from scraper import WebScraper

# ------------- OBJECTIVE ------------------------------------------------------ #
# The PayScale dataset from the last lesson was from 2008 and looked at the prior 10 years.
# Finance ranked very high on post-degree earnings at the time. However, there was a massive
# financial crash in that year. Perhaps things have changed. Use what you've learned about
# web scraping and share some updated information from PayScale's website in the comments below.
# Website: https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors

# BEFORE START: Go to https://www.payscale.com/robots.txt and check that they are ok with me scraping their site. ✅


# # ------------- SCRAPE DATA FROM COLLEGE SALARY REPORT 2021  ------------------- #
scraper = WebScraper()

# --- Check url and path:
print(f"{scraper.url = }")
print(f"{scraper.file_path = }")
#     --> scraper.url = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/'
#     --> scraper.file_path = './pages/bachelors_salary_2021_page{}.html'

# --- Scrape data:
scraper.scrape_and_save_pages(1, 34)

# -- Check for missing/bad pages:
page_overview = scraper.get_page_overview()
print(f"{page_overview = }")
#     --> page_overview = {'desired number of pages': 34, 'actual number of pages': 31,
#         'missing pages': [1, 10, 12], 'bad pages': []}

for page in page_overview['missing pages']:   # Scrape missing pages
    scraper.scrape_and_save_page(page)

print(scraper.get_page_overview())
#     --> {'desired number of pages': 34, 'actual number of pages': 34, 'missing pages': [], 'bad pages': []}


# ----------- OPEN PAGES, MAKE SOUP, GET RELEVANT VALUES, MAKE RAW DATAFRAME ----------------------- #
def make_df_from_pages():
    current_page = 1
    raw_df = None
    pages = os.listdir('./pages')
    for _ in range(len(pages)):
        with open('./pages/bachelors_salary_2021_page{}.html'.format(current_page)) as file:  # Open html-files and make soup.
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.find('title').text
        if content == "Not Found":
            print(f'{current_page} is empty')
        elif 'Error' in title:
            print(f'{current_page} - Error')
        else:
            soup_headers = soup.find_all(name='th', class_='data-table__header')
            column_headers = [header.text for header in soup_headers]
            # -->   ['Rank', 'Major', 'Degree Type', 'Early Career Pay', 'Mid-Career Pay', '% High Meaning']

            # Header explanations: the text that shows up when hovering over a table header.
            soup_data_tips = [header.findChild(name='span', class_='pxl-tooltip') for header in soup_headers]
            header_explanation = [(element['data-tip'] if element is not None else '-')
                                  for element in soup_data_tips]

            # Get table content (all rows):
            soup_table_content = soup.find_all(name='tr', class_='data-table__row')
            rows = [[cell.text.split(':')[1] for cell in row] for row in soup_table_content]
            #       cell.text example -> "Major:Petroleum Engineering"

            if raw_df is None:  # If this is the first loop:
                rows.insert(0, header_explanation)     # Insert header_explanation at index 0 in row_list_1
                raw_df = pd.DataFrame.from_records(data=rows, columns=column_headers)
            else:
                new_page_df = pd.DataFrame.from_records(data=rows, columns=column_headers)
                new_raw_df = pandas.concat([raw_df, new_page_df])
                raw_df = new_raw_df
        current_page += 1
    raw_df.to_csv(f'./raw_csv/raw_college_salary_report_2021.csv', mode='w', index_label=False, header=True)


make_df_from_pages()


# ---------- PRELIMINARY DATA EXPLORATION -------------------------------------------- #
raw_data = pd.read_csv('./raw_csv/raw_college_salary_report_2021.csv')
df = raw_data.reset_index(drop=True)    # Reset index
df = df.drop([0])   # Delete row with column label explanations (at index 0)


# # --- Format numbers:
def format_numbers(data_frame, column_name: str, del_chars='$%,', not_number_value='-'):
    """
    Iterate through values in column and:\n
    - Delete del_chars if present.
    - Replace values equal to not_number_value with the string 'NaN'.
    - Convert Non-NaN-values to integers.\n
    Return number of NaN-values in the column.
    """
    non_number_count = 0
    for (col, row) in data_frame.iterrows():
        value = row[f'{column_name}']
        new_value = value.translate({ord(i): None for i in del_chars})  # Delete del_chars from string.
        if new_value == not_number_value:
            non_number_count += 1
            new_value = new_value.replace(not_number_value, 'NaN')
        else:
            new_value = int(new_value)

        row[f'{column_name}'] = new_value   # Make change in df.
    print(f"There were {non_number_count} occurrences of the string '{not_number_value}' in the column '{column_name}'")
    return non_number_count


format_numbers(df, 'Early Career Pay')
# # --> There were 0 occurrences of the string '-' in the column 'Early Career Pay'
df['Early Career Pay'] = pd.to_numeric(df['Early Career Pay'])

format_numbers(df, 'Mid-Career Pay')
# # --> There were 0 occurrences of the string '-' in the column 'Mid-Career Pay'
df['Early Career Pay'] = pd.to_numeric(df['Early Career Pay'])

format_numbers(df, '% High Meaning')
# # --> There were 64 occurrences of the string '-' in the column '% High Meaning'


import os
import requests
from bs4 import BeautifulSoup

# Scraping the webpage and making soup is done in separate steps. HTML-content is saved to a 
# html-file to limit the number of requests to the website's server. In addition, this method 
# makes it easy to detect (a) if there are any missing pages, and (b) if some of the saved 
# files only contain html code for an error page, or only the text 'Not Found' (here reffered 
# to as 'bad pages'). 

class WebScraper():
    def __init__(self):
        self.url = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/'
        self.dir = './pages'
        self.file_path = './pages/bachelors_salary_2021_page{}.html'
        self.desired_number_of_pages = 34
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                          '(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

    def scrape_and_save_page(self, page_nr):
        """
        Request self.url{page_nr} and save the webpage content to a html-file with the path
        'self.file_path.format(page_nr)'.
        Then call self.bad_page_check(page_nr).
        """
        r = requests.get(url=f"{self.url}{page_nr}", headers=self.headers)
        r.raise_for_status()
        page = r.text
        with open(self.file_path.format(page_nr), mode='w') as f:
            f.write(page)
        self.bad_page_check(page_nr)
        self.get_page_overview()

    def scrape_and_save_pages(self, first_page, last_page):
        """
        :param first_page: number (int) of the first page to be scraped.
        :param last_page: number (int) of the last page to be scraped.
        :return: None. (Saves the html-content to 'self.file_path.format(page_nr)').

        This method will:\n
        Request html-content from {self.url}{page_nr} for page_nr in range (first_page through last_page),
        and write (save) the page-content from each page to a file with the path 'self.file_path.format(page_nr)'.\n\n

        {page_nr} is a local variable set to the page-number that is being scraped in the current loop.
        """
        current_page_nr = first_page
        while current_page_nr <=last_page:
            self.scrape_and_save_page(current_page_nr)
            page_nr += 1

    def bad_page_check(self, page_nr):
        """
        Checks if the file 'self.file_path.format(page_nr)' is bad,
        and if so, asks if you want to delete it.\n

        * A bad page = a file thath:
            - only contain the text 'Not Found'
            - contain html-code with 'Error' in the <title>
        """
        try:
            with open(self.file_path.format(page_nr)) as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')

        except FileNotFoundError:
            print(f"Page/file nr. {page_nr} is missing.")

        else:
            if content == "Not Found":
                print(f'For page number {page_nr}: {content = }.')
                self.delete_pages([page_nr])

            if "Error" in soup.find('title').text:
                print(f'Title of page {page_nr} contains "Error".')
                self.delete_pages([page_nr])

    def actual_number_of_pages(self):
        return len(os.listdir(self.dir))

    def get_page_overview(self):
        """ Check the directory {self.dir} for bad and missing pages (files). Return a dict with
        'desired number of pages', 'actual number of pages', 'missing pages' and 'bad pages'.

        Bad page = a file that:
            - only contain the text 'Not Found'.
            - contain html-code with 'Error' in the <title>.
        Missing pages =
            - Page-numbers from 1 through {self.desired_number_of_pages} that doesn't have a
            corresponding file.
        """

        page_overview = {
            'desired number of pages': self.desired_number_of_pages,
            'actual number of pages': len(os.listdir(self.dir)),
            'missing pages': [],
            'bad pages': [],
        }
        current_page = 1
        for _ in range(self.desired_number_of_pages):
            try:
                with open(self.file_path.format(current_page)) as file:
                    content = file.read()
                    soup = BeautifulSoup(content, 'html.parser')

            except FileNotFoundError:
                page_overview['missing pages'] += [current_page]

            else:
                if content == "Not Found" or "Error" in soup.find('title').text:
                    page_overview['bad pages'].append(current_page)

            current_page += 1
        return page_overview

    def print_page_overview(self):
        print('\nPAGE OVERVIEW:')
        for (key, value) in self.get_page_overview():
            print(f"{key}: {value}")

    def delete_pages(self, page_list: list):
        for page_nr in page_list:
            file_path = self.file_path.format(page_nr)
            q_delete = input(f'Do you want to delete {file_path}?\nType [y] or [n]: ')
            if q_delete == 'y':
                os.remove(file_path)
                self.get_page_overview()



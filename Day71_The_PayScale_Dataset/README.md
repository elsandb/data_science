# Data exploration with Pandas

Goal: To get to know the pandas module.

### The PayScale Dataset 2021

In day 71 of 100 Days of Code*, we looked at data from PayScale concerning salary level for different Undergraduate 
majors. The dataset was from 2008 and looked at the prior 10 years. Finance ranked very high on post-degree earnings 
at the time, but this may have changed after the financial crash that year. To get some updated information, I've 
taken a look at a table from PayScale's College Salary Report, called "Highest Paying Jobs With a Bachelor’s Degree", 
which is updated for 2021. 

- **main.py:**
The contents of the table "Highest Paying Jobs With a Bachelor’s Degree" is extracted from 
https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors 
using HTTP requests and BeautifulSoup, and saved to "raw_college_salary_report_2021.csv".


- **scraper.py:** Contains the class WebScraper. 
  - It can be used to scrape websites with multiple pages if the 
  url-endings are '.../{an_integer}'. With a little modification, it would work with other endings saved in a list.
  
  - Scraping the webpage and 'making soup' is done in separate steps. The HTML-content is first saved to a
  html-file to limit the number of requests to the website's server. This also makes it easy to detect 
  - (a) if there are any missing pages, and (b) if any of the saved files contain html code for an error page 
  - or the text 'Not Found' (here referred to as 'bad pages').

- **ThePayScaleDataset.ipynb:** Here I'm exploring the data with pandas.

---

\* **100 Days of Code:** The Complete Python Pro Bootcamp for 2023. https://www.udemy.com/course/100-days-of-code/ 

**Tip:** https://gka.github.io/palettes makes it easy to find colors 👏
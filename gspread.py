''' Import important libraries '''

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Set the URL of the website to be scraped
url = 'https://edition.cnn.com/'

# Set the headers with user-agent information for the request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1.0.0.0 Safari/5.36'}

# Send a GET request to the URL with the specified headers
re = requests.get(url, headers=headers)

# Parse the HTML content of the response
soup = bs(re.content, 'html.parser')

# Create an empty list to store the extracted news headlines
news_list = []

# Find all HTML elements with the attribute 'data-editable' set to 'headline'
news_headline = soup.find_all('span', {'data-editable': 'headline'})

for news in news_headline[7:27]:
    news_list.append(news.text)

# Create a pandas DataFrame from the news_list
df = pd.DataFrame(zip(news_list), columns=['Headline'])

# Load credentials from a service account JSON file
creds = Credentials.from_service_account_file(r"C:\Users\Mauz Khan\Desktop\vscode\GS API.json",
                                              scopes=["https://spreadsheets.google.com/feeds",
                                                      "https://www.googleapis.com/auth/drive"])

# Authorize the client using the obtained credentials
client = gspread.authorize(creds)

# Set the ID of the target Google Spreadsheet
spreadsheet_id = '1aRfvmI0rj1Ks5apyYRLQKwRAhmrb6mIznAhUTYqco6o'
spreadsheet = client.open_by_key(spreadsheet_id)

worksheet = spreadsheet.get_worksheet(0)

# Append the rows of the DataFrame to the worksheet, specifying the value input option
worksheet.append_rows(df.values.tolist(), value_input_option='USER_ENTERED')

import os
import json
import pytz

from datetime import datetime
from dotenv import load_dotenv

from crawler.selenium_utils import get_chromedriver
from crawler.wikipedia_main_page import WikipediaNewsPage

from aws_utils.boto_wrapper import upload_file_to_s3

#quick selenium flow
driver = get_chromedriver()
wiki_page = WikipediaNewsPage(driver)
wiki_page.navigate()
content_dict = wiki_page.get_daily_content()


bucket_name = os.getenv('AWS_BUCKET_NAME')
tel_aviv_tz = pytz.timezone('Asia/Jerusalem')
now = datetime.now(tel_aviv_tz)
current_time = now.strftime("%Y-%m-%d_%H-%M-%S_%Z")
file_name = f"wikipedia_{current_time}.json"
directory = os.path.abspath(os.path.join("data_output"))

if not os.path.exists(directory):
    os.makedirs(directory)
file_path = os.path.join(directory, file_name)


with open(file_path,"w") as f:
    json.dump(content_dict,f,indent=4)

upload_file_to_s3(file_path, bucket_name, file_name)

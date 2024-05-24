from selenium.common.exceptions import TimeoutException

from crawler.base_page import BasePage


class WikipediaNewsPage(BasePage):
    def __init__(self, driver):

        super().__init__(driver)
        self.news_container = "#mp-right #mp-itn"
        self.on_this_day_section_container = "#mp-right #mp-otd"

        self.base_url = "https://en.wikipedia.org/wiki"
        self.url = f"{self.base_url}/Main_Page"

        self.ignore_links = ["Archive", "By email", "List of days of the year"]

    def get_daily_content(self):
        rd = {}
        rd["on_this_day_text"] = self.elem(self.news_container).text
        rd["in_the_news_text"] = self.elem(self.on_this_day_section_container).text

        # getting interesting links to crawl
        links_elem_otd = self.elems(f"{self.on_this_day_section_container} a")
        otd_links_dict = {
            link.text: link.get_attribute("href") for link in links_elem_otd
        }
        links_elem_itn = self.elems(f"{self.on_this_day_section_container} a")
        itn_links_dict = {
            link.text: link.get_attribute("href") for link in links_elem_itn
        }

        # cleaning image links
        keys_to_remove = self.ignore_links
        for given_dict in [otd_links_dict, itn_links_dict]:
            for key, value in otd_links_dict.items():

                given_dict[key] = value.replace(self.base_url, "")
                if key == "":
                    keys_to_remove.append(key)
                elif value[-4:] == ".tif":
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                del given_dict[key]

        rd["on_this_day_links"] = itn_links_dict
        rd["in_the_news_links"] = otd_links_dict
        return rd

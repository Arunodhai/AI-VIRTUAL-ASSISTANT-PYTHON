from selenium import webdriver
class music():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    def play(self,query):
        self.query=query
        self.driver.get(url="https://www.youtube.com/results?search_query="+query)
        video= self.driver.find_element_by_xpath('//*[@id="title-wrapper"]')
        video.click()







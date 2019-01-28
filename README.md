# Takealot

I noticed Takealot's prices changing quite often so I created a python script to scrape Takealot.com using Selenium, BeautifulSoup4 and MongoDB to track these price changes. The prices are scraped on a schedule using a task scheduler, then the previous day's prices are compared to the current day's prices and the results are then pushed to a device of your choice using PyPushBullet.

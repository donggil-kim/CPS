import requests
from bs4 import BeautifulSoup
import csv

class Scraper():
    def __init__(self):
        self.url = "http://book.interpark.com/display/collectlist.do?_method=bestsellerHourNew&bookblockname=b_gnb&booklinkname=%BA%A3%BD%BA%C6%AE%C1%B8&bid1=w_bgnb&bid2=LiveRanking&bid3=main&bid4=001#"

    def getHTML(self):
        res = requests.get(self.url)
        if res.status_code !=200:
            print("Request Error : ", res.status_code)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getInfo(self, soup):
        books = soup.find_all("div", class_ = "listItem singleType")
        bookName = []
        bookPrice = []
        bookWriter = []
        bookScore = []

        for b in books:
            bookName.append(b.find("div", class_ = "itemName").text)
            bookPrice.append(b.find("span", class_ = "price").text)
            bookWriter.append(b.find("div", class_ ="itemMeta").text)
            bookScore.append(b.find("div", class_ ="reviewStat").text)

        self.writeCSV(bookName, bookPrice, bookWriter, bookScore)
    
    def writeCSV(self, bookName, bookPrice, bookWriter, bookScore):
        file = open("books.csv", "a", newline="")

        wr = csv.writer(file)

        for i in range(len(bookName)):
            wr.writerow([str(i + 1), bookName[i], bookPrice[i], bookWriter[i], bookScore[i]])

        file.close()

    def scrap(self):

        file = open("books.csv", "w", newline="", encoding ="UTF-8")
        wr = csv.writer(file)
        wr.writerow(["Rank", "bookName", "bookPrice", "bookWriter", "bookScore"])
        file.close()

        Soup = self.getHTML()
        self.getInfo(Soup)

if __name__ == "__main__" :
    s=Scraper()
    s.scrap()
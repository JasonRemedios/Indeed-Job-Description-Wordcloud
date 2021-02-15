import bs4
import requests
import re
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd

counter = 0
descList = []

terms = input('Enter search term(s): ')
pages = int(input('Enter # of pages to scrape: '))

#extract job descriptions and add them to list
def extract(i, index):
    newRes = requests.get('http://ca.indeed.com' + i['href'])
    newRes.raise_for_status()
    newSoup = bs4.BeautifulSoup(newRes.text, features='lxml')
    newElems = newSoup.select('div[id="jobDescriptionText"]')
    print(counter)
    if len(newElems) > 0:
        result = regex.sub(' ', str(newElems[0]))
        descList.append(result)
    


#get first job results page and jobs
search = terms.replace(' ', '+')
res = requests.get('https://ca.indeed.com/jobs?q=' + search + '&l')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features='lxml')
elems = soup.select('a[rel="noopener nofollow"]')

#remove HTML tags
regex = re.compile('<[^>]+>')

#extract jobs from first page
for i in elems:
    extract(i, counter)
    counter += 1

#extract jobs from following pages
page = 0
while page < pages * 10 - 10:
    page += 10
    res2 = requests.get('https://ca.indeed.com/jobs?q=' + search + '&start=' + str(page))
    res2.raise_for_status()
    soup2 = bs4.BeautifulSoup(res2.text, features='lxml')
    elems2 = soup2.select('a[rel="noopener nofollow"]')
    for i in elems2:
        extract(i, counter)
        counter += 1

#create final string and remove line breaks
descStr = ' '.join(descList)
descStr = descStr.replace('\n', ' ')

#create wordcloud
stopwords = set(STOPWORDS)
stopwords.update(["s"])
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(descStr)

#create lists for dataframe
words = wordcloud.words_
wordL = []
weightL = []
countL = []

for i in words:
    wordL.append(i)
    weightL.append(words[i])
    reg = re.compile(r'(?i)' + i)
    count = len(reg.findall(descStr))
    countL.append(count)

#create dataframe
data = {'word': wordL, 'weight': weightL, 'appearances': countL}
df = pd.DataFrame(data)
print(df.to_string())

#Display the wordcloud:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()



from datetime import datetime

class ArticleInfo:
   	def __init__(self, id, title, url, date, sentimentScore, sentimentType):
   		self.id = id
  		self.title = title
  		self.url = url
  		self.date = date
  		self.sentimentScore = sentimentScore
		self.sentimentType = sentimentType

	def printInfo(self, article):
		print article.title
		print "\n ---- " + article.url
		print "\n ---- " + article.date
		print "\n ---- " + article.sentimentType + ": " + str(article.sentimentScore)
		print "\n ========================"

import urllib
import json

apiKey = "29d81ed4d30ec0ae3f439ff00c40529c0750c31a"
url = "https://gateway-a.watsonplatform.net/calls/data/GetNews?apikey=" + apiKey

repCandidates = ["Ben Carson", "Carly Fiorina", "Chris Christie", "Donald Trump", "Jeb Bush", "John Kasich", "Marco Rubio", "Mike Huckabee", "Rand Paul", "Rick Santorum", "Ted Cruz"]
demCandidates = ["Bernie Sanders", "Hillary Clinton", "Martin O'Mally"]

start = "now-3d"
rank = "high^medium"
maxResults = "100"
candidate = "Trump"

url = url + "&outputMode=json&rank=" + rank + "&start=" + start + "&end=now&maxResults=" + maxResults + "&q.enriched.url.enrichedTitle.entities.entity=|text=" + candidate + ",type=person|&return=enriched.url.title,enriched.url.url,enriched.url.docSentiment"

print "url called: \n" + url

request = urllib.urlopen(url)
response = request.read()

try: responseJson = json.loads(str(response))
except: responseJson = None

if responseJson == None :
	print "----- PARSE FAILED -----"

articles = responseJson["result"]["docs"]

for item in articles:
	itemUrl = item["source"]["enriched"]["url"]
	itemDate = datetime.fromtimestamp(int(item["timestamp"])).strftime('%Y-%m-%d %H:%M:%S')
	articleInfo = ArticleInfo(item["id"], itemUrl["title"], itemUrl["url"], itemDate, itemUrl["docSentiment"]["score"], itemUrl["docSentiment"]["type"])
	print articleInfo.printInfo(articleInfo)





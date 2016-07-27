from datetime import datetime
import urllib
import json
import csv
import time

def dataNewsRequest(url):
	print "url called: \n" + url

	request = urllib.urlopen(url)
	response = request.read()

	try: responseJson = json.loads(str(response))
	except: 
		responseJson = None
		print "----- PARSE FAILED -----"
		return

	#Uncomment when there are issues in 
	print json.dumps(responseJson, indent=4)

	return responseJson

def fillCsv(articles):
	for item in articles:
		itemUrl = item["source"]["enriched"]["url"]
		itemDate = datetime.fromtimestamp(item["timestamp"]).strftime('%Y-%m-%d')
		articleInfo = ArticleInfo(item["id"], itemUrl["title"].encode('utf-8'), itemUrl["url"].encode('utf-8'), itemDate, itemUrl["docSentiment"]["score"], itemUrl["docSentiment"]["type"])
		#print articleInfo.printInfo(articleInfo)
		articleCandidate = candidate.replace("+", " ")
		writer.writerow((candidate, articleInfo.id, articleInfo.title, articleInfo.url, articleInfo.date, articleInfo.sentimentScore, articleInfo.sentimentType))

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
		print "\n ---- " + article.id
		print "\n ---- " + article.url
		print "\n ---- " + str(article.date)
		print "\n ---- " + article.sentimentType + ": " + str(article.sentimentScore)
		print "\n ========================"

API_KEY = ""

#candidates captured by the data - can be narrowed down to "relevant candidates" in the future
repCandidates = ["Ben+Carson", "Carly+Fiorina", "Chris+Christie", "Donald+Trump", "Jeb+Bush", "John+Kasich", "Marco+Rubio", "Mike+Huckabee", "Rand+Paul", "Rick+Santorum", "Ted+Cruz"]
demCandidates = ["Bernie+Sanders", "Hillary+Clinton", "Martin+O\'Mally"]
genCandidates = ["Donald+Trump", "Hillary+Clinton"]

#open 
file = open("sentiment_data.csv", "w")
writer = csv.writer(file)
writer.writerow(('candidate', 'ID', 'title', 'url', 'date', 'sentiment_score', 'sentiment_type'))

start = "now-60d"
end = "now"
rank = "high"
count = "1000"

#collect the sentiment data for each candidate and write to sentiment_data.csv
for candidate in genCandidates:

	url = "https://gateway-a.watsonplatform.net/calls/data/GetNews?apikey=" + API_KEY

	url = url + "&outputMode=json&count=" + count + "&rank=" + rank + "&start=" + start + "&end=" + end + "&q.enriched.url.enrichedTitle.entities.entity=|text=" + candidate + ",type=person|&q.enriched.url.title=-[poll]&q.enriched.url.url=-[reddit]&return=enriched.url.title,enriched.url.url,enriched.url.docSentiment"

	jsonData = dataNewsRequest(url)

	while  'result' not in jsonData:
		print "----- TIMEOUT ERROR. RETRYING. -----"
		time.sleep(10)
		jsonData = dataNewsRequest(url)

	if 'docs' not in jsonData["result"]:
		print "----- ERROR RETRIEVING DOCS -----"	
	else:
		articles = jsonData["result"]["docs"]
		fillCsv(articles)

	while True:

		if 'next' not in jsonData ['result']:
			print "----- No more results -----"
			break

		nextUrl = url + "&next=" + jsonData['result']['next'].encode('utf-8')

		jsonData = dataNewsRequest(nextUrl)

		while  'result' not in jsonData:
			print "----- TIMEOUT ERROR. RETRYING. -----"
			time.sleep(10)
			jsonData = dataNewsRequest(nextUrl)

		if 'docs' not in jsonData["result"]:
			print "----- ERROR RETRIEVING DOCS -----"	
		else:
			articles = jsonData["result"]["docs"]
			fillCsv(articles)
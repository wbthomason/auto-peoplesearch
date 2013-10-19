import urllib.request
import urllib.parse
import time
import bs4 as BeautifulSoup

#Because I don't want to check for -1 in main, but want to be able to handle different formats of ID/email.
def find_or_end(content, search):
	content = str(content)
	search = str(search)
	index = content.find(search)
	if index == -1:
		return len(content)
	return index

#Again, I don't want to check for -1 in main, but want some format flexibility in filename.
def rfind_or_end(content, search):
	content = str(content)
	search = str(search)
	index = content.rfind(search)
	if index == -1:
		return len(content)
	return index

#Quick method to grab the name from the page. Not flexible, but the format is unikely to change.
def parse_name(htmldata):
	page = BeautifulSoup.BeautifulSoup(htmldata)
	table = page.table
	if table is not None:
		name = table.tr.td.b.font.contents[0]
		name = name[:name.find('(')-1]
		return str(name)
	return "Not found"

#Ugly and could probably be optimized. Could definitely be extended, which might happen. This will remain the simple utility it currently is for now, though.
if __name__ == '__main__':	
	alias_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
			 		 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			 		 "Accept-Language": "en-US,en;q=0.5",
			 		 "Accept-Encoding": "gzip, deflate",
			 		 "Referer": "http://www.virginia.edu/search/",
			 		 "DNT": 1,
			 		 "Connection": "keep-alive"}

	filename = input("Please input the filename containing aliases to search: ")
	data_file = open(filename, "r")
	new_filename = filename[:rfind_or_end(filename, '.')]
	new_filename = new_filename + "_results.txt"
	results_file = open(new_filename, "a")
	aliases = data_file.readlines()

	for alias in aliases:
		alias = alias[:find_or_end(alias,'@')].strip()
		print("Searching for", alias, "...")
		data = urllib.parse.urlencode({'whitepages': alias})
		data = data.encode('utf-8')
		alias_request = urllib.request.Request("http://www.virginia.edu/cgi-local/ldapweb", headers = alias_headers)
		result = urllib.request.urlopen(alias_request, data)
		name = parse_name(result.read().decode('utf-8'))
		print(alias + " is " +name)
		results_file.write(alias + ": " + name+'\n')
		print("Waiting to avoid getting banned...")
		time.sleep(0.05)

	data_file.close()
	results_file.close()
	print("Searches are complete. Results written to", new_filename)

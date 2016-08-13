''' Mingo's movie_recommend script '''

import itertools
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re

def get_html(url):
	send_headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
		'Accept':'*/*',
		'Connection':'keep-alive',
		'Host':'movie.douban.com'
	}

	req = urllib.request.Request(url,headers = send_headers)
	response = urllib.request.urlopen(req)
	html = response.read().decode('utf-8')

	return html

def analyse(html):
	soup = BeautifulSoup(html,'lxml')
	for i in soup.find_all('a'):
		try:
			content = i['href']
			if '/subject/' in content:
				#print (content)
				break
		except:
			pass
	return content

def tag(html):
	soup = BeautifulSoup(html,'lxml')
	tag = []
	for i in soup.find_all('a'):
		try:
			content = i['href']
			if '/tag/' in content:
				tag.append(i.string)
		except:
			pass

	return tag[1:6]

def tag_sort(tag,tag_all):
	for each in tag:
		if each not in tag_all.keys():
			tag_all[each] = 1
		else:
			tag_all[each]+=1
	return tag_all



def arrange(tag,url_pre):

	url_tag = "https://movie.douban.com/tag/"
	all = []

	for num in range(len(tag), 0, -1):
		s = (list(itertools.combinations(tag, num)))
		#print(s)
		for each in s:
			url = url_tag + urllib.parse.quote(' '.join(each))
			html = get_html(url)
			end = 0
			#print (url)
			for i in range(len(re.findall('a class="nbg" href="', html))):
					start = html.find('a class="nbg" href="', end) + len('a class="nbg" href="')
					end = html.find('"  title=', start)
					name_start = end + len('"  title="')
					name_end = html.find('">', name_start)

					if (html[start:end] not in url_pre) and not re.findall(html[start:end], ''.join(all)):
						all.append(html[name_start:name_end] + "\t" + html[start:end] + "\n")
						if len(all) == 10:
							return ''.join(all)
					#print (html[name_start:name_end] + "\n" + html[start:end])
					#print (start,end,name_start,name_end)


if __name__ == "__main__":
	name = input("movie name:")
	name_list = name.split(',')
	tag_all = {}
	movie_url_all = ""
	for name in name_list:
		#print (name)
		url_pre = "https://movie.douban.com/subject_search?search_text=" + urllib.parse.quote(name)
		html = get_html(url_pre)
		movie_url = analyse(html)
		html_movie = get_html(movie_url)
		movie_tag = tag(html_movie)
		tag_all = tag_sort(movie_tag,tag_all)
		movie_url_all = movie_url_all + movie_url
	#print (tag_all)
	tag_dict = sorted(tag_all.items(), key=lambda x:x[1], reverse=True)
	movie_tag = []
	for ta in tag_dict[:5]:
		movie_tag.append(ta[0])
	#print (movie_tag)
	print (arrange(movie_tag, movie_url_all))

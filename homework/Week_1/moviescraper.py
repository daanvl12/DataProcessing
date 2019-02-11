#!/usr/bin/env python
# Name: Daan van Lanschot
# Student number: 12486124
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
import re
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
	"""
	Extract a list of highest rated movies from DOM (of IMDB page).
	Each movie entry should contain the following fields:
	- Title
	- Rating
	- Year of release (only a number!)
	- Actors/actresses (comma separated if more than one)
	- Runtime (only a number!)
	"""

	# Put all movies in a list
	movie_list = (dom.find_all('div', {'class': 'lister-item mode-advanced'}))
	if movie_list:
		movie_list_extracted = []
		
		# Iterate over movies in list, extract information and add to list
		for movie in movie_list:
			info = movie.h3.a.text.replace(',', '') + "," + movie.find('div', {'class': 'ratings-bar'}).strong.text + "," + re.findall('\d+', movie.h3.find('span', {'class': 'lister-item-year text-muted unbold'}).text)[0] + "," + re.findall('\d+', movie.find('span', {'class': 'runtime'}).text)[0]
			movie_list_extracted.append(info)
			# Title
			 #print(movie.h3.a.text.replace(',', ''))
			# Rating
			 #print(movie.find('div', {'class': 'ratings-bar'}).strong.text)
			# Year of release
			 #re.findall('\d+', movie.h3.find('span', {'class': 'lister-item-year text-muted unbold'}).text)[0]
			 #print(str(movie.h3.find('span', {'class': 'lister-item-year text-muted unbold'}).text).strip('()'))
			# HIER NOG ACTEURS DOEN!!!!
			# Runtime
			 #print(re.findall('\d+', movie.find('span', {'class': 'runtime'}).text)[0])
		return movie_list_extracted

	else:
		return None

def save_csv(outfile, movies):
	"""
	Output a CSV file containing highest rated movies.
	"""
	writer = csv.writer(outfile)
	writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])
	
	# Iterate over all movies and write value to row
	for movie in movies:
		writer.writerow([movie])

	# ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK


def simple_get(url):
	"""
	Attempts to get the content at `url` by making an HTTP GET request.
	If the content-type of response is some kind of HTML/XML, return the
	text content, otherwise return None
	"""
	try:
		with closing(get(url, stream=True)) as resp:
			if is_good_response(resp):
				return resp.content
			else:
				return None
	except RequestException as e:
		print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
		return None


def is_good_response(resp):
	"""
	Returns true if the response seems to be HTML, false otherwise
	"""
	content_type = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200
			and content_type is not None
			and content_type.find('html') > -1)


if __name__ == "__main__":

	# get HTML content at target URL
	html = simple_get(TARGET_URL)

	# save a copy to disk in the current directory, this serves as an backup
	# of the original HTML, will be used in grading.
	with open(BACKUP_HTML, 'wb') as f:
		f.write(html)

	# parse the HTML file into a DOM representation
	dom = BeautifulSoup(html, 'html.parser')

	# extract the movies (using the function you implemented)
	movies = extract_movies(dom)

	# write the CSV file to disk (including a header)
	with open(OUTPUT_CSV, 'w', newline='') as output_file:
		save_csv(output_file, movies)

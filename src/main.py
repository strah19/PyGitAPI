from github import Github
import requests
from pprint import pprint
import os
import sys
import operator

URL_LINK = 'https://raw.githubusercontent.com/strah19/Ember/master/'
GITHUB_API_TOKEN = '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'
GITHUB_USER = 'strah19/Ember'
INCLUDE_HEADER = 'Ember/include'

# Will need to pass in the Ember folder in the command args so we can run it in the HVC

#Inits the github API and creates a repo object
def init_git_api():
	token = os.getenv('GITHUB_TOKEN', GITHUB_API_TOKEN)
	g = Github(token)
	repo = g.get_repo(GITHUB_USER)
	return repo

#Loops through the header files in Ember and loads the contents as raw data for us to use
def load_header_content(contents):
	headers = str()
	for content_file in contents:
		URL = URL_LINK + content_file.path
		page = requests.get(URL)
		headers += page.text
	return headers

repo = init_git_api()

clones = repo.get_clones_traffic(per="day")
views = repo.get_views_traffic(per="day")

print(f"Repository has {clones['count']} clones out of which {clones['uniques']} are unique.")
print(f"Repository has {views['count']} views out of which {views['uniques']} are unique.")

best_day = max(*list((day.count, day.timestamp) for day in views["views"]), key=operator.itemgetter(0))

pprint(views)
print(f"Repository had most views on {best_day[1]} with {best_day[0]} views")

print('Loading in Github Ember headers...')
headers = load_header_content(repo.get_contents(INCLUDE_HEADER))
print(headers)

input('Press enter to exit')
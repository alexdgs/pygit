import urllib2
from lxml.html import fromstring
from githubrepo import GitHubRepo
from githubreadme import GitHubReadme

github_url_prefix = 'http://github.com'
github_search_url_prefix = github_url_prefix + '/search?utf8=%E2%9C%93&type=Repositories&q='
github_search_url_page_token = '&p='
xpath_list_regex = ".//*[@class='repo-list js-repo-list']"
xpath_repo_name = ".//*[@class='repo-list-name']"
xpath_repo_description = ".//*[@class='repo-list-description']"
SEPARATOR = '==================================================='

class GitHubPage:
	
	OPTION_PREV_PAGE = 'p'
	OPTION_NEXT_PAGE = 'n'
	OPTION_QUIT = 'q'
	VALUE_ZERO_CHAR = ord('0')
	
	github_repos = []
	refresh = 0
	next = 1
	page = 0
	
	def __init__(self, query):
		self.query_word = query	
	
	def setPage(self, page):
		if self.page == page:
			self.refresh = 0
		else:
			self.refresh = 1
			self.page = page
	
	def print_results(self):
		if self.refresh == 1:
			print 'Loading results...'
			self.github_repos = []
			response = urllib2.urlopen(github_search_url_prefix + self.query_word + github_search_url_page_token + str(self.page));
			html = response.read()
			root = fromstring(html)
			repo_list_parent = root.find(xpath_list_regex)
			if(repo_list_parent != None):
				for list_item in repo_list_parent:	
					repo_name_item = list_item.find(xpath_repo_name)
					repo_full_name = repo_name_item.find("./a").get('href')
					#print repo_full_name
					repo_description = 'No description available.'
					repo_description_item = list_item.find(xpath_repo_description)
					if(repo_description_item != None):
						repo_description = repo_description_item.text.strip()
						for description_item in repo_description_item:
							repo_description += description_item.text
					#print repo_description
					repo_url = github_url_prefix + repo_full_name
					#print repo_url
					self.github_repos.append(GitHubRepo(repo_full_name, repo_description, repo_url))
		
		change_request = 0
		user_option = 'q'
		while change_request == 0:
			if(len(self.github_repos) > 0):
				print 'Page ' + str(self.page) + ' results'
				print SEPARATOR
				self.next = 1
				counter = 0
				for repo in self.github_repos:
					print 'Result index: ' + str(counter)
					print 'Full name: ' + repo.full_name
					print 'Description: ' + repo.description
					print 'Remote URL: ' + repo.url
					print SEPARATOR
					counter += 1
			else:
				self.next = 0
				print 'Mmm, no results here'
		
		
			print 'What do you want to do?'
			if len(self.github_repos) > 1:
				print 'Enter 0-' + str(len(self.github_repos)-1) + ' to see the README file of the respective result index'
			if self.page > 1:
				print 'Enter p to go to the previous results page'
			if self.next == 1:
				print 'Enter n to go to the next results page'
			print 'Enter any other key to exit'
		
			valid_input = 0
			while valid_input != 1:
				valid_input, user_option = self.interpret_user_input(raw_input())
		
			if user_option == self.OPTION_QUIT or user_option == self.OPTION_NEXT_PAGE or user_option == self.OPTION_PREV_PAGE:
				change_request = 1
			else:
				GitHubReadme(self.github_repos[ord(user_option)-self.VALUE_ZERO_CHAR]).show_readme()
		return user_option
	
	def interpret_user_input(self, s):
		option = s
		if len(s) < 1:
			print 'Oops! You forgot to type an option. Try again'
			return 0, option
		if len(s) > 1:
			print "A single character was enough! So I'm taking the first one"
			option = s.charAt(0)
		
		if option == self.OPTION_QUIT:
			return 1, option
		if option == self.OPTION_NEXT_PAGE:
			if self.next == 1:
				return 1, self.OPTION_NEXT_PAGE
			else:
				return 1, self.OPTION_QUIT
		if option == self.OPTION_PREV_PAGE:
			if self.page > 1:
				return 1, self.OPTION_PREV_PAGE
			else:
				return 1, self.OPTION_QUIT
		
		char_value = ord(option) - self.VALUE_ZERO_CHAR
		if char_value >= 0 and char_value < len(self.github_repos):
			return 1, option
		else:
			return 1, self.OPTION_QUIT





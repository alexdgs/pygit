import urllib2
from lxml.html import fromstring

xpath_readme_regex = ".//article[@itemprop='mainContentOfPage']"
SEPARATOR = '==================================================='

class GitHubReadme:
	
	def __init__(self, repo):
		self.repo = repo
	
	def show_readme(self):
		print 'Getting README.md text content for repository ' + self.repo.full_name + ' ...'
		response = urllib2.urlopen(self.repo.url);
		html = response.read()
		root = fromstring(html)
		
		readme_parent = root.find(xpath_readme_regex)
		print SEPARATOR
		if(readme_parent != None):
			for readme_text_container in readme_parent.iter():
				text = readme_text_container.text
				if text != None:
					print text
		else:
			print "Can't retrieve README.md for this repository"
		print SEPARATOR
		raw_input("Press 'Enter' to continue...")




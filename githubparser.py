import string
from githubpage import GitHubPage

page = 1
user_option = 1

query_raw_words = raw_input('Search repositories with words: ')
query_word = string.replace(query_raw_words, ' ', '%20')

if len(query_word) > 0:
	results = GitHubPage(query_word)
	while user_option != GitHubPage.OPTION_QUIT:
		results.setPage(page)
		user_option = results.print_results()
		if user_option == GitHubPage.OPTION_NEXT_PAGE:
			page += 1
			print 'Advancing to results page ' + str(page)
		else:
			if user_option == GitHubPage.OPTION_PREV_PAGE:
				if page > 1:
					page -= 1
					print 'Going back to results page ' + str(page)
				else:
					print "Warning: This is the first page!"
	print 'Good bye!'
else:
	print "Error: I can't guess what are you looking for. Try again writing some words to search for."


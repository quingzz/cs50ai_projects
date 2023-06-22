import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    outgoing_links = corpus[page]
    prob_distribution = {}
    
    no_pages = len(list(corpus.keys()))
    
    # if there is no out going link, return evenly distributed transition model
    if len(outgoing_links) == 0:
        for outpage in list(corpus.keys()):
            prob_distribution[outpage] = 1/no_pages
        return prob_distribution
            
    # instantiate initial values (1-damping_factor)/page for each page in transition model
    for outpage in list(corpus.keys()):
        prob_distribution[outpage] = (1-damping_factor)/no_pages
    # add probability to choose a page linked to current page
    for outpage in outgoing_links:
        prob_distribution[outpage] += damping_factor/len(outgoing_links)
        
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())  # get all pages in corpus
    curr_page = random.choice(pages)  # sample a page
    sample_list = [curr_page] 
    pagerank = {}
    
    # populate samples
    while len(sample_list) < n:
        # get transition model
        trans_model = transition_model(corpus, curr_page, damping_factor)
        
        # get list of linked page and the according probility distribution
        linked_page = list(trans_model.keys())
        probability_dist = [trans_model[page] for page in linked_page]
        
        # choose next sample based on probability distribution
        curr_page = random.choices(linked_page, weights=probability_dist)[0]
        sample_list.append(curr_page)
        
    # calculate estimate pagerank
    for page in pages:
        occurences = sample_list.count(page)
        pagerank[page] = occurences/n
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    pagerank = {}
    
    # populate initial values
    for page in pages:
        pagerank[page] = 1/len(pages)
    
    while True: 
        # continue updating page rank till difference is less than 0.001
        difference = 0
        
        # create temporary pagerank to be updated
        tmp_pagerank = pagerank.copy()
        for page in pages: 
            # get list of page (i) that can lead to current page or page that does not have outgoing links
            parent_pages = [prev_page for (prev_page, linked_page) in corpus.items() 
                            if (page in linked_page) or len(linked_page) == 0]
            
            # calculate sum of PR(i)/NumLinks(i)
            incoming_pages_sum = 0
            for i_page in parent_pages:
                if len(corpus[i_page]) > 0:
                    incoming_pages_sum += pagerank[i_page]/len(corpus[i_page]) 
                else:
                    # if page has no link, interpreted as having one link for every page in the corpus
                    incoming_pages_sum += pagerank[i_page]/len(pages) 
            
            tmp_pagerank[page] = (1-damping_factor)/len(pages) + damping_factor*incoming_pages_sum
            
            # find the difference between old and new value 
            # take max difference to ensure all differences are less than 0.001 before stopping
            difference = max(difference, abs(pagerank[page]-tmp_pagerank[page]))
               
        # stop updating if difference is less than 0.001
        if difference < 0.001:
            break
        
        # update pagerank
        pagerank = tmp_pagerank.copy()
        
    return pagerank


if __name__ == "__main__":
    main()

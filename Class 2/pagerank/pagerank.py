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

    cant_pages = len(corpus)

    # Initialization 
    probs = {pname : 0 for pname in corpus}

    # Current page has links
    if corpus[page]:
        for link in corpus[page]:
            if len(corpus[link]) > 0:
                probs[link] += damping_factor / len(corpus[link])
            else:
                probs[link] = 0
    else: # Current page hasn't links
        for link in corpus:
            probs[link] += damping_factor / cant_pages

    # Probability of jumping to any page in the corpus 
    for link in corpus:
        probs[link] += (1-damping_factor) / cant_pages
    
    return probs



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    cantpage = len(corpus)

    # Initialize the sample counter
    page_counts = {pname : 0 for pname in corpus}

    # CHoose a random home page 
    home_page = random.choice(list(corpus.keys()))

    # Generate the samples
    for num in range(n):
        page_counts[home_page] += 1

        probs = transition_model(corpus, home_page, damping_factor)

        home_page = random.choices(
            list(probs.keys()), 
            weights = list(probs.values()),
            k=1
        )[0]


    # Calculate the estimated PageRank: 
    page_rank = {page: count / n for page, count in page_counts.items()}

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    num_pages = len(corpus)

    # Initialization 
    pr_page = {pname : 1 / num_pages for pname in corpus }

    threshold = 0.001 

    flag = False

    while not flag:
        new_pagerank = {}
        total_change = 0 

        for page in corpus:
            sum_pagerank = 0
            for linkp in corpus:
                if not corpus[linkp]:
                    sum_pagerank += pr_page[linkp] / num_pages
                elif page in corpus[linkp]:
                    sum_pagerank += pr_page[linkp] / len(corpus[linkp])

            new_pagerank[page] = (1 - damping_factor) / num_pages + damping_factor * sum_pagerank

        flag = True 
        for page in corpus:
            change = abs(new_pagerank[page] - pr_page[page])
            if change > threshold:
                flag = False 
            pr_page[page] = new_pagerank[page]
    
    total = sum(pr_page.values())
    pr_page = {page : rank / total for page, rank in pr_page.items()}

    return pr_page


if __name__ == "__main__":
    main()

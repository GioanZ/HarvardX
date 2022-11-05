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
    if page not in corpus:
        Exception("page is not in corpus")

    pages = {x : 0 for x in corpus}

    list_p = corpus[page]
    n_page = len(list_p)
    if n_page > 0:
        prob_1 = damping_factor / n_page
        prob_2 = (1 - damping_factor) / len(corpus)
        for x in pages:
            pages[x] += prob_2
            if x in list_p:
                pages[x] += prob_1
    else:
        for x in pages:
            pages[x] = 1 / len(corpus)

    return pages


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = {x : 0 for x in corpus}
    ranks = {}

    page = random.choice(list(pages.keys()))
    pages[page] += 1

    for i in range(n-1):
        dict_prob = transition_model(corpus, page, damping_factor)
        
        tot_ragg = 0
        num = random.random()

        for pag, prob in dict_prob.items():
            tot_ragg += prob
            if num <= tot_ragg:
                page = pag
                break

        pages[page] += 1

    for pag, n_view in pages.items():
        ranks[pag] = n_view / n

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """ 
    MAX_CHANGE_RANK = 0.001
    N = len(corpus)
    max_rank = 1 / N
    condition1 = (1 - damping_factor) / N
    old_rank = {page : max_rank for page in corpus}
    new_rank = {}

    while True:
        
        for p in corpus:
            tmp = 0
            for i in corpus:
                num_links = len(corpus[i])
                pr_i = old_rank[i]

                # condition 2
                if p in corpus[i] or num_links == 0:
                    pr_i = old_rank[i]
                    tmp += pr_i / (N if num_links == 0 
                                   # ^- A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself)
                                   else num_links)

            new_rank[p] = condition1 + (damping_factor * tmp)

        if (max(abs(new_rank[x] - old_rank[x])
                for x in new_rank) < MAX_CHANGE_RANK):
            break
        else:
            old_rank = new_rank.copy()

    return new_rank


if __name__ == "__main__":
    main()
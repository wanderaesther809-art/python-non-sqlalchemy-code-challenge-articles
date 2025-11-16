#!/usr/bin/env python3
import ipdb

from author import Author
from magazine import Magazine
from article import Article

if __name__ == '__main__':
    print("HELLO! :) let's debug :vibing_potato:")

    # Example test data (you can change these while debugging)
    a1 = Author("Wandera")
    m1 = Magazine("TechMag", "Technology")
    m2 = Magazine("HealthX", "Health")

    Article(a1, m1, "Future of AI")
    Article(a1, m2, "How to Stay Fit")

    # don't remove this line, it's for debugging!
    ipdb.set_trace()

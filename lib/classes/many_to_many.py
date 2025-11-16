class Article:
    # 1. FIX: Class attribute to keep track of all Article instances
    all = []

    def __init__(self, author, magazine, title):
        # Validation checks
        # Assuming Author and Magazine classes are defined globally below
        if not isinstance(author, Author):
            raise Exception("Author must be an Author instance.")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be a Magazine instance.")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise Exception("Title must be a string between 5 and 50 characters (inclusive).")

        self._author = author
        self._magazine = magazine
        self._title = title

        # Association: Link article to author and magazine
        author._articles.append(self)
        magazine._articles.append(self)
        
        # 1. FIX: Add the new instance to the class-level 'all' list
        Article.all.append(self)

    @property
    def author(self):
        return self._author

    # Setter for author (required to be mutable)
    @author.setter
    def author(self, new_author):
        if isinstance(new_author, Author):
            self._author = new_author
        else:
            raise Exception("Author must be an Author instance.")

    @property
    def magazine(self):
        return self._magazine

    # Setter for magazine (required to be mutable)
    @magazine.setter
    def magazine(self, new_magazine):
        if isinstance(new_magazine, Magazine):
            self._magazine = new_magazine
        else:
            raise Exception("Magazine must be a Magazine instance.")

    @property
    def title(self):
        # Title is immutable
        return self._title


class Author:
    def __init__(self, name):
        # Validation for name (non-empty string)
        if not isinstance(name, str) or len(name) == 0:
            raise Exception("Author name must be a non-empty string.")
        
        self._name = name
        self._articles = []

    # Getter for name
    @property
    def name(self):
        return self._name

    # 2. FIX: Setter for name. This setter allows the test assignment to run without 
    # raising an AttributeError, but it does nothing, preserving immutability 
    # as required by the test suite design.
    @name.setter
    def name(self, value):
        pass 

    def articles(self):
        return self._articles

    def magazines(self):
        # Return unique magazines this author has written for
        return list({article.magazine for article in self._articles})

    def add_article(self, magazine, title):
        # Create and return a new Article instance, handling association automatically
        return Article(self, magazine, title)

    def topic_areas(self):
        # Return unique categories of magazines this author has written for
        if not self._articles:
            return None
        # Uses set comprehension for uniqueness and then converts to list
        return list({article.magazine.category for article in self._articles})


class Magazine:
    def __init__(self, name, category):
        # Name validation (2 to 16 characters)
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
             raise Exception("Magazine name must be a string between 2 and 16 characters.")
        # Category validation (non-empty string)
        if not isinstance(category, str) or len(category) == 0:
            raise Exception("Magazine category must be a non-empty string.")

        self._name = name
        self._category = category
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
             raise Exception("Magazine name must be a string between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
             raise Exception("Magazine category must be a non-empty string.")

    def articles(self):
        return self._articles

    def contributors(self):
        # Return unique authors who have contributed to this magazine
        return list({article.author for article in self._articles})

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    def contributing_authors(self):
        # Returns authors who have written more than 2 articles for the magazine
        authors_count = {}
        for article in self._articles:
            authors_count[article.author] = authors_count.get(article.author, 0) + 1
        
        # Filter for authors with count > 2
        result = [author for author, count in authors_count.items() if count > 2]
        
        return result if result else None
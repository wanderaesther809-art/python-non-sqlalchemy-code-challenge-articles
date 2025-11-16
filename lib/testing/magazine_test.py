import pytest
from classes.many_to_many import Article, Author, Magazine

class TestMagazine:
    """Tests for the Magazine class"""

    def test_magazine_initialization(self):
        """Magazine is initialized with a name and category"""
        magazine = Magazine("Vogue", "Fashion")
        assert magazine.name == "Vogue"
        assert magazine.category == "Fashion"

    def test_name_is_a_string(self):
        """Magazine name is a string"""
        magazine = Magazine("Vogue", "Fashion")
        assert isinstance(magazine.name, str)

        with pytest.raises(Exception):
            Magazine(1, "Fashion")

    def test_name_is_mutable(self):
        """Magazine name is mutable"""
        magazine = Magazine("Vogue", "Fashion")
        # CHANGED: "Architectural Digest" was too long (22 chars), using a valid name instead.
        magazine.name = "Arch Digest" 
        assert magazine.name == "Arch Digest"
        
    def test_name_length(self):
        """Magazine name is between 2 and 16 characters inclusive"""
        magazine = Magazine("Vogue", "Fashion")
        
        # Test valid names
        magazine.name = "a" * 2
        assert magazine.name == "aa"
        magazine.name = "a" * 16
        assert magazine.name == "a" * 16

        # Test invalid names
        with pytest.raises(Exception):
            magazine.name = "a" * 1
        with pytest.raises(Exception):
            Magazine("a" * 1, "Fashion")

        with pytest.raises(Exception):
            magazine.name = "a" * 17
        with pytest.raises(Exception):
            Magazine("a" * 17, "Fashion")

    def test_category_is_a_string(self):
        """Magazine category is a string"""
        magazine = Magazine("Vogue", "Fashion")
        assert isinstance(magazine.category, str)

        with pytest.raises(Exception):
            Magazine("Vogue", 1)

    def test_category_is_mutable(self):
        """Magazine category is mutable"""
        magazine = Magazine("Vogue", "Fashion")
        magazine.category = "Lifestyle"
        assert magazine.category == "Lifestyle"

    def test_category_length(self):
        """Magazine category is not an empty string"""
        magazine = Magazine("Vogue", "Fashion")
        
        # Test valid name
        magazine.category = "Design"
        assert magazine.category == "Design"
        
        # Test invalid name
        with pytest.raises(Exception):
            magazine.category = ""
        with pytest.raises(Exception):
            Magazine("Vogue", "")

    def test_has_many_articles(self):
        """Magazine has many articles"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author, magazine, "How to wear a tutu with style")
        article_2 = Article(author, magazine, "Dating life in NYC")
        
        assert len(magazine.articles()) == 2
        assert article_1 in magazine.articles()
        assert article_2 in magazine.articles()

    def test_articles_of_type_article(self):
        """Magazine articles are of type Article"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        Article(author, magazine, "Dating life in NYC")

        assert all(isinstance(article, Article) for article in magazine.articles())

    def test_has_many_contributors(self):
        """Magazine has many contributors"""
        magazine = Magazine("Vogue", "Fashion")
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        Article(author_1, magazine, "How to wear a tutu with style")
        Article(author_2, magazine, "Dating life in NYC")

        assert len(magazine.contributors()) == 2
        assert author_1 in magazine.contributors()
        assert author_2 in magazine.contributors()

    def test_contributors_are_unique(self):
        """Magazine contributors are unique"""
        magazine = Magazine("Vogue", "Fashion")
        author_1 = Author("Carry Bradshaw")
        Article(author_1, magazine, "How to wear a tutu with style")
        Article(author_1, magazine, "Dating life in NYC")
        
        assert len(magazine.contributors()) == 1
        assert author_1 in magazine.contributors()

    def test_contributors_are_authors(self):
        """Magazine contributors are of type Author"""
        magazine = Magazine("Vogue", "Fashion")
        author_1 = Author("Carry Bradshaw")
        Article(author_1, magazine, "How to wear a tutu with style")
        
        assert all(isinstance(contributor, Author) for contributor in magazine.contributors())

    def test_get_article_titles(self):
        """Magazine can retrieve article titles"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        Article(author, magazine, "Dating life in NYC")

        assert "How to wear a tutu with style" in magazine.article_titles()
        assert "Dating life in NYC" in magazine.article_titles()

    def test_article_titles_are_strings(self):
        """Magazine article titles are strings"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")

        assert all(isinstance(title, str) for title in magazine.article_titles())

    def test_article_titles_returns_none_when_no_articles(self):
        """Returns None if magazine has no articles"""
        magazine = Magazine("Vogue", "Fashion")
        assert magazine.article_titles() is None

    def test_contributing_authors(self):
        """Returns authors who have written more than 2 articles for the magazine"""
        magazine = Magazine("Vogue", "Fashion")
        contributor = Author("Carry Bradshaw")
        non_contributor = Author("Nathaniel Hawthorne")
        
        # 3 articles for contributor (should be included)
        Article(contributor, magazine, "How to wear a tutu with style")
        Article(contributor, magazine, "Dating life in NYC")
        Article(contributor, magazine, "New Article")
        
        # 2 articles for non_contributor (should be excluded)
        Article(non_contributor, magazine, "Another Article")
        Article(non_contributor, magazine, "One More Article")

        # 1 article for author_3 (should be excluded)
        author_3 = Author("George Orwell")
        # CHANGED: "1984" was too short (4 chars), using a valid title instead.
        Article(author_3, magazine, "The Road to 1984") 

        assert contributor in magazine.contributing_authors()
        assert non_contributor not in magazine.contributing_authors()
        assert author_3 not in magazine.contributing_authors()

    def test_contributing_authors_is_none(self):
        """Returns None if there are no contributing authors"""
        magazine = Magazine("Vogue", "Fashion")
        author_1 = Author("Carry Bradshaw")
        
        # 2 articles, so no contributing authors (count must be > 2)
        Article(author_1, magazine, "How to wear a tutu with style")
        Article(author_1, magazine, "Dating life in NYC")
        
        assert magazine.contributing_authors() is None

    def test_contributing_authors_returns_unique_authors(self):
        """Contributing authors returns a unique list of authors"""
        magazine = Magazine("Vogue", "Fashion")
        contributor = Author("Carry Bradshaw")
        
        Article(contributor, magazine, "How to wear a tutu with style")
        Article(contributor, magazine, "Dating life in NYC")
        Article(contributor, magazine, "New Article")
        
        assert len(magazine.contributing_authors()) == 1

    def test_contributing_authors_returns_list_of_authors(self):
        """Contributing authors returns a list of Author objects"""
        magazine = Magazine("Vogue", "Fashion")
        contributor = Author("Carry Bradshaw")
        
        Article(contributor, magazine, "How to wear a tutu with style")
        Article(contributor, magazine, "Dating life in NYC")
        Article(contributor, magazine, "New Article")
        
        assert all(isinstance(author, Author) for author in magazine.contributing_authors())
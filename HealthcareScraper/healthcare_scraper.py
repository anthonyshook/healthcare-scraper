# Importing JSON
import errno
import json
from urllib.request import urlopen
from io import StringIO
from html.parser import HTMLParser
import os


# Function to create directories with error safety
def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return(path)


# Stripping HTML tags
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# Just a generic storage class
class GenericStorage():
    def __init__(self):
        self.english = []
        self.spanish = []


class HealthcareScraper():
    """
    Initialization not necessary, only the methods matter
    """

    def __init__(self):
        # Just to get PEP to shut up
        self.article_dict = dict()
        self.blog_dict = dict()
        self.glossary_dict = dict()
        self.articles = GenericStorage()
        self.blogs = GenericStorage()
        self.glossary = GenericStorage()

    @staticmethod
    def __get_json_data(url):
        content = urlopen(url)
        return json.load(content)

    def pull_data(self):
        print(">> Fetching Articles")
        self.article_dict = self.__get_json_data('https://www.healthcare.gov/api/articles.json')
        print(">> Fetching Blogs")
        self.blog_dict = self.__get_json_data('https://www.healthcare.gov/api/blog.json')
        print(">> Fetching Glossary Entries")
        self.glossary_dict = self.__get_json_data('https://www.healthcare.gov/api/glossary.json')

    @staticmethod
    def __parse_data(cdict):
        output = GenericStorage()
        if cdict == 0:
            print('No data found')
            return None
        else:
            all_content = [content for content in cdict if isinstance(content, dict)]
            for content in all_content:
                if content['lang'] == 'es':
                    output.spanish.append(dict(
                        text=strip_tags(content['title'] + "\n\n" + content['content']),
                        slug=content['slug'] + '-' + content['lang']
                    ))
                else:
                    output.english.append(dict(
                        text=strip_tags(content['title'] + "\n\n" + content['content']),
                        slug=content['slug'] + '-' + content['lang']
                    ))
        return output

    def parse_content(self):
        print(">> Parsing Content")
        self.articles = self.__parse_data(self.article_dict['articles'])
        self.blogs    = self.__parse_data(self.blog_dict['blog'])
        self.glossary = self.__parse_data(self.glossary_dict['glossary'])
        return None

    @staticmethod
    def __write_content(data, path):
        # Takes a list, saves each file separately
        if len(data) > 0:
            for d in data:
                fname = path + d['slug'] + '.txt'
                dat = d['text']
                with open(fname, "w") as f:
                    f.write(dat)
        return None

    @staticmethod
    def __prep_directory(path):
        all_paths = [path + x + y
                     for x in ['/english_docs/', '/spanish_docs/']
                     for y in ['articles/', 'blogs/', 'glossary/']]
        for P in all_paths:
            create_dir(P)
        return all_paths

    def save_content(self, path):
        """
        :param path: Where to save the data, where each entry is a single text document
        :return: None
        """
        # Prep the directory
        print(">> Making Output Directory")
        paths = self.__prep_directory(path)

        # Since the order of those paths will always be the same
        # we can just use that known order in the loop
        # Doing this the quick/dirty way
        print(">> Writing Files to Disk")
        self.__write_content(data=self.articles.english, path=paths[0])
        self.__write_content(data=self.blogs.english, path=paths[1])
        self.__write_content(data=self.glossary.english, path=paths[2])
        self.__write_content(data=self.articles.spanish, path=paths[3])
        self.__write_content(data=self.blogs.spanish, path=paths[4])
        self.__write_content(data=self.glossary.spanish, path=paths[5])
        return None

    def fetch_and_save(self, path):
        # Fetch the data
        self.pull_data()
        # Parse the Data
        self.parse_content()
        # Save it to the path
        self.save_content(path)
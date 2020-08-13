# HealthcareScraper

Module intended to provide a quick way to fetch all data from Healthcare.gov, parse the text to remove HTML, 
then save the files as `.txt` format in a standard directory layout.

```
--- Root Directory
  |- english_docs
    |- articles
    |- blogs
    |- glossary
  |- spanish_docs
    |- articles
    |- blogs
    |- glossary
```

## Installation
### Clone Method
Clone the directory, then `cd` to where you saved the code.

### pip method
Just run the following in your terminal.  
```
pip install git+https://github.com/anthonyshook/healthcare-scraper.git
```
The package was written in Python 3.7.3, and only uses Standard Library,
so there shouldn't be any dependencies required to install.

## Using the Package
It's fairly straightforward
```python
import HealthcareScraper as hcs

path = '/PATH/TO/SAVE/DATA/'
scraper = hcs.HealthcareScraper()
scraper.fetch_and_save(path)
```
To see what's going on in `fetch_and_save`, check the source code!

## Notes
When the `fetch_and_save` method is run, the package will complete the following steps:
* Grab all available Articles, Blog Posts, and Glossary entries from https://www.healthcare.gov
* Remove the HTML tags from the content of the posts using the `parse_content` method
* Concatenate the title and content of the post together into a single text block.
* Save each page as a separate text file, using the `save_content` method.
    * Each file is named using the URL slug, and is appended with two 
letters to indicate the language of the document (en for English, es for Spanish).

# coding: utf-8

# # Publications markdown generator for academicpages
# 
# Takes a TSV of publications with metadata and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook, with the core python code in publications.py. Run either from the `markdown_generator` folder after replacing `publications.tsv` with one that fits your format.
# 
# TODO: Make this work with BibTex and other databases of citations, rather than Stuart's non-standard TSV format and citation style.
# 

# ## Data format
# 
# The TSV needs to have the following columns: pub_date, title, venue, excerpt, citation, site_url, and paper_url, with a header at the top. 
# 
# - `excerpt` and `paper_url` can be blank, but the others must have values. 
# - `pub_date` must be formatted as YYYY-MM-DD.
# - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the paper. The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/publications/YYYY-MM-DD-[url_slug]`


# ## Import pandas
# 
# We are using the very handy pandas library for dataframes.

# In[2]:

import pandas as pd
import re
import unicodedata

# ## Import TSV
# 
# Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.
# 
# I found it important to put this data in a tab-separated values format, because there are a lot of commas in this kind of data and comma-separated values can get messed up. However, you can modify the import statement, as pandas also has read_excel(), read_json(), and others.

# In[3]:

code = pd.read_csv("code.tsv", sep="\t", header=0)
code


# ## Escape special characters
# 
# YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands) with their HTML encoded equivilents. This makes them look not so readable in raw format, but they are parsed and rendered nicely.

# In[4]:

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


def slugify(text):
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Lowercase
    text = text.lower()

    # Replace non-alphanumeric by hyphen
    text = re.sub(r"[^a-z0-9]+", "-", text)

    # Trim hyphens
    return text.strip("-")


# ## Creating the markdown files
# 
# This is where the heavy lifting is done. This loops through all the rows in the TSV dataframe, then starts to concatentate a big string (```md```) that contains the markdown for each type. It does the YAML metadata first, then does the description for the individual page. If you don't want something to appear (like the "Recommended citation")

# In[5]:

import os
for row, item in code.iterrows():

    year = item.date[:4]

    md_filename = f"{year}-{slugify(item.title)}.md"

    ## YAML variables
    
    md = "---\ntitle: \"" + item.title + '"\n'

    md += "\ndate: " + str(item.date)

    if len(str(item.code_url)) > 5:
        md += "\ncode_url: '" + item.code_url + "'"

    if len(str(item.teaser_video)) > 3:
        md += "\nteaser_video: '" + item.teaser_video + "'"

    if len(str(item.teaser_image)) > 3:
        md += "\nteaser_image: '" + item.teaser_image + "'"

    md += "\n---"

    if len(str(item.description)) > 3:
        md += "\n" + html_escape(item.description) + "\n"

    md_filename = os.path.basename(md_filename)
       
    with open("../_code/" + md_filename, 'w') as f:
        f.write(md)

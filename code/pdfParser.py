from bs4 import BeautifulSoup
from tika import parser # pip install tika if needed


'''
----------------------------
Parse the PDF
----------------------------
Tika is gold. Converts the
PDF into an XML content
file that enables 
standard parsing techniques.
Cool stuff.
'''

# Parse the original PDF
data = parser.from_file(file_name, xmlContent=True)
xml_data = BeautifulSoup(data['content'])

'''
----------------------------
Table of contents
----------------------------
This bit of code extracts
information from the TOC
in order to construct
individual textfiles
from the entire document.
Also, cool.
'''

# Extracts the pages from the PDFS
pages = xml_data.find_all('div', attrs={'class': 'page'})

# Extracts the table of contents (first 2 pages)
toc = pages[0]
toc.extend(pages[1])

# Parse the table of contents
toc_names = [t.getText().replace('\xa0',' ').replace('\n','') for t in toc.find_all('p')][2:]

# Extract the page numbers 
pages_list = []
for entry in toc_names:
    for token in entry.split():
        try:
            check = int(token)
            pages_list.append(token)
        except:
            pass
        
pages_list.extend([len(pages)+1])

'''
----------------------------
Extract the documents
----------------------------
Once we have the TOC info,
we can extract individual
docs. This makes it easy
to combine things later
on if we want. 
'''
        
# Extract the document lengths
docs_list = [(int(page),int(pages_list[idx+1])-1) for idx,page in enumerate(pages_list) if idx < len(pages_list)-1]


# Now let's extract the documents
docs = [pages[doc[0]-1:doc[1]] for doc in docs_list]

# A function for combining a single document into a single string
def combine_doc(x):
    
    # Length of the document
    page_length = len(x)
    
    return ' '.join([t.getText().replace('\xa0',' ').replace('\n','') for i in range(0,page_length) for t in x[i].find_all('p')])

 
# Get the combined documents 
combined_docs = [combine_doc(docs[i]) for i in range(0,len(docs))]


# Save the files
for i in range(0,len(combined_docs)):
    save_file_path = '/Users/cblackburn/Downloads/pubcom{}.txt'.format(i)
    f = open(save_file_path,'w+')
    f.write(combined_docs[i])

    
        
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# pip install pypdf2
# conda install -c conda-forge pypdf2


# In[1]:


import os
import re
import pandas as pd
import PyPDF2


# In[2]:


INP_PATH = './input/'
OUT_PATH = './output/'


# In[3]:


def load_pdf_files(file_path:str):
    '''
    Loads pdf files and into PyPDF2.pdf.PdfFileReader object
    and append thems into a dictionary.
    
    Parameters
    ----------
    file_path : str
        Location of pdf files.
        
    Returns
    ----------
    inp_files : Dictionary
        Example: {file_1.pdf: PyPDF2.PdfFileReader}
    '''
    inp_files = {}
    
    for file in os.listdir(file_path):
        if file.endswith(".pdf"):
#             print('Reading', os.path.join(file_path, file))
            loaded_file = open(os.path.join(file_path, file), 'rb')
            # Creating a pdf reader object
            fileReader = PyPDF2.PdfFileReader(loaded_file)
            inp_files[file] = fileReader
    return inp_files
        


# In[4]:


main_dict = load_pdf_files(INP_PATH)


# # Define Rules

# In[5]:


rules = {'Rule_1' : {'type': 'simple', 
                     'contains': 'CNPJ', 
                     'case_sens': False, 
                     'n_char_before': 10, 
                     'n_char_after': 30,
                     'all_matches': True
                    }
#          'Rule_2' : {'type': 'regex', }  
}


# # Function to Process rules

# In[51]:


dfs = []
for fn in main_dict:
    df = pd.DataFrame([],columns=['File name', 'Rule', 'Page', 'text'])
    fileReader = main_dict[fn]
    pg_count = fileReader.numPages
    doc = ''
    # Put all pages in single string
    for i in range(pg_count):
        page = fileReader.getPage(i).extractText()
        doc += page
        
    doc = re.sub(r"[\n\t\r]*", "", doc)
    rule = 'Rule_1'
    extract_texts = []
    word = rules[rule]['contains']
    matches = [m.start() for m in re.finditer(word, doc, re.IGNORECASE)]

    for m in matches:
        start = m - rules[rule]['n_char_before']
        end = m + rules[rule]['n_char_after'] + len(word)
        #print(doc[start: end])
        extract_texts.append(doc[start: end])
    
    df = pd.DataFrame({"File name":fn,
                        "Rule":rule,
                        "Page":'x',
                        "text":extract_texts
                        })
    
    dfs.append(df)
    
df_final=pd.concat(dfs)    


# In[55]:


df_final.to_excel(OUT_PATH + 'results.xlsx', index=False)
df_final


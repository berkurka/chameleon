#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# pip install pypdf2
# conda install -c conda-forge pypdf2


# In[ ]:


import os
import re
import pandas as pd
import PyPDF2


# In[ ]:


INP_PATH = './input/'
OUT_PATH = './output/'


# In[ ]:


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
        


# In[ ]:


main_dict = load_pdf_files(INP_PATH)


# # Define Rules

# In[ ]:


rules = {'simple_1' : {'type': 'simple', 
                     'contains': 'CNPJ', 
                     'case_sens': False, 
                     'n_char_before': 10, 
                     'n_char_after': 30,
                     'matches': 'First'
                    },
          'simple_2' : {'type': 'simple',
                      'contains': 'CPF', 
                      'case_sens': False, 
                      'n_char_before': 10, 
                      'n_char_after': 30,
                      'matches': 'All'
                         },
         'regex' : {'type': 'regex',
                      'pattern': 'taxa.{30}',
                      'matches': 'All'
                     },
         
         
}


# # Function to Process rules

# In[ ]:


dfs = []
for fn in main_dict:
    df = pd.DataFrame([],columns=['File name', 'Rule', 'Page', 'text'])
    fileReader = main_dict[fn]
    pg_count = fileReader.numPages
    doc = ''
    # Applying rules for each page
    for i in range(pg_count):
        #Pdf reader
        page = fileReader.getPage(i).extractText()
        doc = page
        doc = re.sub(r"[\n\t\r]*", "", doc)
        
        #Applying rules
        for rule in rules:
            extract_texts = []
            
            ###Simple 
            if rules[rule]['type'] == 'simple':
                word = rules[rule]['contains']
                matches = [m.start() for m in re.finditer(word, doc, re.IGNORECASE)]

                for m in matches:
                    start = m - rules[rule]['n_char_before']
                    end = m + rules[rule]['n_char_after'] + len(word)
                    extract_texts.append(doc[start: end])
                    
            ###Regex
            elif rules[rule]['type'] == 'regex':
                pattern = rules[rule]['pattern']
                matches = re.findall(r"{}".format(pattern), doc)
                extract_texts.append(matches)
                
            
            #Adding results to a temporary dataframe
            df = pd.DataFrame({"File name":fn,
                                "Rule":rule,
                                "Page":i+1,
                                "text":extract_texts
                                })
 
            #Adding results to the main dataframe
            dfs.append(df)
    
df_final=pd.concat(dfs)


# In[ ]:


df_final=df_final.reset_index(drop=True)


# In[ ]:


df_final.to_excel(OUT_PATH + 'results.xlsx', index=False)
df_final


# In[ ]:





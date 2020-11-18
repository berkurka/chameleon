import os
import re
from typing import Dict
import pandas as pd
import PyPDF2

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
            print('Reading', os.path.join(file_path, file))
            loaded_file = open(os.path.join(file_path, file), 'rb')
            # Creating a pdf reader object
            fileReader = PyPDF2.PdfFileReader(loaded_file)
            inp_files[file] = fileReader
    return inp_files


def extract_text(raw_documents: Dict, rules: Dict):
    '''
    For each documents in raw_documents extract text based
    on existing rules.
    
    Parameters
    ----------
    raw_documents : Dictionary
        Contains file names and pdf objects.
        Example: {file_1.pdf: PyPDF2.PdfFileReader}

    rules : Dictionary
        Contains file names and pdf objects.
        Example: 
        {'simple_2' : {'type': 'simple',
                       'contains': 'CPF', 
                       'case_sens': False},
         'regex' : {'type': 'regex',
                    'pattern': 'taxa.{30}',
                    'matches': 'All'}
        } 
    Returns
    ----------
    inp_files : pd.DataFrame
        Data Frame with the extracted information.
        Example:
       File name  |   Rule    | Page | Text   
    0  FILE_1.pdf |    regex  |   1  | EAPC, com CNPJ de n° 87.376...
    1  FILE_1.pdf | simple_1  |   2  | [taxa de juros efetiva anual e.. 
    2  FILE_1.pdf |    regex  |   2  | completo, CNPJ ou..
    3  FILE_1.pdf | simple_1  |   3  | CNPJ ou CPF...  
    4  FILE_1.pdf | simple_2  |   3  | As questões judi..  
    '''
    dfs = []

    for fn in raw_documents:
        df = pd.DataFrame([], columns=['File name', 'Rule', 'Page', 'Text'])
        fileReader = raw_documents[fn]
        pg_count = fileReader.numPages
        doc = ''
        # Applying rules for each page
        for i in range(pg_count):
            # Pdf reader
            page = fileReader.getPage(i).extractText()
            doc = page
            doc = re.sub(r"[\n\t\r]*", "", doc)
            
            # Applying rules
            for rule in rules:
                extract_texts = []
                
                # Simple 
                if rules[rule]['type'] == 'simple':
                    word = rules[rule]['contains']
                    matches = [m.start() for m in re.finditer(word, doc, re.IGNORECASE)]

                    for m in matches:
                        start = max(0, m - rules[rule]['n_char_before'])
                        end = min(len(doc), 
                                  m + rules[rule]['n_char_after'] + len(word))
                        extract_texts.append(doc[start: end])
                        
                # Regex
                elif rules[rule]['type'] == 'regex':
                    pattern = rules[rule]['pattern']
                    matches = re.findall(r"{}".format(pattern), doc)
                    extract_texts.append(matches)
                
                #Adding results to a temporary dataframe
                df = pd.DataFrame({"File name": fn,
                                    "Rule": rule,
                                    "Page": i + 1,
                                    "text": extract_texts
                                    })
    
                #Adding results to the main dataframe
                dfs.append(df)

    df_final = pd.concat(dfs)
    df_final = df_final.reset_index(drop=True)
    return df_final
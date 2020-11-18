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
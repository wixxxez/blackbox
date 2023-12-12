from typing import Any
import pandas as pd 

class CheckForUniqRowsService: 
    
    
    def __init__(self, user_file: pd.DataFrame, website: str) -> None:
        
        self.user_data = user_file,
        self.website = website
        
    def getUniqRows(self):
        
        df = pd.read_excel(f"./databases/{self.website}.xlsx")
         
        dff = self.user_data
        dff = dff[0] 
        merged = pd.merge(dff, df, on=['login', 'password'], how='outer', indicator=True)
        not_in_db = merged[merged['_merge'] == 'left_only']
        num_rows_not_in_db = len(not_in_db)
        duplicates = len(merged[merged['_merge'] == 'both'])
        del merged["_merge"]

        merged.to_excel(f'databases/{self.website}.xlsx')
        
        
        return num_rows_not_in_db, duplicates 
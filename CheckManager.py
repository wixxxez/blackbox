from typing import Any
import pandas as pd 

class CheckForUniqRowsService: 
    
    
    def __init__(self, user_file: pd.DataFrame, website: str, file_path:str) -> None:
        
        self.user_data = user_file
        self.website = website
        self.file_path = file_path
        
    def getUniqRows(self):
        
        print(self.website)
        df = pd.read_excel(f"./databases/{self.website}.xlsx")
        del df['Unnamed: 0']  
        dff = self.user_data

        merged = pd.merge(dff, df, on=['login', 'password'], how='outer', indicator=True)
        not_in_db = merged[merged['_merge'] == 'left_only']
        num_rows_not_in_db = len(not_in_db)
        duplicates = len(merged[merged['_merge'] == 'both'])
        del merged["_merge"]
        del not_in_db['_merge']
        
        not_in_db.to_csv(self.file_path, sep=":", index=False)
        merged.to_excel(f'databases/{self.website}.xlsx')
        
        
        return num_rows_not_in_db, duplicates 
import pandas as pd
 
class FileReaderFactory:
    def create_reader(self, file_type):
        if file_type == 'text':
            return TextFileReader()
        elif file_type == 'excel':
            return ExcelFileReader()
        else:
            raise ValueError("Unsupported file type")

class FileProcessorFacade:
    def __init__(self):
        self.factory = FileReaderFactory()

    def process_file(self, file_path):
        file_type = self.get_file_type(file_path)
        reader = self.factory.create_reader(file_type)
        data = reader.read(file_path)
        return data

    @staticmethod
    def get_file_type(file_path):
        if file_path.endswith('.txt'):
            return 'text'
        elif file_path.endswith('.xlsx'):
            return 'excel'
        else:
            raise ValueError("Unsupported file type")
 
class FileReader:
    def read(self, file_path):
        raise NotImplementedError("Subclasses must implement the read method")
 
class TextFileReader(FileReader):
    def read(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

      
        data = [line.strip().split(':') for line in lines]
        df = pd.DataFrame(data, columns=['login', 'password'])
        
        return df
class ExcelFileReader(FileReader):
    def read(self, file_path):
        return pd.read_excel(file_path)
from dataclasses import dataclass
from PyQt5.QtCore import QDir
import yaml

@dataclass
class FileSystemObject:
    path: str
    type: str  # "File" or "Folder"
    children: list = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

class FileManager:

    def __init__(self):
        pass
    
    @staticmethod
    def read_file_content(file_path: str, mode:str, encoding: str)-> str:
        with open(file_path, mode, encoding=encoding) as file:
            content = file.read()
            return content
    
    @staticmethod
    def generate_folder_tree(directory_path, recursive=True):
        dir_obj = QDir(directory_path)
        objects = []

        # For each sub-directory and file in the current directory
        for file_name in dir_obj.entryList(QDir.Dirs | QDir.Files | QDir.NoDotAndDotDot):
            path = dir_obj.absoluteFilePath(file_name)
            if QDir(path).exists():  # if it's a directory
                folder_obj = FileSystemObject(path, "Folder")
                objects.append(folder_obj)
                
                # If recursive flag is set, then dive into sub-directories
                if recursive:
                    folder_obj.children = FileManager.generate_folder_tree(path, recursive=True)
            else:  # if it's a file
                objects.append(FileSystemObject(path, "File"))
        
        return objects
    
    @staticmethod
    def deserialize_configuration_file(config_file_path:str)->object:
        with open(config_file_path, 'r', encoding="ascii") as file:
            data = yaml.safe_load(file)
        return data
    
            
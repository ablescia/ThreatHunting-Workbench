import yaml

class GrokFunnel:

    def __init__(self):
        self._grok_patterns = []

    @property
    def grok_patterns(self):
        return self._grok_patterns
    
    @grok_patterns.setter
    def __set_grok_patterns(self, value):
        self._grok_patterns = value
    
    def load_grok_patterns(self, yaml_file, keyword):
        with open(yaml_file, 'r', encoding='ascii') as file:
            patterns = yaml.safe_load(file)
        if keyword in patterns:
            self.__set_grok_patterns = patterns[keyword]
        else:
            raise ValueError(f"No patterns found for keyword: {keyword}") 
    
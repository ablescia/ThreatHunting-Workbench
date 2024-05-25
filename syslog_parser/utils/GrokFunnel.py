import yaml

class GrokFunnel:

    def __init__(self):
        pass

    def load_grok_patterns(self, yaml_file, keyword):
        with open(yaml_file, 'r', encoding='ascii') as file:
            patterns = yaml.safe_load(file)
        if keyword in patterns:
            return patterns[keyword]
        else:
            raise ValueError(f"No patterns found for keyword: {keyword}") 
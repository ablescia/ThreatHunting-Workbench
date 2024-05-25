from pygrok import Grok
import json

class LogParser:

    def __init__(self, input_log_path, grok_funnel, output_ndjson_path):
        self.grok_patterns = grok_funnel.grok_patterns
        self.output_ndjson_path = output_ndjson_path
        self.input_log_file_content = []
        self.parsed_logs = []
        self.__load_input_log(input_log_path)

    def __load_input_log(self, input_log_path):
        with open(input_log_path, 'r', encoding='ascii') as log_file_stream:
            self.input_log_file_content  = log_file_stream.readlines()

    def do_analyze(self):
        self.parsed_logs = []
        for log in self.input_log_file_content:
            parsed_log = self.__parse_log(log, self.grok_patterns)
            if parsed_log:
                self.parsed_logs.append(parsed_log)
    
    def __parse_log(self, log_line, grok_patterns):
        for pattern_group in grok_patterns:
            for pattern in pattern_group.get('patterns', []):
                grok = Grok(pattern)
                match = grok.match(log_line)
                if match:
                    match['keyword'] = pattern_group.get('name', 'unknown')
                    return match
        return None

    def do_convert_to_ndjson(self):
        with open(self.output_ndjson_path, 'w') as out_file_stream:
            for log in self.parsed_logs:
                out_file_stream.write(json.dumps(log) + '\n')
    
    
    
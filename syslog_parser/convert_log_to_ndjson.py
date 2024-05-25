import json

import argparse
from utils.GrokFunnel import GrokFunnel
from utils.LogParser import LogParser

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--logtype", help="Select the input log type", type=str, required=True)
    parser.add_argument("-i", "--input", help="Select the input log file path", type=str, required=True)
    parser.add_argument("-o", "--output", help="Select the output ndjson file path", type=str, required=True)
    args = parser.parse_args()


    grok_funnel = GrokFunnel()
    loaded_groks = grok_funnel.load_grok_patterns('./syslog_parser/custom_patterns.yaml',
                                                  args.logtype)

    log_parser = LogParser(args.input, loaded_groks, args.output)
    log_parser.do_analyze()
    log_parser.convert_to_ndjson()

if __name__ == "__main__":
    main()

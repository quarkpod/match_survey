#!/venv/bin/python

import sys
import argparse
from src.match_survey.parser.fotmob_extractor import FotMobCaller



def run():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="scrape match data from FotMob")
    
    # Add arguments
    parser.add_argument("config", type=str, help="filename (JSON) for scraper run")
    parser.add_argument("defaults", type=str, help="filename (JSON) of default values for all runs")
    
    # Parse the arguments
    args = parser.parse_args()
    FotMobCaller(args.config, args.defaults)()
    print('enjoy!')

if __name__ == '__main__':
    run()

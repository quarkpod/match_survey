#!/venv/bin/python

import sys
import argparse
from match_survey.parser.fotmob_extractor import FotMobCaller



def run():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="scrape match data from FotMob")
    
    # Add arguments
    parser.add_argument(
        "run_name",
        type=str,
        help="match run name"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="filename (JSON) of default values for all runs",
        default='.config.json'
    )
    
    # Parse the arguments
    args = parser.parse_args()
    FotMobCaller(args.run_name, args.config)()
    print('enjoy!')

if __name__ == '__main__':
    run()

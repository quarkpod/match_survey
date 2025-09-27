#!venv/bin/python
import json
import pickle
import argparse
import pandas as pd
from pathlib import Path
from selenium import webdriver

def run():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="scrape fbref team stats")

    # Add arguments
    parser.add_argument(
        "--config",
        type=str,
        help="filename (JSON) of default values for all runs",
        default='.config.json'
    )
    parser.add_argument(
        "--overwrite",
        action='store_true',
        help="overwrite output files"
    )

    # Parse the arguments
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text())
    overwrite = args.overwrite

    # Unpack essential config elements
    data_dir = config.get('data_dir')
    urls = config.get('team_stats_urls')
    out_filename = Path(config.get('data_filenames').get('team_stats'))

    for name, url in urls.items():
        outfile = Path(data_dir, f'{name}_{out_filename}')
        if outfile.exists() and not args.overwrite:
            print(f'already have {outfile}')
            continue

        print(f'scraping {name} @ {url}')
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        html = driver.page_source
        tables = pd.read_html(html)
        driver.quit()
        if len(tables) > 1:
            with outfile.open('wb') as outp:
                pickle.dump(tables, outp, pickle.HIGHEST_PROTOCOL)
            print(f'saved {outfile.name}')
        elif len(tables) == 1:
            outfile.suffix = 'csv'
            tables[0].to_csv(outfile.name)
        else:
            print(f'no data for {name}')

if __name__ == '__main__':
    run()

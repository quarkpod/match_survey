#!/venv/bin/python

import sys
import json
import argparse
from pathlib import Path
from tempfile import NamedTemporaryFile as Temp
from match_survey.parser.fbref_extractor import FBRefCaller



def run():
    """
    Example elements of main config:
    config = {
        "data_dir": "data/",
        "fbref_team_url": "https://fbref.com/en/squads/bd97ac1f/St-Louis-City-Stats",
        "data_filenames": {
            "fbref_team_stats": "fbref_season_stats.pkl",
            "fbref_schedule": "fbref_schedule_2025.csv",
            "roster": "roster_2025.csv",
        },
        "rename_maps": {
            "fotmob_surname_rename": {
                "Lowen": "Löwen",
                "Jaaskelainen": "Jääskeläinen",
                "Burki": "Bürki",
                "Ostrak": "Ostrák",
                "Sangbin": "Jeong"
            },
            "fbref_player_rename": {
                "Klauss": "Jo\u00e3o Klauss",
                "Mykhi Joyner": "MyKhi Joyner",
                "Jeong Sangbin": "Sang-bin Jeong"
            },
            "competition_rename": {
                "Major League Soccer": "MLS",
                "US Open Cup": "USOC",
                "U.S. Open Cup": "USOC"
            }
        }
    }


    Example prepared FBRef scraper config:
    fbref_config = {
        "fbref_team_url": "https://fbref.com/en/squads/bd97ac1f/St-Louis-City-Stats",
        "data_dir": "local_dev/data/",
        "name_mapping": {
            "Klauss": "Jo\u00e3o Klauss",
            "Mykhi Joyner": "MyKhi Joyner",
            "Jeong Sangbin": "Sang-bin Jeong"
        }
    }
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="scrape team data from FBRef")

    # Add arguments
    parser.add_argument("--config",
        type=str,
        help="filename (JSON) of default values for all runs",
        default='.config.json'
    )

    # Parse the arguments
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text())

    # Unpack essential config elements
    data_dir = config.get('data_dir')

    roster_filename = config.get('data_filenames').get('roster')
    fbref_schedule_filename = config.get('data_filenames').get('fbref_schedule')
    name_mapping = config.get('rename_maps').get('fbref_player_rename', dict())
    surname_mapping = config.get('rename_maps').get('fotmob_surname_rename', dict())

    # Prepare FBRefCaller config
    fbref_config = {
        "fbref_team_url": config.get('fbref_team_url'),
        'data_dir': data_dir,
        'name_mapping': name_mapping,
    }
    with Temp(mode='w+', delete=False, encoding='utf-8') as fbref_config_file:
        json.dump(fbref_config, fbref_config_file)

    # Run
    fbrc = FBRefCaller(fbref_config_file.name)
    fbrc()

    # Post-process
    # TODO: move to methods within FBRefCaller
    roster = fbrc.get_roster()
    roster.loc[:, 'Surname'] = roster.Surname.apply(lambda x: surname_mapping.get(x, x))
    sort_cols = ['GK', 'DF', 'MF', 'FW', 'Surname','Starts', 'Min']
    ascending_cols = {
        'GK': False,
        'DF': False,
        'MF': False,
        'FW': False,
        'Surname': True,
        'Starts': False,
        'Min': False,
    }
    roster.sort_values(sort_cols, ascending=[v for k,v in ascending_cols.items() if k in sort_cols])

    full_roster_filename = f'{data_dir}/{roster_filename}'
    print(f'saving updated roster at\n{full_roster_filename}\n{roster.shape}')
    roster.to_csv(f'{full_roster_filename}', index=False)

    full_schedule_filename = f'{data_dir}/{fbref_schedule_filename}'
    print(f'saving updated schedule at\n{full_schedule_filename}\n{fbrc.schedule.shape}')
    fbrc.schedule.to_csv(full_schedule_filename, index=False)
    print('enjoy!')

if __name__ == '__main__':
    run()

"""Updates statistics and process achievements script"""
import os, sys, getopt
import json
import datetime as DT
import re
from logger import logger
from config import BB_API_KEY, LEAGUES, ROOT, STORE
from sheet_service import SheetService

import bb2

agent = bb2.api.Agent(BB_API_KEY)
exported_ids_array = []

def filename(uuid):
    return os.path.join(STORE, f"{uuid}.json")

def get_and_save_match_file(uuid):
    if os.path.isfile(filename(uuid)):
        logger.info("File %s exists", filename)
        return
    try:
        detailed = agent.match(id=uuid)
        file = open(filename(uuid), "a")
        file.write(json.dumps(detailed))
        file.close()
    except Exception as exc:
        logger.error(exc)
        raise exc

def load_match(uuid):
    file = open(filename(uuid))
    data = json.loads(file.read())
    file.close()
    return data

def represents_int(string):
    """Check if the `s` is int"""
    try:
        int(string)
        return True
    except ValueError:
        return False

def max_imported_id():
    matches = SheetService.matches()
    ids = sorted([match['ID'] for match in matches])
    if ids and represents_int(ids[-1]):
        max_id = int(ids[-1])
    else:
        max_id = 0
    return max_id

def exported_ids():
    global exported_ids_array
    if not exported_ids_array:
        matches = SheetService.matches()
        exported_ids_array = sorted([match['ID'] for match in matches])
    return exported_ids_array

def export_match(uuid):
    data = load_match(uuid)
    #no coach name => AI
    if not data['match']['coaches'][0]['coachname'] or not data['match']['coaches'][1]['coachname']:
        return

    if data['match']['id'] not in exported_ids():
        t1 = data['match']['teams'][0]
        t2 = data['match']['teams'][1]
        t1_stats = [t1['score'], t1['inflictedtackles'], t1['inflictedcasualties'], t1['inflictedko'], t1['inflictedinjuries'], t1['inflictedpushouts'],
            t1['inflictedinterceptions'], t1['inflictedpasses'], t1['inflictedmeterspassing'], t1['inflictedmetersrunning']
        ]
        t2_stats = [t2['score'], t2['inflictedtackles'], t2['inflictedcasualties'], t2['inflictedko'], t2['inflictedinjuries'], t2['inflictedpushouts'],
            t2['inflictedinterceptions'], t2['inflictedpasses'], t2['inflictedmeterspassing'], t2['inflictedmetersrunning']
        ]
        if t1['score'] > t2['score']:
            wdl1 = [1,0,0]
            wdl2 = [0,0,1]
        elif t1['score'] < t2['score']:
            wdl1 = [0,0,1]
            wdl2 = [1,0,0]
        else:
            wdl1 = [0,1,0]
            wdl2 = [0,1,0]
        clan1 = re.search("\[(.+)\]",t1['teamname'])
        clan1_name = clan1.group() if clan1 else None

        clan2 = re.search("\[(.+)\]",t2['teamname']) 
        clan2_name = clan2.group() if clan2 else None
        export1 = [clan1_name, t1['teamname']] + wdl1 + t1_stats + [data['match']['id'], ""] + t2_stats
        export2 = [clan2_name, t2['teamname']] + wdl2 + t2_stats + [data['match']['id'], ""] + t1_stats   
        SheetService.append_match(export1)
        SheetService.append_match(export2)

# run the application
def main(argv):
    """main()"""
    logger.info("Getting matches")
    try:
        data = agent.contests(league=",".join(LEAGUES))
    except Exception as exc:
        logger.error(exc)
        raise exc
    logger.info("Contest colleted")

    if not os.path.isdir(STORE):
        os.mkdir(STORE)

    for match in data['upcoming_matches']:
        logger.info("Collecting match %s", match['match_uuid'])
        get_and_save_match_file(match['match_uuid'])
        export_match(match['match_uuid'])
        logger.info("Match %s saved", match['match_uuid'])

if __name__ == "__main__":
    main(sys.argv[1:])

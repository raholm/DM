import json

import dota2api

api = dota2api.Initialise(raw_mode=True)
match = api.get_match_details(match_id=2836936292)


parsed = json.loads(match.json)
print(json.dumps(parsed, indent=4, sort_keys=True))
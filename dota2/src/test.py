from src.common.env import get_env_value
from src.database.client import Dota2DBClient

print(get_env_value("D2_DB_URI"))
print(get_env_value("D2_DB_NAME"))
print(get_env_value("D2_DB_COLLECTION_TOURNAMENT"))
print(get_env_value("D2_DB_COLLECTION_MATCH"))

with Dota2DBClient() as client:
    pass

# self.client = MongoClient(get_env_value("D2_DB_URI"))
# self.db = self.client[get_env_value("D2_DB_NAME")]
# self.tournament_collection = self.db[get_env_value("D2_DB_COLLECTION_TOURNAMENT")]
# self.match_collection = self.db[get_env_value("D2_DB_COLLECTION_MATCH")]
from src.library.redisops import RedisOps
import datetime
from src.library.fextras import byte_object_to_str, generate_id
from src.library.mongoops import MongoOperations


class DefaultModel:
    def __init__(self):
        self.rc = RedisOps().rc
        self.dtnow = str(datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=6))))
        self.collection_name = "beats"

    @staticmethod
    def prepare_data_sto_store(data_json):
        new_data = data_json.copy()
        new_data["created_at"] = str(datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=6))))
        new_data["updated_at"] = str(datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=6))))
        return new_data

    def insert_beat(self, data):
        to_return = True
        try:
            MongoOperations(collection_name=self.collection_name).insert_data(data_json=DefaultModel().prepare_data_sto_store(data_json=data))
        except Exception as ex:
            print(ex)
            to_return = False
        return to_return

    def get_beats(self, data):
        to_return = []
        for _ in MongoOperations(collection_name=self.collection_name).get_data(data_json=data)[:100]:
            del _["_id"]
            to_return.append(_)
        return to_return

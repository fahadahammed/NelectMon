from src.library.redisops import RedisOps
import datetime
from src.library.fextras import byte_object_to_str, generate_id
from src.model.user import User


class DefaultModel:
    def __init__(self):
        self.rc = RedisOps().rc
        self.dtnow = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=6)))

    def insert_note(self, note, email):
        """
        Insert a note into the database
        :param note:
        :return:
        """
        note_id = generate_id()
        created_at = self.dtnow
        updated_at = self.dtnow
        note_object = {
            'id': note_id,
            'note': note,
            'author': email,
            'created_at': datetime.datetime.timestamp(created_at),
            'updated_at': datetime.datetime.timestamp(updated_at)
        }

        try:
            self.rc.hset(name=f'note:{note_id}', mapping=note_object)
            return {'status': 'success', 'message': 'Note inserted successfully'}
        except Exception as ex:
            return {'status': 'error', 'msg': str(ex)}

    def get_keys(self, pattern):
        return self.rc.keys(pattern=pattern)

    def get_notes(self):
        try:
            keys = self.get_keys(pattern='note:*')
            total = []
            for key in keys:
                note = self.rc.hgetall(name=key)
                total.append(byte_object_to_str(note))
            return total
        except Exception as ex:
            print(ex)
            return False
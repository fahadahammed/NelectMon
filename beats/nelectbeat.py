import argparse
import datetime
import http.client
import json
import platform
import subprocess
import os
import uuid

import json
import os
import sys
import datetime
import uuid


def get_random_id():
    the_id = uuid.uuid4()
    return str(the_id)


class mjdb:
    def __init__(self, db_file_name="my_mjdb.json"):
        self.db_file_name = db_file_name
        self.create_db()

    def create_db(self):
        try:
            if not os.path.exists(self.db_file_name):
                with open(self.db_file_name, 'a') as opened_db:
                    json.dump([], opened_db)
            return True
        except Exception as ex:
            print(ex)
            return False

    def insert_data(self, data):
        try:
            data["id"] = get_random_id()
            existing_data = self.read_all_data()
            to_insert = existing_data.appened(data)
            with open(self.db_file_name, 'w') as opened_db:
                json.dump(to_insert, opened_db)
            return True
        except Exception as ex:
            print(ex)
            return False

    def read_all_data(self):
        try:
            with open(self.db_file_name, 'r') as opened_db:
                to_return = json.load(opened_db)
            return to_return
        except Exception as ex:
            print(ex)
            return False

    def read_single_data(self, id):
        try:
            existing_data = self.read_all_data()
            to_return = [x for x in existing_data if x.get("id") == id]
            return to_return
        except Exception as ex:
            print(ex)
            return False

    def replace_single_data(self, id, data):
        try:
            existing_data = self.read_all_data()
            to_insert = []
            for _ in existing_data:
                if _.get("id") != id:
                    to_insert.append(_)
            data["id"] = id
            to_insert.append(data)
            with open(self.db_file_name, 'w') as opened_db:
                json.dump(to_insert, opened_db)
            return True
        except Exception as ex:
            print(ex)
            return False

    def update_single_data(self, id, data):
        try:
            existing_data = self.read_all_data()
            to_insert = []
            for _ in existing_data:
                if _.get("id") == id:
                    new_dict = _.copy()
                    for k, v in data.items():
                        new_dict[k] = v
                    to_insert.append(new_dict)
                else:
                    to_insert.append(_)
            with open(self.db_file_name, 'w') as opened_db:
                json.dump(to_insert, opened_db)
            return True
        except Exception as ex:
            print(ex)
            return False

    def delete_single_data(self, id):
        try:
            existing_data = self.read_all_data()
            after_delete = []
            for _ in existing_data:
                if _.get("id") != id:
                    after_delete.append(_)
            with open(self.db_file_name, 'w') as opened_db:
                json.dump(after_delete, opened_db)
            return True
        except Exception as ex:
            print(ex)
            return False





dl = "dead_letter.json"


def write_data(body):
    try:
        with open(dl, "w") as dlf:
            return json.dump(body, dlf)
    except Exception as ex:
        print("ex", ex)
        return False


def read_full_data():
    try:
        with open(dl, "r") as dlf:
            return json.load(dlf)
    except Exception as ex:
        print(ex)
        return []


def update_data(body):
    old_data = read_full_data()
    new_body = old_data.copy()
    new_body.append(body)
    nbody = [d for d in new_body if d('unique_beat_id') in [x["unique_beat_id"] for x in new_body if x.get("unique_beat_id")]]
    print(nbody)
    return write_data(body=nbody)


def removed_data(unique_beat_id):
    all_data = read_full_data()
    if all_data:
        return [x for x in all_data if x.get("unique_beat_id") != unique_beat_id]
    else:
        return False


def ping_check(host="8.8.8.8"):
    parameter = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', parameter, '1', host]
    response = subprocess.call(command, stdout=open(os.devnull, 'wb'))
    if response == 0:
        return True
    else:
        return False


def get_beat_data():
    beat_date_time = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=6)))
    internet_ok = ping_check()
    unique_beat_id = str(uuid.uuid4())
    return {
        "unique_beat_id": unique_beat_id,
        "beat_date_time": str(beat_date_time),
        "internet_ok": internet_ok
    }


def send_beat(body, host="127.0.0.1", port=11000, endpoint="/api/v1/post_beat"):
    if port == 443:
        conn = http.client.HTTPSConnection(f"{host}:{port}")
    else:
        conn = http.client.HTTPConnection(f"{host}:{port}")
    payload = body
    headers = {
        'Content-Type': "application/json"
    }
    conn.request("POST", endpoint, body=json.dumps(payload), headers=headers)
    res = conn.getresponse()
    data = res.read()
    if data:
        return data.decode("utf-8")
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Send HeartBeat to Nelect Server.''')
    parser.add_argument('--host', default="127.0.0.1",
                        help='NelectServer Host')
    parser.add_argument('--port', default=11000,
                        help='NelectServer Port')
    parser.add_argument('--endpoint', default="/api/v1/post_beat",
                        help='NelectServer Endpoint')
    args = parser.parse_args()
    host = str(args.host)
    port = int(args.port)
    endpoint = str(args.endpoint)

    body = get_beat_data()

    def the_try(body, host, port, endpoint):
        try:
            send_beat(body=body, host=host, port=port, endpoint=endpoint)
            to_update_data = removed_data(unique_beat_id=body.get("unique_beat_id"))
            write_data(to_update_data)
        except Exception as ex:
            try:
                update_data(body=body)
            except Exception as ex1:
                print("ex1", ex1)
            print(ex)

    the_try(body=body, host=host, port=port, endpoint=endpoint)

    dead_letters = read_full_data()
    if dead_letters:
        for i, v in enumerate(dead_letters):
            # print(f"DeadLetter #{i}: {v}")
            the_try(body=v, host=host, port=port, endpoint=endpoint)




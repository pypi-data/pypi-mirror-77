from .auth import couchbaseHeaders
from pathlib import Path
import datetime
import pkg_resources
import sqlite3
import requests
import json
import re
import os

# The facilities channel either doesn't have everything or parsing the links from global-facility-service has things that don't exist
class DisneyDatabase:

    def __init__(self, sync_on_init=True):
        self.db_path = os.path.join(Path(os.path.abspath(__file__)).parent, "MouseTools.db")
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

        self.create_last_sequence_table()
        self.create_sync_table()
        self.create_facilities_table()
        self.create_calendar_table()
        print("tables created")

        last_sequence = self.c.execute("""SELECT COUNT(value) FROM lastSequence""").fetchone()[0]
        if last_sequence != 0:
            if sync_on_init:
                self.sync_database()
        else:
            print("before facilities created")
            self.create_facilities_channel('wdw.facilities.1_0.en_us')
            self.create_facilities_channel('dlr.facilities.1_0.en_us')
            print("after facilities created")
            self.conn.commit()
            print("after facilities created commit")

    def sync_database(self):

        self.sync_facilities_channel()
        self.sync_facilitystatus_channel()
        self.sync_today_channel()
        self.sync_calendar_channel()

        self.conn.commit()


    def create_last_sequence_table(self):


        self.c.execute("""CREATE TABLE IF NOT EXISTS lastSequence (channel TEXT PRIMARY KEY, value TEXT, channel_type TEXT)""")

        self.conn.commit()



    def create_facilities_table(self):

        # subType
        self.c.execute("""CREATE TABLE IF NOT EXISTS facilities (id TEXT PRIMARY KEY, name TEXT, entityType TEXT, subType TEXT, doc_id TEXT, destination_code TEXT, park_id TEXT, resort_id TEXT, land_id TEXT, resort_area_id TEXT, entertainment_venue_id TEXT)""")

        self.conn.commit()

    def create_calendar_table(self):

        # subType
        self.c.execute("""CREATE TABLE IF NOT EXISTS calendar (id TEXT PRIMARY KEY, date TEXT, destination_code TEXT, body TEXT)""")

        self.conn.commit()

    def create_sync_table(self):

        self.c.execute("""CREATE TABLE IF NOT EXISTS sync (id TEXT PRIMARY KEY, rev TEXT, body TEXT, channel TEXT)""")

        self.conn.commit()

    def channel_exists(self, channel):

        facility_channel_exists = self.c.execute("""SELECT COUNT(value) FROM lastSequence WHERE channel = '{}'""".format(channel)).fetchone()[0]
        self.conn.commit()


        return facility_channel_exists != 0



    def create_facilities_channel(self, channel):

        payload = {
            "channels": channel,
            "style": 'all_docs',
            "filter": 'sync_gateway/bychannel',
            "feed": 'normal',
            "heartbeat": 30000
        }
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_changes?feed=normal&heartbeat=30000&style=all_docs&filter=sync_gateway%2Fbychannel", data=json.dumps(payload), headers=couchbaseHeaders())
        s = json.loads(r.text)

        self.c.execute("INSERT INTO lastSequence (channel, value, channel_type) VALUES (?, ?, 'facilities')", (channel, s['last_seq'],))

        # search for deleted: i['deleted'] or i['removed']
        docs = []
        for i in s['results']:
            try:
                i['deleted']
                continue
            except:
                this = {}
                this['id'] = i['id']

                docs.append(this)

                split_id = i['id'].split(":")
                if len(split_id) > 1:
                    this = {}
                    this['id'] = split_id[0]
                    docs.append(this)

        print('getting {} docs'.format(len(docs)))

        payload = {"docs": docs, "json":True}
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_bulk_get?revs=true&attachments=true", data=json.dumps(payload), headers=couchbaseHeaders())
        s = r.text

        print("after facilities bulk get")

        cont_reg = re.compile("\w+-\w+:\s\w+\/\w+")
        s = re.sub(cont_reg, "", s)
        s = s.splitlines()
        for x in s:
            if x != '' and x[0] != '-':
                try:
                    x = json.loads(x)
                    print(x['_id'])
                    self.c.execute("INSERT INTO sync (id, rev, body, channel) VALUES (?, ?, ?, ?)", (x['_id'], x['_rev'], json.dumps(x), channel,))

                    split_id = x['_id'].split(':')
                    this['id'] = split_id[-1].split(';')[0].split('.')[-1]


                    this['name'] = x['name']
                    this['entityType'] = x['type']

                    try:
                        this['sub'] = x['subType']
                    except:
                        this['sub'] = None

                    this['cb_id'] = x['_id']
                    this['dest_code'] = x['_id'].split('.')[0]

                    try:
                        this['park_id'] = x['ancestorThemeParkId'].split(';')[0]
                    except:
                        try:
                            this['park_id'] = x['ancestorWaterParkId'].split(';')[0]
                        except:
                            this['park_id'] = None

                    try:
                        this['land_id'] = x['ancestorLandId'].split(';')[0]
                    except:
                        this['land_id'] = None

                    try:
                        this['resort_id'] = x['ancestorResortId'].split(';')[0]
                    except:
                        this['resort_id'] = None

                    try:
                        this['ra_id'] = x['ancestorResortAreaId'].split(';')[0]
                    except:
                        this['ra_id'] = None

                    try:
                        this['ev_id'] = x['ancestorEntertainmentVenueId'].split(';')[0]
                    except:
                        this['ev_id'] = None

                    self.c.execute("INSERT INTO facilities (id, name, entityType, subType, doc_id, destination_code, park_id, land_id, resort_id, resort_area_id, entertainment_venue_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (this['id'], this['name'], this['entityType'], this['sub'], this['cb_id'], this['dest_code'], this['park_id'], this['land_id'], this['resort_id'], this['ra_id'], this['ev_id'],))
                except Exception as e:
                    # print(x)
                    # print(e)
                    continue

        print("after facilities bulk get parsed")
        self.conn.commit()
        print("after facilities bulk get commit")

    def sync_facilities_channel(self):

        docs = []
        for row in self.c.execute("""SELECT * FROM lastSequence WHERE channel_type = 'facilities'""").fetchall():
            payload = {
                "channels": row[0],
                "style": 'all_docs',
                "filter": 'sync_gateway/bychannel',
                "feed": 'normal',
                "heartbeat": 30000
            }
            r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_changes?feed=normal&heartbeat=30000&style=all_docs&since={}&filter=sync_gateway%2Fbychannel".format(row[1]), data=json.dumps(payload), headers=couchbaseHeaders())
            s = json.loads(r.text)

            self.c.execute("REPLACE INTO lastSequence (channel, value, channel_type) VALUES (?, ?, 'facilities')", (row[0], s['last_seq'],))

            # search for deleted: i['deleted'] or i['removed']

            for i in s['results']:
                try:
                    test = i['deleted']
                    self.c.execute("DELETE FROM facilities WHERE doc_id = ?", (i['id'],))
                    self.c.execute("DELETE FROM sync WHERE id = ?", (i['id'],))
                    num_id = i['id'].split(".")[-1].split(";")[0]
                    self.c.execute("DELETE FROM sync WHERE id LIKE '%facilitystatus.1_0.{}%'".format(num_id))
                except:
                    this = {}
                    this['id'] = i['id']

                    docs.append(this)

                    split_id = i['id'].split(":")
                    if len(split_id) > 1:
                        this = {}
                        this['id'] = split_id[0]
                        docs.append(this)

        # print('updating {} docs'.format(len(docs)))

        payload = {"docs": docs, "json":True}
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_bulk_get?revs=true&attachments=true", data=json.dumps(payload), headers=couchbaseHeaders())
        s = r.text

        cont_reg = re.compile("\w+-\w+:\s\w+\/\w+")
        s = re.sub(cont_reg, "", s)
        s = s.splitlines()
        for x in s:
            if x != '':
                try:
                    x = json.loads(x)
                    self.c.execute("INSERT OR REPLACE INTO sync (id, rev, body, channel) VALUES (?, ?, ?, ?)", (x['_id'], x['_rev'], json.dumps(x), row[0],))

                    split_id = x['_id'].split(':')
                    this['id'] = split_id[-1].split(';')[0].split('.')[-1]


                    this['name'] = x['name']
                    this['entityType'] = x['type']

                    try:
                        this['sub'] = x['subType']
                    except:
                        this['sub'] = None

                    this['cb_id'] = x['_id']
                    this['dest_code'] = x['_id'].split('.')[0]

                    try:
                        this['park_id'] = x['ancestorThemeParkId'].split(';')[0]
                    except:
                        this['park_id'] = None

                    try:
                        this['land_id'] = x['ancestorLandId'].split(';')[0]
                    except:
                        this['land_id'] = None

                    try:
                        this['resort_id'] = x['ancestorResortId'].split(';')[0]
                    except:
                        this['resort_id'] = None

                    try:
                        this['ra_id'] = x['ancestorResortAreaId'].split(';')[0]
                    except:
                        this['ra_id'] = None

                    try:
                        this['ev_id'] = x['ancestorEntertainmentVenueId'].split(';')[0]
                    except:
                        this['ev_id'] = None

                    self.c.execute("INSERT OR REPLACE INTO facilities (id, name, entityType, subType, doc_id, destination_code, park_id, land_id, resort_id, resort_area_id, entertainment_venue_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (this['id'], this['name'], this['entityType'], this['sub'], this['cb_id'], this['dest_code'], this['park_id'], this['land_id'], this['resort_id'], this['ra_id'], this['ev_id'],))
                except Exception as e:
                    # print(e)
                    continue


            self.conn.commit()




    def create_facilitystatus_channel(self, channel):

        payload = {
            "channels": channel,
            "style": 'all_docs',
            "filter": 'sync_gateway/bychannel',
            "feed": 'normal',
            "heartbeat": 30000
        }

        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_changes?feed=normal&heartbeat=30000&style=all_docs&filter=sync_gateway%2Fbychannel", data=json.dumps(payload), headers=couchbaseHeaders())
        s = json.loads(r.text)

        self.c.execute("INSERT OR REPLACE INTO lastSequence (channel, value, channel_type) VALUES (?, ?, 'facilitystatus')", (channel, s['last_seq'],))

        # search for deleted: i['deleted'] or i['removed']
        docs = []
        for i in s['results']:
            try:
                i['deleted']
                continue
            except:
                this = {}
                this['id'] = i['id']

                docs.append(this)

                split_id = i['id'].split(":")
                if len(split_id) > 1:
                    this = {}
                    this['id'] = split_id[0]
                    docs.append(this)

        # print('getting {} docs'.format(len(docs)))

        payload = {"docs": docs, "json":True}
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_bulk_get?revs=true&attachments=true", data=json.dumps(payload), headers=couchbaseHeaders())
        s = r.text

        cont_reg = re.compile("\w+-\w+:\s\w+\/\w+")
        s = re.sub(cont_reg, "", s)
        s = s.splitlines()
        for x in s:
            if x != '' and x[0] != '-':
                try:
                    x = json.loads(x)
                    self.c.execute("INSERT INTO sync (id, rev, body, channel) VALUES (?, ?, ?, ?)", (x['_id'], x['_rev'], json.dumps(x), channel,))
                except Exception as e:
                    # print(e)
                    # print(x)
                    continue

        self.conn.commit()


    def sync_facilitystatus_channel(self):

        docs = []
        for row in self.c.execute("""SELECT * FROM lastSequence WHERE channel_type = 'facilitystatus'""").fetchall():
            payload = {
                "channels": row[0],
                "style": 'all_docs',
                "filter": 'sync_gateway/bychannel',
                "feed": 'normal',
                "heartbeat": 30000
                }
            r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_changes?feed=normal&heartbeat=30000&style=all_docs&since={}&filter=sync_gateway%2Fbychannel".format(row[1]), data=json.dumps(payload), headers=couchbaseHeaders())
            s = json.loads(r.text)



            self.c.execute("REPLACE INTO lastSequence (channel, value, channel_type) VALUES (?, ?, 'facilitystatus')", (row[0], s['last_seq'],))

            # search for deleted: i['deleted'] or i['removed']

            for i in s['results']:
                try:
                    i['deleted']
                    continue
                except:
                    this = {}
                    this['id'] = i['id']

                    docs.append(this)

                    split_id = i['id'].split(":")
                    if len(split_id) > 1:
                        this = {}
                        this['id'] = split_id[0]
                        docs.append(this)

        # print('getting {} docs'.format(len(docs)))

        payload = {"docs": docs, "json":True}
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_bulk_get?revs=true&attachments=true", data=json.dumps(payload), headers=couchbaseHeaders())
        s = r.text

        cont_reg = re.compile("\w+-\w+:\s\w+\/\w+")
        s = re.sub(cont_reg, "", s)
        s = s.splitlines()
        for x in s:
            if x != '' and x[0] != '-':
                try:
                    x = json.loads(x)
                    self.c.execute("INSERT OR REPLACE INTO sync (id, rev, body, channel) VALUES (?, ?, ?, ?)", (x['_id'], x['_rev'], json.dumps(x), row[0],))
                except:
                    continue

        self.conn.commit()




    def create_today_channel(self, channel):

        payload = {
            "channels": channel,
            "style": 'all_docs',
            "filter": 'sync_gateway/bychannel',
            "feed": 'normal',
            "heartbeat": 30000
        }
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_changes?feed=normal&heartbeat=30000&style=all_docs&filter=sync_gateway%2Fbychannel", data=json.dumps(payload), headers=couchbaseHeaders())
        s = json.loads(r.text)

        self.c.execute("INSERT OR REPLACE INTO lastSequence (channel, value, channel_type) VALUES (?, ?, 'today')", (channel, s['last_seq'],))

        docs = []
        for i in s['results']:
            try:
                i['deleted']
                continue
            except:
                this = {}
                this['id'] = i['id']

                docs.append(this)

                split_id = i['id'].split(":")
                if len(split_id) > 1:
                    this = {}
                    this['id'] = split_id[0]
                    docs.append(this)

        payload = {"docs": docs, "json":True}
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_bulk_get?revs=true&attachments=true", data=json.dumps(payload), headers=couchbaseHeaders())
        s = r.text

        cont_reg = re.compile("\w+-\w+:\s\w+\/\w+")
        s = re.sub(cont_reg, "", s)
        s = s.splitlines()
        for x in s:
            if x != '' and x[0] != '-':
                try:
                    x = json.loads(x)
                    self.c.execute("INSERT INTO sync (id, rev, body, channel) VALUES (?, ?, ?, ?)", (x['_id'], x['_rev'], json.dumps(x), channel,))
                except:
                    continue

        self.conn.commit()


    def sync_today_channel(self):

        docs = []
        for row in self.c.execute("""SELECT * FROM lastSequence WHERE channel_type = 'today'""").fetchall():
            payload = {
                "channels": row[0],
                "style": 'all_docs',
                "filter": 'sync_gateway/bychannel',
                "feed": 'normal',
                "heartbeat": 30000
                }
            r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_changes?feed=normal&heartbeat=30000&style=all_docs&since={}&filter=sync_gateway%2Fbychannel".format(row[1]), data=json.dumps(payload), headers=couchbaseHeaders())
            s = json.loads(r.text)



            self.c.execute("REPLACE INTO lastSequence (channel, value, channel_type) VALUES (?, ?, 'today')", (row[0], s['last_seq'],))

            # search for deleted: i['deleted'] or i['removed']

            for i in s['results']:
                try:
                    i['deleted']
                    continue
                except:
                    this = {}
                    this['id'] = i['id']

                    docs.append(this)

                    split_id = i['id'].split(":")
                    if len(split_id) > 1:
                        this = {}
                        this['id'] = split_id[0]
                        docs.append(this)

        # print('getting {} docs'.format(len(docs)))

        payload = {"docs": docs, "json":True}
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_bulk_get?revs=true&attachments=true", data=json.dumps(payload), headers=couchbaseHeaders())
        s = r.text

        cont_reg = re.compile("\w+-\w+:\s\w+\/\w+")
        s = re.sub(cont_reg, "", s)
        s = s.splitlines()
        for x in s:
            if x != '' and x[0] != '-':
                try:
                    x = json.loads(x)
                    self.c.execute("INSERT OR REPLACE INTO sync (id, rev, body, channel) VALUES (?, ?, ?, ?)", (x['_id'], x['_rev'], json.dumps(x), row[0],))
                except:
                    continue

        self.conn.commit()



    def create_calendar_channel(self, channel):

        today = datetime.datetime.today()

        dest_code = channel.split('.')[0]

        self.c.execute("DELETE FROM calendar WHERE destination_code = ?", (dest_code,))

        payload = {
            "channels": channel,
            "style": 'all_docs',
            "filter": 'sync_gateway/bychannel',
            "feed": 'normal',
            "heartbeat": 30000
        }
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_changes?feed=normal&heartbeat=30000&style=all_docs&filter=sync_gateway%2Fbychannel", data=json.dumps(payload), headers=couchbaseHeaders())
        s = json.loads(r.text)

        self.c.execute("INSERT OR REPLACE INTO lastSequence (channel, value, channel_type) VALUES (?, ?, 'calendar')", (channel, s['last_seq'],))

        docs = []
        for i in s['results']:
            try:
                i['deleted']
                continue
            except:
                this = {}
                this['id'] = i['id']

                docs.append(this)

                split_id = i['id'].split(":")
                if len(split_id) > 1:
                    this = {}
                    this['id'] = split_id[0]
                    docs.append(this)

        payload = {"docs": docs, "json":True}
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_bulk_get?revs=true&attachments=true", data=json.dumps(payload), headers=couchbaseHeaders())
        s = r.text

        cont_reg = re.compile("\w+-\w+:\s\w+\/\w+")
        s = re.sub(cont_reg, "", s)
        s = s.splitlines()
        for x in s:
            if x != '' and x[0] != '-':
                try:
                    x = json.loads(x)

                    split_id = x['id'].split('-')
                    day = split_id[0]
                    month = split_id[1]
                    if today.month > int(month):
                        year = today.year + 1
                    elif today.month == int(month) and today.day > int(day):
                        year = today.year + 1
                    else:
                        year = today.year

                    date = "{}-{}-{}".format(year, month, day)

                    dest_code = x['_id'].split('.')[0]

                    self.c.execute("INSERT INTO calendar (id, date, destination_code, body) VALUES (?, ?, ?, ?)", (x['_id'], date, dest_code, json.dumps(x),))

                except Exception as e:
                    # print(e)
                    continue

        self.conn.commit()


    def sync_calendar_channel(self):


        for row in self.c.execute("""SELECT * FROM lastSequence WHERE channel_type = 'calendar'""").fetchall():
            self.create_calendar_channel(row[0])

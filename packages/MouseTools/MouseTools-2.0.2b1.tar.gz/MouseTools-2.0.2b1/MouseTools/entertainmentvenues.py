import requests
import json
import sys
import sqlite3
from datetime import datetime, timedelta
from .auth import getHeaders, couchbaseHeaders
from .database import DisneyDatabase

class EntertainmentVenue(object):

    def __init__(self, id = None, sync_on_init=True):
        """
        Constructor Function
        Gets all venue data available and stores various elements into variables.
        """

        error = True
        self.__data = requests.get("https://api.wdpro.disney.go.com/global-pool-override-B/facility-service/entertainment-venues/{}".format(id), headers=getHeaders()).json()
        try:
            if self.__data['id'] is not None:
                error = False
        except:
            pass

        if error:
            raise ValueError('That entertainment venue is not available. id: ' + str(id))

        self.__db = DisneyDatabase(sync_on_init)
        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()


        self.__id = id
        self.__name = self.__data['name']
        self.__entityType = self.__data['type']
        try:
            self.__subType = self.__data['subType']
        except:
            self.__subType = None
        doc_id_query = c.execute("SELECT doc_id from facilities where doc_id LIKE ?", ("%{};entityType={}".format(self.__id, self.__entityType),)).fetchone()
        self.__doc_id = doc_id_query[0] if doc_id_query is not None else None
        self.__facilities_data = self.get_raw_facilities_data()
        try:
            self.__anc_dest_id = self.__data['ancestorDestination']['id'].split(';')[0]
            self.__dest_code = c.execute("SELECT destination_code FROM facilities WHERE id = ?", (self.__anc_dest_id,)).fetchone()[0]
        except:
            self.__anc_dest_id = None
            self.__dest_code = None

        try:
            self.__anc_park_id = self.__data['links']['ancestorThemePark']['href'].split('/')[-1].split('?')[0]
        except:
            try:
                self.__anc_park_id = self.__data['links']['ancestorWaterPark']['href'].split('/')[-1].split('?')[0]
            except:
                try:
                    self.__anc_park_id = self.__facilities_data['ancestorThemeParkId'].split(';')[0]
                except:
                    try:
                        self.__anc_park_id = self.__facilities_data['ancestorWaterParkId'].split(';')[0]
                    except:
                        self.__anc_park_id = None

        try:
            self.__anc_resort_id = self.__data['links']['ancestorResort']['href'].split('/')[-1].split('?')[0]
        except:
            try:
                self.__anc_resort_id = self.__facilities_data['ancestorResortId'].split(';')[0]
            except:
                self.__anc_resort_id = None

        try:
            self.__anc_land_id = self.__data['links']['ancestorLand']['href'].split('/')[-1].split('?')[0]
        except:
            try:
                self.__anc_land_id = self.__facilities_data['ancestorLandId'].split(';')[0]
            except:
                self.__anc_land_id = None

        try:
            self.__anc_ra_id = self.__data['links']['ancestorResortArea']['href'].split('/')[-1].split('?')[0]
        except:
            try:
                self.__anc_ra_id = self.__facilities_data['ancestorResortAreaId'].split(';')[0]
            except:
                self.__anc_ra_id = None

        try:
            self.__anc_ev_id = self.__data['links']['ancestorEntertainmentVenue']['href'].split('/')[-1].split('?')[0]
        except:
            try:
                self.__anc_ev_id = self.__facilities_data['ancestorEntertainmentVenueId'].split(';')[0]
            except:
                self.__anc_ev_id = None

        conn.commit()
        conn.close()

    def get_possible_ids(self):
        """Returns a list of possible ids of this entityType"""
        ids = []

        dest_data = requests.get("https://api.wdpro.disney.go.com/facility-service/destinations/{}".format(self.__anc_dest_id), headers=getHeaders()).json()
        data = requests.get(dest_data['links']['entertainmentVenues']['href'], headers=getHeaders()).json()

        for entry in data['entries']:
            try:
                ids.append(entry['links']['self']['href'].split('/')[-1].split('?')[0])
            except:
                pass

        return ids

    def get_id(self):
        """Return object id"""
        return self.__id

    def get_name(self):
        """Return object name"""
        return self.__name

    def get_entityType(self):
        """Return object entityType"""
        return self.__entityType

    def get_subType(self):
        """Return object subType"""
        return self.__subType

    def get_doc_id(self):
        """Return object doc id"""
        return self.__doc_id

    def get_destination_code(self):
        """Return object destination code"""
        return self.__dest_code

    def get_ancestor_destination_id(self):
        """Return object ancestor destination id"""
        return self.__anc_dest_id

    def get_ancestor_park_id(self):
        """Return object ancestor theme or water park id"""
        return self.__anc_park_id

    def get_ancestor_resort_id(self):
        """Return object ancestor resort id"""
        return self.__anc_resort_id

    def get_ancestor_land_id(self):
        """Return object land id"""
        return self.__anc_land_id

    def get_ancestor_resort_area_id(self):
        """Return object resort area id"""
        return self.__anc_ra_id

    def get_ancestor_entertainment_venue_id(self):
        """Return object entertainment venue id"""
        return self.__anc_ev_id

    def get_links(self):
        """Returns a dictionary of related links"""
        return self.__data['links']

    def get_raw_data(self):
        """Returns the raw data from global-facility-service"""
        return self.__data

    def get_raw_facilities_data(self):
        """Returns the raw facilities data currently stored in the database"""
        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()
        data = c.execute("SELECT body FROM sync WHERE id = ?", (self.__doc_id,)).fetchone()[0]
        conn.commit()
        conn.close()

        if data is None:
            return None
        else:
            return json.loads(data)

    def get_wait_times(self):
        """Returns a list of dictionaries in the form of {rideid:time} for attractions and entertainments for this venue"""
        if self.__db.channel_exists('{}.facilitystatus.1_0'.format(self.__dest_code)):
            self.__db.sync_facilitystatus_channel()
        else:
            self.__db.create_facilitystatus_channel('{}.facilitystatus.1_0'.format(self.__dest_code))

        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()

        ids = [row for row in c.execute("SELECT id, entityType FROM facilities WHERE entertainment_venue_id = ? and (entityType = 'Attraction' or entityType = 'Entertainment')", (self.__id,))]

        data = {}
        for row in ids:
            status_data = c.execute("SELECT body FROM sync WHERE id = ?", ("{}.facilitystatus.1_0.{};entityType={}".format(self.__dest_code, row[0], row[1]),)).fetchone()
            try:
                if status_data is not None:
                    body = json.loads(status_data[0])
                    data[row[0]] = body['waitMinutes']
            except:
                continue

        return data

    def get_wait_times_detailed(self):
        """Returns a list of dictionaries in the form of {rideid:{name, status, wait_time}} for attractions and entertainments for this venue"""
        if self.__db.channel_exists('{}.facilitystatus.1_0'.format(self.__dest_code)):
            self.__db.sync_facilitystatus_channel()
        else:
            self.__db.create_facilitystatus_channel('{}.facilitystatus.1_0'.format(self.__dest_code))

        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()

        ids = [row for row in c.execute("SELECT id, entityType FROM facilities WHERE entertainment_venue_id = ? and (entityType = 'Attraction' or entityType = 'Entertainment')", (self.__id,))]

        data = {}
        for row in ids:
            status_data = c.execute("SELECT body FROM sync WHERE id = ?", ("{}.facilitystatus.1_0.{};entityType={}".format(self.__dest_code, row[0], row[1]),)).fetchone()
            try:
                if status_data is not None:
                    body = json.loads(status_data[0])
                    this = {}
                    this['name'] = c.execute("SELECT name FROM facilities WHERE id = ?", (row[0],)).fetchone()[0]
                    this['status'] = body['status']
                    this['wait_time'] = body['waitMinutes']
                    this['last_updated'] = datetime.strptime(body['lastUpdate'], "%Y-%m-%dT%H:%M:%SZ")
                    data[row[0]] = this
            except Exception as e:
                # print(e)
                continue

        return data

    def get_attraction_wait_times(self):
        """Returns a list of dictionaries in the form of {rideid:time} for attractions for this venue"""
        if self.__db.channel_exists('{}.facilitystatus.1_0'.format(self.__dest_code)):
            self.__db.sync_facilitystatus_channel()
        else:
            self.__db.create_facilitystatus_channel('{}.facilitystatus.1_0'.format(self.__dest_code))

        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()

        ids = [row for row in c.execute("SELECT id, entityType FROM facilities WHERE entertainment_venue_id = ? and entityType = 'Attraction'", (self.__id,))]

        data = {}
        for row in ids:
            status_data = c.execute("SELECT body FROM sync WHERE id = ?", ("{}.facilitystatus.1_0.{};entityType={}".format(self.__dest_code, row[0], row[1]),)).fetchone()
            try:
                if status_data is not None:
                    body = json.loads(status_data[0])
                    data[row[0]] = body['waitMinutes']
            except:
                continue

        return data

    def get_attraction_wait_times_detailed(self):
        """Returns a list of dictionaries in the form of {rideid:{name, status, wait_time}} for attractions for this venue"""
        if self.__db.channel_exists('{}.facilitystatus.1_0'.format(self.__dest_code)):
            self.__db.sync_facilitystatus_channel()
        else:
            self.__db.create_facilitystatus_channel('{}.facilitystatus.1_0'.format(self.__dest_code))

        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()

        ids = [row for row in c.execute("SELECT id, entityType FROM facilities WHERE entertainment_venue_id = ? and entityType = 'Attraction'", (self.__id,))]

        data = {}
        for row in ids:
            status_data = c.execute("SELECT body FROM sync WHERE id = ?", ("{}.facilitystatus.1_0.{};entityType={}".format(self.__dest_code, row[0], row[1]),)).fetchone()
            try:
                if status_data is not None:
                    body = json.loads(status_data[0])
                    this = {}
                    this['name'] = c.execute("SELECT name FROM facilities WHERE id = ?", (row[0],)).fetchone()[0]
                    this['status'] = body['status']
                    this['wait_time'] = body['waitMinutes']
                    this['last_updated'] = datetime.strptime(body['lastUpdate'], "%Y-%m-%dT%H:%M:%SZ")
                    data[row[0]] = this
            except Exception as e:
                # print(e)
                continue

        return data

    def get_entertainment_wait_times(self):
        """Returns a list of dictionaries in the form of {rideid:time} for entertainments for this venue"""
        if self.__db.channel_exists('{}.facilitystatus.1_0'.format(self.__dest_code)):
            self.__db.sync_facilitystatus_channel()
        else:
            self.__db.create_facilitystatus_channel('{}.facilitystatus.1_0'.format(self.__dest_code))

        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()

        ids = [row for row in c.execute("SELECT id, entityType FROM facilities WHERE entertainment_venue_id = ? and entityType = 'Entertainment'", (self.__id,))]

        data = {}
        for row in ids:
            status_data = c.execute("SELECT body FROM sync WHERE id = ?", ("{}.facilitystatus.1_0.{};entityType={}".format(self.__dest_code, row[0], row[1]),)).fetchone()
            try:
                if status_data is not None:
                    body = json.loads(status_data[0])
                    data[row[0]] = body['waitMinutes']
            except:
                continue

        return data

    def get_entertainment_wait_times_detailed(self):
        """Returns a list of dictionaries in the form of {rideid:{name, status, wait_time}} for entertainments for this venue"""
        if self.__db.channel_exists('{}.facilitystatus.1_0'.format(self.__dest_code)):
            self.__db.sync_facilitystatus_channel()
        else:
            self.__db.create_facilitystatus_channel('{}.facilitystatus.1_0'.format(self.__dest_code))

        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()

        ids = [row for row in c.execute("SELECT id, entityType FROM facilities WHERE entertainment_venue_id = ? and entityType = 'Entertainment'", (self.__id,))]

        data = {}
        for row in ids:
            status_data = c.execute("SELECT body FROM sync WHERE id = ?", ("{}.facilitystatus.1_0.{};entityType={}".format(self.__dest_code, row[0], row[1]),)).fetchone()
            try:
                if status_data is not None:
                    body = json.loads(status_data[0])
                    this = {}
                    this['name'] = c.execute("SELECT name FROM facilities WHERE id = ?", (row[0],)).fetchone()[0]
                    this['status'] = body['status']
                    this['wait_time'] = body['waitMinutes']
                    this['last_updated'] = datetime.strptime(body['lastUpdate'], "%Y-%m-%dT%H:%M:%SZ")
                    data[row[0]] = this
            except Exception as e:
                # print(e)
                continue

        return data

    def get_status(self):
        """Return current status of the object."""
        if self.__db.channel_exists('{}.today.1_0'.format(self.__dest_code)):
            self.__db.sync_today_channel()
            # maybe just sync this channel? and do same for previous methods
        else:
            self.__db.create_today_channel('{}.today.1_0'.format(self.__dest_code))

        conn = sqlite3.connect(self.__db.db_path)
        c = conn.cursor()

        today_data = c.execute("""SELECT body FROM sync WHERE id = '{}.today.1_0.{}'""".format(self.__dest_code, self.__entityType)).fetchone()

        if today_data is None:
            return None
        else:
            body = json.loads(today_data[0])
            try:
                return body['facilities'][str(self.__id) + ';entityType=' + self.__entityType][0]['scheduleType']
            except:
                return None

    def get_last_update(self):
        """Returns facilities last update time as a datetime object"""
        facility_data = self.get_raw_facilities_data()
        if facility_data is None:
            return None
        else:
            return datetime.strptime(facility_data['lastUpdate'], "%Y-%m-%dT%H:%M:%SZ")

    def get_coordinates(self):
        """Returns the object's latitude and longitude"""
        try:
            return self.__data['coordinates']['Guest Entrance']['gps']
        except:
            return None

    def get_description(self):
        """Returns the object's descriptions"""
        try:
            long_desc = self.__data["descriptions"]["MM - " + self.__name]["text"].replace("<p>", "").split('</p>')[0]
            return long_desc
        except:
            return None

    def get_list_image(self):
        """Returns the url to the object's list image"""
        facility_data = self.get_raw_facilities_data()
        if facility_data is None:
            return None
        else:
            return facility_data['listImageUrl']

    def get_detail_image(self):
        """Returns the url to the object's detail image"""
        facility_data = self.get_raw_facilities_data()
        if facility_data is None:
            return None
        else:
            return facility_data['detailImageUrl']

    def get_hours(self, date = ""):
        """
        Gets the object's hours on a specific day and returns them as a datetime object.
        Returns the object's hours in the following order: operating open, operating close, Extra Magic open, Extra Magic close.
        Extra Magic hours will return None if there are none for today.
        If all hours are None then Disney has no hours for that day.
        date = "YEAR-MONTH-DATE"
        If you don't pass a date, it will get today's hours
        """

        if date == "":
            DATE = datetime.today()
        else:
            year, month, day = date.split('-')
            DATE = datetime(int(year), int(month), int(day))

        s = requests.get("https://api.wdpro.disney.go.com/facility-service/schedules/{}?date={}-{}-{}".format(self.__id, DATE.year, self.__formatDate(str(DATE.month)), self.__formatDate(str(DATE.day))), headers=getHeaders())
        data = json.loads(s.content)

        operating_hours_start = None
        operating_hours_end = None
        extra_hours_start = None
        extra_hours_end = None

        try:
            for i in range(len(data['schedules'])):
                if data['schedules'][i]['type'] == 'Operating':
                    operating_hours_start = datetime(DATE.year, DATE.month, DATE.day, int(data['schedules'][i]['startTime'][0:2]), int(data['schedules'][i]['startTime'][3:5]))
                    if int(data['schedules'][i]['endTime'][0:2]) >= 0 and int(data['schedules'][i]['endTime'][0:2]) <= 7:
                        DATETEMP = DATE + timedelta(days=1)
                        operating_hours_end = datetime(DATETEMP.year, DATETEMP.month, DATETEMP.day, int(data['schedules'][i]['endTime'][0:2]), int(data['schedules'][i]['endTime'][3:5]))
                    else:
                        operating_hours_end = datetime(DATE.year, DATE.month, DATE.day, int(data['schedules'][i]['endTime'][0:2]), int(data['schedules'][i]['endTime'][3:5]))

                if data['schedules'][i]['type'] == "Special Ticketed Event":
                    extra_hours_start = datetime(DATE.year, DATE.month, DATE.day, int(data['schedules'][i]['startTime'][0:2]), int(data['schedules'][i]['startTime'][3:5]))
                    if int(data['schedules'][i]['endTime'][0:2]) >= 0 and int(data['schedules'][i]['endTime'][0:2]) <= 7:
                        DATETEMP = DATE + timedelta(days=1)
                        extra_hours_end = datetime(DATETEMP.year, DATETEMP.month, DATETEMP.day, int(data['schedules'][i]['endTime'][0:2]), int(data['schedules'][i]['endTime'][3:5]))
                    else:
                        operating_hours_end = datetime(DATE.year, DATE.month, DATE.day, int(data['schedules'][i]['endTime'][0:2]), int(data['schedules'][i]['endTime'][3:5]))

        except KeyError:
            pass
        return operating_hours_start, operating_hours_end, extra_hours_start, extra_hours_end

    def get_advisories(self):
        """
        Gets all the advisories for the venue and returns a list in the form of [{id, name}].
        May take some time because it has to go to every link for each advisory.
        """

        advisories = []

        for i in range(len(self.__data['advisories'])):
            data = requests.get(self.__data['advisories'][i]['links']['self']['href'], headers=getHeaders()).json()
            this = {}
            this['id'] = data['id']
            this['name'] = data['name']
            advisories.append(this)

        return advisories

    def __formatDate(self, num):
        """
        Formats month and day into proper format
        """
        if len(num) < 2:
            num = '0'+num
        return num

    def __eq__(self, other):
        """
        Checks if objects are equal
        """
        return self.__id == other.get_id()

    def __str__(self):
        return 'Entertainment Venue object for {}'.format(self.__name)

# TODO get attraction_ids

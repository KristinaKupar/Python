import xml.etree.ElementTree as ET
import MySQLdb as mdb
import sys


class DataBase:
    def __init__(self):
        self.con = mdb.connect('localhost', 'taliZorah', 'tali1597', 'mydb')

    def clear_existing_table(self, table_name):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("SET AUTOCOMMIT = 0")
            cur.execute("START TRANSACTION")
            cur.execute("TRUNCATE " + table_name)
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            cur.execute("COMMIT")
            cur.execute("SET AUTOCOMMIT = 1")

    def parse_xml(self):
        tree = ET.parse('dbManager/static/datatables/mydb.xml')
        root = tree.getroot()
        with self.con:
            cur = self.con.cursor()
            for child in root:
                if child.tag == "singers":
                    self.clear_existing_table("SingerTb")
                    for singer in child:
                        cur.execute("INSERT INTO SingerTb(Singer_name, Singer_from, Album_count)  VALUES ('" +
                                      singer.attrib["name"] + "','" +
                                      singer.attrib["from"] + "','" +
                                      singer.attrib["album_count"] + "')")
                if child.tag == "songs":
                    self.clear_existing_table("SongTb")
                    for song in child:
                        cur.execute("INSERT INTO SongTb(SongName, Style, Singer_id, Song_len) VALUES ('" +
                                      song.attrib["name"] + "','" +
                                      song.attrib["style"] + "','" +
                                      song.attrib["singer_id"] + "','" +
                                        song.attrib["len"]  +

                                      "')")
                if child.tag == "customers":
                    self.clear_existing_table("CustomerTb")
                    for customer in child:
                        cur.execute("INSERT INTO CustomerTb(CustomerName) VALUES ('" +
                                      customer.attrib["name"] +
                                      "')")
                if child.tag == "history":
                    self.clear_existing_table("MusicShopDb")
                    for order in child:
                        cur.execute("INSERT INTO MusicShopDb(Customer_id, Song_id, Date) VALUES ('" +
                                      order.attrib["cust_id"] + "','" +
                                      order.attrib["song_id"] + "','" +
                                      order.attrib["date"] +
                                      "')")

    def insert_song(self, request, id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO SongTb(SongName, Style, Singer_id, Song_len) VALUES ('" +
                          request["name"] + "','" +
                          request["style"] + "','" +
                          id + "','" +
                          request["len"] +
                          "')")

    def insert_order(self, cust_id, song_id, date):
        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO MusicShopDb(Customer_id, Song_id, Date) VALUES ('" +
                          cust_id + "','" +
                          song_id + "','" +
                          date +
                          "')")

    def delete_singer_by_id(self, id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("Delete from SingerTb Where Singer_id = " + id)

    def delete_order_by_id(self, request):
        with self.con:
            cur = self.con.cursor()
            cur.execute("Delete from MusicShopDb Where idMusicShopDb = " + request.POST.get("DeleteOrder", False))

    def delete_songs_by_id(self, id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("Delete from SongTb Where Singer_id = " + id)

    def get_songs(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM SongTb INNER JOIN SingerTb ON SongTb.Singer_id=SingerTb.Singer_id")
            return cur.fetchall()

    def get_singers(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM SingerTb")
            return cur.fetchall()

    def get_history(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM MusicShopDb INNER JOIN CustomerTb ON\
                  MusicShopDb.Customer_id=CustomerTb.CustomerId INNER JOIN SongTb\
                              ON MusicShopDb.Song_id=SongTb.Song_id")
            return cur.fetchall()

    def get_history_by_id(self, id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT Song_id FROM MusicShopDb WHERE idMusicShopTb=" + id)
            return cur.fetchone()

    def get_singers_in_range(self, request):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM SingerTb Where Album_count > {0} and Album_count <\
                        {1}".format(request["Min"], request["Max"]))
            return cur.fetchall()

    def get_id_by_name(self, name):
        with self.con:
            cur = self.con.cursor()
            cur.execute('Select Singer_id FROM SingerTb WHERE Singer_name = "{0}"'.format(name))
            return cur.fetchone()

    def get_song_by_name(self, name):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                'Select Song_id FROM SongTb WHERE SongName = "{0}"'.format(name))
            return cur.fetchone()

    def get_singer_by_name(self, name):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                'Select Singer_id FROM SingerTb WHERE Name = "{0}"'.format(name))
            return cur.fetchone()

    def get_customer(self, request):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                'Select CustomerId FROM CustomerTb WHERE CustomerName = "{0}"'.format(request.POST["Cust_name"]))
            return cur.fetchone()

    def get_name_by_id(self, id):
        with self.con:
            cur = self.con.cursor()
            cur.execute('Select Singer_name FROM SingerTb Where Singer_id = {0}'.format(id))
            return cur.fetchone()

    def update_song(self, request, id):
        with self.con:
            cur = self.con.cursor()
            cur.execute('UPDATE SongTb SET SongName= "{0}", Style = "{1}"\
                              , Singer_id= {2} , Song_len= {3}  Where Song_id ={4}' \
                        .format(request["nameEdit"], request["styleEdit"], id, \
                                request["lenEdit"], request["idEdit"]))

    def update_order(self, song_id, order_id):
        with self.con:
            cur = self.con.cursor()
            cur.execute('UPDATE MusicShopDb SET Song_id = {0} Where idMusicShopDb={1}' \
                        .format(song_id, order_id))


    def find_in_boolean_mode(self, name):
        with self.con:
            cur = self.con.cursor()
            print name
            cur.execute(
                'Select * From SongTb INNER JOIN SingerTb ON SongTb.Singer_id=SingerTb.Singer_id Where match(SongTb.SongName) against("+{0}" IN BOOLEAN MODE)'.format(
                    name))
            return cur.fetchall()
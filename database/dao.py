from database.DB_connect import DBConnect
from model.artist import Artist
from model.album import Album
from model.track import Track

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_albums():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM album"""
        cursor.execute(query)
        for row in cursor:
            album = Album(id=row['id'], title=row['title'], artist_id=row["artist_id"])
            result.append(album)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_tracks():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT id, album_id, genre_id, milliseconds FROM track"""
        cursor.execute(query)
        for row in cursor:
            track = Track(id=row['id'], album_id=row['album_id'], genre_id=row["genre_id"], milliseconds=row["milliseconds"])
            result.append(track)
        cursor.close()
        conn.close()
        return result

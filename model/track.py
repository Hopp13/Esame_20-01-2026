from dataclasses import dataclass


@dataclass
class Track:
    id : int
    album_id : int
    genre_id : int
    milliseconds : int

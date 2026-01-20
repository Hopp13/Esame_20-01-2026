from dataclasses import dataclass

@dataclass
class Album:
    id : int
    title : str
    artist_id : int

    def __str__(self):
        return f"{self.id}, {self.title}, {self.artist_id}"

    def __hash__(self):
        return hash(self.id)

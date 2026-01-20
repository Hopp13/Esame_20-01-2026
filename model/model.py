import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()

        self._max_weight = 0
        self._best_path = []
        self._artists_for_path = []

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()

    def build_graph(self, min_albums):
        albums = DAO.get_albums()

        for artist in self._artists_list:
            n_albums = 0
            for album in albums:
                if album.artist_id == artist.id:
                    n_albums += 1
            if n_albums >= min_albums:
                self._graph.add_node(artist)

        tracks = DAO.get_tracks()

        genres_by_artists = []
        for node in list(self._graph.nodes()):
            artist_genres = set()

            for album in albums:
                if album.artist_id == node.id:

                    for track in tracks:
                        if track.album_id == album.id:
                            artist_genres.add(track.genre_id)
            genres_by_artists.append((node, artist_genres))

        for artist1, genres1 in genres_by_artists:
            for artist2, genres2 in genres_by_artists:
                if not artist1 == artist2:
                    common_genres = 0
                    for genre1 in genres1:
                        for genre2 in genres2:
                            if genre1 == genre2:
                                common_genres += 1

                    if common_genres > 0:
                        self._graph.add_edge(artist1, artist2, weight=common_genres)

    def get_graph_data(self):
        return len(list(self._graph.nodes())), len(list(self._graph.edges()))

    def get_nodes(self):
        return list(self._graph.nodes())

    def get_neighbors_weights(self, actual_artist):
        artists = DAO.get_all_artists()

        for artist in artists:
            if actual_artist == artist.id:
                actual_artist = artist

        neighbors = self._graph.neighbors(actual_artist)

        weight_by_neighbors = []
        for neighbor in neighbors:
            weight_by_neighbors.append((neighbor, self._graph.get_edge_data(actual_artist, neighbor)))

        return weight_by_neighbors

    def get_artists(self):
        return self._artists_list

    def get_artists_min_duration(self, min_duration):
        tracks = DAO.get_tracks()
        albums = DAO.get_albums()

        duration_by_artist = []
        for node in list(self._graph.nodes()):
            duration = 0

            for album in albums:
                if album.artist_id == node.id:

                    for track in tracks:
                        if track.album_id == album.id:
                            if track.milliseconds / 60000 >= duration:
                                duration = track.milliseconds / 60000
            duration_by_artist.append((node, duration))

        winning_artists = []
        for artist, duration in duration_by_artist:
            if duration > min_duration:
                winning_artists.append(artist)

        return winning_artists

    def get_path(self, artista, artisti_massimi, durata_minima):
        self._max_weight = 0
        self._best_path = []
        self._artists_for_path = self.get_artists_min_duration(durata_minima)
        self._artists_for_path.remove(artista)

        self._ricorsione(artisti_massimi, 0, [], artista)

        best_path = [artista]
        for x in self._best_path:
            best_path.append(x)

        return best_path, self._max_weight

    def _ricorsione(self, artisti_massimi, peso_attuale, percorso_attuale, artista_precedente):

        if len(percorso_attuale) == artisti_massimi:
            if peso_attuale > self._max_weight:
                self._max_weight = peso_attuale
                self._best_path = percorso_attuale.copy()
        else:
            for artista in self._artists_for_path:
                print()
                for tuple in list(self._graph.edges(data = False)):
                    print(tuple)
                print()
                if (artista, artista_precedente) in list(self._graph.edges(data = False)):
                    self._artists_for_path.remove(artista)
                    peso_attuale += self._graph.get_edge_data(artista, artista_precedente)['weight']
                    percorso_attuale.append(artista)
                    nuovo_artista_precedente = artista

                    self._ricorsione(artisti_massimi, peso_attuale, percorso_attuale, nuovo_artista_precedente)

                    self._artists_for_path.append(artista)
                    peso_attuale -= self._graph.get_edge_data(artista, artista_precedente)['weight']
                    percorso_attuale.remove(artista)

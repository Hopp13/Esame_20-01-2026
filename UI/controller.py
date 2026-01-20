import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        self._view.txt_result.controls.clear()
        self._view.ddArtist.options.clear()

        try:
            int(self._view.txtNumAlbumMin.value)
        except ValueError:
            self._view.show_alert("Hai inserito un valore non corretto")
        if int(self._view.txtNumAlbumMin.value) <= 0:
            self._view.show_alert("Hai inserito un valore non corretto")

        self._model.build_graph(int(self._view.txtNumAlbumMin.value))

        n_nodes, n_edges = self._model.get_graph_data()

        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {n_nodes} nodi, {n_edges} archi"))

        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False

        nodes = self._model.get_nodes()

        for node in nodes:
            self._view.ddArtist.options.append(ft.DropdownOption(key = node.id, text = node.name))

        self._view.update_page()

    def handle_connected_artists(self, e):
        artist = int(self._view.ddArtist.value)

        weights_by_neighbor = self._model.get_neighbors_weights(artist)

        weights_by_neighbor = sorted(weights_by_neighbor, key=lambda item: item[0].id)

        for neighbor, edge_data in weights_by_neighbor:
            weight = edge_data['weight']
            self._view.txt_result.controls.append(ft.Text(f"{neighbor.id}, {neighbor.name} - Generi in comune: {weight}"))

        self._view.txtMinDuration.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.btnSearchArtists.disabled = False

        self._view.update_page()

    def handle_search(self, e):
        self._view.txt_result.controls.clear()

        try:
            float(self._view.txtMinDuration.value)
        except ValueError:
            self._view.show_alert("Hai inserito un valore non corretto")
        if float(self._view.txtMinDuration.value) <= 0:
            self._view.show_alert("Hai inserito un valore non corretto")

        n_nodes, n_edges = self._model.get_graph_data()
        try:
            int(self._view.txtMaxArtists.value)
        except ValueError:
            self._view.show_alert("Hai inserito un valore non corretto")
        if int(self._view.txtMaxArtists.value) <= 0 or int(self._view.txtMaxArtists.value) > n_nodes:
            self._view.show_alert("Hai inserito un valore non corretto")

        artista = int(self._view.ddArtist.value)
        artists = self._model.get_artists()
        for artist in artists:
            if artist.id == artista:
                artista = artist

        path, peso_massimo = self._model.get_path(artista, int(self._view.txtMaxArtists.value), float(self._view.txtMinDuration.value))

        self._view.txt_result.controls.append(ft.Text(f"Cammino di peso massimo dall'artista: {artista}"))
        self._view.txt_result.controls.append(ft.Text(f"Lunghezza: {len(path)}"))
        for node in path:
            self._view.txt_result.controls.append(ft.Text(f"{node.id}, {node.name}"))
        self._view.txt_result.controls.append(ft.Text(f"Peso massimo: {peso_massimo}"))

        self._view.update_page()

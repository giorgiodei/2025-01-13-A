import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def filldd_localization(self, dd: ft.Dropdown()):
        localization= self._model.get_all_locations_desc()
        for l in localization:
            dd.options.append(ft.dropdown.Option(text=l))

    def handle_graph(self, e):

        localization = self._view.dd_localization.value
        if localization is None:
            self._view.create_alert("Seleziona una localizzazione")
            return
        self._model.creaGrafo(localization)
        n, m = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! "
                    f"Il grafo è costituito di {n} nodi e {m} archi")
        )

        topA = self._model.getTopArchi()

        if len(topA) > 0:
            self._view.txt_result.controls.append(
                ft.Text("archi per peso crescente", color="blue")
            )

            for a1, a2, dati in topA:
                peso = dati["weight"]
                self._view.txt_result.controls.append(
                    ft.Text(f"{a1} -> {a2}, peso: {peso}")
                )
        else:
            self._view.txt_result.controls.append(
                ft.Text("Nessun arco presente nel grafo.", color="red")
            )

        self._view.update_page()

    def analyze_graph(self, e):
        self._view.txt_result.controls.clear()
        if not self._model._grafo.number_of_nodes() > 0:
            self._view.txt_result.controls.append(
                ft.Text("Devi prima creare il grafo.")
            )
            self._view.update_page()
            return

        components = self._model.get_connected_components()

        if not components:
            self._view.txt_result.controls.append(
                ft.Text("Nessuna componente connessa di dimensione maggiore di 1.")
            )
        else:
            for i, comp in enumerate(components, start=1):
                self._view.txt_result.controls.append(
                    ft.Text(f"Componente {i} - dimensione: {len(comp)}")
                )
                for nodo in comp:
                    self._view.txt_result.controls.append(
                        ft.Text(f"   GeneID: {nodo.GeneID}")
                    )

        self._view.update_page()

    def handle_path(self, e):
        pass


from operator import itemgetter

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.annodd = None
        self.squadradd = None

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        self._view.update_page()

        self._model.build_graph(self.annodd)

        self._view._txt_result.controls.append(ft.Text(self._model.grafo))
        self.fill_dropdownSquadra()

        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        dettagli = self._model.get_dettagli(self.squadradd)
        lista_ordinata = sorted(dettagli, key=lambda x: x[1], reverse= True)
        for d in lista_ordinata:
            self._view._txt_result.controls.append(ft.Text(f"{d[0]} - tot salary: {d[1]} $ "))
        self._view.update_page()


    def handlePercorso(self, e):
        if self.squadradd is not None:
            self._view.show_loading_bar()
            self._model.bestPath(self.squadradd)
            self._view.remove_loading_bar()


    def fill_dropdownAnni(self):
        lista_opzioni = DAO.getter_anni()
        for o in lista_opzioni:
            self._view._ddAnno.options.append(ft.dropdown.Option(key=o,
                                                                  text=o,
                                                                  data=o,
                                                                  on_click=self.read_dropdownAnni))

    def read_dropdownAnni(self, e):
        self.annodd = e.control.data
        print(f"valore letto: {self.annodd} - {type(self.annodd)}")

        self._view._txtOutSquadre.controls.clear()
        for team in DAO.getter_teams_year(self.annodd).values():
            self._view._txtOutSquadre.controls.append(ft.Text(f"{team}"))
        self._view._page.update()



    def fill_dropdownSquadra(self):
        self._view._ddSquadra.options.clear()
        lista_opzioni = list(self._model.grafo.nodes)
        for o in lista_opzioni:
            self._view._ddSquadra.options.append(ft.dropdown.Option(key=o,
                                                                  text=o,
                                                                  data=o,
                                                                  on_click=self.read_dropdownSquadra))

    def read_dropdownSquadra(self, e):
        self.squadradd = e.control.data
        print(f"valore letto: {self.squadradd} - {type(self.squadradd)}")

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDYear(self):
        years = self._model.getYears() #lista con tutti gli anni, per metterli nel dropdown della view devo ciclare questa lista e appendere ad una lista vuota ft.dropdown.Option(year)
        yearsDD = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = yearsDD
        self._view.update_page()
        # yearsDD = []
        # for year in years:
        #     yearsDD.append(ft.dropdown.Option(year))



    def handleDDYearSelection(self, e):
        teams = self._model.getTeamsofYear(self._view._ddAnno.value) #lista dei team
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"ho trovato {len(teams)} squadre che hanno giocoato nel {self._view._ddAnno.value} "))
        for team in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{team.teamCode} "))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data = team, text = team.teamCode, on_click=self.readDDTeams))


        self._view.update_page()

    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
        print(f" readTTTeams called -- {self._selectedTeam}")



    def handleCreaGrafo(self, e):

        year = self._view._ddAnno.value
        if year is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione: selezionare un anno", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(int(year))
        numNodi, numArchi = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {numNodi} vertici e {numArchi} archi."))
        self._view.update_page()



    def handleDettagli(self, e):
        source = self._selectedTeam
        if self._selectedTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("per favore selezionare un team", color = "red"))
            self._view.update_page()
            return
        # [  (v0, p0) (v1,p1) (v2,p2) ] lista di tuple dove il primo elemento di una tupla è un nodo e il secomndo elemento è un peso
        viciniSorted = self._model.getNeighborsSorted(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"il vicinato conta {len(viciniSorted)} squadre"))
        for v in viciniSorted:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} -- peso: {v[1]} "))

        self._view.update_page()



    def handlePercorso(self, e):
        if self._selectedTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("per favore selezionare un team", color="red"))
            self._view.update_page()
            return
        path, score = self._model.getBestPathV2(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f" trovato un cammino che parte da {self._selectedTeam} con somma dei pesi= {score} "))
        for v in path:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} -- peso: {v[1]} "))

        self._view.update_page()


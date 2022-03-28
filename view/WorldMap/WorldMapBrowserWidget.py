from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from consts import *
import pandas as pd
import json
import plotly.express as px
from ColoringAlgos import ColoringAlgos
from graph import *
from PyQt5 import QtWebEngineWidgets
import plotly.offline as po
import os

class WorldMapBrowserWidget(QtWidgets.QWidget):   

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.fig = self.get_fig()
        self.save_fig()
        self.show_graph()

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.browser)

        self.setLayout(vlayout)

    def load_us(self):
        vertices = VerticesList()
        edges = EdgesSet()
        dfBorders = pd.read_csv("res/wm_us/us-state-borders.csv")
        for idx, row in dfBorders.iterrows():
            st1, st2 = row["ST1ST2"].split("-")
            if st1 not in vertices:
                vertices.add(Vertex(st1))
            if st2 not in vertices:
                vertices.add(Vertex(st2))

            edges.add((vertices[st1], vertices[st2]))

        graph = Graph(vertices,edges)
        
        dfBound = pd.read_csv("res/wm_us/us-state-boundaries.csv", delimiter=";")
        geo = None
        with open("res/wm_us/us-geo.json", "r") as f:
            geo = json.load(f)

        dfColor = pd.DataFrame(columns=["stusab", "color"])

        limit = ColoringAlgos.coloredLimit
        ColoringAlgos.coloredLimit = 999
        ColoringAlgos.sat(graph)
        ColoringAlgos.coloredLimit = limit
        for vertex in graph.vertices:
            dfC = pd.DataFrame([[vertex.id, vertex.color]], columns=["stusab", "color"])
            dfColor = pd.concat([dfColor, dfC])

        dfBound = dfBound.merge(dfColor, how="inner", left_on="stusab", right_on="stusab")

        fig = px.choropleth_mapbox(dfBound, geojson=geo, color="color",
                                locations="name", featureidkey="properties.name",
                                center={"lat": 42.5517, "lon": -95.7073},
                                mapbox_style="carto-positron", zoom=2.7, color_discrete_sequence=COLORS_ORDER)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(showlegend=False)

        return fig

    def load_fr(self):
        vertices = VerticesList()
        edges = EdgesSet()
        with open("res/wm_fr/departements_fr_boundaries.txt", "r") as f:
            for line in f.readlines():
                row = line.strip().split(",")
                dept = row[0]
                if dept not in vertices:
                    vertices.add(Vertex(dept))


                for vois in row[1:]:
                    if vois not in vertices:
                        vertices.add(Vertex(vois))
                    edges.add((vertices[dept], vertices[vois]))

        graph = Graph(vertices,edges)
        
        geo = None
        with open("res/wm_fr/fr-geo.json", "r") as f:
            geo = json.load(f)

        dfColor = pd.DataFrame(columns=["stusab", "color"])

        limit = ColoringAlgos.coloredLimit
        ColoringAlgos.coloredLimit = 999
        ColoringAlgos.sat(graph)
        ColoringAlgos.coloredLimit = limit
        for vertex in graph.vertices:
            dfC = pd.DataFrame([[vertex.id, vertex.color]], columns=["stusab", "color"])
            dfColor = pd.concat([dfColor, dfC])
            
        fig = px.choropleth_mapbox(dfColor, geojson=geo, color="color",
                                locations="stusab", featureidkey="properties.code",
                                center={"lat": 46.8517, "lon": 1.7073},
                                mapbox_style="carto-positron", zoom=4.7, color_discrete_sequence=COLORS_ORDER)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(showlegend=False)

        return fig

    def get_fig(self, center={"lat": 46.8517, "lon": 1.7073}):
        fig_us = self.load_us()
        fig_fr = self.load_fr()

        for data in fig_us.data:
            fig_fr.add_trace(data)

        fig_fr.update_geos(center=center)

        return fig_fr
        
    def save_fig(self):
        wDir = os.getcwd()
        path = wDir+"/res/wm-plot.html"
        po.plot(self.fig, auto_open=False, filename=path)
    
    def show_graph(self):
        wDir = os.getcwd()
        path = wDir+"/res/wm-plot.html"

        self.browser.load(QUrl.fromLocalFile(path))
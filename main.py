import sys
from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from network_graph_widget import *
import networkx as nx
import json

import requests
import requests_cache
session = requests_cache.CachedSession('./test_cache', expire_after=requests_cache.NEVER_EXPIRE, backend='filesystem')

#G = nx.Graph()
#G.add_node(1)
#G.add_node(2)
#G.add_edge(1, 2)

#G = nx.Graph()
#G.add_node(user["login"], img=user["avatar_url"])
#for follower in followers:
#    G.add_node(follower["login"], img=follower["avatar_url"])
#    G.add_edge("FearMyShotz", follower["login"])


class UiLoader(QtUiTools.QUiLoader):
    _baseinstance = None

    def createWidget(self, classname, parent=None, name=''):
        if parent is None and self._baseinstance is not None:
            widget = self._baseinstance
        else:
            widget = super().createWidget(classname, parent, name)
            if self._baseinstance is not None:
                setattr(self._baseinstance, name, widget)
        return widget

    def loadUi(self, uifile, baseinstance=None):
        self._baseinstance = baseinstance
        widget = self.load(uifile)
        QtCore.QMetaObject.connectSlotsByName(baseinstance)
        return widget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loader = UiLoader()
        loader.registerCustomWidget(network_graph_widget)
        loader.loadUi('mainwindow.ui', self)
        #self.network_graph.set_graph(G)
        self.network_graph.node_clicked.connect(self.cmd_out)

        self.search_bar.returnPressed.connect(self.get_user)

        #for i in G.nodes:
        #    tmp = QtGui.QPixmap()
        #    tmp.loadFromData(session.get(G.nodes[i]["img"]).content)

        #    G.nodes[i]["pixmap"] = QtGui.QPixmap(tmp.width(), tmp.height())
        #    G.nodes[i]["pixmap"].fill(QtGui.QColor("transparent"))

        #    painter = QtGui.QPainter(G.nodes[i]["pixmap"])
        #    brush = QtGui.QBrush(tmp)
        #    painter.setBrush(brush)
        #    painter.setPen(Qt.PenStyle.NoPen)

        #    painter.drawRoundedRect(0, 0,
        #                            G.nodes[i]["pixmap"].width(),
        #                            G.nodes[i]["pixmap"].height(),
        #                            int(G.nodes[i]["pixmap"].width() / 2),
        #                            int(G.nodes[i]["pixmap"].height() / 2))
        #    print(i)
    def get_user(self):
        self.cmd_out(self.search_bar.text())
        user = json.loads(session.get("https://api.github.com/users/" + self.search_bar.text()).text)
        followers = json.loads(session.get("https://api.github.com/users/" + self.search_bar.text() + "/followers").text)

        G = nx.Graph()
        G.add_node(user["login"], img=user["avatar_url"])
        for follower in followers:
            G.add_node(follower["login"], img=follower["avatar_url"])
            G.add_edge(user["login"], follower["login"])
        self.network_graph.set_graph(G)
    def cmd_out(self, out):
        self.cmd_output.appendPlainText(out)

if __name__ == '__main__':

    app = QtWidgets.QApplication(['SocialMediaAnalyzer'])
    window = MainWindow()
    window.show()
    try:
        app.exec()
    except AttributeError:
        app.exec_()


from PySide6.QtWidgets import QLabel
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
import networkx as nx


class network_graph_widget(QLabel):
    def __init__(self, *argv, **kargv):
        super().__init__()
        self.offset = [0, 0]
        self.scale = 1
        self.mouse_pos = QtCore.QPointF(0, 0)
        self.mouse_moved = False
        self.collision_pixmap = None
        self.collision_map = {}

    ############
    ## EVENTS ##
    ############

    def resizeEvent(self, event):
        self.draw()

    # Mouse Events
    def mousePressEvent(self, event):
        self.mouse_moved = False
        self.mouse_pos = event.position()

    def mouseMoveEvent(self, event):
        self.mouse_moved = True
        mouse_delta = event.position() - self.mouse_pos
        self.offset[0] += mouse_delta.x()
        self.offset[1] += mouse_delta.y()
        self.mouse_pos = event.position()
        self.draw()

    def mouseReleaseEvent(self, event):
        if self.mouse_moved:
            return
        self.nodeClickedEvent(event)

    #node_clicked = QtCore.Signal(QtGui.QMouseEvent)
    node_clicked = QtCore.Signal(str)
    def nodeClickedEvent(self, event):
        event.node = "lel"
        # print(event.node)
        # print(self.collision_pixmap.toImage().pixel(event.position().toPoint()))
        # self.node_clicked.emit(event)
        # for i in self.G.edges:
        #    if self.G.edges[i]["c_color"] == self.collision_pixmap.toImage().pixel(event.position().toPoint()):
        #        print(self.G.edges[i])
        #        return
        #print(self.collision_map[f"{self.collision_pixmap.toImage().pixel(event.position().toPoint())}"])
        try:
            self.node_clicked.emit(str(self.collision_map[f"{self.collision_pixmap.toImage().pixel(event.position().toPoint())}"]))
        except:
            ...

    def wheelEvent(self, event):
        position = event.position()
        if event.angleDelta().y() > 0:
            self.scale *= 0.9
            self.offset[0] /= 0.9
            self.offset[1] /= 0.9
        else:
            self.scale *= 1.1
            self.offset[0] /= 1.1
            self.offset[1] /= 1.1
        self.draw()

    ###############
    ## FUNCTIONS ##
    ###############

    def set_graph(self, G):
        self.G = G
        self.G_pos = nx.spring_layout(G, k=0.2, iterations=100, scale=250, center=(0, 0))
        self.draw()
        print("lel")

    def draw(self):
        if not hasattr(self, "G"):
            return
        # Defining Canvases
        front_canvas = QtGui.QPixmap(self.width(), self.height())
        front_canvas.fill(QtGui.QColor("transparent"))
        back_canvas = QtGui.QPixmap(self.width(), self.height())
        back_canvas.fill(QtGui.QColor("transparent"))
        self.collision_pixmap = QtGui.QPixmap(self.width(), self.height())
        self.collision_pixmap.fill(4280000000)
        rounded = QtGui.QPainter(front_canvas)
        painter = QtGui.QPainter(back_canvas)
        collision = QtGui.QPainter(self.collision_pixmap)
        collision_color = 4280000000

        # Drawing
        pen = QtGui.QPen()
        pen.setWidth(int(5 / self.scale))
        pen.setColor(QtGui.QColor("#585b70"))
        painter.setPen(pen)

        cpen = QtGui.QPen()
        cpen.setWidth(int(5 / self.scale))
        cpen.setColor(QtGui.QColor(collision_color))
        collision.setPen(cpen)

        for i in self.G.edges:
            painter.drawLine(int(self.width() / 2 + (self.G_pos[i[0]][0]) / self.scale + self.offset[0]),
                             int(self.height() / 2 + (self.G_pos[i[0]][1]) / self.scale + self.offset[1]),
                             int(self.width() / 2 + (self.G_pos[i[1]][0]) / self.scale + self.offset[0]),
                             int(self.height() / 2 + (self.G_pos[i[1]][1]) / self.scale + self.offset[1]))
            collision_color += 1
            self.collision_map[f"{collision_color}"] = i
            cpen.setColor(QtGui.QColor(collision_color))
            collision.setPen(cpen)
            collision.drawLine(int(self.width() / 2 + (self.G_pos[i[0]][0]) / self.scale + self.offset[0]),
                               int(self.height() / 2 + (self.G_pos[i[0]][1]) / self.scale + self.offset[1]),
                               int(self.width() / 2 + (self.G_pos[i[1]][0]) / self.scale + self.offset[0]),
                               int(self.height() / 2 + (self.G_pos[i[1]][1]) / self.scale + self.offset[1]))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#45475a"), Qt.BrushStyle.SolidPattern))

        collision.setPen(Qt.PenStyle.NoPen)

        for i in self.G_pos:
            painter.drawEllipse(int(self.width() / 2 + (self.G_pos[i][0] - 25) / self.scale + self.offset[0]),
                                int(self.height() / 2 + (self.G_pos[i][1] - 25) / self.scale + self.offset[1]),
                                int(50 / self.scale), int(50 / self.scale))
            if "pixmap" in self.G.nodes[i]:
                painter.drawPixmap(int(self.width() / 2 + (self.G_pos[i][0] - 25) / self.scale + self.offset[0]),
                                   int(self.height() / 2 + (self.G_pos[i][1] - 25) / self.scale + self.offset[1]),
                                   int(50 / self.scale), int(50 / self.scale),
                                   self.G.nodes[i]["pixmap"])
            collision_color += 1
            self.collision_map[f"{collision_color}"] = i
            collision.setBrush(QtGui.QBrush(QtGui.QColor(collision_color), Qt.BrushStyle.SolidPattern))
            collision.drawEllipse(int(self.width() / 2 + (self.G_pos[i][0] - 25) / self.scale + self.offset[0]),
                                  int(self.height() / 2 + (self.G_pos[i][1] - 25) / self.scale + self.offset[1]),
                                  int(50 / self.scale), int(50 / self.scale))

        # Finishing up
        painter.end()
        brush = QtGui.QBrush(back_canvas)
        rounded.setBrush(brush)
        rounded.setPen(Qt.PenStyle.NoPen)
        rounded.drawRoundedRect(0, 0, self.width(), self.height(), 16, 16)
        rounded.end()
        self.setPixmap(front_canvas)

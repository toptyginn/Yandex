import sys
import io

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic.properties import QtGui

ui = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>2560</width>
    <height>1440</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget"/>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>2560</width>
     <height>21</height>
    </rect>
   </property>
   <widget class="QMenu" name="menu">
    <property name="title">
     <string>Инструменты</string>
    </property>
    <widget class="QMenu" name="fill">
     <property name="title">
      <string>Цвет</string>
     </property>
     <addaction name="red"/>
     <addaction name="orange"/>
     <addaction name="yellow"/>
     <addaction name="green"/>
     <addaction name="cyan"/>
     <addaction name="blue"/>
     <addaction name="violet"/>
     <addaction name="white"/>
     <addaction name="black"/>
    </widget>
    <addaction name="brush_act"/>
    <addaction name="line_act"/>
    <addaction name="round_act"/>
    <addaction name="fill"/>
    <addaction name="del_act"/>
    <addaction name="rect_act_2"/>
    <addaction name="separator"/>
    <addaction name="save"/>
    <addaction name="download"/>
   </widget>
   <addaction name="menu"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <widget class="QToolBar" name="toolBar">
   <property name="windowTitle">
    <string>toolBar</string>
   </property>
   <attribute name="toolBarArea">
    <enum>TopToolBarArea</enum>
   </attribute>
   <attribute name="toolBarBreak">
    <bool>false</bool>
   </attribute>
   <addaction name="brush_act"/>
   <addaction name="line_act"/>
   <addaction name="round_act"/>
   <addaction name="del_act"/>
   <addaction name="rect_act_2"/>
   <addaction name="save"/>
   <addaction name="download"/>
  </widget>
  <action name="brush_act">
   <property name="text">
    <string>Кисть</string>
   </property>
  </action>
  <action name="line_act">
   <property name="text">
    <string>Линия</string>
   </property>
  </action>
  <action name="round_act">
   <property name="text">
    <string>Окружность</string>
   </property>
  </action>
  <action name="del_act">
   <property name="text">
    <string>Ластик</string>
   </property>
  </action>
  <action name="rect_act_2">
   <property name="text">
    <string>Прямоугольник</string>
   </property>
  </action>
  <action name="red">
   <property name="text">
    <string>Красный</string>
   </property>
  </action>
  <action name="orange">
   <property name="text">
    <string>Оранжевый</string>
   </property>
  </action>
  <action name="yellow">
   <property name="text">
    <string>Жёлтый</string>
   </property>
  </action>
  <action name="green">
   <property name="text">
    <string>Зелёный</string>
   </property>
  </action>
  <action name="cyan">
   <property name="text">
    <string>Голубой</string>
   </property>
  </action>
  <action name="blue">
   <property name="text">
    <string>Синий</string>
   </property>
  </action>
  <action name="violet">
   <property name="text">
    <string>Фиолетовый</string>
   </property>
  </action>
  <action name="white">
   <property name="text">
    <string>Белый</string>
   </property>
  </action>
  <action name="black">
   <property name="text">
    <string>Чёрный</string>
   </property>
  </action>
  <action name="action">
   <property name="text">
    <string>Сохранить</string>
   </property>
  </action>
  <action name="save">
   <property name="text">
    <string>Сохранить и выйти</string>
   </property>
  </action>
  <action name="download">
   <property name="text">
    <string>Загрузить</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class BrushPoint:
    def __init__(self, x, y, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.x = x
        self.y = y

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(self.r, self.g, self.b)))
        painter.setPen(QPen(QColor(self.r, self.g, self.b), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawEllipse(self.x - 5, self.y - 5, 10, 10)


class Line:
    def __init__(self, cx, cy, x, y, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(self.r, self.g, self.b)))
        painter.setPen(QPen(QColor(self.r, self.g, self.b), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.cx, self.cy, self.x, self.y)


class Circle:
    def __init__(self, cx, cy, x, y, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(self.r, self.g, self.b)))
        painter.setPen(QPen(QColor(0, 0, 0), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        radius = int(((self.cx - self.x) ** 2 + (self.cy - self.y) ** 2) ** 0.5)
        painter.drawEllipse(self.cx - radius, self.cy - radius, 2 * radius, 2 * radius)


class Rectangle:
    def __init__(self, cx, cy, x, y, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(self.r, self.g, self.b)))
        painter.setPen(QPen(QColor(0, 0, 0), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawRect(self.cx, self.cy, self.x, self.y)


class Canvas(QWidget):
    def __init__(self, SizeOfMainWindow):
        super(Canvas, self).__init__()
        self.Size = SizeOfMainWindow
        self.objects = []
        self.instrument = 'brush'
        self.color = [0, 0, 0]
        self.image = QImage(self.Size, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def paintEvent(self, event, **kwargs):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())
        painter_image = QPainter(self.image)
        painter.begin(self)
        for obj in self.objects:
            obj.draw(painter_image)
        painter.end()

    def mousePressEvent(self, event, **kwargs):
        if self.instrument == 'brush':
            self.objects.append(BrushPoint(event.x(), event.y(), self.color[0], self.color[1], self.color[2]))
        elif self.instrument == 'line':
            self.objects.append((Line(event.x(), event.y(), event.x(), event.y(), self.color[0], self.color[1],
                                      self.color[2])))
        elif self.instrument == 'rect':
            self.objects.append((Rectangle(event.x(), event.y(), event.x(), event.y(), self.color[0], self.color[1],
                                           self.color[2])))
        elif self.instrument == 'circle':
            self.objects.append((Circle(event.x(), event.y(), event.x(), event.y(), self.color[0], self.color[1],
                                        self.color[2])))
        elif self.instrument == 'clean':
            self.objects.append(BrushPoint(event.x(), event.y(), 255, 255, 255))

        self.update()

    def mouseMoveEvent(self, event, **kwargs):
        if self.instrument == 'brush':
            self.objects.append(BrushPoint(event.x(), event.y(), self.color[0], self.color[1], self.color[2]))
            self.update()
        elif self.instrument == 'line':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        elif self.instrument == 'rect':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        elif self.instrument == 'circle':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        if self.instrument == 'clean':
            self.objects.append(BrushPoint(event.x(), event.y(), 255, 255, 255))
            self.update()

    def setBrush(self):
        self.instrument = 'brush'

    def setLine(self):
        self.instrument = 'line'

    def setCircle(self):
        self.instrument = 'circle'

    def setRect(self):
        self.instrument = 'rect'

    def setClean(self):
        self.instrument = 'clean'

    # Каждый охотник желает знать, где сидит фазан)

    def setRed(self):
        self.color = [255, 0, 0]

    def setOrange(self):
        self.color = [255, 69, 0]

    def setYellow(self):
        self.color = [255, 255, 0]

    def setGreen(self):
        self.color = [0, 255, 0]

    def setCyan(self):
        self.color = [0, 255, 255]

    def setBlue(self):
        self.color = [0, 0, 255]

    def setViolet(self):
        self.color = [128, 0, 128]

    def setBlack(self):
        self.color = [0, 0, 0]

    def setWhite(self):
        self.color = [255, 255, 255]

    def save(self):

        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        # if file path is blank return back
        if filePath == "":
            return

        # saving canvas at desired path
        self.image.save(filePath)

    def download(self):
        filename = QFileDialog.getOpenFileName(self, 'Download Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg)")[0]

        if filename == "":
            return

        self.image = QImage(filename)


class Paint(QMainWindow):
    def __init__(self):
        super(Paint, self).__init__()
        x = io.StringIO(ui)
        uic.loadUi(x, self)
        self.setCentralWidget(Canvas(self.size()))

        self.brush_act.triggered.connect(self.centralWidget().setBrush)
        self.line_act.triggered.connect(self.centralWidget().setLine)
        self.round_act.triggered.connect(self.centralWidget().setCircle)
        self.rect_act_2.triggered.connect(self.centralWidget().setRect)
        self.del_act.triggered.connect(self.centralWidget().setClean)
        #Colors
        self.red.triggered.connect(self.centralWidget().setRed)
        self.orange.triggered.connect(self.centralWidget().setOrange)
        self.yellow.triggered.connect(self.centralWidget().setYellow)
        self.green.triggered.connect(self.centralWidget().setGreen)
        self.cyan.triggered.connect(self.centralWidget().setCyan)
        self.blue.triggered.connect(self.centralWidget().setBlue)
        self.violet.triggered.connect(self.centralWidget().setViolet)
        self.black.triggered.connect(self.centralWidget().setBlack)
        self.white.triggered.connect(self.centralWidget().setWhite)
        #File
        self.save.triggered.connect(self.centralWidget().save)
        self.download.triggered.connect(self.centralWidget().download)

    def closeEvent(self, event, **kwargs):
        quit_msg = "Сохранить изменения?"
        reply = QMessageBox.question(self, 'Message',
                                           quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.centralWidget().save()
        else:
            event.ignore()
            sys.exit(QApplication(sys.argv).exec())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Paint()
    ex.show()
    sys.exit(app.exec())

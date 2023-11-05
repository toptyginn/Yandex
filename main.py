import io

from PyQt5 import uic

import Photoshop
import Paint
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

ui = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>544</width>
    <height>374</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="horizontalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>60</x>
      <y>40</y>
      <width>391</width>
      <height>211</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="horizontalLayout">
     <item>
      <widget class="QPushButton" name="Change_btn">
       <property name="text">
        <string>Редактировать изображение</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="Create_btn">
       <property name="text">
        <string>Рисовать</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>544</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        x = io.StringIO(ui)
        uic.loadUi(x, self)
        self.Change_btn.clicked.connect(self.setPhotoshop)
        self.Create_btn.clicked.connect(self.setPaint)
        self.dialogs = list()

    def setPhotoshop(self):
        dialog = Photoshop.Photoshop()
        self.dialogs.append(dialog)
        dialog.show()

    def setPaint(self):
        dialog = Paint.Paint()
        self.dialogs.append(dialog)
        dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
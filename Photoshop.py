import io
import sys

from PIL import Image
from PyQt5 import uic
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QImage, QColor, QTransform, qGray, qRgb
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox

ui = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1944</width>
    <height>764</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="horizontalLayoutWidget_3">
    <property name="geometry">
     <rect>
      <x>110</x>
      <y>30</y>
      <width>549</width>
      <height>156</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="horizontalLayout_3">
     <item>
      <widget class="QPushButton" name="red">
       <property name="text">
        <string>R</string>
       </property>
       <attribute name="buttonGroup">
        <string notr="true">channelButtons</string>
       </attribute>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="green">
       <property name="text">
        <string>G</string>
       </property>
       <attribute name="buttonGroup">
        <string notr="true">channelButtons</string>
       </attribute>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="blue">
       <property name="text">
        <string>B</string>
       </property>
       <attribute name="buttonGroup">
        <string notr="true">channelButtons</string>
       </attribute>
      </widget>
     </item>
     <item>
      <widget class="QSlider" name="bright_change">
       <property name="orientation">
        <enum>Qt::Horizontal</enum>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="All">
       <property name="text">
        <string>All</string>
       </property>
       <attribute name="buttonGroup">
        <string notr="true">channelButtons</string>
       </attribute>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="AllGray">
       <property name="text">
        <string>All-Gray</string>
       </property>
       <attribute name="buttonGroup">
        <string notr="true">channelButtons</string>
       </attribute>
      </widget>
     </item>
    </layout>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget_2">
    <property name="geometry">
     <rect>
      <x>110</x>
      <y>560</y>
      <width>549</width>
      <height>121</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="horizontalLayout_2">
     <item>
      <widget class="QPushButton" name="counterclockwise">
       <property name="text">
        <string>Против часовой стрелки</string>
       </property>
       <attribute name="buttonGroup">
        <string notr="true">rotateButtons</string>
       </attribute>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="clockwise">
       <property name="text">
        <string>По часовой стрелке</string>
       </property>
       <attribute name="buttonGroup">
        <string notr="true">rotateButtons</string>
       </attribute>
      </widget>
     </item>
    </layout>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>110</x>
      <y>180</y>
      <width>549</width>
      <height>381</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="horizontalLayout">
     <item>
      <widget class="QLabel" name="image">
       <property name="text">
        <string>TextLabel</string>
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
     <width>1944</width>
     <height>21</height>
    </rect>
   </property>
   <widget class="QMenu" name="menu">
    <property name="title">
     <string>Файл</string>
    </property>
    <addaction name="save"/>
   </widget>
   <addaction name="menu"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <action name="save">
   <property name="text">
    <string>Сохранить</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
 <buttongroups>
  <buttongroup name="rotateButtons"/>
  <buttongroup name="channelButtons"/>
 </buttongroups>
</ui>
'''


class Photoshop(QMainWindow):
    def __init__(self):
        super(Photoshop, self).__init__()

        f = io.StringIO(ui)
        uic.loadUi(f, self)

        self.filename = \
            QFileDialog.getOpenFileName(self,
                                        'Выберите картинку',
                                        '',
                                        'Картинки (*.jpg)')[0]
        self.bright = 0
        self.bright_change.setMinimum(-100)
        self.bright_change.setMaximum(100)
        self.bright_change.setValue(0)

        self.bright_change.setSingleStep(1)
        self.bright_change.valueChanged.connect(self.set_bright2)
        self.degree = 0
        self.new_img = 'new.png'
        self.save.triggered.connect(self.saving)
        self.setWindowTitle('Редактор изображений')

        self.orig_image = QImage(self.filename)
        self.curr_image = self.orig_image.copy()
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.image.setPixmap(self.pixmap)
        for button in self.channelButtons.buttons():
            button.clicked.connect(self.set_channel)
        for button in self.rotateButtons.buttons():
            button.clicked.connect(self.rotate)

    def set_channel(self):
        self.curr_image = self.orig_image.copy()
        x, y = self.curr_image.size().width(), self.curr_image.size().height()

        for i in range(x):
            for j in range(y):
                r, g, b, _ = self.curr_image.pixelColor(i, j).getRgb()
                if self.sender().text() == 'R':
                    self.curr_image.setPixelColor(QPoint(i, j),
                                                  QColor(r, 0, 0))
                elif self.sender().text() == 'G':
                    self.curr_image.setPixelColor(QPoint(i, j),
                                                  QColor(0, g, 0))
                elif self.sender().text() == 'B':
                    self.curr_image.setPixelColor(QPoint(i, j),
                                                  QColor(0, 0, b))
                elif self.sender().text() == 'All-Gray':
                    gray = qGray(r, g, b)
                    self.curr_image.setPixelColor(QPoint(i, j), QColor(gray, gray, gray))
                #t = QTransform().rotate(self.degree)
                #self.curr_image = self.curr_image.transformed(t)
                self.pixmap = QPixmap.fromImage(self.curr_image)
                self.image.setPixmap(self.pixmap)

    def rotate(self):

        if self.sender() is self.clockwise:
            self.degree += 90
            degree = 90
        else:
            self.degree -= 90
            degree = -90
        self.degree %= 360

        t = QTransform().rotate(degree)
        self.curr_image = self.curr_image.transformed(t)

        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.image.setPixmap(self.pixmap)

    def set_bright(self):
        transp = int(self.bright_change.value())
        self.curr_image.save(self.new_img)
        img = Image.open(self.new_img)
        img.putalpha(transp)
        img.save(self.new_img)
        new_image = QImage(self.new_img)

        t = QTransform().rotate(self.degree)
        new_image = new_image.transformed(t)
        self.pixmap = QPixmap.fromImage(new_image)
        self.image.setPixmap(self.pixmap)

    def set_bright2(self):
        brightness = int(self.bright_change.value()) * 0.01
        self.curr_image = self.orig_image.copy()
        x, y = self.curr_image.size().width(), self.curr_image.size().height()

        for i in range(x):
            for j in range(y):
                r, g, b, _ = self.curr_image.pixelColor(i, j).getRgb()
                h, s, l, a = self.curr_image.pixelColor(i, j).getHslF()
                # r = r + brightness if 255 > r + brightness > 0 else r
                # g = g + brightness if 255 > g + brightness > 0 else g
                # b = b + brightness if 255 > b + brightness > 0 else b

                # self.curr_image.setPixelColor(QPoint(i, j),
                #                               QColor(r, g, b))
                self.curr_image.setPixelColor(QPoint(i, j),
                                              QColor(QColor(r, g, b).setHslF(h, s, l + brightness, a)))
                #t = QTransform().rotate(self.degree)
                #self.curr_image = self.curr_image.transformed(t)
                self.pixmap = QPixmap.fromImage(self.curr_image)
                self.image.setPixmap(self.pixmap)

    def saving(self):
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        # if file path is blank return back
        if filePath == "":
            return

        # saving canvas at desired path
        self.curr_image.save(filePath)

    def closeEvent(self, event, **kwargs):
        quit_msg = "Сохранить изменения?"
        reply = QMessageBox.question(self, 'Message',
                                           quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.saving()
        else:
            event.ignore()
            sys.exit(QApplication(sys.argv).exec())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Photoshop()
    ex.show()
    sys.exit(app.exec())

from PySide2 import QtGui
from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QDial, QSlider, QLabel, QLineEdit, QGraphicsScene
from PySide2.QtCore import Qt, QRect
import sys

class Slider(QSlider):
    def __init__(self, minimum, maximum):
        super().__init__()
        self.slider = QSlider()
        self.label = QLabel("0")
        self.label.setFont(QtGui.QFont("Sanserif", 15))
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Turntable")
        self.top = 200
        self.left = 500
        self.width = 500
        self.height = 150
        self.setGeometry(self.left, self.top, self.width, self.height)
                
        self.textEdit = QLineEdit()
        self.nameLabel = QLabel()
        self.textEdit.setObjectName("textEdit")
        self.textEdit.resize(10,10)
        self.h_slider = Slider(1, 100)
        self.h_slider.resize(20,10)
        self.v_slider = Slider(1, 100)
        self.nameLabel.setText('Angles')
        self.h_slider.label.setText('Horizontal')
        self.v_slider.label.setText('Vertical')
        self.last_h = 0
        self.last_v = 0
        self.get_orientation()

        #self.dial = QDial()
        #self.dial.setMinimum(0)
        #self.dial.setMaximum(360)
        #self.dial.setValue(40)
        #self.dial.valueChanged.connect(self.slider_moved)


        hbox = QHBoxLayout()
        self.h_slider.valueChanged.connect(self.changed_value_h)
        self.v_slider.valueChanged.connect(self.changed_value_v)
        # self.v_slider.valueChanged.connect(self.changed_value(self.v_slider))
        hbox.addWidget(self.nameLabel)
        hbox.addWidget(self.textEdit)
        hbox.addWidget(self.h_slider.label)
        hbox.addWidget(self.h_slider)
        hbox.addWidget(self.v_slider.label)
        hbox.addWidget(self.v_slider)
        self.setLayout(hbox)
        self.show()

    def get_orientation(self):
        self.v_slider.label.setAlignment(Qt.AlignRight)
        self.h_slider.label.setAlignment(Qt.AlignCenter)
        self.v_slider.setOrientation(Qt.Vertical)
        self.h_slider.setOrientation(Qt.Horizontal)

    def changed_value_h(self):
        self.h_slider.label.setText(str(self.h_slider.value()))

    def changed_value_v(self):
        self.v_slider.label.setText(str(self.v_slider.value()))
        return self.v_slider.value()


    def slider_moved(self):
        print("Dial value = %i" % (self.dial.value()))
        
    def GetActiveCamera():
        perspPanel = cmds.getPanel( withLabel='Persp View')
        
        #Get the active camera in the panel
        ActiveCamera = cmds.modelPanel( perspPanel, query = True, camera = Trßue)
        return ActiveCamera
    
    def create_camera(self):
        cmds.duplicate( GetActiveCamera(), name = 'CAM2')
        try:cmds.delete("|CMForegroundPlane")
        except:pass
        try:cmds.delete("|CMBackgroundPlane")
        except:pass
        i = 0
        while(cmds.objExists("shot_" + str(i))):
            try:cmds.delete("|" + "shot_" + str(i) + "_ImagePlane")
            except:pass
            i = i + 1

        cmds.camera('CAM2', edit = True, startupCamera = False, displayResolution = True)


        #Make the camera hidden
        #cmds.setAttr('CAM2'+".visibility", False)

        #Add the attributes to define range and renderability
        cmds.select('CAM2')
    
    def change_camera_h(self):
        cameras = cmds.ls(type=('camera'), l=True) or []
        p = cmds.camera(cameras[0], q=True, p=True)  
        val = self.h_slider.value() 
        distance = val - self.last_h
        print(cameras[0], p, distance, p[2]+distance)    
        cmds.move(p[0],p[1],p[2]+distance, cameras[0], absolute=True)
        self.last_h = val
        
    def change_camera_v(self):
        cameras = cmds.ls(type=('camera'), l=True) or []
        p = cmds.camera(cameras[0], q=True, p=True)
        val = self.v_slider.value() 
        distance = val - self.last_v
        print(cameras[0], p, distance, p[1]+distance)    
        cmds.move(p[0],p[1]+distance,p[2], cameras[0], absolute=True)
        self.last_v = val
    
    #def setKeyFrames(self):
     #   val = self.textEdit.value() 
      #  angle = 360/val
       # noKeys = 180/angle
        
hello = Window()
hello.show()


nonStartup = [c for c in cmds.ls(cameras=True) if not cmds.camera(c, q=True, startupCamera=True)]

if not nonStartup:
    hello.create_camera()

    
hello.h_slider.valueChanged.connect(hello.change_camera_h)
hello.v_slider.valueChanged.connect(hello.change_camera_v)
#hello.textEdit.valueChanged.connect(hello.setKeyFrames)


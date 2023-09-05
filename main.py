from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import requests
import sys

BED_TEMPERATURE = 180
CHAMBER_TEMPERATURE = 180
VOLUME_TEMPERATURE = 180
STEP_SIZE = 10


class GUI(QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi("untitled.ui", self)
        # self.label_4.setStyleSheet("background-image: url('C:\\Users\\NetFabb\PycharmProjects\purple_laser.jpg'); background-repeat: no-repeat;")
        pixmap = QPixmap('purple_laser.jpg')

        # API
        self.api_endpoint = "http://10.114.56.121"
        self.params = {"apikey": 'B508534ED20348F090B4D0AD637D3660'}

        self.label_4.setPixmap(pixmap)
        self.label_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.show()

        self.pushButton.clicked.connect(self.login)

    def switch_screen(self, index):
        if index < self.MainWindow.stackedWidget.count():
            screen = self.MainWindow.stackedWidget.widget(index)
            self.MainWindow.stackedWidget.setCurrentWidget(screen)

    def login(self):
        if self.lineEdit.text() == "Associate" and self.lineEdit_2.text() == "tomandjerry":
            print("Successful login")
            self.close()
            self.MainWindow = uic.loadUi("mainwindow.ui")
            self.MainWindow.pushButton_4.clicked.connect(lambda: self.switch_screen(0))
            self.MainWindow.pushButton_5.clicked.connect(lambda: self.switch_screen(1))
            self.MainWindow.pushButton_6.clicked.connect(lambda: self.switch_screen(2))
            self.MainWindow.pushButton_10.clicked.connect(lambda: self.switch_screen(3))


        #PARAMETERS
            self.BedTempFlag = False
            self.VolumeTempFlag = False
            self.ChamberTempFlag = False

        #HOPPER
            self.MainWindow.Hopper_in_manual.clicked.connect(lambda: self.move_hopper_up())
            self.MainWindow.Hopper_out_manual.clicked.connect(lambda: self.move_hopper_down())
            self.MainWindow.Hopper_home_manual.clicked.connect(lambda: self.move_hopper_home())

        #Z-AXIS
            self.slider_value = 0
            #LOADING MOTOR
            self.MainWindow.ZmotorOk.clicked.connect(lambda: self.moveLoadingMotor(True))
            self.MainWindow.ZmotorUp.clicked.connect(lambda: self.moveLoadingMotor(False,"up"))
            self.MainWindow.ZmotorDown.clicked.connect(lambda: self.moveLoadingMotor(False, "down"))
            self.MainWindow.ZmotorHome.clicked.connect(lambda: self.moveLoadingMotor(False, "home"))
            self.MainWindow.ZmotorZero.clicked.connect(lambda: self.moveLoadingMotor(False, "zero"))

            #Z-AXIS MOTOR
            self.MainWindow.ZaxisOk.clicked.connect(lambda: self.moveZaxis(True))
            self.MainWindow.ZaxisStepUp.clicked.connect(lambda: self.moveZaxis(False,"up"))
            self.MainWindow.ZaxisStepDown.clicked.connect(lambda: self.moveZaxis(False,"Down"))
            self.MainWindow.ZaxisHome.clicked.connect(lambda: self.moveZaxis(False,"home"))
            self.MainWindow.ZaxisZero.clicked.connect(lambda: self.moveZaxis(False, "zero"))

            #TEMPERATURE
            self.MainWindow.TempControlOk.clicked.connect(lambda:self.update_temperature(False))
            self.MainWindow.BedHeater.clicked.connect(lambda:self.BedHeating(True,None))
            self.MainWindow.VolumeHeater.clicked.connect(lambda: self.VolumeHeating(True))
            self.MainWindow.ChamberHeater.clicked.connect(lambda: self.ChamberHeating(True))

            #CLOSE
            self.MainWindow.actionclose.triggered.connect(self.MainWindow.close)





            self.MainWindow.showFullScreen()
            #self.setWindowFlag(self.windowFlags() | Qt.FramelessWindowHint)
            self.MainWindow.show()

        else:
            message = QMessageBox()
            message.setText("Invalid Login")
            message.exec_()


    def moveLoadingMotor(self,auto,direction=""):
        print("papi")
        current_pos = self.MainWindow.ZmotorPos.text()
        speed = self.MainWindow.ZmotorSpeed.text()
        moveTo = self.MainWindow.ZmotorTo.text()
        ZmStepUp = self.MainWindow.ZmotorUpStepSize.text()
        ZmStepDown = self.MainWindow.ZmotorDownStepSize.text()
        print("Si")

        if ZmStepUp == "":
            ZmStepUp = STEP_SIZE

        if ZmStepDown == "":
            ZmStepDown = STEP_SIZE

        if direction == "home":
            print("Moving to home loading")
            self.slider_value = 0
            cmd = {
                "command": "home",
                "axes":["x","y"]
            }

            request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead",params=self.params,json=cmd)
            print("Home API Status:")
            request.raise_for_status()

        elif direction == "zero":
            print("Moving to 0 loading")
            self.slider_value = 100

        elif direction == 'up':
            self.slider_value = self.slider_value + int(ZmStepUp)

        elif direction == 'down':
            self.slider_value = self.slider_value - int(ZmStepDown)

        print("outside if branch")

        self.MainWindow.ZSlider.setValue(self.slider_value)




    def moveZaxis(self,auto,direction=""):
        current_pos = self.MainWindow.ZmotorPos.text()
        speed = self.MainWindow.ZmotorSpeed.text()
        moveTo = self.MainWindow.ZmotorTo.text()
        ZaxisStepUp = self.MainWindow.ZmotorUpStepSize.text()
        ZaxisStepDown = self.MainWindow.ZmotorDownStepSize.text()
        pass

    def update_temperature(self):
        print(self.MainWindow.BedTempIn.text(), self.MainWindow.VolumeTempIn.text(), self.MainWindow.ChamberTempIn.text())
        bedtemp = int(self.MainWindow.BedTempIn.text())
        voltemp = int(self.MainWindow.VolumeTempIn.text())
        chambertemp = int(self.MainWindow.ChamberTempIn.text())
        self.currentBedTemp = ''
        self.currentVolTemp = ''
        self.currentChamTemp = ''

        if bedtemp == "":
            bedtemp = self.currentBedTemp
        if voltemp == "":
            voltemp = self.currentVolTemp
        if chambertemp == "":
            chambertemp = self.currentChamTemp

        print("calling sub functions")

        self.BedHeating(False,bedtemp)
        self.VolumeHeating(False,voltemp)
        self.ChamberHeating(False,chambertemp)



    def BedHeating(self,direct,bedtemp):
        if direct:
            print('inside direct')
            if not self.BedTempFlag:
                print('inside second if')
                self.BedTempFlag = True
                self.MainWindow.BedHeater.setStyleSheet("background-color: green")

                cmd = {
                    "command": "target",
                    "target": 75
                }
                request = requests.post(url=f"http://{self.api_endpoint}/api/printer/bed", params=self.params, json=cmd)
                print("Bed Heating API Status:")
                request.raise_for_status()

            else:
                self.BedTempFlag = False
                self.MainWindow.BedHeater.setStyleSheet("background-color:rgb(160,0,50);")

        else:
            if self.currentBedTemp < bedtemp:
                pass



        bed_header = {
            'Authorization': f"Bearer {self.api_key}",
            'command': 'target',
            'target': bedtemp
        }


    def VolumeHeating(self,voltemp):

        if not self.VolumeTempFlag:
            self.VolumeTempFlag = True

        else:
            self.VolumeTempFlag = False


        vol_header = {
            'Authorization': f"Bearer {self.api_key}",
            'command': 'target',
            'target': voltemp
        }
        pass

    def ChamberHeating(self,chambertemp):

        if not self.ChamberTempFlag:
            self.ChamberTempFlag = True

        else:
            self.ChamberTempFlag = False

        chamber_header = {
            'Authorization': f"Bearer {self.api_key}",
            'command': 'target',
            'target': chambertemp
        }
        pass

    def update_parameters(self):
        #BED TEMPERATURE
        get_bed_data = requests.get(url=f"http://{self.api_endpoint}/api/printer/bed",params=self.params)
        print("Get BED API Status:")
        get_bed_data.raise_for_status()

        #CHAMBER TEMPERATURE
        get_chamber_data = requests.get(url=f"http://{self.api_endpoint}/api/printer/bed", params=self.params)
        print("Get CHAMBER API Status:")
        get_chamber_data.raise_for_status()



    def move_hopper_in(self):
        headers = {
            'Authorization': f"Bearer {self.api_key}",
            'command': 'M106'
            ''
        }

    def move_hopper_out(self):
        pass

    def move_hopper_home(self):
        pass


def main():
    app = QApplication([])
    window = GUI()
    app.exec_()


if __name__ == '__main__':
    main()

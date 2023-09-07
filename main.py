from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import requests
import sys

BED_TEMPERATURE = 180
CHAMBER_TEMPERATURE = 180
VOLUME_TEMPERATURE = 180
STEP_SIZE = 10
DIRECTION = "forward"      #Roller Default Direction
ROLLER_RPM = 10            #Roller Default RPM


class GUI(QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi("untitled.ui", self)
        # self.label_4.setStyleSheet("background-image: url('C:\\Users\\NetFabb\PycharmProjects\purple_laser.jpg'); background-repeat: no-repeat;")
        pixmap = QPixmap('purple_laser.jpg')

        # API
        self.api_endpoint = "10.114.56.128"
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
        if True:   #self.lineEdit.text() == "Associate" and self.lineEdit_2.text() == "tomandjerry":
            print("Successful login")
            self.close()
            self.MainWindow = uic.loadUi("mainwindow.ui")
            self.MainWindow.pushButton_4.clicked.connect(lambda: self.switch_screen(0))
            self.MainWindow.pushButton_5.clicked.connect(lambda: self.switch_screen(1))
            self.MainWindow.pushButton_6.clicked.connect(lambda: self.switch_screen(2))
            self.MainWindow.pushButton_10.clicked.connect(lambda: self.switch_screen(3))

            # PARAMETERS
            self.BedTempFlag = False
            self.VolumeTempFlag = False
            self.ChamberTempFlag = False
            self.currentBedTemp = None
            self.currentChamTemp = None
            self.currentVolTemp = None

            #LEFT HOPPER
            self.MainWindow.LHopperMove.clicked.connect(lambda: self.move_Lhopper())
            self.MainWindow.LHopperMUp.clicked.connect(lambda: self.move_Lhopper("Up"))
            self.MainWindow.LHopperMDown.clicked.connect(lambda: self.move_Lhopper("Down"))
            self.MainWindow.LHopperHome.clicked.connect(lambda: self.move_Lhopper("Home"))
            self.MainWindow.LHopperHeater.clicked.connect(lambda: self.hopperTemperatureControl())

            #RIGHT HOPPER
            self.MainWindow.RHopperMove.clicked.connect(lambda: self.move_Rhopper())
            self.MainWindow.RHopperMUp.clicked.connect(lambda: self.move_Rhopper("Up"))
            self.MainWindow.RHopperMDown.clicked.connect(lambda: self.move_Rhopper("Down"))
            self.MainWindow.RHopperHome.clicked.connect(lambda: self.move_Rhopper("Home"))
            self.MainWindow.RHopperHeater.clicked.connect(lambda: self.hopperTemperatureControl())


            # Z-AXIS
            self.slider_value = 0
            # LOADING MOTOR
            self.MainWindow.ZmotorOk.clicked.connect(lambda: self.moveLoadingMotor(True))
            self.MainWindow.ZmotorUp.clicked.connect(lambda: self.moveLoadingMotor(False, "up"))
            self.MainWindow.ZmotorDown.clicked.connect(lambda: self.moveLoadingMotor(False, "down"))
            self.MainWindow.ZmotorHome.clicked.connect(lambda: self.moveLoadingMotor(False, "home"))
            self.MainWindow.ZmotorZero.clicked.connect(lambda: self.moveLoadingMotor(False, "zero"))

            # Z-AXIS MOTOR
            self.MainWindow.ZaxisOk.clicked.connect(lambda: self.moveZaxis(True))
            self.MainWindow.ZaxisStepUp.clicked.connect(lambda: self.moveZaxis(False, "up"))
            self.MainWindow.ZaxisStepDown.clicked.connect(lambda: self.moveZaxis(False, "Down"))
            self.MainWindow.ZaxisHome.clicked.connect(lambda: self.moveZaxis(False, "home"))
            self.MainWindow.ZaxisZero.clicked.connect(lambda: self.moveZaxis(False, "zero"))

            # TEMPERATURE
            self.MainWindow.TempControlOk.clicked.connect(lambda: self.update_temperature())
            self.MainWindow.BedHeater.clicked.connect(lambda: self.BedHeating(True))
            self.MainWindow.VolumeHeater.clicked.connect(lambda: self.VolumeHeating(True))
            self.MainWindow.ChamberHeater.clicked.connect(lambda: self.ChamberHeating(True))


            #ROLLER
            self.MainWindow.RollerStart.clicked.connect(lambda: self.Roller())
            self.MainWindow.RollerInstantStop.clicked.connect(lambda: self.Roller())
            self.MainWindow.RollerStop.clicked.connect(lambda: self.Roller())


            # CLOSE
            self.MainWindow.actionclose.triggered.connect(self.MainWindow.close)

            self.MainWindow.showFullScreen()
            # self.setWindowFlag(self.windowFlags() | Qt.FramelessWindowHint)
            self.MainWindow.show()

        else:
            message = QMessageBox()
            message.setText("Invalid Login")
            message.exec_()

    def moveLoadingMotor(self, auto, direction=''):
        self.update_parameters()

        if not auto:
            try:
                ZmStepUp = self.MainWindow.ZmotorUpStepSize.text()
                ZmStepDown = self.MainWindow.ZmotorDownStepSize.text()

                if ZmStepUp == "":
                    ZmStepUp = STEP_SIZE

                if ZmStepDown == "":
                    ZmStepDown = STEP_SIZE

                if direction == "home":
                    print("Moving to home loading")
                    self.slider_value = 0
                    cmd = {
                        "command": "home",
                        "axes": ["x", "y"]
                    }

                    # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead", params=self.params,
                    #                         json=cmd)
                    # print("Home API Status:")
                    # request.raise_for_status()

                elif direction == "zero":
                    print("Moving to 0 loading")
                    self.slider_value = 100
                    cmd = {
                        "command": "",
                    }

                    # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead", params=self.params,
                    #                         json=cmd)
                    # print("Zero API Status:")
                    # request.raise_for_status()

                elif direction == 'up':
                    self.slider_value = self.slider_value + int(ZmStepUp)
                    cmd = {
                        "command": "",
                    }

                    # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead", params=self.params,
                    #                         json=cmd)
                    # print("Up movement API Status:")
                    # request.raise_for_status()

                elif direction == 'down':
                    self.slider_value = self.slider_value - int(ZmStepDown)
                    cmd = {
                        "command": "",
                    }

                    # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead", params=self.params,
                    #                         json=cmd)
                    # print("Down movement API Status:")
                    # request.raise_for_status()

                self.MainWindow.ZSlider.setValue(self.slider_value)

            except:
                pass

        else:
            try:
                self.speed = self.MainWindow.ZmotorSpeed.text()
                self.moveTo = self.MainWindow.ZmotorTo.text()
                self.stepsize = self.MainWindow.Zstep.text()

                cmd = {
                    "command": ""
                }

                # request = requests.post(url='', params=self.params, json=cmd)
                # request.raise_for_status()
            except:
                pass

        self.update_parameters()

    def moveZaxis(self, auto, direction=""):
        self.update_parameters()

        if not auto:
            try:
                ZaxisStepUp = self.MainWindow.ZaxisUpStepSize.text()
                ZaxisStepDown = self.MainWindow.ZaxisDownStepSize.text()

                if ZaxisStepUp == "":
                    ZaxisStepUp = STEP_SIZE

                if ZaxisStepDown == "":
                    ZaxisStepDown = STEP_SIZE

                if direction == "home":
                    print("Moving to home axis motor")
                    self.slider_value = 0
                    cmd = {
                        "command": "home",
                        "axes": ["x", "y"]
                    }

                    # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead", params=self.params,
                    #                         json=cmd)
                    # print("Home API Status:")
                    # request.raise_for_status()

                elif direction == "zero":
                    print("Moving to 0 axis motor")
                    self.slider_value = 100
                    cmd = {
                        "command": "",
                    }

                    # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead", params=self.params,
                    #                         json=cmd)
                    # print("Zero API Status:")
                    # request.raise_for_status()


                elif direction == 'up':
                    self.slider_value = self.slider_value + int(ZaxisStepUp)
                    cmd = {
                        "command": "",
                    }

                    # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead", params=self.params,
                    #                         json=cmd)
                    # print("Up movement API Status:")
                    # request.raise_for_status()


                elif direction == 'down':
                    self.slider_value = self.slider_value - int(ZaxisStepDown)
                    cmd = {
                        "command": "",
                    }

                    # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/printhead", params=self.params,
                    #                         json=cmd)
                    # print("Down movement API Status:")
                    # request.raise_for_status()

                self.MainWindow.ZSlider.setValue(self.slider_value)

            except:
                pass

        else:
            try:
                self.speed = self.MainWindow.ZaxisSpeed.text()
                self.moveUp = self.MainWindow.ZaxisUp.text()
                self.moveDown = self.MainWindow.ZaxisDown.text()

                cmd = {
                    "command": ""
                }

                # request = requests.post(url='', params=self.params, json=cmd)
                # request.raise_for_status()
            except:
                pass

        self.update_parameters()

    def update_temperature(self):
        self.update_parameters()
        print(self.MainWindow.BedTempIn.text(), self.MainWindow.VolumeTempIn.text(),
              self.MainWindow.ChamberTempIn.text())
        bedtemp = int(self.MainWindow.BedTempIn.text())
        voltemp = int(self.MainWindow.VolumeTempIn.text())
        chambertemp = int(self.MainWindow.ChamberTempIn.text())

        if bedtemp == "":
            bedtemp = self.currentBedTemp
        if voltemp == "":
            voltemp = self.currentVolTemp
        if chambertemp == "":
            chambertemp = self.currentChamTemp

        print("calling sub functions")

        self.BedHeating(False, bedtemp)
        self.VolumeHeating(False, voltemp)
        self.ChamberHeating(False, chambertemp)

    def BedHeating(self, direct, bedtemp=""):
        self.update_parameters()
        print("After update parameters")
        if not self.BedTempFlag:
            self.BedTempFlag = True
            self.MainWindow.BedHeater.setStyleSheet("background-color: green")
        else:
            self.BedTempFlag = False
            self.MainWindow.BedHeater.setStyleSheet("background-color:black")  # RED:rgb(160,0,50)


        if direct:
            pass
        else:
            try:
                cmd = {
                    "command": "target",
                    "target": 75
                }
                # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/bed", params=self.params, json=cmd)
                # print("Bed Heating API Status:")
                # request.raise_for_status()
            except:
                pass

    def VolumeHeating(self, direct, voltemp=''):
        self.update_parameters()
        print("after vloume heater update")
        if not self.VolumeTempFlag:
            print("Volume 1")
            self.VolumeTempFlag = True
            self.MainWindow.VolumeHeater.setStyleSheet("background-color: green")

        else:
            self.VolumeTempFlag = False
            self.MainWindow.VolumeHeater.setStyleSheet("background-color: black")

        try:
            if not direct:
                pass

        except:
            pass

    def ChamberHeating(self, direct, chambertemp=''):
        print("inside chamber")
        self.update_parameters()
        if not self.ChamberTempFlag:
            print("chamber 1")
            self.ChamberTempFlag = True
            self.MainWindow.ChamberHeater.setStyleSheet("background-color: green")

        else:
            self.ChamberTempFlag = False
            self.MainWindow.ChamberHeater.setStyleSheet("background-color: black")

        try:
            if not direct:
                cmd = {
                    "command": "target",
                    "target": 75
                }
                # request = requests.post(url=f"http://{self.api_endpoint}/api/printer/chamber", params=self.params,
                #                         json=cmd)
                # print("Chamber Heating API Status:")
                # request.raise_for_status()
        except:
            pass
        self.update_parameters()

    def Roller(self):
        if self.MainWindow.RollerDir.text() == "":
            direction = DIRECTION
        else:
            direction = self.MainWindow.RollerDir.text()

        if self.MainWindow.RollerRpm.text() == "":
            rpm = ROLLER_RPM
        else:
            rpm = self.MainWindow.RollerRpm.text()

    def update_parameters(self):
        pass
        # try:
        #     # BED TEMPERATURE
        #     print(f"bedhttp://{self.api_endpoint}/api/printer/bed")
        #     get_bed_data = requests.get(url=f"http://{self.api_endpoint}/api/printer/bed", params=self.params)
        #     print("Get BED API Status:")
        #     get_bed_data.raise_for_status()
        #     get_bed_data = get_bed_data.json()
        #     print(get_bed_data['bed']['actual'])
        #     self.currentBedTemp = get_bed_data['bed']['actual']
        #     self.MainWindow.CurrentBuildPlateTemp.display(self.currentBedTemp)
        #     print("error check 1")
        # except:
        #     print("Unable to update bed temperature")
        #
        # try:
        #     # CHAMBER TEMPERATURE
        #     get_chamber_data = requests.get(url=f"http://{self.api_endpoint}/api/printer/chamber", params=self.params)
        #     print("Get CHAMBER API Status:")
        #     get_chamber_data.raise_for_status()
        #     get_chamber_data = get_chamber_data.json()
        #     print(get_chamber_data['chamber']['actual'])
        #     self.currentChamTemp = get_chamber_data['chamber']['actual']
        #     self.MainWindow.CurrentBuildChamberTemp.display(self.currentChamTemp)
        #     print("error check 2")
        #
        # except:
        #     print("Unable to update Chamber temperature")
        #
        # try:
        #     # GET Z LOADING MOTOR CURRENT POSITION
        #
        #     self.ZmotorCurrPos = requests.get(url='', params=self.params)
        #     self.MainWindow.ZmotorPos.display(self.ZmotorCurrPos)
        # except:
        #     pass
        #
        # try:
        #     # GET Z AXIS MOTOR CURRENT POSITION
        #     self.ZaxisCurrPos = requests.get(url='', params=self.params)
        #     self.MainWindow.ZaxisPos.display(self.ZaxisCurrPos)
        #
        # except:
        #     pass

    def move_Lhopper(self,move):
        self.update_parameters()
        if move == None:
            #From the Input
            pass
        else:
            #From the Buttons
            pass
        self.update_parameters()
    def move_Rhopper(self,move):
        self.update_parameters()
        if move == None:
            #From the Input
            pass
        else:
            #From the Buttons
            pass
        self.update_parameters()
    def hopperTemperatureControl(self):
        pass

def main():
    app = QApplication([])
    window = GUI()
    app.exec_()


if __name__ == '__main__':
    main()

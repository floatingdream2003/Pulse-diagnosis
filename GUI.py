from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtGui import QPalette, QBrush, QColor
from PyQt5.QtWidgets import QPushButton, QApplication, QComboBox, QLabel, QFileDialog, QStatusBar, QDesktopWidget, \
    QMessageBox, QMainWindow, QFrame,QVBoxLayout, QWidget
import pyqtgraph as pg
import sys
from process import *
from webcam import Webcam
from video import Video
from interface import waitKey, plotXY
import subprocess
import time
# import pyautogui
class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()


        print("Screen height {}".format(self.screenheight))#1600
        print("Screen width {}".format(self.screenwidth))#2560


        self.initUI()
        self.webcam = Webcam()
        self.video = Video()
        self.input = self.webcam
        self.dirname = ""
        print("输入：实时拍摄")
        self.statusBar.showMessage("输入：实时拍摄", 5000)
        self.btnOpen.setEnabled(False)
        self.process = Process()
        self.status = False
        self.frame = np.zeros((10, 10, 3), np.uint8)
        # self.plot = np.zeros((10,10,3),np.uint8)
        self.bpm = 0
        self.terminate = False

    def initUI(self):
#融合用的，调用emotion程序的按钮###############################################################
        # self.btnLaunchPlot = QPushButton("Launch Plot", self)
        # self.btnLaunchPlot.clicked.connect(self.launchPlot)
        # self.btnLaunchPlot.move(0,550)
        # self.btnLaunchPlot.setFixedWidth(912)
        # self.btnLaunchPlot.setFixedHeight(50)
###########################################################################################
        # set font 字体
        font = QFont()
        font.setPointSize(16)

        # background——》》》灰色背景
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # 灰色的RGB值230，230，230
        self.setPalette(palette)
#2560/1600
        # widgets 按钮
        self.btnStart = QPushButton("开始", self)
        self.btnStart.move(0, 0)
        self.btnStart.setFixedWidth(self.screenwidth*304/2560)
        self.btnStart.setFixedHeight(self.screenheight*50/1600)
        self.btnStart.setFont(font)
        self.btnStart.clicked.connect(self.run)#######################################################################111

        self.btnOpen = QPushButton("打开文件", self)
        self.btnOpen.move(self.screenwidth*304/2560, 0)
        self.btnOpen.setFixedWidth(self.screenwidth*304/2560)
        self.btnOpen.setFixedHeight(self.screenheight*50/1600)
        self.btnOpen.setFont(font)
        self.btnOpen.clicked.connect(self.openFileDialog)#######################################################################111

        self.cbbInput = QComboBox(self)
        self.cbbInput.addItem("实时拍摄")
        self.cbbInput.addItem("本地视频")
        self.cbbInput.setCurrentIndex(0)
        self.cbbInput.setFixedWidth(self.screenwidth*304/2560)
        self.cbbInput.setFixedHeight(self.screenheight*50/1600)
        self.cbbInput.move(self.screenwidth*606/2560,self.screenheight*0/1600)
        self.cbbInput.setFont(font)
        self.cbbInput.activated.connect(self.selectInput)
        # -------------------

        # 创建字体对象
        font = QFont("Comic Sans MS", 15, QFont.Bold)

        # 设置标签
        self.frame = QFrame(self)
        self.frame.setGeometry(0, self.screenheight*50/1600, self.screenwidth*910/2560,self.screenheight*500/1600)
        self.frame.setStyleSheet("border: 2px solid black;")  # 添加黑色边框

        self.lblDisplay = QLabel(self.frame)
        self.lblDisplay.setGeometry(0, 0, self.screenwidth*910/2560,self.screenheight*500/1600)
        self.lblDisplay.setStyleSheet("border: 2px solid #808080")
        self.lblDisplay.setScaledContents(True)

        self.lblHR_1 = QLabel(self)  # label to show HR change over time 用于显示随时间变化的心率的标签
        self.lblHR_1.setGeometry(self.screenwidth * 910 / 2560, self.screenheight * 50 / 1600, self.screenwidth * 300 / 2560,self.screenheight * 40 / 1600)
        self.lblHR_1.setFont(font)
        # self.lblHR_1.setText("实时心率（寸）: ")

        self.lblHR2_1 = QLabel(self)  # label to show stable HR 用于显示稳定心率的标签
        self.lblHR2_1.setGeometry(self.screenwidth * 910 / 2560, self.screenheight * 100 / 1600, self.screenwidth * 300 / 2560,self.screenheight * 40 / 1600)
        self.lblHR2_1.setFont(font)
        # self.lblHR2_1.setText("稳定心率（寸）: ")

        self.lblHR_2 = QLabel(self)  # label to show HR change over time 用于显示随时间变化的心率的标签
        self.lblHR_2.setGeometry(self.screenwidth * 910 / 2560, self.screenheight * 150 / 1600, self.screenwidth * 300 / 2560,self.screenheight * 40 / 1600)
        self.lblHR_2.setFont(font)
        # self.lblHR_2.setText("实时心率（关）: ")

        self.lblHR2_2 = QLabel(self)  # label to show stable HR 用于显示稳定心率的标签
        self.lblHR2_2.setGeometry(self.screenwidth * 910 / 2560, self.screenheight * 200 / 1600, self.screenwidth * 300 / 2560,self.screenheight * 40 / 1600)
        self.lblHR2_2.setFont(font)
        # self.lblHR2_2.setText("稳定心率（关）: ")

        self.lblHR_3 = QLabel(self)  # label to show HR change over time 用于显示随时间变化的心率的标签
        self.lblHR_3.setGeometry(self.screenwidth * 910 / 2560, self.screenheight * 250 / 1600, self.screenwidth * 300 / 2560,self.screenheight * 40 / 1600)
        self.lblHR_3.setFont(font)
        # self.lblHR_3.setText("实时心率（尺）: ")

        self.lblHR2_3 = QLabel(self)  # label to show stable HR 用于显示稳定心率的标签
        self.lblHR2_3.setGeometry(self.screenwidth * 910/2560,self.screenheight * 300/1600,self.screenwidth*300/2560,self.screenheight*40/1600)
        self.lblHR2_3.setFont(font)
        # self.lblHR2_3.setText("稳定心率（尺）: ")


        # dynamic plot 动态绘图
        self.signal_Plt1 = pg.PlotWidget(self)
        self.signal_Plt1.move(self.screenwidth*0/2560,self.screenheight*600/1600)
        self.signal_Plt1.resize(self.screenwidth*744/2560,self.screenheight*290/1600)
        self.signal_Plt1.setLabel('bottom', "心率图（寸）")
        self.signal_Plt1.setBackground((255, 255, 255))  # 设置背景为透明
        axis_x = self.signal_Plt1.getAxis('bottom')
        axis_x.setPen(pg.mkPen(color=(0,0,0), width=2))
        axis_y = self.signal_Plt1.getAxis('left')
        axis_y.setPen(pg.mkPen(color=(0,0,0), width=2))
        axis_x.setTextPen((0,0,0))
        axis_y.setTextPen((0,0,0))

        self.signal_Plt2 = pg.PlotWidget(self)
        self.signal_Plt2.move(self.screenwidth*0/2560,self.screenheight*890/1600)
        self.signal_Plt2.resize(self.screenwidth*744/2560,self.screenheight*290/1600)
        self.signal_Plt2.setLabel('bottom', "心率图（关）")
        self.signal_Plt2.setBackground((255, 255, 255))  # 设置背景为透明
        axis_x = self.signal_Plt2.getAxis('bottom')
        axis_x.setPen(pg.mkPen(color=(0,0,0), width=2))
        axis_y = self.signal_Plt2.getAxis('left')
        axis_y.setPen(pg.mkPen(color=(0,0,0), width=2))
        axis_x.setTextPen((0,0,0))
        axis_y.setTextPen((0,0,0))

        self.signal_Plt3 = pg.PlotWidget(self)
        self.signal_Plt3.move(self.screenwidth*0/2560,self.screenheight*1180/1600)
        self.signal_Plt3.resize(self.screenwidth*744/2560,self.screenheight*290/1600)
        self.signal_Plt3.setLabel('bottom', "心率图（尺）")
        self.signal_Plt3.setBackground((255, 255, 255))  # 设置背景为透明
        axis_x = self.signal_Plt3.getAxis('bottom')
        axis_x.setPen(pg.mkPen(color=(0,0,0), width=2))
        axis_y = self.signal_Plt3.getAxis('left')
        axis_y.setPen(pg.mkPen(color=(0,0,0), width=2))
        axis_x.setTextPen((0,0,0))
        axis_y.setTextPen((0,0,0))

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)

        self.statusBar = QStatusBar()
        self.statusBar.setFont(font)
        self.setStatusBar(self.statusBar)

        # config main window 配置主窗口
        self.setGeometry(self.screenwidth*0/2560, self.screenheight*0/1600, self.screenwidth, self.screenheight*1540/1600)  # self.screenheight
        #1280/2560，1480/1600
        self.center()
        self.setWindowTitle("心率检测仪")

        self.show()

    # 初始化用户界面

    def update(self):
        pen = pg.mkPen(color=(0, 0, 0), width=2)

        self.signal_Plt1.clear()
        self.signal_Plt1.plot(self.process.samples[20:], pen=pen)

        self.signal_Plt2.clear()
        self.signal_Plt2.plot(self.process.samples[20:], pen=pen)

        self.signal_Plt3.clear()
        self.signal_Plt3.plot(self.process.samples[20:], pen=pen)

    # 更新绘图数据，清除原有数据并绘制新数据。

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 窗口居中显示

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure want to quit",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
            self.input.stop()
            # cv2.destroyAllWindows()
            self.terminate = True
            sys.exit()

        else:
            event.ignore()

    # 处理关闭事件，弹出确认对话框并根据用户选择执行相应操作。

    def selectInput(self):
        self.reset()
        if self.cbbInput.currentIndex() == 0:
            self.input = self.webcam
            print("Input: webcam")
            self.btnOpen.setEnabled(False)
            # self.statusBar.showMessage("Input: webcam",5000)
        elif self.cbbInput.currentIndex() == 1:
            self.input = self.video
            print("Input: video")
            self.btnOpen.setEnabled(True)
            # self.statusBar.showMessage("Input: video",5000)

    # 根据下拉框选择的输入源重置界面并更新相应设置。

    def key_handler(self):
        self.pressed = waitKey(1) & 255  # wait for keypress for 10 ms
        if self.pressed == 27:  # exit program on 'esc'
            print("[INFO] Exiting")
            self.webcam.stop()
            sys.exit()

    # 摁esc退出

    def openFileDialog(self):
        self.dirname = QFileDialog.getOpenFileName(self, 'OpenFile')

    # 打开文件对话框

    def reset(self):
        self.process.reset()
        self.lblDisplay.clear()
        self.lblDisplay.setStyleSheet("background-color: #000000")

    # 重置界面
    def ROI(self):
        frame = self.input.get_frame()
        ROI1, ROI2, ROI3 = wrist_detect(frame)
        return ROI1, ROI2, ROI3

    def main_loop(self, ROI,lblHR,lblHR2):
        frame = self.input.get_frame()

        self.process.frame_in = frame
        if self.terminate == False:
            ret = self.process.run(ROI)  ####################

        # cv2.imshow("Processed", frame)
        if ret == True:
            self.frame = self.process.frame_out  # get the frame to show in GUI
            self.f_fr = ROI
            # print(self.f_fr.shape)
            self.bpm = self.process.bpm  # get the bpm change over the time
        else:
            self.frame = frame
            self.f_fr = np.zeros((10, 10, 3), np.uint8)
            self.bpm = 0

        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        cv2.putText(self.frame, "FPS " + str(float("{:.2f}".format(self.process.fps))),
                    (20, 460), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)
        img = QImage(self.frame, self.frame.shape[1], self.frame.shape[0],
                     self.frame.strides[0], QImage.Format_RGB888)
        self.lblDisplay.setPixmap(QPixmap.fromImage(img))

        self.f_fr = cv2.cvtColor(self.f_fr, cv2.COLOR_RGB2BGR)
        self.f_fr = np.transpose(self.f_fr, (0, 1, 2)).copy()
        f_img = QImage(self.f_fr, self.f_fr.shape[1], self.f_fr.shape[0],
                       self.f_fr.strides[0], QImage.Format_RGB888)

        lblHR.setText("Freq: " + str(float("{:.2f}".format(self.bpm))))

        if self.process.bpms.__len__() > 50:
            if (max(self.process.bpms - np.mean(
                    self.process.bpms)) < 5):  # show HR if it is stable -the change is not over 5 bpm- for 3s
                lblHR2.setText("Heart rate: " + str(float("{:.2f}".format(np.mean(self.process.bpms)))) + " bpm")
        self.key_handler()  # if not the GUI cant show anything


    def run(self, input):
        print("run")
        self.reset()
        input = self.input
        self.input.dirname = self.dirname
        if self.input.dirname == "" and self.input == self.video:
            print("choose a video first")
            # self.statusBar.showMessage("choose a video first",5000)
            return
        if self.status == False:
            self.status = True
            input.start()
            self.btnStart.setText("Stop")
            self.cbbInput.setEnabled(False)
            self.btnOpen.setEnabled(False)
            self.lblHR2_1.clear()
            self.lblHR2_2.clear()
            self.lblHR2_3.clear()
            while self.status == True:
                ROI1, ROI2, ROI3 = self.ROI()
                print(ROI1)
                self.main_loop(ROI1,self.lblHR_1,self.lblHR2_1)
                self.main_loop(ROI2,self.lblHR_2,self.lblHR2_2)
                self.main_loop(ROI3,self.lblHR_3,self.lblHR2_3)



        elif self.status == True:
            self.status = False
            input.stop()
            self.btnStart.setText("开始")
            self.cbbInput.setEnabled(True)


    # def launchPlot(self):
    #     python_executable = "D:/ANACONDA/envs/HACI/python.exe"
    #     script_path = "C:/Users/91274/Desktop/enmtion_recognition/source/run.py"
    #     command = f"{python_executable} {script_path}"
    #     subprocess.Popen(command, shell=True)


    # def launchPlot(self):
    #     # 打开控制台
    #     pyautogui.hotkey('win', 'r')  # 组合键Win + R 打开运行窗口
    #     time.sleep(1)  # 等待1秒，确保运行窗口已经打开
    #     pyautogui.typewrite('cmd')  # 输入cmd，即打开命令提示符窗口
    #     pyautogui.press('enter')  # 模拟按下回车键
    #
    #     # 输入内容
    #     time.sleep(2)  # 等待2秒，确保控制台已经打开
    #     input_text = 'activate HACI'  # 待输入的内容
    #     pyautogui.typewrite(input_text)  # 输入内容
    #     pyautogui.press('enter')  # 模拟按下回车键
    #
    #     time.sleep(2)  # 等待2秒，确保控制台已经打开
    #     input_text = 'cd Desktop\enmtion_recognition\source'  # 待输入的内容
    #     pyautogui.typewrite(input_text)  # 输入内容
    #     pyautogui.press('enter')  # 模拟按下回车键
    #
    #     input_text = 'python run.py'  # 待输入的内容
    #     pyautogui.typewrite(input_text)  # 输入内容
    #     pyautogui.press('enter')  # 模拟按下回车键


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

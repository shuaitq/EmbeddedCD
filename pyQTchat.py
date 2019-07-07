from PyQt5.QtChart import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3
import sys

def change(str):
    time = QDateTime.fromString(str, "yyyy-MM-dd hh:mm:ss")
    time.setOffsetFromUtc(8)
    return time.toLocalTime().toMSecsSinceEpoch()

class Chart(QChart):
    limit = 30
    database = '/home/pi/github/DHT22_raspberry/weather.db'
    offset = 0.15
    def __init__(self):
        super().__init__()

        conn = sqlite3.connect(Chart.database)
        cursor = conn.cursor()
        cursor.execute('select * from weather order by id desc limit ?', [Chart.limit])
        data = cursor.fetchall()
        data.reverse()
        conn.commit()
        cursor.close()
        conn.close()

        #self.setAnimationOptions(QChart.AllAnimations)
        #chart.legend().hide()
        #chart.setTitle('Test')
        self.hmin = 100
        self.hmax = 0
        self.tmin = 100
        self.tmax = 0

        axisX = QDateTimeAxis()
        axisX.setFormat("hh:mm:ss")
        self.addAxis(axisX, Qt.AlignBottom)

        self.temperature = QSplineSeries()
        #self.temperature = QLineSeries()
        self.temperature.setUseOpenGL()
        self.temperature.setName("Temperature")
        for row in data:
            print(row[1], row[3])
            self.tmin = min(self.tmin, row[3])
            self.tmax = max(self.tmax, row[3])
            self.temperature.append(QPointF(change(row[1]), row[3]))
        self.addSeries(self.temperature)

        self.axisL = QValueAxis()
 
        self.addAxis(self.axisL, Qt.AlignLeft)
        self.temperature.attachAxis(axisX)
        self.temperature.attachAxis(self.axisL)

        self.humidity = QSplineSeries()
        #self.humidity = QLineSeries()
        self.humidity.setUseOpenGL()
        self.humidity.setName("Humidity")
        for row in data:
            print(row[1], row[2])
            self.hmin = min(self.hmin, row[2])
            self.hmax = max(self.hmax, row[2])
            self.humidity.append(QPointF(change(row[1]), row[2]))
        self.addSeries(self.humidity)

        self.axisR = QValueAxis()

        self.addAxis(self.axisR, Qt.AlignRight)
        self.humidity.attachAxis(axisX)
        self.humidity.attachAxis(self.axisR)

        self.updateRange()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10000)
    
    def update(self):
        x = self.plotArea().width() / Chart.limit

        print(self.plotArea().width(), Chart.limit)

        print('Tick')

        conn = sqlite3.connect(Chart.database)
        cursor = conn.cursor()
        cursor.execute('select * from weather order by id desc limit 1')
        data = cursor.fetchall()
        self.humidity.append(QPointF(change(data[0][1]), data[0][2]))
        self.hmin = min(self.hmin, data[0][2])
        self.hmax = max(self.hmax, data[0][2])
        print(data[0][1], data[0][2])
        self.temperature.append(QPointF(change(data[0][1]), data[0][3]))
        self.tmin = min(self.tmin, data[0][3])
        self.tmax = max(self.tmax, data[0][3])
        print(data[0][1], data[0][3])
        conn.commit()
        cursor.close()
        conn.close()

        self.updateRange()
        
        self.scroll(x, 0)
    
    def updateRange(self):
        hlength = self.hmax - self.hmin
        tlength = self.tmax - self.tmin
        hoffset = Chart.offset * hlength
        toffset = Chart.offset * tlength
        self.axisR.setRange(self.hmin - hoffset, self.hmax + hoffset)
        self.axisL.setRange(self.tmin - toffset, self.tmax + toffset)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    chart = Chart()
 
    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.setWindowTitle('Temperature and Humidity')
    window.resize(800, 600)
    window.showFullScreen()
    #window.show()

    sys.exit(app.exec_())

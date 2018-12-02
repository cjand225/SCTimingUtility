from random import randint
from string import ascii_lowercase
from datetime import datetime, timedelta
import time
from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractTableModel, QModelIndex
from src.table.CarStorage import CarStorage
from src.system.TimeReferences import strptimeMultiple
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class LapDataTableModel(QAbstractTableModel):
    def __init__(self, parent, cs=None):
        super().__init__(parent)

        if not cs:
            self.cs = CarStorage()
        else:
            self.cs = cs
        self.connectActions()
        # self.test()

    def connectActions(self):
        self.cs.dataModified.connect(self.storageModifiedEvent)

    def storageModifiedEvent(self, col, row):
        changeIndex = self.index(row, col)
        self.dataChanged.emit(changeIndex, changeIndex)
        self.headerDataChanged.emit(Qt.Horizontal, col, col)
        self.headerDataChanged.emit(Qt.Vertical, row, row)

    def rowCount(self, p):
        lapListLengths = [len(i.LapList) for i in self.cs.storageList]
        if lapListLengths:
            return max(max(lapListLengths) + 1, 19)
        else:
            return 19

    def columnCount(self, p):
        return max(len(self.cs.storageList) + 1, 11)

    def data(self, i, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if i.column() < len(self.cs.storageList) and i.row() < len(self.cs.storageList[i.column()].LapList):
                return str(self.cs.storageList[i.column()].LapList[i.row()])
            else:
                return None

    def setData(self, i, value, role):
        self.formatTime(value)
        try:
            value_split = value.split(".")
            value_time = strptimeMultiple(value_split[0], ["%H:%M:%S", "%M:%S", "%S"])
            seconds = timedelta(hours=value_time.hour, minutes=value_time.minute,
                                seconds=value_time.second).total_seconds()


            if len(value_split) == 2:
                milliseconds = int(value_split[1])
                seconds = seconds + (milliseconds / pow(10, len(value_split[1])))
            elif len(value_split) > 2:
                return False
        except ValueError:
            return False
        if role == Qt.EditRole:
            if i.column() < len(self.cs.storageList):

                if not self.cs.storageList[i.column()].initialTime:

                    self.cs.storageList[i.column()].initialTime = time.time()
                # lapTime = Lap_Time(self.cs.storageList[i.column()-1].recordedTime+seconds,seconds)
                if i.row() < len(self.cs.storageList[i.column()].LapList):
                    # self.cs.storageList[i.column()].LapList[i.row()][1] = value
                    self.cs.storageList[i.column()].editLapTime(i.row(), seconds)
                    return True
                elif i.row() == len(self.cs.storageList[i.column()].LapList):
                    self.cs.appendLapTime(i.column(), seconds)
                    return True
            else:
                return False

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.cs.storageList):
                    return self.cs.storageList[section].TeamName
                else:
                    return None
            elif orientation == Qt.Vertical:
                lengthList = [len(i.LapList) for i in self.cs.storageList]
                if lengthList and section < max(lengthList):
                    return section

    def flags(self, i):
        flags = super().flags(i)
        if i.column() < len(self.cs.storageList) and i.row() <= len(self.cs.storageList[i.column()].LapList):
            flags |= Qt.ItemIsEditable
        return flags



    def formatTime(self, value):
        if(len(value) > 0 and len(value) <= 2):
            print(time.strptime(value, "%S").tm_sec)
        elif len(value) > 2 and len(value) <= 4:
            print(time.strptime(value, "%M %S").tm_min)
        elif len(value) > 4 and len(value) <= 6:
            print(time.strptime(value, "%H %M %S").tm_hour)





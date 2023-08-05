import sqlite3
import os
from .configController import ConfigController
from .models.GPIORelaisModel import GPIOSwitchPoint
from .models.GPIORelaisModel import GPIOStoppingPoint

class DatabaseController():
    curs = None
    conn = None

    def openDatabase(self):
        config = ConfigController()
        dbPath = config.getDataBasePath()
        if dbPath is not None:
            if not os.path.exists(dbPath):
                self.createInitalDatabse(dbPath)
            
            try:
                self.conn = sqlite3.connect(dbPath)
                print(self.conn)
                self.curs = self.conn.cursor()
                print(self.curs)
                return True
            except Exception as e: 
                print(e)
                print('Error connecting database')
        return False

    def createInitalDatabse(self, dbPath):
        connection = sqlite3.connect(dbPath)
        cursor = connection.cursor()
        sqlStatementStop = 'CREATE TABLE "TMStopModel" ("uid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "relais_id" INTEGER NOT NULL, "mess_id" INTEGER)'
        sqlStatementSwitch = 'CREATE TABLE "TMSwitchModel" ("uid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "relais_id" INTEGER NOT NULL, "switchType" TEXT, "defaultValue" INTEGER)'
        cursor.execute(sqlStatementStop)
        cursor.execute(sqlStatementSwitch)
        connection.commit()
        connection.close()

    def insertStopModel(self, relaisId, messId):
        if self.openDatabase():
            # Insert a row of data
            print('Insert Stop: %i' % relaisId)
            if messId is not None:
                self.curs.execute("INSERT INTO TMStopModel(relais_id, mess_id) VALUES ('%i','%i')" % (relaisId, messId))
            else:
                self.curs.execute("INSERT INTO TMStopModel(relais_id) VALUES ('%i')" % (relaisId))
            self.conn.commit()
            self.conn.close()

    def insertSwitchModel(self, model):
        if self.openDatabase():
            # Insert a row of data
            print('Insert Switch: %i' % model.pin)
            self.curs.execute("INSERT INTO TMSwitchModel(relais_id, switchType, defaultValue) VALUES ('%i','%s', '%i')" % (model.pin, model.switchType, model.defaultValue))
            self.conn.commit()
            self.conn.close()

    def removeAll(self):
        if self.openDatabase():
            self.curs.execute("DELETE FROM TMSwitchModel")
            self.curs.execute("DELETE FROM TMStopModel")
            self.conn.commit()
            self.conn.close()
    
    def getAllSwichtModels(self):
        allSwitchModels = []
        if self.openDatabase():
            self.curs.execute("SELECT * FROM TMSwitchModel")            
            for dataSet in self.curs:
                switchModel = GPIOSwitchPoint(dataSet[1], dataSet[2], dataSet[1])
                switchModel.setDefaultValue(dataSet[3])
                allSwitchModels.append(switchModel)
        return allSwitchModels

    def getAllStopModels(self):
        allStopModels = []
        if self.openDatabase():
            self.curs.execute("SELECT * FROM TMStopModel")            
            for dataSet in self.curs:
                stop = GPIOStoppingPoint(dataSet[1], dataSet[1], dataSet[2])
                allStopModels.append(stop)
        return allStopModels
            
            
                



    
        
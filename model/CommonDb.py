from model.BaseModel import *
import datetime

class CommonDb(BaseModel):
    def __init__(self,tablename,dbname=""):
        if dbname == "":
            BaseModel.__init__(self)
        else:
            BaseModel.__init__(self,dbname)
        self.table = tablename

    def add(self,info,isctime=False,noUpdate=False):
        sInsertField = ""
        sInsertValue = ""

        sUpdateSql = ""
        for key in info.keys():
            sInsertField += "," + key
            sInsertValue += ",\"" + str(info[key]) + "\""
            sUpdateSql += key + "=\"" + str(info[key]) + "\","
        if noUpdate:
            sql = "insert into " + self.table + "(" + sInsertField[1:] + ") values(" + sInsertValue[1:]+ ") ON DUPLICATE KEY UPDATE " + sUpdateSql[:-1] + ";"
        else:
            sql = "insert into " + self.table + "(" + sInsertField[1:] + ") values(" + sInsertValue[1:] + ");"
        print(sql)
        return self.db.add(sql)

    def select(self,page,num,field,desc):
        if page <= 1:
            start = 0;
        else:
            start = (page-1) * num;
        sql = "select * from " + self.table + " order by " + field + " " + desc + " limit " + str(start) + "," + str(num) +  ";"
        print(sql)
        return self.db.executeSql(sql)

    def selectAll(self,wheresql,optionstr="*",map=False):
        sql = "select " + optionstr + " from " + self.table + " where 1 and " + wheresql + ";"
        print(sql)
        if map:
            return self.db.executeSqlMap(sql,self.table)
        else:
            return self.db.executeSql(sql)

    def selectByWhere(self,wheresql,page,num,field,desc):
        if page <= 1:
            start = 0;
        else:
            start = (page-1) * num;
        sql = "select * from " + self.table + " where 1 and " + wheresql + " order by " + field + " " + desc + " limit " + str(start) + "," + str(num) +  ";"
        print(sql)
        return self.db.executeSql(sql)

    def update(self,info,wheresql):
        sUpdateSql = ""
        for key in info.keys():
            sUpdateSql += key + "=\"" + str(info[key]) + "\","
        sql = "update " + self.table + " set " + sUpdateSql[0:-1] + " where 1 and " + wheresql;
        print(sql)
        return self.db.update(sql)

    def delete_where(self,wheresql):
        sql = "delete from " + self.table + " where 1 and " + wheresql + ";"
        print(sql)
        return self.db.update(sql)

    def executeMap(self,sql):
        print(sql)
        return self.db.executeSqlMap(sql,self.table)

    def execute(self,sql):
        return self.db.executeSql(sql)

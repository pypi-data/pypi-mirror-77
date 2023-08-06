import pymysql


class DBMySQL:
    def __init__(self, sql_conn_str):
        '''
        127.0.0.1,3306,newdb,sa,123456,
        '''
        print('''conn DBMySQL database''')
        sqlstr = sql_conn_str.split(',')
        self.conn = pymysql.connect(host=sqlstr[0],
                                    port=int(sqlstr[1]),
                                    user=sqlstr[3],
                                    passwd=sqlstr[4],
                                    db=sqlstr[2],
                                    charset='utf8')
        self.dowork = False
        self.cursor = self.conn.cursor()

    # 开启事务
    def setDoWork(self):
        print('DBMySQL.setDoWork')
        self.dowork = True

    def commitWork(self):
        print('DBMySQL.commitWork')
        self.conn.commit()

    def backWork(self):
        print('DBMySQL.backWork')
        self.conn.rollback()

    def __del__(self):
        self.close()

    def exec(self, sql_str, sql_par=()):
        print(sql_str)
        print(sql_par)
        try:
            self.cursor.execute(sql_str, sql_par)
            if self.dowork is False:
                print('exec.commit')
                self.conn.commit()

            # 返回影响数
            return self.cursor.rowcount
        except Exception as e:
            if self.dowork is False:
                self.conn.rollback()
            print('DBMySQL.exec:', e)
            raise e

    def query_all(self, sql_str, sql_par=()):
        cur = self.query(sql_str=sql_str, sql_par=sql_par)
        que = cur.fetchall()
        cols = cur.description
        tmp = []
        for v in que:
            row = {}
            for v2 in range(0, len(cols)):
                row[cols[v2][0]] = v[v2]
            tmp.append(row)
        return tmp

    def query_one(self, sql_str, sql_par=()):
        cur = self.query(sql_str=sql_str, sql_par=sql_par)
        que = cur.fetchone()
        if que is None:
            return None
        cols = cur.description
        row = {}
        for v2 in range(0, len(cols)):
            row[cols[v2][0]] = que[v2]
        return row

    def query(self, sql_str, sql_par=()):
        print(sql_str)
        print(sql_par)
        # 执行SQL语句
        self.cursor.execute(sql_str, sql_par)
        return self.cursor

    def getcols(self):
        return self.cursor.description

    def get_db(self):
        if self.cursor is None:
            self.cursor = self.conn.cursor()
        return self.cursor

    def close(self):
        if self.conn is not None:
            self.conn.close()
        print('''close DBMySQL database''')

    def add(self, obj, tableName):
            sql = "INSERT INTO `"+ tableName +"` "
            par = []
            bval = '('
            eval = '('
            for key in obj:
                bval = bval + str(key) + ','
                eval = eval + '%s,'
                par.append(obj[key])

            bval = bval[0:-1] + ')'
            eval = eval[0:-1] + ') '
            sql = sql + bval + ' VALUES ' + eval
            bak = self.exec(sql_str=sql, sql_par=par)
            return bak

    def delById(self, id,tableName):
        if id <= 0:
            raise Exception("id < 0")
        sql = 'DELETE FROM `' + tableName + '` WHERE id = %s'
        par = [id]

        bak = self.exec(sql_str=sql, sql_par=par)
        return bak

    def findById(self, id,tableName):
        if id <= 0:
            raise Exception("id < 0")
        sql = 'SELECT * FROM `' + tableName + '` where id = %s'
        par = [id]

        bak = self.query(sql_str=sql, sql_par=par).fetchone()
        return bak
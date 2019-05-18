import sqlite3

connection = sqlite3.connect("eleclib.db")
cursor = connection.cursor()


class Lib(object):
    def __init__(self, c):
        self.__c = c

    def ui(self):
        print("请输入需要的服务序号",
              "1：按书名查找",
              "2：按作者查找",
              "3：按类型查找")
        num = input()
        con = []          #查询条件，用于存储execute中的变量
        if num == '1':
            print("title")
            title = '《' + input() + '》'
            con.append(title)
            result = self.__c.execute("select * from mainstorage where title = ?;", con)
            con = []
            if result:
                for inf in result:
                    print("title :" + inf[0] + '\n',
                          "author :" + inf[1] + '\n',
                          "type :" + inf[2] + '\n',
                          "introduction :" + inf[3] + '\n'
                          )
            else:
                print("no information about this title")
        elif num == '2':
            print("author")
        elif num == '3':
            print("type")
        else:
            print("useless input")
            self.ui()


test = Lib(cursor)
test.ui()



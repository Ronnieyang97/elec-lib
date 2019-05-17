import sqlite3

connection = sqlite3.connect("eleclib.db")
cursor = connection.cursor()


class Lib(object):
    def ui(self):
        print("请输入需要的服务序号",
              "1：按书名查找",
              "2：按作者查找",
              "3：按类型查找")
        num = input()
        if num == '1':
            print("title")
        elif num == '2':
            print("author")
        elif num == '3':
            print("type")
        else:
            print("useless input")
            self.ui()


test = Lib()
test.ui()




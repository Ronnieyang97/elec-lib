import sqlite3
import sys

connection = sqlite3.connect("eleclib.db")
cursor = connection.cursor()


class Lib(object):
    def __init__(self, c):
        self.__c = c

    def ui(self):
        print("请输入需要的服务序号",
              "1：按书名查找",
              "2：按作者查找",
              "3：按类型查找",
              "0: 退出程序")
        num = input()
        if num == '1':   #功能1按照书名查找
            self.findbytitle()
        elif num == '2':
            print("author")
            self.findbyauthor()
        elif num == '3':
            print("type")
            self.printtype()
        elif num == '0':
            sys.exit(0)
        else:
            print("useless input")
            self.ui()

    def continue_use(self):
        print("是否继续使用？(yes/no)")
        command = input()
        if command == 'yes':
            self.ui()
        elif command == 'no':
            sys.exit(0)
        else:
            print("请输入正确的指令")
            self.continue_use()

    def findbytitle(self):
        con = []
        print("input the title")
        title = '《' + input() + '》'
        con.append(title)
        result = self.__c.execute("select * from mainstorage where title = ?;", con)
        x = 0
        for i in result:
            x = 1
        result = self.__c.execute("select * from mainstorage where title = ?;", con)
        if x == 1:
            for inf in result:
                print(1)
                print("title :" + inf[0] + '\n',
                      "author :" + inf[1] + '\n',
                      "type :" + inf[2] + '\n',
                      "introduction :" + inf[3] + '\n'
                      )
            self.continue_use()
        else:
            print("no such title in the mainstorage \n back to the main interface")
            self.continue_use()

    def findbyauthor(self):
        print("input the author")
        con = [input()]
        result = self.__c.execute("select title, type from mainstorage where author = ?;", con)
        x = 0
        for i in result:
            x = 1
        result = self.__c.execute("select title, type from mainstorage where author = ?;", con)
        if x == 1:
            for inf in result:
                print("title :", inf[0], '\n'
                      "type :", inf[1], '\n')
            self.continue_use()
        else:
            print("no suach author \n back to the main interface")
            self.continue_use()


test = Lib(cursor)
test.ui()


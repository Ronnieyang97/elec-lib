import sqlite3
import sys

connection = sqlite3.connect("eleclib.db")
cursor = connection.cursor()


class Lib(object):
    def __init__(self, connect):
        self.__connection = connect
        self.__c = self.__connection.cursor()

    def ui(self):
        print("请输入要进行的操作序号：\n",
              "1、查询\n",
              "2、新建\n",
              "3、更改\n",
              "4、删除\n",
              "0、退出程序")
        num = input()
        if num == '1':
            self.ui_find()
        elif num == '2':
            self.ui_insert()
        elif num == '3':
            self.ui_update()
        elif num == '4':
            pass
        elif num == '0':
            self.__connection.commit()
            sys.exit()
        else:
            print("请输入正确的指令！")
            self.ui()
        pass

    def ui_insert(self):
        print("请输入title（退出输入0）")        #sqlite中title为主键因此不能为空
        title = input()
        if title == '' or title[0] == ' ':
            print("title不能为空！！！")
            self.ui_insert()
        elif title == '0':
            self.ui()
        else:
            print("请输入作者")
            author = input()
            print("请输入类型")
            booktype = input()
            print("请输入简介")
            introduction = input()
            title = "《" + title + "》"
            self.__c.execute("insert into mainstorage (title, author, type, introduction) values(?,?,?,?)",
                             [title, author, booktype, introduction])
        print("insert over，back to the main interface")
        self.ui()

    def ui_update(self):
        print("请输入需要更新信息的title(退出请输入0)")   #必须为准确的书名
        title = input()
        if title == '0':
            self.ui()
        title = "《" + title + "》"
        print("请输入需要更改的对象（title/author/type/introduction）")
        target = input()
        if target != "title" and target != "author" and target != "type" and target != "introduction":
            print("输入无效！")
            self.ui_update()
        print("请输入更新的内容")
        content = input()
        if target == "title":
            content = "《" + content + "》"
        result = self.__c.execute("select ? from mainstorage where title = ?", [target, title])
        x = 0                   #查看输入的title是否存在于database中
        for i in result:
            x = 1
        if x == 0:
            print("title is not in the storage，insert please")
            self.ui_insert()
        elif x == 1:
            result = self.__c.execute("select ? from mainstorage where title = ?", [target, title])
            for inf in result:
                print("将" + title + "中的" + inf[0] + "改为" + content + "(yes/no)")
            judge = input()
            if judge == "no":
                print("cancel the update,back to the main interface")
            elif judge == "yes":
                if target == "title":
                    self.__c.execute("update mainstorage set title = ? where title = ?", [content, title])
                elif target == "author":
                    self.__c.execute("update mainstorage set author = ? where title = ?", [content, title])
                elif target  == "type":
                    self.__c.execute("update mainstorage set type = ? where title = ?", [content, title])
                elif target == "introduction":
                    self.__c.execute("update mainstorage set introduction = ? where title = ?", [content, title])
                print("update over,back to the main interface")
                self.ui()
            else:
                print("输入无效！！！")
                self.ui_update()

    def ui_find(self):      #查找界面
        print("请输入要进行的操作序号：\n",
              "1：按书名查找\n",
              "2：按作者查找\n",
              "3：按类型查找\n",
              "9：返回主界面\n",
              "0: 退出程序")
        num = input()
        if num == '1':   #功能1按照书名查找
            self.findbytitle()
        elif num == '2':    #功能2按照作者查找
            self.findbyauthor()
        elif num == '3':        #功能3按照类型查找
            self.findbytype()
        elif num == '9':        #返回上一界面
            self.ui()
        elif num == '0':
            sys.exit(0)
        else:
            print("useless input")
            self.ui_find()

    def findbytitle(self):              #按照书名查找
        print("input the title")
        con = ["%" + input() + "%"]      #对输入加%后，转为模糊搜索格式
        result = self.__c.execute("select * from mainstorage where title like ?", con)   #sqlite查询
        x = 0
        for i in result:        #sqlite如果返回为空，则i为0，将显示无此项并提供返回主界面的询问；如果不为空则进入显示结果
            x = 1
        result = self.__c.execute("select * from mainstorage where title like ?", con)
        if x == 1:          #查询结果不为空，显示结果
            for inf in result:
                print("title :" + inf[0] + '\n',
                      "author :" + inf[1] + '\n',
                      "type :" + inf[2] + '\n',
                      "introduction :" + inf[3] + '\n'
                      )
            self.ui_find()
        else:       #查询结果为空，返回主界面
            print("no such title in the mainstorage \n back to the finding interface")
            self.ui_find()

    def findbyauthor(self):
        print("input the author")
        con = ["%" + input() + "%"]     #将输入转为list
        result = self.__c.execute("select title, author, type from mainstorage where author like ?", con)
        x = 0
        for i in result:        #查询结果为空则为0，显示无此信息并询问是否返回主界面，否则为1，显示结果
            x = 1
        result = self.__c.execute("select title, author, type from mainstorage where author like ?", con)
        if x == 1:              #查询结果不为空，循环显示所有结果
            for inf in result:
                print("title :", inf[0], '\n'
                      "author :", inf[1], '\n'
                      "type :", inf[2], '\n')
            self.ui_find()
        else:           #查询结果为空，询问是否返回主界面
            print("no such author \n back to the finding interface")
            self.ui_find()

    def findbytype(self):
        alltype = self.__c.execute("select type from mainstorage group by type having count(type) > 1")
        print("we have types like:")
        i = 0
        for x in alltype:       #显示所有type
            if i % 5 == 0:
                print(x[0])
            else:
                print(x[0], end="     ")
            i += 1
        print("请输入想要查询的种类")
        con = ["%" + input() + "%"]  #将输入转为list
        result = self.__c.execute("select title, author, type from mainstorage where type like ?", con)
        x = 0
        for i in result:
            x = 1
        result = self.__c.execute("select title, author, type from mainstorage where type like ?", con)
        if x == 1:
            for inf in result:
                print("title :", inf[0], '\n'
                      "author :", inf[1], '\n'
                      "type :", inf[2], '\n')
            self.ui_find()
        else:
            print("no such type \n back to the finding interface")
            self.ui_find()


test = Lib(connection)
test.ui()

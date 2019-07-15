import sqlite3
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
#database中有mainstorage; recyclebin; favourite; read四个sheet分别存储主书库，回收站，收藏夹和已读;
#均包含title, author, type, introduction;


class Lib(object):
    def __init__(self, connect):
        self._connection = connect
        self._c = self._connection.cursor()

    def ui(self):
        print("输入任意字符开始")
        input()      #随意输入，起到暂停程序的作用
        print("请输入要进行的操作序号：\n",
              "1、查询\n",
              "2、新建\n",
              "3、更改\n",
              "4、删除\n",
              "5、添加到已读\n",
              "6、添加到收藏\n",
              "7、显示已读书目\n",
              "8、显示收藏夹书目\n",
              "9、在线查询\n",
              "10、在线添加\n",
              "0、退出程序")
        num = input()
        if num == '1':
            self.ui_find()
        elif num == '2':
            self.insert()
        elif num == '3':
            self.update()
        elif num == '4':
            self.delete()
        elif num == '5':
            self.ui_insert_read()
        elif num == '6':
            self.ui_insert_favourite()
        elif num == '7':
            self.print_read()
        elif num == '8':
            self.print_favourite()
        elif num == '9':
            self.ui_olsearch()
        elif num == "10":
            self.insert_online()
        elif num == '0':
            self._connection.commit()
            sys.exit()
        else:
            print("请输入正确的指令！")
            self.ui()
        pass

    def insert_online(self):
        self.check_connect()
        print("请输入连接：（输入完后加一个空格，否则会直接打开网页）")             #暂时只能手动复制输入连接
        url = input()
        self.check_resource(url)
        self.getpassage(url)
        print("导入结束")
        self.ui()

    def getpassage(self, url):          #从给到的url获取有效信息并添加到主书库中
        browser = webdriver.Chrome()
        browser.get(url)
        name = browser.find_element_by_id('activity-name')          #根据标题查找书目可能的类型
        alltype = ["书信集", "传记", "医学", "历史", "哲学", "悬疑小说", "心理", "散文集", "文学", "法律", "游记", "社科",
                   "科学", "科幻小说", "纪实", "经济", "绘画绘本", "职场", "艺术", "计算机", "诗歌", "随笔", "小说"]
        for i in alltype:
            if i in name.text:
                booktype = i
                break
            else:
                booktype = ' '
        content = browser.find_element_by_id("js_content")          #查找正文
        start = content.text.index("01")  # 截头
        end = content.text.index("05")
        try:
            end1 = content.text[end:].index("\n\n\n") + end
        except ValueError:
            end1 = -1
        finally:
            result = content.text[start:end1]
        for i in range(5):
            start = result.index('0' + str(i + 1))
            end = result[start:].index('\n') + start
            title = result[start + 2:end]                   #标题要去掉开头的数字01，02，03，04，05
            start = end + 1
            end = result[start:].index('\n') + start
            author = result[start:end]
            start = end + 1
            end = result[start:].index('\n') + start
            start = end + 1
            if i == 4:
                end = -1
            else:
                end = result.index(str('0' + str(i + 2) + '《'))             #加书名号避免干扰数字出现
            introduction = result[start:end]
            print("title:", title,
                  "author", author,
                  "type:", booktype,
                  "introduction:", introduction)
            self._c.execute("insert into mainstorage (title, author, type, introduction) values(?,?,?,?)",
                            [title, author, booktype, introduction])
            print("是否添加到收藏夹？(yes/no)")
            judge = input()
            if judge == "yes":
                self._c.execute("insert into favourite (title, author, type, introduction) values(?,?,?,?)",
                                [title, author, booktype, introduction])
            elif judge == "no":
                pass
            else:
                print("invalid input(default no add to the favourite)")
        browser.quit()

    def check_resource(self, url):           #确认是否来源为书单来了，来源错误则无法执行解析与导入
        browser = webdriver.Chrome()
        try:
            browser.get(url)
        except InvalidArgumentException:
            print("来源错误，请重新确认")
            browser.quit()
            self.ui()
        try:
            name = browser.find_element_by_id('profileBt')
            if name.text == "书单来了":
                print("来源正确")
            else:
                print("来源错误，请重新确认")
                browser.quit()
                self.ui()
        except NoSuchElementException:
            print("来源错误，请重新确认")
            browser.quit()
            self.ui()

    def check_connect(self):        #在线查找前先检测网络连接是否有效
        exit_code = os.system('ping www.baidu.com')
        if exit_code:
            print('connect failed.'
                  'check your internet connection')
            self.ui()
        else:
            print("\nUSEFUL CONNECTION!\n")

    def ui_olsearch(self):
        self.check_connect()
        print("请选择相应的查询渠道\n"
              "1、上海海事大学图书馆\n"
              "0、返回主界面")
        num = input()
        if num == '1':
            self.smu_search()
        elif num == '0':
            self.ui()
        else:
            print("invalid input")

    def smu_search(self):
        def get_vaild(inf):         #整理从网页爬取的相关信息
            i = -1
            while inf[i] == ' ' or 57 >= ord(inf[i]) >= 48:   #去除末尾两项无用数字项和空格
                i -= 1
            inf = inf[0:i]
            end1 = inf.rindex(' ')
            start1 = inf[0:end1].rindex(' ') + 1
            print(inf[start1:end1])         #显示位置
            space1 = inf.index(' ')
            space2 = inf[space1 + 1:-1].index(' ') + space1 + 1
            space3 = inf[space2 + 2:-1].index(' ') + space2 + 2
            if space3 - space2 == 8:
                print(inf[0:space2])        #显示存在空格的索书号
            else:
                print(inf[0:space1])        #显示不存在空格的索书号
            i = 0
            while inf[i] == ' ' or 57 >= ord(inf[i]) >= 45 or 65 <= ord(inf[i]) <= 90 or 97 <= ord(inf[i]) <= 122:
                i += 1                      #显示是否在馆
            start2 = i
            end2 = inf[start2:-1].index(' ') + start2
            print(inf[start2:end2])

        print("请输入想要查询的书目")
        title = input()
        browser = webdriver.Chrome()
        browser.get('http://www.library.shmtu.edu.cn/')
        input1 = browser.find_element_by_id('q')
        input1.send_keys(title)
        button = browser.find_element_by_class_name("button")
        button.click()
        browser.switch_to.window(browser.window_handles[-1])
        button1 = browser.find_elements_by_class_name("bookmetaTitle")
        if len(list(button1)) == 0:
            print("no result")
        elif len(list(button1)) < 5:
            lenth = len(list(button1))
        else:
            lenth = 5
        for i in range(lenth):
            button1 = browser.find_elements_by_class_name("bookmetaTitle")
            button1[i].click()
            result = browser.find_element_by_id("rightDiv")
            print("\n题名/作者：")
            start = result.text.index("题名/责任者:") + 8
            end = result.text[start:].index('\n')
            print(result.text[start:start + end])
            location = browser.find_element_by_id("holdingGrid-row-0")
            get_vaild(location.text)
            browser.back()
        browser.quit()
        print("\n输入任意字符返回主界面")
        input()
        self.ui()

    def ui_insert_favourite(self):
        print(" 1、从主书库中添加\n",
              "2、直接新建收藏书目\n",
              "3、返回主界面")
        num = input()
        if num == '1':
            print("请输入书名")
            con = ['《' + input() + '》']
            x = 0
            result = self._c.execute("select * from mainstorage where title = ?", con)  # sqlite查询
            for i in result:  # sqlite如果返回为空，则i为0，将显示无此项并提供返回主界面的询问；如果不为空则进入显示结果
                x = 1
            result = self._c.execute("select * from mainstorage where title = ?", con)
            if x == 1:  # 查询结果不为空，显示结果
                for inf in result:
                    print("title :" + inf[0] + '\n',
                          "author :" + inf[1] + '\n',
                          "type :" + inf[2] + '\n',
                          "introduction :" + inf[3] + '\n'
                          )
                print("是否将此书添加到收藏夹（yes/no）")
                judge = input()
                if judge == "yes":
                    result = self._c.execute("select * from mainstorage where title = ?", con)
                    for inf in result:
                        title = inf[0]
                        author = inf[1]
                        booktype = inf[2]
                        introduction = inf[3]
                    self._c.execute("insert into favourite (title, author, type, introduction) values(?, ?, ?, ?)",
                                    [title, author, booktype, introduction])
                    print("添加到favourite成功")
                    self.ui()
                elif judge == "no":
                    print("back to the main interface")
                    self.ui()
            else:
                print("no such book in the mainstorage\nback to the main interface")
                self.ui()
        elif num == '2':
            print("请输入书名")
            title = "《" + input() + "》"
            print("请输入作者")
            author = input()
            print("请输入类型")
            booktype = input()
            print("请输入简介")
            introduction = input()
            self._c.execute("insert into favourite (title, author, type, introduction) values(?, ?, ?, ?)",
                            [title, author, booktype, introduction])
            self._c.execute("insert into mainstorage (title, author, type, introduction) values(?, ?, ?, ?)",
                            [title, author, booktype, introduction])
            print("新建完成，并同步添加到mainstorage")
            self.ui()
        elif num == '0':
            self.ui()
        else:
            print("输入无效")
            self.ui()

    def print_read(self):
        result = self._c.execute("select * from read")
        for inf in result:
            print(" title :" + inf[0] + '\n',
                  "author :" + inf[1] + '\n',
                  "type :" + inf[2] + '\n',
                  "introduction :" + inf[3] + '\n'
                  )
        self.ui()

    def print_favourite(self):
        result = self._c.execute("select * from favourite")
        for inf in result:
            print(" title :" + inf[0] + '\n',
                  "author :" + inf[1] + '\n',
                  "type :" + inf[2] + '\n',
                  "introduction :" + inf[3] + '\n'
                  )
        self.ui()

    def ui_insert_read(self):
        print("1、从主书库中添加\n",
              "2、直接新建\n",
              "0、返回主界面")
        num = input()
        if num == '1':
            print("请输入书名")
            con = ['《' + input() + '》']
            x = 0
            result = self._c.execute("select * from mainstorage where title = ?", con)  # sqlite查询
            for i in result:  # sqlite如果返回为空，则i为0，将显示无此项并提供返回主界面的询问；如果不为空则进入显示结果
                x = 1
            result = self._c.execute("select * from mainstorage where title = ?", con)
            if x == 1:  # 查询结果不为空，显示结果
                for inf in result:
                    print("title :" + inf[0] + '\n',
                          "author :" + inf[1] + '\n',
                          "type :" + inf[2] + '\n',
                          "introduction :" + inf[3] + '\n'
                          )
                print("是否将此书添加到已读（yes/no）")
                judge = input()
                if judge == "yes":
                    result = self._c.execute("select * from mainstorage where title = ?", con)
                    for inf in result:
                        title = inf[0]
                        author = inf[1]
                        booktype = inf[2]
                        introduction = inf[3]
                    self._c.execute("insert into read (title, author, type, introduction) values(?, ?, ?, ?)",
                                    [title, author, booktype, introduction])
                    print("添加到read成功")
                    self.ui()
                elif judge == "no":
                    print("back to the main interface")
                    self.ui()
            else:
                print("no such book in the mainstorage\nback to the main interface")
                self.ui()
        elif num == '2':
            print("请输入书名")
            title = "《" + input() + "》"
            print("请输入作者")
            author = input()
            print("请输入类型")
            booktype = input()
            print("请输入简介")
            introduction = input()
            self._c.execute("insert into read (title, author, type, introduction) values(?, ?, ?, ?)",
                            [title, author, booktype, introduction])
            self._c.execute("insert into mainstorage (title, author, type, introduction) values(?, ?, ?, ?)",
                            [title, author, booktype, introduction])
            print("新建完成，并同步添加到mainstorage")
            self.ui()
        elif num == '0':
            self.ui()
        else:
            print("输入无效")
            self.ui_insert_read()

    def delete(self):
        print("请输入想要删除条目的title(输入0退出)")
        target = input()
        if target == '0':
            self.ui()
        target = ["《" + target + "》"]
        result = self._c.execute("select * from mainstorage where title = ?", target)
        x = 0
        for i in result:
            x = 1
        if x == 0:
            print("no such title,back to the main interface")
            self.ui()
        elif x == 1:
            result = self._c.execute("select * from mainstorage where title = ?", target)
            for inf in result:
                print("是否确定删除以下信息？(yes/no)\n",
                      "title :", inf[0], '\n',
                      "author :", inf[1], '\n',
                      "type :", inf[2], '\n',
                      "introduction :", inf[3], '\n')
                judge = input()
                if judge == "no":
                    self.delete()
                elif judge == "yes":
                    temp = self._c.execute("select * from mainstorage where title = ?", target)
                    for i in temp:
                        bin1 = i[0]
                        bin2 = i[1]
                        bin3 = i[2]
                        bin4 = i[3]
                    self._c.execute("insert into recyclebin(title, author, type, introduction) \
                                     values(?, ?, ?, ?)", [bin1, bin2, bin3, bin4])     #删除项将被放入recyclebin中
                    self._c.execute("delete from mainstorage where title = ?", target)
                    print("delete over,back to the main interface")
                    self.ui()
                else:
                    print("无效输入！！！")
                    self.ui()

    def insert(self):
        print("请输入title（退出输入0）")        #sqlite中title为主键因此不能为空
        title = input()
        if title == '' or title[0] == ' ':
            print("title不能为空！！！")
            self.insert()
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
            self._c.execute("insert into mainstorage (title, author, type, introduction) values(?,?,?,?)",
                            [title, author, booktype, introduction])
        print("insert over，back to the main interface")
        print("是否同步到favourite?(yes/no)")
        judge = input()
        if judge == "yes":
            self._c.execute("insert into favourite (title, author, type, introduction) values(?,?,?,?)",
                            [title, author, booktype, introduction])
            print("已同步到favourite")
            self.ui()
        elif judge == "no":
            self.ui()
        else:
            print("无效输入")
            self.ui()

    def update(self):
        print("请输入需要更新信息的title(退出请输入0)")   #必须为准确的书名
        title = input()
        if title == '0':
            self.ui()
        title = "《" + title + "》"
        print("请输入需要更改的对象（title/author/type/introduction）")
        target = input()
        if target != "title" and target != "author" and target != "type" and target != "introduction":
            print("输入无效！")
            self.update()
        print("请输入更新的内容")
        content = input()
        if target == "title":
            content = "《" + content + "》"
        result = self._c.execute("select ? from mainstorage where title = ?", [target, title])
        x = 0                   #查看输入的title是否存在于database中
        for i in result:
            x = 1
        if x == 0:
            print("title is not in the storage，insert please")
            self.insert()
        elif x == 1:        #根据target的值来对相应的列做出update
            result = self._c.execute("select ? from mainstorage where title = ?", [target, title])
            for inf in result:
                print("将" + title + "中的" + inf[0] + "改为" + content + "(yes/no)")
            judge = input()
            if judge == "no":
                print("cancel the update,back to the main interface")
                self.update()
            elif judge == "yes":
                if target == "title":
                    self._c.execute("update mainstorage set title = ? where title = ?", [content, title])
                elif target == "author":
                    self._c.execute("update mainstorage set author = ? where title = ?", [content, title])
                elif target == "type":
                    self._c.execute("update mainstorage set type = ? where title = ?", [content, title])
                elif target == "introduction":
                    self._c.execute("update mainstorage set introduction = ? where title = ?", [content, title])
                print("update over,back to the main interface")
                self.ui()
            else:
                print("输入无效！！！")
                self.update()

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
        x = 0
        result = self._c.execute("select * from mainstorage where title like ?", con)   #sqlite查询
        for i in result:        #sqlite如果返回为空，则i为0，将显示无此项并提供返回主界面的询问；如果不为空则进入显示结果
            x = 1
        result_favour = self._c.execute("select * from favourite where title like ?", con)
        y = 0
        for i in result_favour:
            y = 1
        result_favour = self._c.execute("select * from favourite where title like ?", con)
        if y == 1:
            print("books in FAVOURITE :")
            for inf in result_favour:
                print("title :" + inf[0] + '\n',
                      "author :" + inf[1] + '\n',
                      "type :" + inf[2] + '\n',
                      "introduction :" + inf[3] + '\n'
                      )
            print("是否继续显示所有结果（yes/no）")
            judge = input()
            if judge == "no":
                print("back to the main interface")
                self.ui()
            elif judge == "yes":
                print("continue to print")
            else:
                print("invalid input")
                self.ui()
        result = self._c.execute("select * from mainstorage where title like ?", con)
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
        result = self._c.execute("select title, author, type from mainstorage where author like ?", con)
        x = 0
        for i in result:        #查询结果为空则为0，显示无此信息并询问是否返回主界面，否则为1，显示结果
            x = 1
        result_favourite = self._c.execute("select title, author, type from favourite where author like ?", con)
        y = 0
        for i in result_favourite:
            y = 1
        result_favourite = self._c.execute("select title, author, type from favourite where author like ?", con)
        if y == 1:
            for inf in result_favourite:
                print("title :", inf[0], '\n'
                      "author :", inf[1], '\n'
                      "type :", inf[2], '\n')
            print("是否继续显示所有结果（yes/no）")
            judge = input()
            if judge == "no":
                print("back to the main interface")
                self.ui()
            elif judge == "yes":
                print("continue to print")
            else:
                print("invalid input")
                self.ui()
        result = self._c.execute("select title, author, type from mainstorage where author like ?", con)
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
        alltype = self._c.execute("select type from mainstorage group by type having count(type) > 1")
        print("we have types like:")
        i = 0
        for x in alltype:       #显示所有type
            if i % 5 == 0:
                print(x[0])
            else:
                print(x[0], end="     ")
            i += 1
        print("\n请输入想要查询的种类")
        con = ["%" + input() + "%"]  #将输入转为list
        result = self._c.execute("select title, author, type from mainstorage where type like ?", con)
        x = 0
        for i in result:
            x = 1
        result_favourite = self._c.execute("select title, author, type from mainstorage where type like ?", con)
        y = 0
        for i in result_favourite:
            y = 1
        result_favourite = self._c.execute("select title, author, type from mainstorage where type like ?", con)
        if y == 1:
            for inf in result_favourite:
                print("title :", inf[0], '\n'
                      "author :", inf[1], '\n'
                      "type :", inf[2], '\n')
            print("是否继续显示所有结果（yes/no）")
            judge = input()
            if judge == "no":
                print("back to the main interface")
                self.ui()
            elif judge == "yes":
                print("continue to print")
            else:
                print("invalid input")
                self.ui()
        result = self._c.execute("select title, author, type from mainstorage where type like ?", con)
        if x == 1:
            for inf in result:
                print("title :", inf[0], '\n'
                      "author :", inf[1], '\n'
                      "type :", inf[2], '\n')
            self.ui_find()
        else:
            print("no such type \n back to the finding interface")
            self.ui_find()


#connection = sqlite3.connect("eleclib.db")     #用with取代；暂时保留
#test = Lib(connection)
#test.ui()

with sqlite3.connect("eleclib.db") as connection:
    test = Lib(connection)
    test.ui()

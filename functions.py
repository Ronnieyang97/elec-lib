import sqlite3
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException


def search_by_title(title):
    with sqlite3.connect("eleclib.db") as connection:
        c = connection.cursor()
        con = ["%" + title + "%"]
        x = 0
        result = c.execute("select * from mainstorage where title like ?", con)  # sqlite查询
        for i in result:  # sqlite如果返回为空，则i为0，将显示无此项并提供返回主界面的询问；如果不为空则进入显示结果
            x = 1
        result = c.execute("select * from mainstorage where title like ?", con)
        if x:  # 查询结果不为空，显示结果
            output = []
            for inf in result:
                output.append([inf[0], inf[1], inf[2], inf[3]])
        else:  # 查询结果为空，返回主界面
            output = ''
        return output


def search_by_author(author):
    with sqlite3.connect("eleclib.db") as connection:
        c = connection.cursor()
        con = ["%" + author + "%"]  # 将输入转为list
        result = c.execute("select title, author, type from mainstorage where author like ?", con)
        x = 0
        for i in result:  # 查询结果为空则为0，显示无此信息并询问是否返回主界面，否则为1，显示结果
            x = 1
        result_favourite = c.execute("select * from favourite where author like ?", con)
        y = 0
        for i in result_favourite:
            y = 1
        result_favourite = c.execute("select * from favourite where author like ?", con)
        result = c.execute("select title, author, type from mainstorage where author like ?", con)
        if x:  # 查询结果不为空，循环显示所有结果
            output = []
            for info in result:
                output.append([info[0], info[1], info[2]])
        else:
            output = ''
        if y:
            output_favour = []
            for info in result_favourite:
                output_favour.append([info[0], info[1], info[2], info[3]])
        else:
            output_favour = ''
        return output, output_favour


def search_by_type(thetype):
    with sqlite3.connect('eleclib.db') as connection:
        c = connection.cursor()
        con = ["%" + thetype + "%"]  # 将输入转为list
        result = c.execute("select title, author, type from mainstorage where type like ?", con)
        x = 0
        for i in result:
            x = 1
        result_favourite = c.execute("select * from mainstorage where type like ?", con)
        y = 0
        for i in result_favourite:
            y = 1
        result_favourite = c.execute("select * from mainstorage where type like ?", con)
        if y:
            output_favour = []
            for info in result_favourite:
                output_favour.append([info[0], info[1], info[2], info[3]])
        else:
            output_favour = ''
        result = c.execute("select title, author, type from mainstorage where type like ?", con)
        if x:
            output = []
            for info in result:
                output.append([info[0], info[1], info[2]])
        else:
            output = ''
        return output, output_favour



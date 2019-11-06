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
        if x == 1:  # 查询结果不为空，显示结果
            output = []
            for inf in result:
                output.append([inf[0], inf[1], inf[2], inf[3]])
        else:  # 查询结果为空，返回主界面
            output = ''
        return output

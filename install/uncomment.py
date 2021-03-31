#! /home/wenyu/anaconda3/bin/python3
# -*- coding: utf-8 -*-


"""
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---=' 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
         佛祖保佑       永无BUG 

'''
  

Created on 


@author: wenyu_xu
@mail:wenyu__xu@163.com




"""


import os
import re
import sys
import configparser


class uncomment:
    def __init__(self, src, encoding="utf-8"):
        self.__src = src
        self.__encoding = encoding

        self.__pattern_c = {re.compile(r'//.*'), re.compile(r'/\*((?:.|\n)*?)\*/'), }
        self.__pattern_cpp = self.__pattern_c
        self.__pattern_java = self.__pattern_c
        self.__pattern_py = {re.compile(r'#.*'), re.compile(r'("""((?:.|\n)*?)""")*|(\'\'\'((?:.|\n)*?)\'\'\')*'), }

        self.__pattern_map = {
            'c': self.__pattern_c,
            'cpp': self.__pattern_cpp,
            'java': self.__pattern_java,
            'py': self.__pattern_py,
        }
        pass

    def is_pass_line(self, line):
        # . 表示除\n之外的任意字符
        # * 表示匹配0-无穷
        # ? 表示懒惰匹配模式
        # .*? 匹配任意数量的重复，但是在能使整个匹配成功的前提下使用最少的重复
        re.compile(r'(""".*?""")*|(\'\'\'.*?\'\'\')*')
        print(line)
        # 可忽略行的正则表达式列表
        RegularExpressions = ["""/'.*#.*/'""",
                              '''/".*#.*/"''',
                              """/'/'/'.*#.*/'/'/'""",
                              '''/"/"/".*#.*/"/"/"''']
        for One in RegularExpressions:
            pattern = re.compile(One)
            if re.search(pattern, line) == None:
                continue
            else:
                return True  # 有匹配 则忽略

        return False

    '''
    @staticmethod
    def remove_comment(strInput):
        """
        对流字符串进行去注释
        :param strInput:
        :return:
        """
        state = 0  # 设正常状态为0，并初始为正常状态
        strOutput = ''
        strRemoved = ''

        for c in strInput:
            # print("state = ", state)
            if state == 0 and c == '/':  # ex. [/] : 状态0中遇到'/', 说明可能会遇到注释, 则进入状态1　
                state = 1

            elif state == 1 and c == '*':  # ex. [/*]
                state = 2
            elif state == 1 and c == '/':  # ex. [#]
                state = 4
            elif state == 1:  # ex. [<secure/_stdio.h> or 5/3]
                print('/')
                strOutput += '/'
                state = 0

            elif state == 3 and c == '*':  # ex. [/*he**]
                state = 3
            elif state == 2 and c == '*':  # ex. [/*he*]
                state = 3
            elif state == 2:  # ex. [/*heh]
                state = 2

            elif state == 3 and c == '/':  # ex. [/*heh*/]
                state = 0
            elif state == 3:  # ex. [/*heh*e]
                state = 2

            elif state == 4 and c == '\\':  # ex. [//hehe\]
                state = 9
            elif state == 9 and c == '\\':  # ex. [//hehe\\\\\]
                state = 9
            elif state == 9:  # ex. [//hehe\<enter> or //hehe\a]
                state = 4
            elif state == 4 and c == '\n':  # ex. [//hehe<enter>]
                state = 0

            elif state == 0 and c == '\'':  # ex. [']
                state = 5
            elif state == 5 and c == '\\':  # ex. ['\]
                state = 6
            elif state == 6:  # ex. ['\n or '\' or '\t etc.]
                state = 5
            elif state == 5 and c == '\'':  # ex. ['\n' or '\'' or '\t' ect.]
                state = 0

            elif state == 0 and c == '\"':  # ex. ["]
                state = 7
            elif state == 7 and c == '\\':  # ex. ["\]
                state = 8
            elif state == 8:  # ex. ["\n or "\" or "\t ect.]
                state = 7
            elif state == 7 and c == '\"':  # ex. ["\n" or "\"" or "\t" ect.]
                state = 0

            ### new request
            #  []
            # elif state == 0 and c == '[':  # ex. [[]
            #    state = 10
            # elif state == 10 and c == ']':  # ex. []]
            #    state = 11

            # [[]]
            elif state == 10 and c == '[':  # ex. []]
                state = 12
            elif state == 12 and c == ']':  # ex. [[]
                state = 13
            elif state == 13 and c == ']':  # ex. [[]
                state = 14

            # remove character in []
            # elif state == 10:
            #    state = 10

            # remove character in [[]]
            elif state == 12:
                state = 12
            elif state == 13:
                state = 13
            # restore state
            elif state == 11:
                state = 0
            elif state == 14:
                state = 0

            elif state == 11 and c == ']':
                state = 14
            elif state == 1 and c == ']':
                state = 13

            elif state == 10:
                state = 10
            elif state == 12:
                state = 12

            elif state == 11:
                state = 13
            elif state == 12:
                state = 0
            elif state == 13:
                state = 0

            # remove "=-1" in "int a = -1;"
            # elif state == 0 and c == '=':
            #    state = 15
            # elif state == 15 and c == ';':
            #    state = 0

            if (state == 0 and c != '/') or state == 5 or \
                    state == 6 or state == 7 or state == 8:
                strOutput += c
                # print("strOutput", strOutput)
            else:
                # removed chareters
                strRemoved += c
                # print("strRemoved", strRemoved)

            # ToDo: #if 0 的情况

        return strOutput
    '''

    def remove_comment(self, content, suffix):
        patterns = self.__pattern_map.get(suffix, self.__pattern_c)
        result = content
        for pattern in patterns:
            result = re.sub(pattern, "", result)

        return result

    '''
    def remove_comment_py(self, lines):
        strOutput = ''

        count = 0
        for line in lines:
            print("line = ", line)
            index = line.find('#')                                  # 获取带注释句‘#'的位置索引
            if index == -1 or count < 3 or self.is_pass_line(line): # 当前行没有'#'
                if line.strip() != '':                              # 排除纯空的行
                    strOutput = strOutput + line
            else:                                                   # 当前行有'#'
                if index != 0:
                    strOutput = strOutput + line[:index] + '\n'     # 截取后面的注释部分
            count += 1

        return strOutput
    '''
    def remove_file(self, src):
        """
        对整个文件去注释
        :param src:
        :return:
        """
        # 文件是否存在
        if not os.path.exists(src):
            print('Error: file - {} is not exist.'.format(src))
            return False

        # 文件是否是链接
        if os.path.islink(src):
            print('Error: file - {} is a link.'.format(src))
            return False

        # 根据后缀名，判断是否是C/C++代码
        filetype = (os.path.splitext(src))[-1]
        if filetype not in ['.c', '.h', '.cpp', '.hh', '.cc', '.java', '.py']:
            return False

        inputf = open(src, 'r+', encoding=self.__encoding)
        outputfilename = (os.path.splitext(src))[0] + '_no_comment' + filetype
        outputf = open(outputfilename, 'w')

        content = inputf.read()
        remain = self.remove_comment(content, filetype[1:])

        outputf.write(remain)

        inputf.close()
        outputf.close()

        os.remove(src)
        os.rename(outputfilename, src)

        return True

    def remove_dir(self, path):
        """
        对整个目录去注释
        :param path:
        :return:
        """
        # 目录是否存在
        if not os.path.exists(path):
            print("Error: dir - {} is not exist.".format(path))
            return False

        files = os.listdir(path)  # 返回指定的文件夹包含的文件或文件夹的名字的列表
        for file in files:
            file = path + '/' + file
            if os.path.isdir(file):
                self.remove_dir(file)
            elif os.path.isfile(file):
                self.remove_file(file)

        return True

    def run(self):
        if os.path.isdir(src):  # 判断是目录还是文件
            dir_path = os.path.abspath(self.__src)      # 获取绝对路径
            self.remove_dir(dir_path)
        elif os.path.isfile(src):
            file_path = os.path.abspath(self.__src)     # 获取绝对路径
            self.remove_file(file_path)
        else:
            print('Error: {} is not dir or file!'.format(src))
            self.usage()


if __name__ == '__main__':
    cf = configparser.ConfigParser()
    cf.read("uncomment.ini")

    src = cf.get("CleanNote", "src")
    print("src = ", src)
    encoding = cf.get("CleanNote", "encoding")
    print("encoding = ", encoding)

    notes = uncomment(src=src, encoding=encoding)
    notes.run()

    pass

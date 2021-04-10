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

from Crypto.Cipher import AES


class AesCrypt:
    def __init__(self, key, model, iv):
        self.key = self.add_16(key)
        self.model = model
        self.iv = iv

    def add_16(self,par):
        if type(par) == str:
            par = par.encode()
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self, text):
        text = self.add_16(text)
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key,self.model,self.iv)
        elif self.model == AES.MODE_ECB:
            self.aes = AES.new(self.key,self.model)
        self.encrypt_text = self.aes.encrypt(text)
        return self.encrypt_text

    def aesdecrypt(self, text):
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key,self.model,self.iv)
        elif self.model == AES.MODE_ECB:
            self.aes = AES.new(self.key,self.model)
        self.decrypt_text = self.aes.decrypt(text)
        self.decrypt_text = self.decrypt_text.strip(b"\x00")
        return self.decrypt_text
        # return str(self.decrypt_text, encoding='utf-8')


if __name__ == '__main__':
    passwd = "w#E~n0y^U38J:"
    iv = '1111111111111111'

    aescryptor = AesCrypt(passwd, AES.MODE_CBC, iv)  # CBC模式
    # aescryptor = Aescrypt(passwd,AES.MODE_ECB,"") # ECB模式
    text = "gmw"
    en_text = aescryptor.aesencrypt(text)
    print("密文:", en_text)
    text = aescryptor.aesdecrypt(en_text)
    print("明文:", text)
    pass


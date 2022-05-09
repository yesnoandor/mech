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


from rtsp.ABVideoCapture import ABVideoCapture
import cv2


class VideoCapture(ABVideoCapture):
    """
    继承ABVideoCapture，对缓存栈中的图片不做处理直接返回
    """
    def process_image(self, image):
        """
        这里对图像的处理算法可以随意制定
        """
        return image


if __name__ == '__main__':
    camera_addr = 0
    cap = VideoCapture(camera_addr)
    while True:
        _, img = cap.read()
        if _:
            cv2.imshow('img', img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    """
    camera_addr = 0
    with VideoCapture(camera_addr) as cap:
    for img in cap:
        cv2.imshow('img', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
            
    CV2.destroyAllWindows()
    """
    pass

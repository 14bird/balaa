import socket
import threading
import tkinter
import random
import platform
import time
import re
from message_pack import message
try:
    import my_config as config
except:
    import config
service_addr = config.website
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_port = 2000 + random.randint(400, 1000)


def receiver_fun():
    while True:
        try:
            buff = s.recv(1024)
            mes = message()
            mes.unpackage(buff.decode('utf-8'))
            buff = mes['timestamp'] + '@' + \
                mes['recv_from_name'] + ':' + mes.content() + '\n'
            tmps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if buff == '':
                continue
            tmps.connect(('127.0.0.1', server_port))
            tmps.send(buff.encode('utf-8'))
            tmps.close()
        except Exception as e:
            print('end in local_serve')
            break


class MainWin:
    def rec(self):
        self.tmpss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tmpss.bind(('0.0.0.0', server_port))
        self.tmpss.listen(20)
        while True:
            self.sock, self.addr = self.tmpss.accept()
            self.datat = self.sock.recv(1024)
            self.datat = self.datat.decode('utf-8')
            if self.datat[0] == '\1':
                self.tmpss.close()
                break
            self.reflu(self.datat)
        print('err!')

    def __init__(self):
        self.tki = tkinter.Tk()
        self.tki.title('balaa')
        self.tki.geometry('600x400+200+200')
        self.fra = tkinter.Frame(self.tki)
        self.reg = threading.Thread(target=self.rec, daemon=True)
        self.reg.start()

    def sendmessage(self):
        self.tmp = self.tex.get('1.0', tkinter.END)
        self.me = message(None, None, self.tmp[0:-1], time.ctime(), None)
        s.send(self.me.package().encode('utf-8'))
        self.clearwin()
        tmps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmps.connect(('127.0.0.1', server_port))
        self.tmp = 'you:' + self.tmp
        tmps.send(self.tmp.encode('utf-8'))
        tmps.close()

    def sendpicture(self):
        print("picture")

    def managewin(self):
        print("manage")

    def chan(self):
        print('change')

    def seehistory(self):
        self.reflu()
        print('history')

    def closewin(self):
        self.close()

    def clearwin(self):
        self.tex.delete('1.0', tkinter.END)

    def reflu(self, tmpstr):
        self.lis.delete(first=0, last=self.siz)
        if tmpstr != '':
            self.ft = open('tmp', 'a+')
            self.ft.write(tmpstr)
            self.ft.close()
        self.siz = 0
        self.listmp = re.split('\n', tmpstr)
        for i in self.listmp:
            if i=='':
                continue
            self.cont.append(i)
        if len(self.cont) >= 30:
            self.cont = self.cont[-30:]

        for i in self.cont:
            self.lis.insert(self.siz, i)
            self.siz += 1
            if self.siz >= 30:
                print(self.siz)
                break
        self.lis.pack(fill='x')

    def sta(self):
        self.fra.pack()
        self.lis = tkinter.Listbox(width=80, height=15)
        self.siz = 0
        self.conte = ''
        self.cont = []
        self.reflu('')
        self.tex = tkinter.Text(self.tki, width=80, height=5)
        self.tex.pack(fill='x')
        self.sen = tkinter.Button(
            self.tki, text='send', fg='#ffffff', bg='#2fbf1f', command=self.sendmessage)
        self.sen.pack(side='left')
        self.pic = tkinter.Button(
            self.tki, text='picture', fg='#ffffff', bg='#00bfbf', command=self.sendpicture)
        self.pic.pack(side='left', expand='no')
        self.fil = tkinter.Button(
            self.tki, text='file', fg='#ffffff', bg='#cfcf00')
        self.fil.pack(side='left', expand='no')
        self.man = tkinter.Button(
            self.tki, text='manageofwindows', fg='#ffffff', bg='#cc0000', command=self.managewin)
        self.man.pack(sid='left', expand='no')
        self.cha = tkinter.Button(
            self.tki, text='change', fg='#ffffff', bg='#cc00cc', command=self.chan)
        self.cha.pack(side='left', expand='no')
        self.his = tkinter.Button(
            self.tki, text='history', bg='#cc1c1c', fg='#ffffff', command = self.seehistory)
        self.his.pack(side='left', expand='no')
        self.clo = tkinter.Button(
            self.tki, text='close', bg='#cc1c1c', fg='#ffffff', command=self.closewin)
        self.clo.pack(side='left', expand='no')
        '''self.cle = tkinter.Button(
            self.tki, text='clear', bg='#cc8c4c', fg='#ffffff', command=self.clearwin)
        self.cle.pack(side='left', expand='no')'''
        photo = tkinter.PhotoImage(file='tr1.gif')
        self.tu = tkinter.Button(self.tki, image=photo, command=self.clearwin,text='clear')
        self.tu.pack(side='left', expand='no')
        self.tki.mainloop()

    def close(self):
        print('bye')
        try:
            tmps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmps.connect(('127.0.0.1', server_port))
            tmps.send('\1'.encode('utf-8'))
            tmps.close()
        except Exception as e:
            print('error when close')
        self.tki.destroy()

    def __delete__(self):
        print('close')


def display():
    s.connect((service_addr, config.portno))
    d = MainWin()
    receiver = threading.Thread(target=receiver_fun, daemon=True)
    receiver.start()
    d.sta()
    mess = message(None, None, '\\exit', time.ctime(), None)
    s.send(mess.package().encode('utf-8'))
    s.send('\\exit'.encode('utf-8'))
    s.close()


if __name__ == '__main__':
    open('tmp', 'a').close()
    print(platform.system())
    display()

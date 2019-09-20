from tkinter import *
from tkinter.messagebox import *
import os
import shutil
import sys

system = sys.platform
base_dir = sys.path[0]
if system.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'
base_dir += dir_char


def remove(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def setup_xdg_open():
    status = os.system('yum install xdg-open')
    return status


def OpenPic():
    if dir_char == '/':
        if system == 'darwin':
            os.system('open pic.png')
        else:
            status = os.system('xdg-open pic.png')
            print(status)
            if status:
                print('No xdg-open! Auto setuping...')
                status = setup_xdg_open()
                if status:
                    exit('setup xdg-open failed')
                os.system('xdg-open pic.png')
    else:
        os.system('pic.png')


def verify_click():
    with open('pic.dot', 'w') as f:
        string = dg.get()
        f_content = content.get(0.0, END)
        f.write('%s G{\n' % string)
        if string == 'digraph':
            f_content = f_content.replace('--', '->')
        f.write(f_content)
        f.write('}')
    os.system('dot pic.dot -T png -o pic.png')
    OpenPic()
    ask = askokcancel('图片以生成', '是否保存')
    if not ask:
        remove('pic.dot')
        remove('pic.png')


def cancel_click():
    content.delete(0.0, END)


def text_change(event):
    global flag
    if flag:
        cancel_click()
        flag = False


flag = True
win = Tk()
win.title('Graphviz画图器')
content = Text(win, width=40, height=30, font="Helvetica 14 bold", bd=10, )
content.grid(row=0, columnspan=2)
content.bind('<BackSpace>', text_change)
content.insert(END, '输入图:\nx--y\n...')
dg = StringVar()
digraph = Radiobutton(win, text='有向图', var=dg, value='digraph')
graph = Radiobutton(win, text='无向图', var=dg, value='graph')
digraph.grid(column=0, row=1)
graph.grid(column=1, row=1)
verify = Button(win, text='确认', command=verify_click)
cancel = Button(win, text='清空', command=cancel_click)
verify.grid(column=0, row=2)
cancel.grid(column=1, row=2)


def main():
    win.mainloop()


if __name__ == '__main__':
    main()

from tkinter import *
from PIL import ImageTk
from qw_an import qw_an
from tkinter.messagebox import showinfo, askyesno
from pathlib import Path
import os
import random
import json
from pygame import mixer

mixer.init()
mixer.music.load('play.mp3')
mixer.music.play(-1)

root = Tk()
root.title("Who wants to become a millionaire?")
root.iconbitmap(default="icon.ico")
root.geometry("885x663")
root.resizable(width=False, height=False)

copied = qw_an.copy()
work_dict = {}
while len(work_dict) < 15:
    add = random.choice(list(copied))
    work_dict[add] = copied[add]


def get_rgb(rgb):
    return "#%02x%02x%02x" % rgb


def calc_prize():
    if 15 >= len(work_dict) > 10:
        return 0
    elif 10 >= len(work_dict) > 5:
        return money_list.get(10)
    elif 5 >= len(work_dict) > 0:
        return money_list.get(5)


def open_save():
    global work_dict
    with open('saves.txt') as svs:
        work_dict = json.loads(svs.read())
    Path('saves.txt').unlink()
    with open('help_btns_state.txt') as hbs:
        btn_call["state"], btn_crowd["state"], btn_fifty['state'] = hbs.read().strip().split(
            ' ')
    Path('help_btns_state.txt').unlink()


def save():
    with open('saves.txt', 'w') as svs:
        w_d_to_save = json.dumps(work_dict)
        svs.write(w_d_to_save)
    with open('help_btns_state.txt', 'w') as hbs:
        res = ''
        for i in (btn_call, btn_crowd, btn_fifty):
            res += i['state']+' '
        hbs.write(res)


def ask_open_save():
    result = askyesno(title="What to do?",
                      message="Do you want to continue last game?")
    if result:
        open_save()
    else:
        Path('saves.txt').unlink()
        Path('help_btns_state.txt').unlink()


def set_question():
    if os.path.exists('saves.txt'):
        ask_open_save()
    money_list.select_set(len(work_dict)-1)
    if len(work_dict) < 15:
        money_list.select_clear(len(work_dict), END)
    global a_a, a_b, a_c, a_d, q_l
    question = random.choice(list(work_dict))
    q_l = StringVar(value=question)
    a_a = StringVar(value=work_dict[question][0])
    a_b = StringVar(value=work_dict[question][1])
    a_c = StringVar(value=work_dict[question][2])
    a_d = StringVar(value=work_dict[question][3])
    btn_a = Button(textvariable=a_a, background=get_rgb((4, 2, 49)),
                   foreground="white", font="Arial 10 normal roman", command=lambda x=a_a.get(): check(x), wraplength=300)
    btn_a.place(relx=0.095, rely=0.807, width=320, height=50)
    btn_b = Button(textvariable=a_b, background=get_rgb((4, 2, 49)),
                   foreground="white", font="Arial 10 normal roman", command=lambda x=a_b.get(): check(x), wraplength=300)
    btn_b.place(relx=0.59, rely=0.807, width=320, height=50)
    btn_c = Button(textvariable=a_c, background=get_rgb((4, 2, 49)),
                   foreground="white", font="Arial 10 normal roman", command=lambda x=a_c.get(): check(x), wraplength=300)
    btn_c.place(relx=0.095, rely=0.911, width=320, height=50)
    btn_d = Button(textvariable=a_d, background=get_rgb((4, 2, 49)),
                   foreground="white", font="Arial 10 normal roman", command=lambda x=a_d.get(): check(x), wraplength=300)
    btn_d.place(relx=0.59, rely=0.911, width=320, height=50)
    question_label = Label(textvariable=q_l, background=get_rgb(
        (4, 2, 49)), foreground="white", font="Arial 12 normal roman", wraplength=600)
    question_label.place(relx=0.09, rely=0.6, width=700, height=100)


def show_res(text):
    showinfo(title="Result", message=text)


def try_again():
    global work_dict
    result = askyesno(title="You won!!! What to do?",
                      message="Play one more time?")
    if result:
        money_list.select_clear(len(work_dict)-1)
        work_dict = qw_an.copy()

        set_question()
    else:
        root.destroy()


def fifty():
    count = 0
    for i in (a_a, a_b, a_c, a_d):
        if work_dict[q_l.get()].index(i.get()) == work_dict[q_l.get()][4]:
            continue
        i.set(' ')
        count += 1
        if count == 2:
            btn_fifty['state'] = DISABLED
            break


def right_answer():
    for i in (a_a, a_b, a_c, a_d):
        if work_dict[q_l.get()].index(i.get()) == work_dict[q_l.get()][4]:
            continue
        i.set(' ')


def btn_call_click():
    right_answer()
    btn_call['state'] = DISABLED


def btn_crowd_click():
    right_answer()
    btn_crowd['state'] = DISABLED


def check(text):
    if work_dict[q_l.get()].index(text) == work_dict[q_l.get()][4]:
        msg = "Correct!"
        del work_dict[q_l.get()]
        if len(work_dict) != 0:
            show_res(msg)
            set_question()
        else:
            msg += f"You won 1638400"
            show_res(msg)
            money_list.select_clear(0)
            try_again()

    else:
        print(calc_prize())
        show_res(f"You failed! Your prize is:{calc_prize()}")


root.image = PhotoImage(file="back_grnd.png")
bg_logo = Label(root, image=root.image)
bg_logo.grid(row=0, column=0)

img_fifty = ImageTk.PhotoImage(file="fifty.png")
btn_fifty = Button(root, image=img_fifty, bd=0, command=fifty)
btn_fifty.place(relx=0.75, rely=0.02, height=36, width=54)

img_call = ImageTk.PhotoImage(file="call.png")
btn_call = Button(root, image=img_call, bd=0, command=btn_call_click)
btn_call.place(relx=0.82, rely=0.02, height=36, width=54)

img_crowd = ImageTk.PhotoImage(file="crowd.png")
btn_crowd = Button(root, image=img_crowd, bd=0, command=btn_crowd_click)
btn_crowd.place(relx=0.89, rely=0.02, height=36, width=54)


el = 100
m_l = [el]
for i in range(1, 15):
    el *= 2
    m_l.insert(0, el)
mon_list = Variable(value=m_l)
money_list = Listbox(listvariable=mon_list, background=get_rgb(
    (4, 4, 68)), foreground="yellow", font="Arial 12 normal roman", bd=0)
money_list.place(relx=0.76, rely=0.08, width=200, height=330)
money_list.select_set(first=END)

btn_start = Button(root, text="START", bd=0, background=get_rgb((4, 2, 49)),
                   foreground="white", font="Arial 15 normal roman", command=set_question)
btn_start.place(relx=0.01, rely=0.02, height=50, width=100)

btn_save = Button(root, text="Save", bd=0, background=get_rgb((4, 2, 49)),
                  foreground="white", font="Arial 15 normal roman", command=save)
btn_save.place(relx=0.01, rely=0.1, height=50, width=100)


root.mainloop()

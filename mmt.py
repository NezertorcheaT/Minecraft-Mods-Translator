import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile

import googletrans
from googletrans import Translator

print(
    """
        Welcome to Mods Translator!
        This is a program for translating Minecraft mods written by NezertorcheaT.
        To start working, select the original file with the .lang extension.
        Next, enter your language in the "Lang to" field.
        "Index" is the number of the line being edited.
        By entering a value in the "Input Index" field and pressing the "Set Index" button, you will instantly jump to the desired line.
        The button located under the translation input field is responsible for saving the data in a separate cell.
        It is this cell that will subsequently be saved to a separate file.
        Click this button every time you finish translating, otherwise nothing will be saved.
        You can automatically use Google Translate by clicking the "Try Google Translate" button.
        Finally you can save the translation file and send it to the mod creator by clicking the "Save" button.
        At the moment, this is the entire functionality of the program, but it will be expanded soon.
        
        __
        
        Добро пожаловать в Mods Translator!
        Это программа для перевода модов Minecraft, написанная NezertorcheaT.
        Для начала работы выберите исходный файл с расширением .lang.
        Затем введите свой язык в поле "Lang to".
        "Index" — это номер редактируемой строки.
        Введя значение в поле "Input Index" и нажав кнопку "Set Index", вы мгновенно перейдёте на нужную строку.
        Кнопка находящаяся под полем ввода перевода отвечает за сохранение данных в отдельную ячейку.
        Именно эта ячейка в последующем будет сохранена в отдельный файл.
        Нажимайте эту кнопку всякий раз, когда закончите переводить, иначе ничего не сохранится.
        Вы можете автоматически использовать Google Translate, нажав кнопку "Try Google Translate".
        Наконец, вы можете сохранить файл перевода и отправить его создателю мода, нажав кнопку "Save".
        На данный момент это весь функционал программы, но в скором времени он будет расширен.
    """
)
w = 16
h = 9


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def translt(text, lng):
    s = e.get()
    try:
        e.delete(0, 'end')
        e.insert(0, Translator().translate(text, src="en", dest=lng).text)
    except:
        e.insert(0, s)
        MsgBox = messagebox.askquestion(message='Type Language in "Language" field.\nShow languages array?',
                                        icon='error', title="Language Error")
        if MsgBox == 'yes':
            y = googletrans.LANGUAGES.keys()
            yy = ''
            for i in y:
                yy += str(i) + ', '
            messagebox.showinfo(title="Languages array", message=yy)


def update_all(add_num=0):
    global strings
    global index_tr
    index_tr = clamp(index_tr, 0, len(strings) - 1)
    l.config(text=strings[index_tr][0] + ": ")
    l2.config(text=strings_prew[index_tr][1])
    l3.config(text=f"Index: {index_tr + 1} of {len(strings)}. Language: ")
    strings[index_tr + add_num][1] = e.get()
    e.delete(0, tk.END)
    e.insert(0, strings[index_tr][1])
    b6.config(text=strings_save[index_tr][1])


def print_array(a):
    for i in range(len(a)):
        print(a[i])


def save():
    update_all()

    file = f'# Translated with Mods Translator\n'
    for i in range(len(strings_save)):
        file += strings_save[i][0] + "=" + strings_save[i][1] + '\n'
    new_file = asksaveasfile(title="Save mod .lang file", defaultextension=".lang",
                             filetypes=(("Text files", "*.lang"),))
    if new_file:
        new_file.write(file)
        new_file.close()


def save_to_clipboard():
    update_all()
    file = f'# Translated with Mods Translator\n'
    for i in range(len(strings_save)):
        file += strings_save[i][0] + "=" + strings_save[i][1] + '\n'
    win.clipboard_append(file)


def op():
    global index_tr
    global f
    global ff
    global strings_prew
    global strings
    global strings_save
    try:
        f = open(filedialog.askopenfilename(initialdir="/",
                                            title="Select a mod .lang file",
                                            filetypes=(("Text files",
                                                        "*.lang*"),
                                                       ("all files",
                                                        "*.*"))), 'r')
    except:
        MsgBox = messagebox.askquestion(message='A file selection error has occurred.\nExit or try again?',
                                        icon='error', title="File Error")
        if MsgBox == 'yes':
            win.destroy()
        else:
            op()
            return

    strings = []
    strings_prew = []
    strings_save = []
    ff = f.read()
    f.close()
    ff = re.sub(r"#.*", "", ff, flags=re.M)
    ff = re.sub(r"^[^\w\d]", "", ff, flags=re.M)
    result = re.findall(r".+[=]|.+$", ff, flags=re.M)
    k = 0
    for i in result:
        k += 1
        if k % 2 == 0:
            a = result[k - 2]
            a = re.sub(r"=$", "", a, flags=re.M)
            strings.append([a, i])
            strings_prew.append([a, i])
            strings_save.append([a, i])


index_tr = 0
win = tk.Tk()
w = win.winfo_screenwidth()
h = win.winfo_screenheight()
# photo = tk.PhotoImage(file=r'D:\BeckUP\Backgrounds\YouTube\ikon5 - копия.png')
win.geometry(f"{w}x{h}")
# win.iconphoto(False, photo)
win.title("Mods Translator")
win.config(bg='#383838')
win.resizable(False, False)


# print_array(strings)
def make_menu(w):
    global the_menu
    the_menu = tk.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")


def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
                            command=lambda: w.event_generate("<<Cut>>"))

    the_menu.entryconfigure("Copy",
                            command=lambda: w.event_generate("<<Copy>>"))

    the_menu.entryconfigure("Paste",
                            command=lambda: w.event_generate("<<Paste>>"))

    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)


def dele(e):
    global l2
    l2['text'] = ''
    e.delete(0, tk.END)


def next_s():
    global index_tr
    index_tr += 1
    update_all(add_num=-1)


def prew_s():
    global index_tr
    index_tr -= 1
    update_all(add_num=1)


def index_set():
    global index_tr
    try:
        index_tr = int(e3.get()) - 1
    except:
        messagebox.showerror(message='Type number', title="Input Error")

    update_all(add_num=1)


def save_to_str_s():
    update_all()
    strings_save[index_tr][1] = e.get()
    update_all()


def clear():
    for widget in frame.winfo_children():
        widget.destroy()


make_menu(win)
canvas = tk.Canvas(win, height=h, width=w)
canvas.pack()
frame = tk.Frame(canvas, bg='#383838')
frame.place(relheight=1, relwidth=1)

op()

l = tk.Label(frame, text=strings[index_tr][0] + ": ", justify=tk.LEFT)
l2 = tk.Label(frame, text=strings[index_tr][1], justify=tk.LEFT, wraplength=w - 200)
l3 = tk.Label(frame, text=f"Index: {index_tr + 1} of {len(strings)}. Language: ", justify=tk.RIGHT)
l4 = tk.Label(frame, text=f"Input index:", justify=tk.RIGHT)
e = tk.Entry(frame)
e2 = tk.Entry(frame)
e3 = tk.Entry(frame)
e.delete(0, tk.END)
e.insert(0, strings[index_tr][1])
b = tk.Button(frame,
              text='Try Google Translate',
              command=lambda: translt(e.get(), e2.get())
              )
b2 = tk.Button(frame,
               text='Next ->',
               command=next_s
               )
b3 = tk.Button(frame,
               text='<- Prew',
               command=prew_s
               )
b4 = tk.Button(frame,
               text='Save',
               command=save
               )
b5 = tk.Button(frame,
               text='Set index',
               command=index_set
               )
b6 = tk.Button(frame,
               text='',
               command=save_to_str_s,
               justify=tk.LEFT,
               wraplength=max(w - 200, 200)
               )
b7 = tk.Button(frame,
               text='Add all text to clipboard',
               command=save_to_clipboard,
               justify=tk.LEFT,
               wraplength=max(w - 200, 200)
               )
strings[index_tr][1] = e.get()
e.delete(0, tk.END)
e.insert(0, strings[index_tr][1])

l3.grid(row=0, column=0, stick="we")
e2.grid(row=0, column=1, stick="we")
b4.grid(row=0, column=2, stick="we")

l4.grid(row=0, column=3, stick="we")
e3.grid(row=0, column=4, stick="we")
b5.grid(row=0, column=5, stick="we")

l.grid(row=1, column=0, stick="we")
l2.grid(row=2, column=0, stick="we", columnspan=6)

e.grid(row=4, column=0, stick="we", columnspan=6)
e.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
b6.grid(row=5, column=0, stick="we", columnspan=6)
b3.grid(row=1, column=1, stick="we")
b.grid(row=1, column=2, stick="we")
b2.grid(row=1, column=3, stick="we")
b7.grid(row=6, column=0, stick="we")

update_all()

win.mainloop()

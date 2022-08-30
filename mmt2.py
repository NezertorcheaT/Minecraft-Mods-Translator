import codecs
import json
import re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.font import *

import googletrans
from googletrans import Translator


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def translt(text, lng, ee):
    s = ee.get('1.0', 'end-1c')
    b = s
    try:
        b = Translator().translate(text, src="en", dest=lng).text
    except ValueError:
        b = s
        MsgBox = messagebox.askquestion(message='Type Language in "Language" field.\nShow languages array?',
                                        icon='error', title="Language Error")
        if MsgBox == 'yes':
            y = googletrans.LANGUAGES.keys()
            yy = ''
            for i in y:
                yy += str(i) + ', '
            messagebox.showinfo(title="Languages array", message=yy)
    ee.delete('1.0', END)
    ee.insert('1.0', b)


def save():
    isJsonp = messagebox.askyesno(message='Yes=.json\nNo=.lang',
                                  icon='error', title="Select file type")
    if not isJsonp:
        file = '# Translated with Mods Translator\n'
        for i in range(len(strings_save)):
            file += strings_save[i][0] + u"=" + strings_save[i][1] + '\n'
        new_file = asksaveasfilename(title="Save mod .lang\.json file", defaultextension=".lang",
                                     filetypes=[("Lang files", "*.lang")])
    else:
        file = ''
        d = {}
        d.update({"_comment": 'Translated with Mods Translator'})
        for i in strings_save:
            d.update({i[0]: i[1]})
        file = json.dumps(d, indent=2)
        new_file = asksaveasfilename(title="Save mod .lang\.json file", defaultextension=".json",
                                     filetypes=[("Json files", "*.json")])
    if new_file:
        if isJsonp:
            with codecs.open(new_file, "w", "utf-8-sig") as temp:
                temp.write(file.encode('utf8').decode("unicode_escape"))
        else:
            with open(new_file, 'w', encoding='utf-8') as s:
                s.write(file)


def save_to_clipboard():
    # update_all()

    if not isJson:
        file = u'# Translated with Mods Translator\n'
        for i in range(len(strings_save)):
            file += strings_save[i][0] + u"=" + strings_save[i][1] + '\n'
    else:
        file = u''
        d = {}
        for i in strings_save:
            d.update({i[0]: i[1]})
        file = json.dumps(d, indent=2)
    win.clipboard_clear()
    win.clipboard_append(file.encode('utf8').decode("unicode_escape"))


def op():
    global isJson
    isJson = False
    MsgBox = messagebox.askquestion(message='Yes=.json\nNo=.lang',
                                    icon='error', title="Select file type")
    if MsgBox == 'yes':
        isJson = True
    else:
        isJson = False
    global index_tr
    global f
    global ff
    global strings_prew
    global strings
    global strings_save
    try:
        if not isJson:
            f = open(filedialog.askopenfilename(initialdir="/",
                                                title="Select a mod .lang file",
                                                filetypes=(("Text files",
                                                            "*.lang*"),
                                                           ("all files",
                                                            "*.*"))), 'r')
        else:
            f = open(filedialog.askopenfilename(initialdir="/",
                                                title="Select a mod .json file",
                                                filetypes=(("Text files",
                                                            "*.json*"),
                                                           ("all files",
                                                            "*.*"))), 'r')
    except:
        MsgBox = messagebox.askquestion(message='A file selection error has occurred.\nExit or try again?',
                                        icon='error', title="File Error")
        if MsgBox == 'yes':
            win.destroy()
            raise RuntimeError
        else:
            op()
            return

    strings = []
    strings_prew = []
    strings_save = []
    ff = f.read()
    f.close()
    if not isJson:
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
    else:
        result = json.loads(ff)
        for i in result:
            strings.append([i, result[i]])
        result1 = json.loads(ff)
        for i in result:
            strings_save.append([i, result[i]])
        result2 = json.loads(ff)
        for i in result:
            strings_prew.append([i, result[i]])


index_tr = 0
win = Tk()
photo = PhotoImage(file=r'D:\BeckUP\Backgrounds\YouTube\ikon5 - копия.png')
w = 640
h = 300
win.geometry(f"{w}x{h}")
win.iconphoto(False, photo)
win.title("Minecraft Mods Translator")
win.config(bg='#383838')
win.resizable(False, False)
ifont = Font(family='Raavi', size=9)


def make_menu(w):
    global the_menu
    the_menu = Menu(w, tearoff=0)
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


def save_to_str_s(a, ee, gl):
    strings_save[a][1] = ee.get()
    ee.config(bg='green')
    gl.config(text=ee.get())


def save_to_str_w2(a, ee, l82, ev):
    strings_save[a][1] = ee.get("1.0", "end-1c")
    ev.delete(0, END)
    ev.insert(0, ee.get("1.0", "end-1c"))
    l82.config(text=ee.get("1.0", "end-1c"))


def clear():
    for widget in frame.winfo_children():
        widget.destroy()


def redactCopy(win2, a=int):
    win2.clipboard_clear()
    win2.clipboard_append(strings[a][1])
    print(strings)
    print(strings_save)


def redact(l2, ef, a=int):
    win2 = Tk()
    w2 = 600
    h2 = 400
    win2.geometry(f"{w2}x{h2}")
    win2.title("Translate")
    win2.config(bg='#383838')
    win2.resizable(False, False)
    canvas2 = Canvas(win2, height=win2.winfo_height(), width=win2.winfo_width())
    textEditor = Text(canvas2, font=ifont)
    textEditor.insert(1.0, strings_save[a][1])
    textEditor.bind_class("Text", "<Button-3><ButtonRelease-3>", show_menu)
    bgrid = Frame(win2, bg='#383838')
    l22 = Button(bgrid, text="Copy original", command=lambda win2=win2, a=a: redactCopy(win2, a), anchor="w",
                 font=ifont)
    b22 = Button(bgrid, text="Save",
                 command=lambda a=a, textEditor=textEditor, l2=l2, e=e: save_to_str_w2(a, textEditor, l2, ef),
                 anchor="w", font=ifont)
    b21 = Button(bgrid,
                 text='Try Google Translate',
                 command=lambda e=e: translt(textEditor.get(1.0, 'end-1c'), e2.get(), textEditor),
                 anchor="w", font=ifont
                 )
    textEditor.pack()
    l22.grid(column=0, row=0)
    b22.grid(column=1, row=0)
    b21.grid(column=2, row=0)
    bgrid.pack(fill=X)
    canvas2.pack()
    print(strings)
    print(strings_save)


def StringVarCallback(ee, sv, a):
    if sv.get() == strings_save[a][1]:
        ee.config(bg='green')
    elif sv.get() != strings[a][1]:
        ee.config(bg='red')
    else:
        ee.config(bg='blue')


make_menu(win)
canvas = Canvas(win, height=win.winfo_height(), width=win.winfo_width())
canvas.pack(fill="both")
frame = Frame(canvas, bg='#383838')
frame.pack(fill="both")

op()

frame2 = Frame(canvas, bg='#383838')
frame2.pack(fill="both", expand=1)
my_canvas = Canvas(frame2, bg='#383838')
my_canvas.pack(side=LEFT, fill="both", expand=1)
my_scrollbar = ttk.Scrollbar(frame2, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
second_frame = Frame(my_canvas, bg='#383838')
my_canvas.create_window((0, 0), window=second_frame, anchor='nw')

for i in range(len(strings)):
    sv = StringVar()
    e = Entry(second_frame, bg='blue')
    sv.trace("w", lambda name, index, mode, i=i, e=e, sv=sv: StringVarCallback(e, sv, i))
    e.config(textvariable=sv)
    l = Label(second_frame, text=strings[i][0] + ": ", justify=LEFT, anchor="w", width=13, font=ifont)
    l2 = Button(second_frame, text=strings[i][1], justify=LEFT, width=50,
                anchor="w", font=ifont)
    l2.config(command=lambda l2=l2, e=e, i=i: redact(l2, e, i))
    l.grid(row=2 + i, column=0, stick="we")
    l2.grid(row=2 + i, column=1, stick="we")
    b6 = Button(second_frame,
                text='Enter',
                command=lambda i=i, e=e, l2=l2: save_to_str_s(i, e, l2),
                justify=LEFT,
                wraplength=max(w - 200, 200),
                anchor="w", font=ifont
                )
    e.delete(0, END)
    e.insert(0, strings[i][1])
    e.grid(row=2 + i, column=2, stick="we")
    e.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
    e.delete(0, END)
    e.insert(0, strings[i][1])
    b6.grid(row=2 + i, column=3, stick="we")

e2 = Entry(frame)

b4 = Button(frame,
            text='Save',
            command=save, font=ifont
            )

b7 = Button(frame,
            text='Add all text to clipboard',
            command=save_to_clipboard,
            justify=LEFT,
            wraplength=max(w - 200, 200), font=ifont
            )
ll = Label(frame, text='Language:', anchor='w', font=ifont)
ll.grid(row=0, column=0, stick="we")
e2.grid(row=0, column=1, stick="we")
b4.grid(row=0, column=2, stick="we")

b7.grid(row=0, column=3, stick="we")

# update_all()

win.mainloop()

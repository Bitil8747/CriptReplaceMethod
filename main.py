from functools import partial
from tkinter import *
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import random
import time
import math
from matplotlib.figure import Figure


def CryptFile():
    global file_name
    file_name = fd.askopenfilename()
    text2.delete(1.0, END)
    text2.insert(1.0, "Файл %s выбран!" % file_name)


def Crypt():
    global file_name, alphabet
    text2.delete(1.0, END)
    if(text1.get(1.0, END) == text2.get(1.0, END)):
        wordCount = [0 for i in range(len(alphabet))]
        criptMessage = []
        exist = False
        text = []
        lenght = 0
        text2.delete(1.0, END)
        text1.delete(1.0, END)

        with open(file_name, 'r', encoding='utf-8') as file:
            for char in iter(partial(file.read, 1), ''):
                for j in range(len(alphabet)):
                    if (char.lower() == alphabet[j]):
                        wordCount[j] += 1
                        criptMessage.append(alpList[j])
                        exist = True
                        lenght += 1
                if (exist == False):
                    criptMessage.append(char)
                else:
                    exist = False
        # text2.insert(1.0,''.join(criptMessage))
        text2.insert(1.0, "Файл %s зашифрован!" % file_name)

        with open("C:/Users/Airat/Desktop/lab1_cript.txt", 'w', encoding='utf-8') as file:
            file.write(''.join(criptMessage))

        RefreshGraf(wordCount, lenght)
    else:
        message = list(text1.get(1.0, END))
        criptMessage = []
        wordCount = [0 for i in range(len(alphabet))]
        exist = False
        lenght = len(message) - 1
        for i in range(len(message)):
            for j in range(len(alphabet)):
                if (message[i].lower() == alphabet[j]):
                    wordCount[j] += 1
                    criptMessage.append(alpList[j])
                    exist = True
            if (exist == False):
                criptMessage.append(message[i])
            else:
                exist = False
        text2.insert(1.0, ''.join(criptMessage))
        RefreshGraf(wordCount, lenght)


def DeCrypt():
    global file_name
    text2.delete(1.0, END)
    if(text1.get(1.0, END) == text2.get(1.0, END)):
        text1.delete(1.0, END)
        criptMessage = []
        wordCount = [0 for i in range(len(alphabet))]
        exist = False
        lenght = 0

        with open(file_name, 'r', encoding='utf-8') as file:
            for char in iter(partial(file.read, 1), ''):
                for j in range(len(alpList)):
                    if (char.lower() == alphabet[j]):
                        wordCount[j] += 1
                    if (char.lower() == alpList[j]):
                        criptMessage.append(alphabet[j])
                        exist = True
                        lenght += 1
                if (exist == False):
                    criptMessage.append(char)
                else:
                    exist = False
        # text2.insert(1.0, ''.join(criptMessage))
        text2.insert(1.0, "Файл %s расшифрован!" % file_name)

        with open("C:/Users/Airat/Desktop/lab1_decript.txt", 'w', encoding='utf-8') as file:
            file.write(''.join(criptMessage))

        
        RefreshGraf(wordCount, lenght)
    else:
        message = list(text1.get(1.0, END))
        deCriptMessage = []
        wordCount = [0 for i in range(len(alphabet))]
        exist = False
        lenght = len(message) - 1
        for i in range(len(message)):
            for j in range(len(alpList)):
                if (message[i].lower() == alpList[j]):
                    deCriptMessage.append(alphabet[j])
                    exist = True
                if (message[i].lower() == alphabet[j]):
                    wordCount[j] += 1
            if (exist == False):
                deCriptMessage.append(message[i])
            else:
                exist = False
        text2.insert(1.0, ''.join(deCriptMessage))

        RefreshGraf(wordCount, lenght)


def GenerateTable():
    global alpList
    l = list(alphabet)
    random.shuffle(l)
    alpList = ''.join(l)
    label1.config(text=alpList)


def SetTable():
    global alpList
    alpList = entry.get()
    label1.config(text=alpList)


def DownloadTable():
    global alpList
    file_name = fd.askopenfilename()
    file = open(file_name, 'r', encoding='utf-8')
    alpList = ''.join(list(file.read()))
    label1.config(text=alpList)


def SaveKey():
    global alpList
    with open("C:/Users/Airat/Desktop/lab1_key.txt", 'w', encoding='utf-8') as file:
        file.write(alpList)

def RefreshGraf(wordCount, lenght):
    figure = Figure(figsize=(8, 2))
    figure.set_facecolor("#AA96DA")
    figure.set_dpi(80)
    s = figure.add_subplot(1, 1, 1)
    proc = [0 for a in range(len(wordCount))]
    alphabet_sort = list(alphabet)
    for i in range(len(wordCount)):
        proc[i] = (wordCount[i] / lenght) * 100
    for i in range(len(proc)):
        minimum = i
        for j in range(i + 1, len(proc)):
            # Выбор наименьшего значения
            if proc[j] < proc[minimum]:
                minimum = j
        # Помещаем это перед отсортированным концом массива
        proc[minimum], proc[i] = proc[i], proc[minimum]
        alphabet_sort[minimum], alphabet_sort[i] = alphabet_sort[i], alphabet_sort[minimum]
    alphabet_sort.reverse()
    proc.reverse()
    s.bar(alphabet_sort, proc)
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=410, y=430)

    #Вычисляем энтропию
    Introp = 0
    for i in range((len(wordCount))):
        if(wordCount[i] == 0):
            Introp += 0
        else: Introp += (wordCount[i] / lenght) * math.log2(wordCount[i] / lenght)
    IntropText = "H(X) = " + "%s" %-Introp
    label2.config(text=IntropText)


def FricqAnalise():
    global file_name, alpList, alphabet
    f = [0 for i in range(len(alphabet))]
    max = 0
    criptMessage = []
    wordCount = [0 for i in range(len(alphabet))]
    key = ['' for i in range(len(alphabet))]
    ref = " оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъё"
    wordCountTmp = [0 for i in range(len(alphabet))]
    exist = False
    text2.delete(1.0, END)
    if (text1.get(1.0, END) == text2.get(1.0, END)):
        text1.delete(1.0, END)
        lenght = 0
        with open(file_name, 'r', encoding='utf-8') as file:
            for char in iter(partial(file.read, 1), ''):
                for j in range(len(alphabet)):
                    if (char.lower() == alphabet[j]):
                        wordCount[j] += 1
                        wordCountTmp[j] += 1
                        lenght += 1
            #найдем примерный ключ по частоте встречаемости букв в тексте
            for i in range(0, len(alphabet)):
                max = 0
                for k in range(0, len(wordCountTmp)):
                    if(wordCountTmp[k] > wordCountTmp[max]):
                        max = k
                for c in range(len(alphabet)):
                    if(list(ref)[i] == alphabet[c]):
                        key[c] = alphabet[max]
                wordCountTmp[max] = -1
            alpList = key
            #расшифруем текст с использованием полученного ключа
            file.seek(0)
            for char in iter(partial(file.read, 1), ''):
                for l in range(len(alphabet)):
                    if (char.lower() == alpList[l]):
                        exist = True
                        criptMessage.append(alphabet[l])
                if (exist == False):
                    criptMessage.append(char)
                else:
                    exist = False

            alpList = ''.join(alpList)
            file.seek(0)
            text1.insert(1.0, ''.join(file.read()))
            text2.insert(1.0, ''.join(criptMessage))
            label1.config(text=alpList)


            RefreshGraf(wordCount, lenght)





## Создаем рабочее окно программы
global alpList, file_name, alphabet

matplotlib.use('TkAgg')

root = Tk()
root.title("Программная реализация шифра замены")
root.geometry("990x600")
root.resizable(False, False)

canvas = Canvas(width=990, height=600, bg="#AA96DA")
canvas.place(x=0,y=0)

text1 = Text(width=60, height=20, bg="#FFFFD2", fg='#1C1C1C', wrap=WORD)
text1.place(x=4, y=4)

text2 = Text(width=60, height=20,bg="#FFFFD2", fg='#1C1C1C', wrap=WORD)
text2.place(x=500, y=4)

button1 = Button(root, text="Обзор", bg="#FCBAD3", fg='#1C1C1C', command=CryptFile)
button1.place(x=320, y=340)
button2 = Button(root, text="Зашифровать текст", bg="#FCBAD3", fg='#1C1C1C', command=Crypt)
button2.place(x=370, y=340)
button3 = Button(root, text="Расшифровать текст", bg="#FCBAD3", fg='#1C1C1C', command=DeCrypt)
button3.place(x=500, y=340)

label = Label(root, text="Таблица замены: ", bg="#95E1D3", fg='#1C1C1C')
label.place(x=4, y=410)
label1 = Label(root, text="-", bg="#95E1D3", fg='#1C1C1C')
label1.place(x=114, y=410)

entry = Entry(root, width=40, bg="#FFFFD2", fg='#1C1C1C')
entry.place(x=4, y=440)
button5 = Button(root, text="Задать ключ", bg="#FCBAD3", fg='#1C1C1C', command=SetTable)
button5.place(x=6, y=470)

button6 = Button(root, text="Сгенерировать ключ", bg="#FCBAD3", fg='#1C1C1C', command=GenerateTable)
button6.place(x=6, y=500)
button7 = Button(root, text="Загрузить ключ из файла", bg="#FCBAD3", fg='#1C1C1C', command=DownloadTable)
button7.place(x=6, y=530)
button8 = Button(root, text="Сохранить ключ в файл", bg="#FCBAD3", fg='#1C1C1C', command=SaveKey)
button8.place(x=6, y=560)
label2 = Label(root, text="", bg="#AA96DA", fg='#1C1C1C')
label2.place(x=490, y=410)
button9 = Button(root, text="Частотный анализ", bg="#FCBAD3", fg='#1C1C1C', command=FricqAnalise)
button9.place(x=630, y=340)


alpList = ''
file_name = ''
alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "

GenerateTable()

root.mainloop()
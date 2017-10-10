import urllib.request
import tkinter
from tkinter import *


class StockParser():
    def __init__(self, code_data, edit):
        self.stock_data = code_data
        self.edit = edit

        if self.stock_data.split('"')[1] == '':
            pass
        else:
            print(self.stock_data.split('"')[1])
            self.stock_data = self.stock_data.split('"')[1]
            name = self.stock_data.split(',')[0]
            opening_price = float(self.stock_data.split(',')[1])
            closing_price = float(self.stock_data.split(',')[2])
            price = float(self.stock_data.split(',')[3])
            high = float(self.stock_data.split(',')[4])
            low = float(self.stock_data.split(',')[5])

            self.edit.insert(END, [name, opening_price, closing_price, high, low, price, ])


class Window:
    def __init__(self, root):
        #輸入與按鈕布局
        self.root = root
        self.entryUrl = tkinter.Entry(root, width=20)
        self.entryUrl.place(x=50, y=13)
        self.get = tkinter.Button(root, text='查詢', command=self.Get)
        self.get.place(x=200, y=10)
        self.add = tkinter.Button(root, text='添加', command=self.Add)
        self.delete = tkinter.Button(root, text='删除', command=self.Del)
        self.add.place(x=80, y=55)
        self.delete.place(x=120, y=55)
        #frame布局
        self.frame = tkinter.Frame(root, bd=2)
        self.frame.place(x=200, y=90)
        self.scrollbar = tkinter.Scrollbar(self.frame)
        self.edit = tkinter.Listbox(self.frame, yscrollcommand=self.scrollbar.set,
                                    width=50, height=10)
        self.scrollbar.config(command=self.edit.yview)

        self.edit.grid(row=1, column=2)
        self.scrollbar.grid(row=1, column=3, sticky='ew')

        self.indicate = tkinter.Label(root, text='(Please input stock code:sh000000)', fg='red')
        self.indicate.place(x=50, y=35)
        self.StockList = []

    def ListUpdate(self):
        self.lb = tkinter.Listbox(self.root, selectmode=BROWSE)
        for code in self.StockList:
            self.lb.insert(END, code)
        self.lb.pack()
        self.lb.place(x=50, y=90)

    def Add(self):
        code = self.entryUrl.get()
        #判斷匹配 是否為前2字母 後6數字
        if re.match(r'\w{2}\d{6}$', code) and code not in self.StockList:
            self.StockList.append(code)
        else:
            pass
        self.ListUpdate()

    def Del(self):
        code = self.entryUrl.get()
        if code in self.StockList:
            self.StockList.remove(code)
        self.ListUpdate()

    def Get(self):
        if self.edit.get(0):
            print(self.edit.get(0))
            self.edit.delete(0, END)
        self.edit.insert(END, ['名 字', '開盤價', '關盤價', '最高', '最低', '當前價格'])
        for code in self.StockList:

            #股票爬蟲 大陸股票的數據對接口
            url = 'http://hq.sinajs.cn/list=%s' % (code,)
            page = urllib.request.urlopen(url)
            html = page.read()
            stock_data = html.decode('gb2312')

            hp = StockParser(stock_data, self.edit)


def main():
    root = tkinter.Tk()
    root.title('簡易股票查詢')
    window = Window(root)
    root.minsize(600, 300)
    root.maxsize(600, 300)
    root.mainloop()


if __name__ == '__main__':
    main()
import tkinter as tk
from tkinter import messagebox
import pickle
import time
import csv
import os

window = tk.Tk()
window.title('物品租借系統')
window.geometry('750x475')
window.resizable(0,0)

path = "C:\ rentSysData"
if not os.path.isdir(path):
    os.mkdir(path)
pathname = path + '\ '

ava =False   #管理員登入與否
ad_check = False  #管理員確認與否
admin_button = '管理員'
Time = ''
check = ''   #判別新增、刪除、歸還之狀況
data_check = []
end = False


def intoPickle(num,name,state,time,person,ps):
    info ={num:{'name':name,'state':state,'time':time,'person':person,'ps':ps}}
    return info

def takeTime():
    global Time
    Time = time.strftime("%Y/%m/%d")+'--'+ time.strftime("%H:%M")
    return Time

#管理員登入
def admin_login():
    global ava
    global admin_button

    if ava == False:
        def logout_confirm():
            global ava
            ava = False
            window_login.destroy()
            tk.messagebox.showerror(message='log out !!')

        def login_confirm():
            global ava
            global admin_button
            global btn_admin_login
            an = admin_name.get()
            ap = admin_pwd.get()
            try:
                with open(pathname + 'admin_info.pickle', 'rb') as admin_file:
                    admin_info = pickle.load(admin_file)
            except FileNotFoundError:
                with open(pathname + 'admin_info.pickle', 'wb') as admin_file:
                    admin_info = {'admin': 'admin'}
                    pickle.dump(admin_info, admin_file)

            if an in admin_info:
                if ap == admin_info[an]:
                    ava = True
                    window_login.destroy()
                    btn_admin_login.configure(text='管理員登出')
                    tk.messagebox.showerror(message='log in !!')

                else:
                    tk.messagebox.showerror(message='Error, your password is wrong, try again.')
            else:
                tk.messagebox.showerror(message='Error, you have not sign up yet')

        window_login = tk.Toplevel(window)
        window_login.geometry('250x150')
        window_login.title('管理員控制')

        admin_name = tk.StringVar()
        tk.Label(window_login, text='管理員帳號: ').place(x=10, y=10)
        entry_admin_name = tk.Entry(window_login, textvariable=admin_name)
        entry_admin_name.place(x=80, y=10)

        admin_pwd = tk.StringVar()
        tk.Label(window_login, text='管理員密碼: ').place(x=10, y=50)
        entry_admin_pwd = tk.Entry(window_login, textvariable=admin_pwd, show='*')
        entry_admin_pwd.place(x=80, y=50)

        btn_login = tk.Button(window_login, text='登入', command=login_confirm, width=5)
        btn_login.place(x=60, y=100)

        btn_login = tk.Button(window_login, text='登出', command=logout_confirm, width=5)
        btn_login.place(x=140, y=100)
    else:
        ava = False
        tk.messagebox.showerror(message='log out !!')
        btn_admin_login.configure(text='管理員登入')
#管理員確認
def admin_check():
    global ad_check
    global check
    global end

    def check_confirm():
        global ad_check
        global check
        global end

        an = var_usr_name.get()
        cp = check_pwd.get()
        try:
            with open(pathname + 'admin_info.pickle', 'rb') as admin_file:
                admin_info = pickle.load(admin_file)
        except FileNotFoundError:
            with open(pathname + 'admin_info.pickle', 'wb') as admin_file:
                admin_info = {'admin': 'admin'}
                pickle.dump(admin_info, admin_file)
        if check == 'new':
            if an in admin_info:
                if cp == admin_info[an]:
                    ad_check = True
                    check_login.destroy()
                    new()
                else:
                    tk.messagebox.showerror(message='Error, your password is wrong, try again.')
            else:
                tk.messagebox.showerror(message='Error, you are not admin')
        elif check == 'delet':
            if an in admin_info:
                if cp == admin_info[an]:
                    ad_check = True
                    check_login.destroy()
                    delet()
                else:
                    tk.messagebox.showerror(message='Error, your password is wrong, try again.')
            else:
                tk.messagebox.showerror(message='Error, you are not admin')
        else:
            for i in admin_info:
                if cp == admin_info[i]:
                    ad_check = True
                    check_login.destroy()
                    if check == 'turn':
                        turnback()
                    elif check == 'adv':
                        how_use()
                    elif check == 'add_admin':
                        end = True
                        add_admin()
                    elif check == 'delete_admin':
                        end = True
                        delete_admin()

    check_login = tk.Toplevel(window)
    check_login.geometry('250x150')
    check_login.title('管理員確認')

    check_pwd = tk.StringVar()
    tk.Label(check_login, text='管理員密碼: ').place(x=10, y=30)
    check_admin_pwd = tk.Entry(check_login, textvariable=check_pwd, show='*')
    check_admin_pwd.place(x=80, y=30)

    check_btn_login = tk.Button(check_login, text='登入', command=check_confirm, width=5)
    check_btn_login.place(x=100, y=80)
    return


#新增
def new():
    global ava
    global check
    global ad_check

    check = 'new'
    if ava == False:
        tk.messagebox.showerror(message='請先登入管理員')
    else:
        if ad_check == True:
            st_num = var_stuff.get()
            st_name = var_ps.get()
            st_time = takeTime()

            try:
                with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
                    stuff_info = pickle.load(stuff_file)
                with open(pathname + 'stuff_info.pickle', 'wb') as stuff_file:
                    stuff_info.update(intoPickle(st_num, st_name, True, st_time, '管理員', '新增'))
                    pickle.dump(stuff_info, stuff_file)

            except FileNotFoundError:
                with open(pathname + 'stuff_info.pickle', 'wb') as stuff_file:
                    stuff_info = intoPickle(st_num, st_name, True, st_time, '管理員', '新增')
                    pickle.dump(stuff_info, stuff_file)
            show_rec(st_name, '新增', '管理者', '')
            tk.messagebox.showerror(message='新增一物品')
            stuff_ava_get()
            ad_check =False
        else:
            admin_check()
#刪除
def delet():
    global ava
    global check
    global ad_check

    check = 'delet'
    if ava == False:
        tk.messagebox.showerror(message='請先登入管理員')
    else:
        if ad_check == True:
            try:
                st_num = var_stuff.get()
                with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
                    stuff_info = pickle.load(stuff_file)

                if st_num in stuff_info:
                    st_name = stuff_info[st_num]['name']
                    del stuff_info[st_num]
                    with open(pathname + 'stuff_info.pickle', 'wb') as stuff_file:
                        pickle.dump(stuff_info, stuff_file)
                    tk.messagebox.showerror(message='刪除一物品')
                    show_rec(st_name, '刪除', '管理者', '')
                else:
                    tk.messagebox.showerror(message='無該項物品')
                stuff_ava_get()
            except FileNotFoundError:
                tk.messagebox.showerror(message='物品清單尚未建立')
            ad_check = False
        else:
            admin_check()
#借出
def rent():
    global ava
    rent_check = False #判斷實際借出與否

    if ava == False:
        tk.messagebox.showerror(message='請先登入管理員')
    else:
        st_person = var_usr_name.get()
        st_num = data_processing()
        if st_num == []:
            tk.messagebox.showerror(message='租借暫存區尚無物品')
        st_ps = var_ps.get()

        try:
            with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
                stuff_info = pickle.load(stuff_file)
        except FileNotFoundError:
            tk.messagebox.showerror(message='沒有物品可借，請管理員新增')

        for i in st_num:
            if stuff_info[i]['state'] == True:
                stuff_info[i]['person'] = st_person
                stuff_info[i]['ps'] = st_ps
                stuff_info[i]['state'] = False
                rent_check = True
            else:
                tk.messagebox.showerror(message=stuff_info[i]['name']+'已借出')
            show_rec(stuff_info[i]['name'], '被借出', st_person, '')

        with open(pathname + 'stuff_info.pickle', 'wb') as stuff_file:
            pickle.dump(stuff_info, stuff_file)
        if rent_check == True:
            tk.messagebox.showerror(message='借出物品')


        stuff_ava_get()
#歸還
def turnback():
    global ava
    global check
    global ad_check
    turn_check = False
    check ='turn'

    if ava == False:
        tk.messagebox.showerror(message='請先登入管理員')
    else:
        if ad_check == True:
            st_person = var_usr_name.get()
            st_num = data_processing()
            if st_num == []:
                tk.messagebox.showerror(message='租借暫存區尚無物品')

            try:
                with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
                    stuff_info = pickle.load(stuff_file)
            except FileNotFoundError:
                tk.messagebox.showerror(message='沒有物品可歸還，請管理員新增')

            for i in st_num:
                if stuff_info[i]['state'] == False:
                    if stuff_info[i]['person'] == st_person:
                        stuff_info[i]['person'] == '管理員'
                        stuff_info[i]['state'] = True
                        turn_check = True
                        show_rec(stuff_info[i]['name'], '被歸還', st_person, '')
                    else:
                        tk.messagebox.showerror(message='請以'+stuff_info[i]['person']+'之身分歸還'+stuff_info[i]['name'])
                else:
                    tk.messagebox.showerror(message=stuff_info[i]['name']+'已歸還')


            with open(pathname + 'stuff_info.pickle', 'wb') as stuff_file:
                pickle.dump(stuff_info, stuff_file)

            if turn_check == True:
                tk.messagebox.showerror(message='歸還物品')


            stuff_ava_get()
            ad_check =False
        else:
            admin_check()


#讀取存檔資料
def read_file():
    global pathname
    try:
        with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
            stuff_info = pickle.load(stuff_file)
            return stuff_info
    except FileNotFoundError:
        tk.messagebox.showerror(message='Error, there is no stuff')
        stuff_info = ''
        return stuff_info

#顯示stuff狀態
def stuff_ava_get():
    try:
        with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
            stuff_info = pickle.load(stuff_file)
    except FileNotFoundError:
        tk.messagebox.showerror(message='Error, there is no stuff')
        stuff_info = ''

    list.delete(0,'end')

    if stuff_info == '':
        pass
    else:
        for i in stuff_info:
            if stuff_info[i]['state'] == False:
                message = stuff_info[i]['name'] +'(已借出)'
                list.insert('end',message)
            else:
                message = stuff_info[i]['name'] +'(可借)'
                list.insert('end', message)

#顯示租借紀錄
def show_rec(name,state,person,ps):
    # rec_show = lb
    rec_time = takeTime()
    rec_text = []


    try:
        with open(pathname + 'rec_info.pickle', 'rb') as rec_file:
            rec_info = pickle.load(rec_file)
            rec_code_num = int(len(rec_info))+1
            rec_info.update({rec_code_num:{'time':rec_time,'name':name,'state':state,'person':person,'ps':ps}})
        with open(pathname + 'rec_info.pickle', 'wb') as rec_file:
            pickle.dump(rec_info, rec_file)

    except FileNotFoundError:
        with open(pathname + 'rec_info.pickle', 'wb') as rec_file:
            rec_code_num = 1
            rec_info = {rec_code_num:{'time':rec_time,'name':'','state':'開始記錄','person':'管理員','ps':''}}
            pickle.dump(rec_info, rec_file)

    rec_show.delete(0,'end')
    for i in rec_info:
        rec_str = rec_info[i]['time'] + '  ' + rec_info[i]['name'] + ' 由' + rec_info[i]['person'] + rec_info[i]['state'] +'( '+ rec_info[i]['ps'] + ')'
        rec_text.append(rec_str)
    for k in rec_text:
        rec_show.insert(0,k)


#從租借狀況籃和登記資料中的物品 新增要操作的物品內容  可以一次確認租借物品
def data_add():
    global data_check
    data_value=''
    data_lb.delete(0,'end')
    stuff_num = var_stuff.get()
    #從右邊列表取物品
    if (stuff_num == ''):
        try:
            data_value = list.get(list.curselection())
            data_value = data_value.split('(')[0]
        except :
            tk.messagebox.showerror(message='尚未選擇物品')
    else:
        try:
            with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
                stuff_info = pickle.load(stuff_file)
                if stuff_num in stuff_info:
                    data_value = stuff_info[stuff_num]['name']
                else:
                    tk.messagebox.showerror(message='沒有該物品')
        except FileNotFoundError:
            tk.messagebox.showerror(message='Error, there is no stuff')

    if data_value in data_check:
        tk.messagebox.showerror(message='您已放入租借籃')
    else:
        data_check.append(data_value)

    for i in data_check:
        data_lb.insert('end',i)
#從租借狀況籃和登記資料中的物品 移除要操作的物品內容  可以一次確認租借物品
def data_delete():
    global data_check
    data_value = ''
    stuff_num = var_stuff.get()
    data_lb.delete(0, 'end')
    if (stuff_num == ''):
        try:
            data_value = list.get(list.curselection())
            data_value = data_value.split('(')[0]
        except :
            tk.messagebox.showerror(message='尚未選擇物品')
    else:
        try:
            with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
                stuff_info = pickle.load(stuff_file)
                if stuff_num in stuff_info:
                    data_value = stuff_info[stuff_num]['name']
                else:
                    tk.messagebox.showerror(message='沒有該物品')
        except FileNotFoundError:
            tk.messagebox.showerror(message='Error, there is no stuff')

    if data_value in data_check:
        del data_check[data_check.index(data_value)]
    else:
        tk.messagebox.showerror(message='沒有此物品')
    for i in data_check:
        data_lb.insert('end', i)
#取得確認資料內容
def data_processing():
    data_value = data_lb.get(0,'end')
    data_pro_num=[]
    try:
        with open(pathname + 'stuff_info.pickle', 'rb') as stuff_file:
            stuff_info = pickle.load(stuff_file)
    except FileNotFoundError:
        tk.messagebox.showerror(message='尚未建立物品清單')

    for i in data_value:
        for num in stuff_info:
            if stuff_info[num]['name'] == i:
                data_pro_num.append(num)

    return data_pro_num


#檔案管理
def new_rec():
    his_rec_info = {}
    new_rec_info = {}
    new_rec_text = []
    try:
        with open(pathname + 'his_rec_info.pickle', 'rb') as his_rec_file:
            his_rec_info = pickle.load(his_rec_file)
    except FileNotFoundError:
        tk.messagebox.showerror(message='目前沒有歷史租借紀錄')
        pass

    try:
        with open(pathname + 'rec_info.pickle', 'rb') as rec_file:
            rec_info = pickle.load(rec_file)
    except FileNotFoundError:
        tk.messagebox.showerror(message='目前沒有租借紀錄')
        return

    total_num = len(rec_info)
    total_his_num = len(his_rec_info)
    count_num = 0
    for i in rec_info:
        if count_num <= (total_num - 11):
            his_rec_info.update({i+total_his_num:rec_info[i]})
            count_num += 1
        else:
            new_rec_info.update({i-count_num:rec_info[i]})



    with open(pathname + 'his_rec_info.pickle', 'wb') as his_rec_file:
        pickle.dump(his_rec_info, his_rec_file)
    with open(pathname + 'rec_info.pickle', 'wb') as rec_file:
        pickle.dump(new_rec_info, rec_file)

    rec_show.delete(0, 'end')
    for i in new_rec_info:
        new_rec_str = new_rec_info[i]['time'] + '  ' + new_rec_info[i]['name'] + ' 由' + new_rec_info[i]['person'] + new_rec_info[i]['state'] + '( ' + new_rec_info[i]['ps']  + ')'
        new_rec_text.append(new_rec_str)
    for k in new_rec_text:
        rec_show.insert(0, k)

def his_rec_output():
    first = True

    try:
        with open(pathname + 'his_rec_info.pickle', 'rb') as his_rec_file:
            his_rec_info = pickle.load(his_rec_file)

        with open('D:\歷史租借紀錄.csv', 'w')as file:
            w = csv.writer(file)

            for i in his_rec_info:
                if first == True:
                    w.writerow(his_rec_info[i].keys())
                    first = False
                w.writerow(his_rec_info[i].values())
    except FileNotFoundError:
        tk.messagebox.showerror(message='目前沒有歷史租借紀錄')




#管理員設定
def add_admin():
    global ad_check
    global check
    global end
    if end ==False:
        check = 'add_admin'
        admin_check()

    if ad_check == True:
        def add_signin():
            try:
                with open(pathname + 'admin_info.pickle', 'rb') as admin_file:
                    admin_info = pickle.load(admin_file)
            except FileNotFoundError:
                with open(pathname + 'admin_info.pickle', 'wb') as admin_file:
                    admin_info = {'admin': 'admin'}
                    pickle.dump(admin_info, admin_file)
            new_admin_name = admin_new_name.get()
            new_admin_pwd = admin_new_pwd.get()

            if new_admin_name in admin_info:
                tk.messagebox.showerror(message='已有相同管理員名稱，請再試試看')
            else:
                admin_info.update({new_admin_name: new_admin_pwd})

                with open(pathname + 'admin_info.pickle', 'wb') as admin_file:
                    pickle.dump(admin_info, admin_file)
                    tk.messagebox.showerror(message='已經新增管理員')
                    window_add_admin.destroy()

        window_add_admin = tk.Toplevel(window)
        window_add_admin.geometry('270x150')
        window_add_admin.title('新增管理員')
        window_add_admin.resizable(0, 0)

        admin_new_name = tk.StringVar()
        tk.Label(window_add_admin, text='新管理員帳號: ').place(x=10, y=10)
        entry_new_name = tk.Entry(window_add_admin, textvariable=admin_new_name)
        entry_new_name.place(x=100, y=10)

        admin_new_pwd = tk.StringVar()
        tk.Label(window_add_admin, text='新管理員密碼: ').place(x=10, y=50)
        entry_new_pwd = tk.Entry(window_add_admin, textvariable=admin_new_pwd, show='*')
        entry_new_pwd.place(x=100, y=50)

        btn_singin = tk.Button(window_add_admin, text='新增', command=add_signin, width=5)
        btn_singin.place(x=110, y=100)

        ad_check = False
        end = False

def delete_admin():
    global ad_check
    global check
    global end
    if end == False:
        check = 'delete_admin'
        admin_check()

    if ad_check == True:
        def delete_signin():
            try:
                with open(pathname + 'admin_info.pickle', 'rb') as admin_file:
                    admin_info = pickle.load(admin_file)
            except FileNotFoundError:
                with open(pathname + 'admin_info.pickle', 'wb') as admin_file:
                    admin_info = {'admin': 'admin'}
                    pickle.dump(admin_info, admin_file)
            delete_admin_name = admin_delete_name.get()


            if delete_admin_name in admin_info:
                del admin_info[delete_admin_name]
                with open(pathname + 'admin_info.pickle', 'wb') as admin_file:
                    pickle.dump(admin_info, admin_file)
                tk.messagebox.showerror(message='已刪除')
                window_delete_admin.destroy()
            else:
                    tk.messagebox.showerror(message='無該管理員')

        window_delete_admin = tk.Toplevel(window)
        window_delete_admin.geometry('270x100')
        window_delete_admin.title('刪除管理員')
        window_delete_admin.resizable(0, 0)

        admin_delete_name = tk.StringVar()
        tk.Label(window_delete_admin, text='刪除管理員帳號: ').place(x=10, y=10)
        entry_delete_name = tk.Entry(window_delete_admin, textvariable=admin_delete_name)
        entry_delete_name.place(x=110, y=10)

        btn_find = tk.Button(window_delete_admin, text='刪除', command=delete_signin, width=5)
        btn_find.place(x=110, y=50)

        ad_check = False
        end = False

def forget_admin():
    pass

#使用說明
def how_use():
    global check
    global ad_check
    global end

    def how_use_adv():
        global check
        global end
        if end == True:
            end = False
            window_help.destroy()
        else:
            check = 'adv'
            admin_check()
            window_help.destroy()

    window_help = tk.Toplevel(window)
    window_help.geometry('500x500')
    window_help.title('使用說明')

    t = tk.Text(window_help, width=70, height=35)
    t.pack()


    adv = tk.Button(window_help,text="進階",command = how_use_adv)
    adv.pack()
    if ad_check == True:
        file = open('admin_item.txt', 'r')
        t.insert('end', file.read())
        file.close()
        end = True
        ad_check = False
        adv.config(text='關閉')
    else:
        file = open('Readme.txt', 'r')
        t.insert('end', file.read())
        file.close()




##視窗架構

frm = tk.Frame(window,width = 800,height = 600)
frm.pack()
frm_top = tk.Frame(frm,width = 800,height = 65)
frm_top.pack()
frm_mid = tk.Frame(frm,width = 800,height = 400)
frm_mid.pack()
frm_l = tk.Frame(frm_mid,width = 600,height = 400)
frm_r = tk.Frame(frm_mid,width = 200,height = 400)
frm_l.pack(side='left')
frm_r.pack(side='right')
frm_log = tk.Frame(frm_l,width = 500,height = 150)
frm_rec = tk.Frame(frm_l,width = 500,height = 250)
frm_log.pack()
frm_rec.pack()

##menubar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar,tearoff = 0)
menubar.add_cascade(label = '檔案',menu = filemenu)
filemenu.add_command(label = '刷新租借紀錄',command = new_rec)
filemenu.add_command(label = '輸出歷史租借紀錄',command = his_rec_output)

adminmenu = tk.Menu(menubar,tearoff = 0)
menubar.add_cascade(label = '管理員',menu = adminmenu)
adminmenu.add_command(label = '新增管理員',command = add_admin)
adminmenu.add_command(label = '刪除管理員',command = delete_admin)
adminmenu.add_command(label = '忘記密碼',command = forget_admin)



helpmenu = tk.Menu(menubar,tearoff = 0)
menubar.add_cascade(label = '關於',menu = helpmenu)
helpmenu.add_command(label = '使用說明',command = how_use)

window.config(menu = menubar)





##上方 Button 設置
frm_topl = tk.Frame(frm_top,width = 200,height = 65)
frm_topr = tk.Frame(frm_top,width = 600,height = 65)
frm_topl.pack(side='left')
frm_topr.pack(side='right')


btn_admin_login = tk.Button(frm_topl,width = 15,height = 3 ,text='管理員登入',command =admin_login)
btn_admin_login.place(x=0, y=5,anchor='nw')

btn_turnback = tk.Button(frm_topr,width = 15,height = 3 ,text='歸還',command = turnback)
btn_turnback.pack(side='right')
btn_rent = tk.Button(frm_topr,width = 15,height = 3 ,text='借出',command = rent)
btn_rent.pack(side='right')
btn_delete = tk.Button(frm_topr,width = 15,height = 3 ,text='刪除',command = delet)
btn_delete.pack(side='right')
btn_new = tk.Button(frm_topr,width = 15,height = 3 ,text='新增',command = new)
btn_new.pack(side='right')

##中間 登記資料 設置
frm_logtitle = tk.LabelFrame(frm_log,width=250,height=130,text = '登記資料')
frm_logtitle.place(x=10, y=10,anchor='nw')
frm_confirm = tk.LabelFrame(frm_log,width=210,height=130,text = '租借暫存區')
frm_confirm.place(x=275, y=10,anchor='nw')


tk.Label(frm_logtitle, text='帳號: ').place(x=10, y=10,anchor='nw')
tk.Label(frm_logtitle, text='物品: ').place(x=10, y=40,anchor='nw')
tk.Label(frm_logtitle, text='備註: ').place(x=10, y=70,anchor='nw')

var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(frm_logtitle, textvariable=var_usr_name)
entry_usr_name.place(x=70, y=10)

var_stuff = tk.StringVar()
entry_stuff = tk.Entry(frm_logtitle, textvariable=var_stuff)
entry_stuff.place(x=70, y=40)

var_ps = tk.StringVar()
entry_ps = tk.Entry(frm_logtitle, textvariable=var_ps)
entry_ps.place(x=70, y=70)


data_lb = tk.Listbox(frm_confirm,selectmode = 'single',width = 20,height = 6)
data_lb.place(x=5, y=0)


data_in = tk.Button(frm_confirm,width = 5,height = 2 ,text='添加',command = data_add)
data_in.place(x=155, y=5)

data_out = tk.Button(frm_confirm,width = 5,height = 2 ,text='移除',command = data_delete)
data_out.place(x=155, y=55)



##中間 租借紀錄 設置
frm_rtitle = tk.LabelFrame(frm_rec,width = 475,height = 225,text='紀錄')
frm_rtitle.place(x=10, y=10,anchor='nw')

scroll_confirm = tk.Scrollbar(frm_rtitle)
scroll_confirm.pack(side='right',fill='y')

rec_show = tk.Listbox(frm_rtitle,yscrollcommand = scroll_confirm.set,width = 64,height = 13)
rec_show.pack()

scroll_confirm.config(command=rec_show.yview)


##右側租借狀況
frm_rtitle = tk.LabelFrame(frm_r,width = 250,height = 600,text='租借狀況')
frm_rtitle.place(x=0, y=10,anchor='nw')

scroll = tk.Scrollbar(frm_rtitle)
scroll.pack(side='right',fill='y')
list = tk.Listbox(frm_rtitle,yscrollcommand = scroll.set,height = 22,width = 23)
list.pack()
scroll.config(command = list.yview)

#開啟程式時執行
stuff_ava_get()
show_rec('','開啟程式','管理者','')


window.mainloop()
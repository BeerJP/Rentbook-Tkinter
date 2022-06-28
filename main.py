"""Rent book system management"""
from tkinter import Tk, Frame, PhotoImage, Button, Label, Toplevel, StringVar, filedialog, messagebox, ttk
from PIL import ImageTk, Image
from modules.widget_Config import *
from modules.db_Connect import *
from itertools import chain
from datetime import date, timedelta

conn = Connect()


class TitleFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(**m_color)
        self.pack(side="top", fill="x")
        self.__title_widget()

    def __title_widget(self):
        self.title_bt = [
            Button(self, text="╳", **ttf_bt_config, command=lambda: app.destroy()),
            Button(self, text="―", **ttf_bt_config, command=lambda: [app.overrideredirect(0), app.iconify()])
        ]
        self.title_bt[0].pack(side="right")
        self.title_bt[1].pack(side="right")


class MenuFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#0F0F1D", width=130)
        self.pack(side="left", fill="y")
        self.__menu_widget()
        self.parent = parent
        self.getPage = [
            BooksPage(parent),
            RentAndReturn(parent),
            MemberPage(parent),
            RecordPage(parent)
        ]

    def __menu_widget(self):
        self.title = Label(self, text="RBSM", fg="#F8F9F9", bg="#0F0F1D", font=("Courier", 18))
        self.menu_ic = {
            "Home": PhotoImage(file="icon/homepage.png"),
            "Book": PhotoImage(file="icon/book.png"),
            "Group": PhotoImage(file="icon/group.png"),
            "Calen": PhotoImage(file="icon/calendar.png")
        }
        self.menu_bt = [
            Button(self, image=self.menu_ic["Home"], **mnf_bt_config, command=lambda: self._show_hide(0)),
            Button(self, image=self.menu_ic["Book"], **mnf_bt_config, command=lambda: self._show_hide(1)),
            Button(self, image=self.menu_ic["Group"], **mnf_bt_config, command=lambda: self._show_hide(2)),
            Button(self, image=self.menu_ic["Calen"], **mnf_bt_config,
                   command=lambda: [self._show_hide(3), self.getPage[3]._tbl_Ct()])
        ]
        self.title.pack(pady=5)
        self.menu_bt[0].pack()
        self.menu_bt[1].pack()
        self.menu_bt[2].pack()
        self.menu_bt[3].pack()

    def _show_hide(self, num):
        for i in range(4):
            self.getPage[i].pack_forget()
            self.menu_bt[i].config(bg="#0F0F1D")
        self.getPage[num].pack(fill="both", expand=1, padx=2, pady=2)
        self.menu_bt[num].config(bg="#e6e6e6")


class BooksPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(**m_color)
        self.__booksMenu()
        self.__tbl_books()
        self.__info_books("RBSM")
        self.__tbl_Ct("all")

        def info_selected(event):
            for selected_item in self.tbl_TreeView.selection():
                item = self.tbl_TreeView.item(selected_item)
                record = str(item["values"][0])
                if len(record) < 8: record = "0" + record
                self.info_BookFrame.destroy()
                self.__info_books(record)

        self.tbl_TreeView.bind('<<TreeviewSelect>>', info_selected)

    def __booksMenu(self):
        self.book_MenuFrame = Frame(self, **m_color)
        self.book_WidgetFrame = {
            "Name": Frame(self.book_MenuFrame, **m_color),
            "Butt": Frame(self.book_MenuFrame, **m_color)
        }
        self.add_icon = PhotoImage(file="icon/mem_add.png")
        self.menu_widget = [
            Label(self.book_WidgetFrame["Name"], text="Home Page", **nm_config),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="ALL", command=lambda: self.__tbl_Ct("all")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="General", command=lambda: self.__tbl_Ct("01")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="Philosophy", command=lambda: self.__tbl_Ct("02")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="Religion", command=lambda: self.__tbl_Ct("03")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="Social", command=lambda: self.__tbl_Ct("04")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="Language", command=lambda: self.__tbl_Ct("05")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="Science", command=lambda: self.__tbl_Ct("06")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="Technology", command=lambda: self.__tbl_Ct("07")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="Arts", command=lambda: self.__tbl_Ct("08")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="Literature", command=lambda: self.__tbl_Ct("09")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_config,
                   text="History", command=lambda: self.__tbl_Ct("10")),
            Button(self.book_WidgetFrame["Butt"], **mn_bt_ic_config,
                   image=self.add_icon, command=lambda: self.__add_Books())
        ]
        self.book_MenuFrame.pack(fill="x")
        self.book_WidgetFrame["Name"].pack(fill="x", padx=40, pady=10)
        self.book_WidgetFrame["Butt"].pack(padx=10, pady=10)
        self.menu_widget[0].pack(fill="both")
        self.menu_widget[1].pack(side="left")
        self.menu_widget[2].pack(side="left")
        self.menu_widget[3].pack(side="left")
        self.menu_widget[4].pack(side="left")
        self.menu_widget[5].pack(side="left")
        self.menu_widget[6].pack(side="left")
        self.menu_widget[7].pack(side="left")
        self.menu_widget[8].pack(side="left")
        self.menu_widget[9].pack(side="left")
        self.menu_widget[10].pack(side="left")
        self.menu_widget[11].pack(side="left")
        self.menu_widget[12].pack(side="left")

    def __info_books(self, record):
        try:
            self.raw_img = Image.open("img/{}.jpg".format(record)).resize((250, 300), Image.ANTIALIAS)
            self.unit = conn.show_Unit(record)
        except FileNotFoundError:
            self.raw_img = Image.open("img/RBSM.jpg").resize((250, 300), Image.ANTIALIAS)
        except TypeError:
            self.unit = ["0", "0"]
        finally:
            self.img = ImageTk.PhotoImage(self.raw_img)

        self.info_BookFrame = Frame(self, width=345, **m_color)
        self.info_WidgetFrame = {
            "Image Frame": Frame(self.info_BookFrame, **m_color),
            "Unit Frame": Frame(self.info_BookFrame, **m_color)
        }
        self.info_label = [
            Label(self.info_WidgetFrame["Image Frame"], image=self.img),
            Label(self.info_WidgetFrame["Unit Frame"], text="In Stock :", **if_lb_config),
            Label(self.info_WidgetFrame["Unit Frame"], text="In Rent :", **if_lb_config),
            Label(self.info_WidgetFrame["Unit Frame"], text=self.unit[0], **if_ct_config, width=5),
            Label(self.info_WidgetFrame["Unit Frame"], text=self.unit[1], **if_ct_config, width=5)
        ]
        self.info_BookFrame.pack(side="right", fill="both")
        self.info_WidgetFrame["Image Frame"].pack(side="top", fill="both")
        self.info_WidgetFrame["Unit Frame"].pack()
        self.info_label[0].pack(side="top", padx=30)
        self.info_label[1].grid(row=0, column=0)
        self.info_label[2].grid(row=1, column=0)
        self.info_label[3].grid(row=0, column=1)
        self.info_label[4].grid(row=1, column=1)

    def __tbl_books(self):
        self.tbl_BookFrame = Frame(self, **m_color)
        self.tbl_BookFrame.pack(side="left", fill="both", expand=1)
        self.columns = ("#1", "#2", "#3")
        self.tbl_TreeView = ttk.Treeview(self.tbl_BookFrame, column=self.columns, show="headings")
        self.tbl_TreeView.heading("#1", text="ID")
        self.tbl_TreeView.heading("#2", text="Name")
        self.tbl_TreeView.heading("#3", text="State")
        self.tbl_TreeView.column("#1", anchor="s")
        self.tbl_TreeView.column("#2", width=500)
        self.tbl_TreeView.column("#3", anchor="s")
        self.tbl_TreeView.pack(fill="y", expand=1, padx=10)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tbl_TreeView.yview)
        self.tbl_TreeView.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="left", fill="both")

    def __add_Books(self):
        self.menu_widget[12].config(state="disabled")
        self.regFrame = Toplevel(self)
        self.regFrame.title("Add Book")
        self.regFrame.resizable(False, False)
        self.posRight = int(self.winfo_screenwidth() / 2 - 250)
        self.posDown = int(self.winfo_screenheight() / 2 - 175)
        self.regFrame.geometry("500x350+{}+{}".format(self.posRight, self.posDown))
        self.add_var = {
            "Name": StringVar(),
            "Unit": StringVar(),
            "Category": StringVar(),
            "S_Category": StringVar(),
            "Image": StringVar()
        }

        self.add_Widget = [
            ttk.Label(self.regFrame, text="Name :"),
            ttk.Label(self.regFrame, text="Unit :"),
            ttk.Label(self.regFrame, text="Category :"),
            ttk.Label(self.regFrame, text="Sub Category :"),
            ttk.Label(self.regFrame, text="Image File :"),
            ttk.Entry(self.regFrame, width=35, textvariable=self.add_var["Name"], **ttk_en_config),
            ttk.Entry(self.regFrame, justify="center", width=5, textvariable=self.add_var["Unit"], **ttk_en_config),
            ttk.Combobox(self.regFrame, width=25, font=("Yatra One", 12), textvariable=self.add_var["Category"]),
            ttk.Combobox(self.regFrame, width=25, font=("Yatra One", 12), textvariable=self.add_var["S_Category"]),
            ttk.Entry(self.regFrame, text="123", width=35, textvariable=self.add_var["Image"], **ttk_en_config),
            ttk.Button(self.regFrame, text="Choose File", command=lambda: self.__chooseFIle()),
            ttk.Button(self.regFrame, text="Save", command=lambda: self.__add_Db())
        ]
        self.add_Widget[7]['values'] = [
            "ความรู้ทั่วไป", "ปรัชญาและจิตวิทยา", "ศาสนา", "สังคมศาสตร์", "ภาษา", "วิทยาศาสตร์ธรรมชาติและคณิตศาสตร์",
            "เทคโนโลยี(วิทยาศาสตร์ประยุกต์)", "ศิลปะวิจิตรศิลป์และมัณฑนศิลป์", "วรรณคดี", "ภูมิศาสตร์และประวิตศาสตร์"
        ]

        self.add_Widget[0].grid(row=0, column=0, pady=20, padx=5)
        self.add_Widget[1].grid(row=1, column=0, pady=20, padx=5)
        self.add_Widget[2].grid(row=2, column=0, pady=20, padx=5)
        self.add_Widget[3].grid(row=3, column=0, pady=20, padx=5)
        self.add_Widget[4].grid(row=4, column=0, pady=20, padx=5)
        self.add_Widget[5].grid(row=0, column=1, sticky="w")
        self.add_Widget[6].grid(row=1, column=1, sticky="w")
        self.add_Widget[7].grid(row=2, column=1, sticky="w")
        self.add_Widget[8].grid(row=3, column=1, sticky="w")
        self.add_Widget[9].grid(row=4, column=1, sticky="w")
        self.add_Widget[10].grid(row=5, column=1, sticky="w")
        self.add_Widget[11].grid(row=5, column=1)

        def returnBtt():
            self.regFrame.destroy()
            self.menu_widget[12].config(state="normal")

        def selected_Category(event):
            category = self.add_var["Category"].get()
            self.add_var["S_Category"].set("")
            self.add_Widget[8]['values'] = list(chain.from_iterable(conn.show_Sc(category)))

        self.add_Widget[7].bind('<<ComboboxSelected>>', selected_Category)
        self.regFrame.protocol("WM_DELETE_WINDOW", returnBtt)

    def __chooseFIle(self):
        fn = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("JPG files", "*.jpg*"),))
        self.add_var["Image"].set(fn)

    def __set_BID(self):
        c_id = conn.c_id(self.add_var["Category"].get())
        sc_id = conn.sc_id(self.add_var["S_Category"].get())
        b_id = int(list(chain.from_iterable(conn.check_bID(c_id[0] + sc_id[0] + "%")))[-1]) + 1
        return "0" + str(b_id)

    def __add_Db(self):
        b_id = self.__set_BID()
        b_n = self.add_var["Name"].get()
        b_u = self.add_var["Unit"].get()
        b_sc = conn.sc_id(self.add_var["S_Category"].get())
        img = Image.open(self.add_var["Image"].get())
        img.save("img/" + b_id + ".jpg")
        conn.bookInsert(b_id, b_n, b_u, b_sc)
        messagebox.showinfo("Insert Book", "Successful")
        self.regFrame.destroy()
        self.menu_widget[12].config(state="normal")

    def __tbl_Ct(self, category):
        if category == "all":
            data = conn.show_AllBooks()
            self.tbl_TreeView.delete(*self.tbl_TreeView.get_children())
            for i in data:
                self.tbl_TreeView.insert("", 'end', values=(i[0], i[1], i[2] > 0))
        else:
            data = conn.show_Books(category)
            self.tbl_TreeView.delete(*self.tbl_TreeView.get_children())
            for i in data:
                self.tbl_TreeView.insert("", 'end', values=(i[0], i[1], i[2] > 0))


class RentAndReturn(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(**m_color)
        self.__rentMenu()
        self.__Info_Page()
        self.__Info_Rent().pack()
        self.__Info_Return()
        self.__tbl()

    def __rentMenu(self):
        self.menuFrame = Frame(self, **m_color)
        self.menuFrame.pack(fill="x")
        self.menu_WgFrame = {
            "Name Frame": Frame(self.menuFrame),
            "Icon Frame": Frame(self.menuFrame, bg="#21303D")
        }
        self.record_Menu = [
            Label(self.menu_WgFrame["Name Frame"], text="Rent & Return", **nm_config),
            Button(self.menu_WgFrame["Icon Frame"], text="Rent", state="disabled", **mn_bt_config,
                   command=lambda: self.__menu_ct("Rent")),
            Button(self.menu_WgFrame["Icon Frame"], text="Return", **mn_bt_config,
                   command=lambda: self.__menu_ct("Return"))
        ]
        self.menu_WgFrame["Name Frame"].pack(side="top", fill="x", padx=40, pady=10)
        self.menu_WgFrame["Icon Frame"].pack(side="bottom", fill="x", padx=10, pady=10)
        self.record_Menu[0].pack(fill="both")
        self.record_Menu[1].pack(side="left")
        self.record_Menu[2].pack(side="left")

    def __Info_Page(self):
        self.info_Frame = Frame(self, width=345, **m_color)
        self.info_Frame.pack(side="left", fill="y", padx=10)

    def __Info_Return(self):
        self.info_reFrame = ttk.Labelframe(self.info_Frame)
        self.info_reVar = {
            "Oid": StringVar(),
            "Du": StringVar(),
            "Re": StringVar(),
            "State": StringVar()
        }
        self.info_rewg = [
            ttk.Label(self.info_reFrame, text="Order ID :"),
            ttk.Label(self.info_reFrame, text="Due Date :"),
            ttk.Label(self.info_reFrame, text="Return Date :"),
            ttk.Label(self.info_reFrame, textvariable=self.info_reVar["State"]),
            ttk.Entry(self.info_reFrame, textvariable=self.info_reVar["Oid"]),
            ttk.Label(self.info_reFrame, width=10, textvariable=self.info_reVar["Du"]),
            ttk.Label(self.info_reFrame, width=10, textvariable=self.info_reVar["Re"]),
            ttk.Button(self.info_reFrame, text="Check", command=lambda: self.__check("Return")),
            ttk.Button(self.info_reFrame, text="Confirm Return", state="disabled", command=lambda: self.cf_Return())
        ]
        self.info_rewg[0].grid(row=0, column=0, pady=5)
        self.info_rewg[1].grid(row=1, column=0, pady=5)
        self.info_rewg[2].grid(row=2, column=0, pady=5)
        self.info_rewg[3].grid(row=3, column=0, pady=5)
        self.info_rewg[4].grid(row=0, column=1, pady=5, sticky="w")
        self.info_rewg[5].grid(row=1, column=1, pady=5, sticky="w")
        self.info_rewg[6].grid(row=2, column=1, pady=5, sticky="w")
        self.info_rewg[7].grid(row=0, column=2, pady=5, padx=5)
        self.info_rewg[8].grid(row=3, column=1, pady=5, sticky="w")
        self.info_reVar["Re"].set(date.today())
        return self.info_reFrame

    def __Info_Rent(self):
        self.info_rnFrame = ttk.Labelframe(self.info_Frame)
        self.info_rnVar = {
            "MId": StringVar(),
            "Rn": StringVar(),
            "Du": StringVar(),
            "Re": StringVar(),
            "State": StringVar(),
            "O_ID": StringVar()
        }

        self.info_rnwg = [
            ttk.Label(self.info_rnFrame, text="Member ID :"),
            ttk.Label(self.info_rnFrame, text="Rent Date :"),
            ttk.Label(self.info_rnFrame, text="Due Date :"),
            ttk.Label(self.info_rnFrame, text="Return Date :"),
            ttk.Label(self.info_rnFrame, text="Order ID :"),
            ttk.Label(self.info_rnFrame, textvariable=self.info_rnVar["State"]),
            ttk.Entry(self.info_rnFrame, textvariable=self.info_rnVar["MId"]),
            ttk.Label(self.info_rnFrame, width=10, textvariable=self.info_rnVar["Rn"]),
            ttk.Combobox(self.info_rnFrame, width=5, font=("Yatra One", 12), textvariable=self.info_rnVar["Du"]),
            ttk.Label(self.info_rnFrame, width=10, textvariable=self.info_rnVar["Re"]),
            ttk.Button(self.info_rnFrame, text="Check", command=lambda: self.__check("Rent")),
            ttk.Label(self.info_rnFrame, width=6, textvariable=self.info_rnVar["O_ID"]),
            ttk.Button(self.info_rnFrame, text="Add", state="disabled", command=lambda: self.__addFrame()),
            ttk.Button(self.info_rnFrame, text="Confirm Rent", state="disabled", command=lambda: self.cf_Rent())
        ]
        self.info_rnwg[8]["values"] = [
            "3", "7", "14", "30"
        ]

        self.info_rnwg[0].grid(row=0, column=0, pady=5)
        self.info_rnwg[1].grid(row=1, column=0, pady=5)
        self.info_rnwg[2].grid(row=2, column=0, pady=5)
        self.info_rnwg[3].grid(row=3, column=0, pady=5)
        self.info_rnwg[4].grid(row=4, column=0, pady=5)
        self.info_rnwg[5].grid(row=5, column=0, pady=5)
        self.info_rnwg[6].grid(row=0, column=1, pady=5, sticky="w")
        self.info_rnwg[7].grid(row=1, column=1, pady=5, sticky="w")
        self.info_rnwg[8].grid(row=2, column=1, pady=5, sticky="w")
        self.info_rnwg[9].grid(row=3, column=1, pady=5, sticky="w")
        self.info_rnwg[10].grid(row=0, column=2, pady=5, padx=5)
        self.info_rnwg[11].grid(row=4, column=1, pady=5, padx=5, sticky="w")
        self.info_rnwg[12].grid(row=5, column=1, pady=8, sticky="w")
        self.info_rnwg[13].grid(row=6, column=1, sticky="w")
        self.info_rnVar["Rn"].set(date.today())
        self.info_rnVar["O_ID"].set(conn.select_Oid()[0]+1)

        def selected_date(event):
            today = date.today()
            duDate = self.info_rnVar["Du"].get()
            reDate = today + timedelta(days=int(duDate))
            self.info_rnVar["Re"].set(reDate)

        self.info_rnwg[8].bind('<<ComboboxSelected>>', selected_date)
        return self.info_rnFrame

    def __tbl(self):
        self.tbl_Frame = Frame(self, **m_color)
        self.tbl_Frame.pack(side="right", fill="both", expand=1)
        self.columns = ("#1", "#2")
        self.r_TreeView = ttk.Treeview(self.tbl_Frame, column=self.columns, show="headings")
        self.r_TreeView.heading("#1", text="Book ID")
        self.r_TreeView.heading("#2", text="Book Name")
        self.r_TreeView.column("#1", anchor="s", width=200)
        self.r_TreeView.column("#2", width=650)
        self.r_TreeView.pack(fill="y", expand=1, padx=10)

    def __addFrame(self):
        self.info_rnwg[10].config(state="disabled")
        self.addFrame = Toplevel(self.info_rnFrame)
        self.addFrame.title("Selected Book")
        self.addFrame.resizable(False, False)
        self.posRight = int(self.winfo_screenwidth() / 2 - 375)
        self.posDown = int(self.winfo_screenheight() / 2 - 250)
        self.addFrame.geometry("750x500+{}+{}".format(self.posRight, self.posDown))
        self.columns = ("#1", "#2")
        self.add_TreeView = ttk.Treeview(self.addFrame, column=self.columns, show="headings")
        self.add_TreeView.heading("#1", text="ID")
        self.add_TreeView.heading("#2", text="Name")
        self.add_TreeView.column("#1", anchor="s")
        self.add_TreeView.column("#2", width=500)
        self.add_TreeView.pack(side="left", fill="y", expand=1, padx=10)
        self.scrollbar = ttk.Scrollbar(self.addFrame, orient="vertical", command=self.add_TreeView.yview)
        self.add_TreeView.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="both")
        data = conn.show_AllBooks()
        for i in data:
            if i[2] > 0:
                self.add_TreeView.insert("", 'end', values=(i[0], i[1]))
            else:
                pass

        def doubleClick(event):
            for selected_item in self.add_TreeView.selection():
                item = self.add_TreeView.item(selected_item)
                record = [str(item["values"][0]), str(item["values"][1])]
                if len(record[0]) < 8: record[0] = "0" + record[0]
                self.r_TreeView.insert("", 'end', values=record)
                returnBtt()

        def returnBtt():
            self.addFrame.destroy()
            self.info_rnwg[10].config(state="normal")

        self.add_TreeView.bind("<Double-1>", doubleClick)
        self.addFrame.protocol("WM_DELETE_WINDOW", returnBtt)

    def __check(self, mode):
        if mode == "Rent":
            m_id = self.info_rnVar["MId"].get()
            self.r_TreeView.delete(*self.r_TreeView.get_children())
            try:
                conn.show_Mid(m_id)
                if conn.check_Order(m_id)[0] == "1":
                    self.info_rnVar["State"].set("Available :")
                    self.info_rnwg[12].config(state="normal")
                    self.info_rnwg[13].config(state="normal")
                else:
                    self.info_rnVar["State"].set("Unavailable :")
            except TypeError:
                self.info_rnVar["State"].set("Unavailable :")
        elif mode == "Return":
            o_id = self.info_reVar["Oid"].get()
            self.r_TreeView.delete(*self.r_TreeView.get_children())
            self.info_reVar["State"].set("")
            self.info_reVar["Du"].set("")
            try:
                order = conn.show_Oid(o_id)
                if order[2] != "1":
                    self.info_reVar["State"].set("Available :")
                    self.info_rewg[8].config(state="normal")
                    self.info_reVar["Du"].set(order[1])
                    self.__tbl_Return(order[0])
                else:
                    self.info_rewg[8].config(state="disabled")
                    self.info_reVar["State"].set("Unavailable :")
                    self.__tbl_Return(order[0])
            except TypeError:
                self.info_reVar["State"].set("Unavailable :")

    def __tbl_Return(self, o_id):
        data = conn.return_detail(o_id)
        for i in data:
            self.r_TreeView.insert("", 'end', values=i)

    def cf_Return(self):
        o_id = self.info_reVar["Oid"].get()
        day = self.info_reVar["Re"].get()
        item = []
        for i in self.r_TreeView.get_children():
            item.append(self.r_TreeView.item(i)["values"])
        conn.order_update(o_id)
        for x in range(len(item)):
            if len(str(item[x][0])) < 8:
                item[x][0] = "0"+str(item[x][0])
                unit = conn.show_Unit(item[x][0])
                conn.book_update(unit[0]+1, unit[1]-1, item[x][0])
            else:
                unit = conn.show_Unit(item[x][0])
                conn.book_update(unit[0]+1, unit[1]-1, item[x][0])
        conn.return_insert(day, o_id)
        messagebox.showinfo("Rent", "Successful")
        self.r_TreeView.delete(*self.r_TreeView.get_children())
        self.info_reFrame.destroy()
        self.__Info_Return().pack()

    def cf_Rent(self):
        o_id = self.info_rnVar["O_ID"].get()
        m_id = self.info_rnVar["MId"].get()
        rnDate = self.info_rnVar["Rn"].get()
        reDate = self.info_rnVar["Re"].get()
        item = []
        for i in self.r_TreeView.get_children():
            item.append(self.r_TreeView.item(i)["values"])
        conn.order_insert(o_id, m_id, rnDate, reDate)
        for x in range(len(item)):
            if len(str(item[x][0])) < 8:
                item[x][0] = "0"+str(item[x][0])
                conn.order_detail(item[x][0], o_id)
                unit = conn.show_Unit(item[x][0])
                conn.book_update(unit[0]-1, unit[1]+1, item[x][0])
            else:
                conn.order_detail(item[x][0], o_id)
                unit = conn.show_Unit(item[x][0])
                conn.book_update(unit[0]-1, unit[1]+1, item[x][0])
        messagebox.showinfo("Rent", "Successful")
        self.r_TreeView.delete(*self.r_TreeView.get_children())
        self.info_rnFrame.destroy()
        self.__Info_Rent().pack()

    def __menu_ct(self, mode):
        self.r_TreeView.delete(*self.r_TreeView.get_children())
        if mode == "Rent":
            self.info_reFrame.destroy()
            self.__Info_Rent().pack()
            self.record_Menu[1].config(state="disabled")
            self.record_Menu[2].config(state="normal")
        elif mode == "Return":
            self.info_rnFrame.destroy()
            self.__Info_Return().pack()
            self.record_Menu[2].config(state="disabled")
            self.record_Menu[1].config(state="normal")


class MemberPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(**m_color)
        self.__memberMenu()
        self.__tbl_member()
        self.__tbl_Ct("All")

    def __memberMenu(self):
        self.member_MenuFrame = Frame(self, **m_color)
        self.member_WgFrame = {
            "Name Frame": Frame(self.member_MenuFrame),
            "Icon Frame": Frame(self.member_MenuFrame, bg="#21303D")
        }
        self.member_icon = [
            PhotoImage(file="icon/mem_add.png"),
            PhotoImage(file="icon/mem_search.png")
        ]
        self.member_menu = [
            Label(self.member_WgFrame["Name Frame"], text="Member", **nm_config),
            Button(self.member_WgFrame["Icon Frame"], **mn_bt_config, text="ALL",
                   command=lambda: self.__tbl_Ct("All")),
            Button(self.member_WgFrame["Icon Frame"], **mn_bt_ic_config, image=self.member_icon[0],
                   command=lambda: self.__reg_Member()),
            Button(self.member_WgFrame["Icon Frame"], **mn_bt_ic_config, image=self.member_icon[1],
                   command=lambda: self.__tbl_Ct(self.member_menu[4].get())),
            ttk.Entry(self.member_WgFrame["Icon Frame"], justify="center", **ttk_en_config)
        ]
        self.member_MenuFrame.pack(fill="x")
        self.member_WgFrame["Name Frame"].pack(side="top", fill="x", padx=40, pady=10)
        self.member_WgFrame["Icon Frame"].pack(side="bottom", fill="x", padx=10, pady=10)
        self.member_menu[0].pack(fill="both")
        self.member_menu[1].pack(side="left")
        self.member_menu[2].pack(side="left")
        self.member_menu[3].pack(side="right")
        self.member_menu[4].pack(side="right", padx=5, ipady=10)

    def __tbl_member(self):
        self.tbl_MemberFrame = Frame(self, **m_color)
        self.tbl_MemberFrame.pack(side="left", fill="both", expand=1)
        self.columns = ("#1", "#2", "#3", "#4", "#5")
        self.tbl_TreeView = ttk.Treeview(self.tbl_MemberFrame, column=self.columns, show="headings")
        self.tbl_TreeView.heading("#1", text="ID")
        self.tbl_TreeView.heading("#2", text="First Name")
        self.tbl_TreeView.heading("#3", text="Last Name")
        self.tbl_TreeView.heading("#4", text="Phone")
        self.tbl_TreeView.heading("#5", text="Reg.")
        self.tbl_TreeView.column("#1", anchor="s", width=200)
        self.tbl_TreeView.column("#2", width=300)
        self.tbl_TreeView.column("#3", width=300)
        self.tbl_TreeView.column("#4", anchor="s", width=200)
        self.tbl_TreeView.column("#5", anchor="s", width=200)
        self.tbl_TreeView.pack(fill="y", expand=1, padx=10)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tbl_TreeView.yview)
        self.tbl_TreeView.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="left", fill="both")

    def __reg_Member(self):
        self.member_menu[2].config(state="disabled")
        self.regFrame = Toplevel(self)
        self.regFrame.title("Register")
        self.regFrame.resizable(False, False)
        self.posRight = int(self.winfo_screenwidth() / 2 - 250)
        self.posDown = int(self.winfo_screenheight() / 2 - 175)
        self.regFrame.geometry("500x350+{}+{}".format(self.posRight, self.posDown))
        self.reg_var = {
            "Fname": StringVar(),
            "Lname": StringVar(),
            "Phone": StringVar(),
            "Date": StringVar()
        }
        self.reg_Wg = [
            ttk.Label(self.regFrame, text="First Name :"),
            ttk.Label(self.regFrame, text="Last Name :"),
            ttk.Label(self.regFrame, text="Phone :"),
            ttk.Label(self.regFrame, text="Reg DATE :"),
            ttk.Entry(self.regFrame, width=35, **ttk_en_config, textvariable=self.reg_var["Fname"]),
            ttk.Entry(self.regFrame, width=35, **ttk_en_config, textvariable=self.reg_var["Lname"]),
            ttk.Entry(self.regFrame, width=35, **ttk_en_config, textvariable=self.reg_var["Phone"]),
            ttk.Label(self.regFrame, textvariable=self.reg_var["Date"]),
            ttk.Button(self.regFrame, text="Confirmed", command=lambda: self.__reg_db()),
            ttk.Button(self.regFrame, text="Clear", command=lambda: self.__reg_clear())
        ]
        self.reg_Wg[0].grid(row=0, column=0, pady=20, padx=5)
        self.reg_Wg[1].grid(row=1, column=0, pady=20, padx=5)
        self.reg_Wg[2].grid(row=2, column=0, pady=20, padx=5)
        self.reg_Wg[3].grid(row=3, column=0, pady=20, padx=5)
        self.reg_Wg[4].grid(row=0, column=1, sticky="w")
        self.reg_Wg[5].grid(row=1, column=1, sticky="w")
        self.reg_Wg[6].grid(row=2, column=1, sticky="w")
        self.reg_Wg[7].grid(row=3, column=1, sticky="w")
        self.reg_Wg[8].grid(row=4, column=1, sticky="w")
        self.reg_Wg[9].grid(row=4, column=1)
        self.reg_var["Date"].set(date.today())

        def returnBtt():
            self.regFrame.destroy()
            self.member_menu[2].config(state="normal")

        self.regFrame.protocol("WM_DELETE_WINDOW", returnBtt)

    def __tbl_Ct(self, member):
        if member == "All":
            data = conn.show_Member()
            self.tbl_TreeView.delete(*self.tbl_TreeView.get_children())
            for i in data: self.tbl_TreeView.insert("", 'end', values=i)
        else:
            data = conn.word_Member(member + "%", member + "%", member + "%")
            self.tbl_TreeView.delete(*self.tbl_TreeView.get_children())
            for i in data: self.tbl_TreeView.insert("", 'end', values=i)

    def __reg_db(self):
        fn = self.reg_var["Fname"].get()
        ln = self.reg_var["Lname"].get()
        ph = self.reg_var["Phone"].get()
        dt = self.reg_var["Date"].get()
        conn.member_insert(fn, ln, ph, dt)
        messagebox.showinfo("Register Member", "Successful")
        self.regFrame.destroy()
        self.member_menu[2].config(state="normal")

    def __reg_clear(self):
        self.reg_var["Fname"].set("")
        self.reg_var["Lname"].set("")
        self.reg_var["Phone"].set("")


class RecordPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(**m_color)
        self.__recordMenu()
        self.__tbl_record()
        self._tbl_Ct()

    def __recordMenu(self):
        self.record_MenuFrame = Frame(self, **m_color)
        self.record_WidgetFrame = {
            "Name Frame": Frame(self.record_MenuFrame, **m_color),
            "Status Frame": Frame(self.record_MenuFrame, **m_color)
        }
        self.re_val = {
            "ALL": StringVar(),
            "Return": StringVar(),
            "Rent": StringVar()
        }
        self.record_widget = [
            Label(self.record_WidgetFrame["Name Frame"], text="Record", **nm_config),
            Label(self.record_WidgetFrame["Status Frame"], text="RENT\nNUMBER", **rp_sb_config),
            Label(self.record_WidgetFrame["Status Frame"], **rp_sb_config, relief="ridge", bd=1,
                  textvariable=self.re_val["ALL"]),
            Label(self.record_WidgetFrame["Status Frame"], text="RETURN\nNUMBER", **rp_sb_config),
            Label(self.record_WidgetFrame["Status Frame"], **rp_sb_config, relief="ridge", bd=1,
                  textvariable=self.re_val["Return"]),
            Label(self.record_WidgetFrame["Status Frame"], text="NON RETURN\nNUMBER", **rp_sb_config),
            Label(self.record_WidgetFrame["Status Frame"], **rp_sb_config, relief="ridge", bd=1,
                  textvariable=self.re_val["Rent"])
        ]
        self.record_MenuFrame.pack(fill="x")
        self.record_WidgetFrame["Name Frame"].pack(side="top", fill="x", padx=40, pady=10)
        self.record_WidgetFrame["Status Frame"].pack(side="bottom", fill="x", padx=10, pady=10)
        self.record_widget[0].pack(fill="both")
        self.record_widget[1].pack(side="left")
        self.record_widget[2].pack(side="left", padx=10)
        self.record_widget[3].pack(side="left")
        self.record_widget[4].pack(side="left", padx=10)
        self.record_widget[5].pack(side="left")
        self.record_widget[6].pack(side="left", padx=10)

    def __tbl_record(self):
        self.tbl_RecordFrame = Frame(self, **m_color)
        self.tbl_RecordFrame.pack(side="left", fill="both", expand=1)
        self.columns = ("#1", "#2", "#3", "#4", "5", "6")
        self.tbl_TreeView = ttk.Treeview(self.tbl_RecordFrame, column=self.columns, show="headings")
        self.tbl_TreeView.heading("#1", text="Order ID")
        self.tbl_TreeView.heading("#2", text="Rent Date")
        self.tbl_TreeView.heading("#3", text="Due Date")
        self.tbl_TreeView.heading("#4", text="Return Date")
        self.tbl_TreeView.heading("#5", text="State")
        self.tbl_TreeView.heading("#6", text="Member ID")
        self.tbl_TreeView.column("#1", anchor="s", width=200)
        self.tbl_TreeView.column("#2", anchor="s", width=200)
        self.tbl_TreeView.column("#3", anchor="s", width=200)
        self.tbl_TreeView.column("#4", anchor="s", width=200)
        self.tbl_TreeView.column("#5", anchor="s", width=200)
        self.tbl_TreeView.column("#6", anchor="s", width=200)
        self.tbl_TreeView.pack(fill="y", expand=1, padx=10)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tbl_TreeView.yview)
        self.tbl_TreeView.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="left", fill="both")

    def _tbl_Ct(self):
        data = conn.show_Order()
        self.tbl_TreeView.delete(*self.tbl_TreeView.get_children())
        al = len(data)
        re = 0
        rn = 0
        for i in data:
            if i[4] == "1":
                re += 1
                reDay = conn.get_reDate(i[0])
                self.tbl_TreeView.insert("", 'end', values=(i[0], i[2], i[3], reDay, i[4] == "1", i[1]))
            elif i[4] == "0":
                rn += 1
                self.tbl_TreeView.insert("", 'end', values=(i[0], i[2], i[3], "-", i[4] == "1", i[1]))
        self.re_val["ALL"].set(str(al))
        self.re_val["Return"].set(str(re))
        self.re_val["Rent"].set(str(rn))


class MainFrame(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(**m_color)
        self.pack(fill="both", expand=1)
        self.menu = MenuFrame(self)
        self.title = TitleFrame(self)
        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Yatra One", 12), pady=15)
        self.style.configure("TLabel", font=("Yatra One", 12), width=15, anchor="e")

        def show(event):
            container.deiconify()
            container.overrideredirect(1)

        def appear(event):
            container.overrideredirect(1)

        self.bind("<Button-3>", show)
        self.bind("<Map>", appear)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.posRight = int(self.winfo_screenwidth() / 2 - 700)
        self.posDown = int(self.winfo_screenheight() / 2 - 390)
        self.geometry("1400x750+{}+{}".format(self.posRight, self.posDown))
        self.resizable(False, False)
        self.mainFrame = MainFrame(self)


if __name__ == '__main__':
    app = App()
    app.mainloop()

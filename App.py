import datetime
import io
import os
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import sqlite3


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


# not in use right now
def convertToBinaryData(img_file):
    # Convert digital data to binary format
    with open(img_file, 'rb') as file:
        binaryData = file.read()
    return binaryData


def retrieve_data_from_db():
    try:
        sqliteConnection = sqlite3.connect('data.sqlite')
        cursor = sqliteConnection.cursor()
        sqlite_query = (
            """SELECT 
            item_image, item_id, name, item_price, item_status, entry_date, quantity, item_selling_price,
             item_description
            FROM Item_data""")
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        sqliteConnection.close()
        return data

    except sqlite3.Error as error:
        print("Failed to get data from sqlite table", error)


def save_all(item_id, name, quantity, item_price, place, item_sellingprice, status, text, date, img):
    sqliteConnection = sqlite3.connect('data.sqlite')
    cursor = sqliteConnection.cursor()
    sqlite_insert_blob_query = """ INSERT INTO item_data
                                      (item_id, name, quantity, item_price, place_of_purchase, item_selling_price, 
                                      item_status, item_description, entry_date, item_image)
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    print("Connected to SQLite")
    byteImgIO = io.BytesIO()
    byteImg = Image.open(img)
    byteImg.save(byteImgIO, "PNG")
    byteImgIO.seek(0)
    byteImg = byteImgIO.read()
    if item_price == '':
        item_price = "0"
    if item_sellingprice == '':
        item_sellingprice = "0"
    data_tuple = (
        int(item_id), name, int(quantity), float(item_price), place,
        float(item_sellingprice), status, text, date, byteImg)

    try:
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("data inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def view_data_screen(data_insPanel, imagePanel, idLabel, idEnry, saveBtn, uploadBtn, exitBtn, resetBtn, dataViewBtn):
    data_insPanel.destroy()
    imagePanel.destroy()
    idLabel.destroy()
    idEnry.destroy()
    saveBtn.destroy()
    uploadBtn.destroy()
    exitBtn.destroy()
    resetBtn.destroy()
    dataViewBtn.destroy()
    Appcreator.data_view()


def upload_img(panel):
    global display_img
    global img_path
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="select file name", filetypes=(
        ("JPG File", "*.jpg"), ("PNG File", "*.png"), ("All Files", "*.txt")))
    if filename == "":
        filename = "imges/question-mark.png"
    img = (Image.open(filename))
    img_path = filename
    resized_img = img.resize((round(Appcreator.winX / 6), round(Appcreator.winY / 3)))
    display_img = ImageTk.PhotoImage(resized_img)
    panel.config(image=display_img)


def Status_check(widget, panel):
    param = widget.get()

    c = tkinter.Canvas(panel, width=40, height=40, bg="#C0C0C0")
    c.place(x=Appcreator.winX / 5 * 3.6, y=Appcreator.winY / 5 * 1.55)
    if param == 'For sale':
        c.create_oval(5, 5, 38, 38, fill="green")
    elif param == 'Hold':
        c.create_oval(5, 5, 38, 38, fill="yellow")
    elif param == 'Sold':
        c.create_oval(5, 5, 38, 38, fill="red")
    else:
        c.create_oval(5, 5, 38, 38, fill="#C0C0C0")


display_img = PhotoImage
img_path = ""
page_counter_variable = 0


def retrieve_last_id():
    sqliteConnection = sqlite3.connect('data.sqlite')
    cursor = sqliteConnection.cursor()
    cursor.execute("""SELECT COUNT(*) FROM Item_data""")
    var = cursor.fetchone()
    sqliteConnection.close()
    return var[0] + 1


def data_view_purge(dataViewFrame):
    for widget in dataViewFrame.winfo_children():
        widget.destroy()


def data_show(dataViewFrame, Var):
    global page_counter_variable
    dataList = retrieve_data_from_db()
    items_num = len(dataList)
    j = Var
    dimx = Appcreator.winX / 5 * 4
    dataViewFrame.config(text=" Items ", bg="#C0C0C0", fg="black",
                         width=Appcreator.winX / 5 * 4, height=Appcreator.winY)
    dataViewFrame.place(x=0, y=Appcreator.winY / 10)
    dataViewFrame.grid_propagate(FALSE)
    label_width = round(dimx / 90)
    Label(dataViewFrame, text="image", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2, width=label_width,
          height=5).grid_configure(
        column=0, row=0, sticky="we")
    Label(dataViewFrame, text="item id", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2, width=label_width,
          height=5).grid_configure(
        column=1, row=0, sticky="we")
    Label(dataViewFrame, text="item name", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2, width=label_width,
          height=5).grid_configure(
        column=2, row=0, sticky="we")
    Label(dataViewFrame, text="item price", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2, width=label_width,
          height=5).grid_configure(
        column=3, row=0, sticky="we")
    Label(dataViewFrame, text="item status", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2, width=label_width,
          height=5).grid_configure(
        column=4, row=0, sticky="we")
    Label(dataViewFrame, text="entry date", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2, width=label_width,
          height=5).grid_configure(
        column=5, row=0, sticky="we")
    Label(dataViewFrame, text="item quantity", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2, width=label_width,
          height=5).grid_configure(
        column=6, row=0, sticky="we")
    Label(dataViewFrame, text="item selling price", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2,
          width=label_width + 5, height=5).grid_configure(column=7, row=0, sticky="we")
    Label(dataViewFrame, text="item description", bg="#C0C0C0", font="Arial 10 bold", padx=3, pady=2, width=label_width,
          height=5).grid_configure(
        column=8, row=0, sticky="we")
    for i in range(0, 6):
        if (j + i) < items_num:
            for elem in range(9):
                if elem != 0 and elem != 8:
                    (Label(dataViewFrame, text=dataList[j+i][elem], bg="#C0C0C0", font="Arial 10 bold",
                          width=label_width,  height=5, padx=3, pady=3)
                     .grid_configure(column=elem, row=i + 1, sticky="we"))
                elif elem == 0:
                    cn = io.BytesIO(dataList[j+i][elem])
                    foto = Image.open(cn)
                    pic = ImageTk.PhotoImage(foto)
                    imgLb = Label(dataViewFrame, bg="#C0C0C0", width=70, height=100)
                    imgLb.grid_configure(column=0, row=i + 1)
                    imgLb.image = pic
                    imgLb.config(image=pic)
                else:
                    tx = Text(dataViewFrame, bg="#C0C0C0", font="Arial 10 bold",
                              width=label_width + 5, height=5, padx=3, pady=3)
                    tx.grid_configure(column=elem, row=i + 1, sticky="we", columnspan=2)
                    tx.insert("1.0", dataList[j+i][elem])
        else:
            Label(dataViewFrame, text="NO", bg="#C0C0C0", font="Arial 20 bold", padx=3,
                  pady=3).grid(row=i + 1, column=0)
            Label(dataViewFrame, text="further", bg="#C0C0C0", font="Arial 20 bold", padx=3,
                  pady=3).grid(row=i + 1, column=1)
            Label(dataViewFrame, text="data", bg="#C0C0C0", font="Arial 20 bold", padx=3,
                  pady=3).grid(row=i + 1, column=2)
            Label(dataViewFrame, text="to", bg="#C0C0C0", font="Arial 20 bold", padx=3,
                  pady=3).grid(row=i + 1, column=3)
            Label(dataViewFrame, text=" show", bg="#C0C0C0", font="Arial 20 bold", padx=3,
                  pady=3).grid(row=i + 1, column=4)
            break


def insert_data_screen(dataViewFrame, data_insert_btn, exit_btn, data_value_counter, data_profit_counter):
    dataViewFrame.destroy()
    data_insert_btn.destroy()
    exit_btn.destroy()
    data_value_counter.destroy()
    data_profit_counter.destroy()
    Appcreator.data_insertion()


def total_available_item_stored():
    sqliteConnection = sqlite3.connect('data.sqlite')
    cursor = sqliteConnection.cursor()
    sqlite_query = (
        """SELECT 
        item_price, item_status, quantity
        FROM Item_data""")
    cursor.execute(sqlite_query)
    data = cursor.fetchall()
    sqliteConnection.close()
    total = 0
    for item_data in data:
        if item_data[1] != "Sold":
            total = total + int(item_data[2]) * float(item_data[0])

    return total


def total_available_item_profit():
    sqliteConnection = sqlite3.connect('data.sqlite')
    cursor = sqliteConnection.cursor()
    sqlite_query = (
        """SELECT 
        item_price, item_status, quantity
        FROM Item_data""")
    cursor.execute(sqlite_query)
    data = cursor.fetchall()
    sqliteConnection.close()
    total = 0
    for item_data in data:
        if item_data[1] == "Sold":
            total = total + int(item_data[2]) * float(item_data[0])

    return total


def increase_page_number(DelFrame):
    global page_counter_variable
    dataList = retrieve_data_from_db()
    items_num = len(dataList)
    if page_counter_variable + 6 < items_num:
        page_counter_variable += 6
    data_view_purge(DelFrame)
    print(page_counter_variable)


def decrease_page_number(DelFrame):
    global page_counter_variable
    page_counter_variable -= 6
    if page_counter_variable < 0:
        page_counter_variable = 0
    data_view_purge(DelFrame)
    print(page_counter_variable)


class Appcreator:
    root = tk.Tk()
    xSize = root.winfo_screenwidth()
    ySize = root.winfo_screenheight()

    display_img = PhotoImage

    winX = round(xSize * 3 / 4)
    winY = round(ySize * 3 / 4)
    xspace = round(xSize * 0.125)
    yspace = round(ySize * 0.125)
    winGeometry = str(winX) + 'x' + str(winY) + '+'

    root.title("Store manager")
    root.config(bg="#696969")
    pad = 3
    root.geometry(winGeometry + str(xspace) + '+' + str(yspace))

    # top side of app
    BtnFrame = tk.Frame(root, width=winX, height=winY * 0.1, bg="red")
    BtnFrame.pack(side=TOP)
    BtnFrame.pack_propagate(FALSE)
    Label(BtnFrame, text="Store Manager", font="Arial 20 bold", anchor="w", bg="red").pack(side=LEFT)

    @staticmethod
    def data_insertion():

        global display_img
        global img_path
        xFrameDim = Appcreator.winX / 5 * 3.9
        yFrameDim = Appcreator.winY / 5 * 4

        DataLoad = tk.LabelFrame(Appcreator.root, text="Item Data", width=xFrameDim, height=yFrameDim)
        DataLoad.config(fg="black", relief=GROOVE, font=20, padx=3, pady=3, bg="#C0C0C0", bd=3)
        DataLoad.place(x=Appcreator.winX / 5, y=Appcreator.winY * 0.15)

        item_id = StringVar()
        item_id.set(retrieve_last_id())
        id_label = Label(Appcreator.root, text="ID : ", font=20, bg="#696969", width=5, anchor='w')
        id_label.place(x=Appcreator.winX / 5 * 1, y=Appcreator.winY / 10 * 1.1)
        id_entry = Entry(Appcreator.root, textvariable=item_id, font=20, bg="#696969")
        id_entry.place(x=Appcreator.winX / 5 + Appcreator.winX / 30, y=Appcreator.winY / 10 * 1.1)

        date = StringVar()
        Appcreator.display_date(0, date)

        Name = StringVar()
        Appcreator.entry_creation(DataLoad, "Item Name", Name, xFrameDim / 20, yFrameDim / 20)

        Price = StringVar()
        Appcreator.entry_creation(DataLoad, "Price per Item", Price, xFrameDim / 20, yFrameDim / 20 * 4)

        Quantity = StringVar()
        Appcreator.entry_creation(DataLoad, "Quantity", Quantity, xFrameDim / 2, yFrameDim / 20)

        Place_Purchase = StringVar()
        Appcreator.entry_creation(DataLoad, "Place of purchase", Place_Purchase, xFrameDim / 2,
                                  yFrameDim / 20 * 4)

        PriceOfSale = StringVar()
        Appcreator.entry_creation(DataLoad, "Sale Price", PriceOfSale, xFrameDim / 20, yFrameDim / 20 * 7)

        (Label(DataLoad, text="Select status", font=20, fg="black", bg="#C0C0C0").
         place(x=xFrameDim / 2, y=yFrameDim / 20 * 7))

        Status = Combobox(DataLoad, values=['For sale', 'Hold', 'Sold'], font="Arial 20 bold", state='r',
                          width=25)
        Status.place(x=xFrameDim / 2, y=yFrameDim / 20 * 7 + 25)
        Status.bind('<<ComboboxSelected>>', lambda x: (Status_check(Status, DataLoad)))

        L = Label(DataLoad, text="Description", font=20, bg="#C0C0C0", width=20, anchor='w')
        L.place(x=xFrameDim / 20, y=yFrameDim / 20 * 10)
        tx = Text(DataLoad, width=round(xFrameDim / 30 * 3.1), height=round(yFrameDim / 50))
        tx.place(x=xFrameDim / 20, y=yFrameDim / 20 * 10 + 25)

        imageFrame = Frame(Appcreator.root, bd=3, bg="grey", relief=GROOVE, width=Appcreator.winX / 6,
                           height=Appcreator.winY / 3)
        imageFrame.place(x=Appcreator.winX / 55, y=Appcreator.winY / 6.5)
        display_img = PhotoImage(file="imges/question-mark.png")
        img_path = "imges/question-mark.png"
        imgLbl = Label(imageFrame, bg="black", image=display_img)
        imgLbl.image = display_img  # anchor the image to the label, otherwise the garbage collector destroys it
        imgLbl.place(x=0, y=0)

        upload_btn = Button(Appcreator.root, text="Upload", font="Arial 20", width=int(Appcreator.winX / 96),
                            bg="lightblue", command=lambda: upload_img(imgLbl))
        upload_btn.place(x=Appcreator.winX / 55, y=Appcreator.winY * 0.55)

        save_btn = Button(Appcreator.root, text="Save", font="Arial 20", width=int(Appcreator.winX / 96), bg="green",
                          command=lambda: (save_all(item_id.get(), Name.get(), Quantity.get(), Price.get(),
                                                    Place_Purchase.get(),
                                                    PriceOfSale.get(), Status.get(), tx.get("1.0", END), date.get(),
                                                    img_path), item_id.set(retrieve_last_id())))
        save_btn.place(x=Appcreator.winX / 55, y=Appcreator.winY * 0.65)

        reset_btn = Button(Appcreator.root, text="Reset", font="Arial 20", width=int(Appcreator.winX / 96), bg="yellow",
                           command=lambda: (Name.set(""), Quantity.set(""), Price.set(""), Place_Purchase.set(""),
                                            PriceOfSale.set(""), Status.set("Select status"), tx.delete("1.0", END),
                                            date.set(datetime.date.today().strftime("%d/%m/%Y"))))
        reset_btn.place(x=Appcreator.winX / 55, y=Appcreator.winY * 0.75)

        exit_btn = Button(Appcreator.root, text="Exit", font="Arial 20", width=int(Appcreator.winX / 96), bg="red",
                          command=lambda: Appcreator.root.destroy())
        exit_btn.place(x=Appcreator.winX / 55, y=Appcreator.winY * 0.85)

        data_view_btn = Button(Appcreator.BtnFrame, text="View Items", font="Arial 20 bold", width=10, padx=5, bd=5,
                               bg="lightblue", anchor="w",
                               command=lambda: view_data_screen(DataLoad, imageFrame, id_label, id_entry,
                                                                save_btn,
                                                                upload_btn, exit_btn, reset_btn, data_view_btn))
        data_view_btn.pack(side=RIGHT)

    @staticmethod
    def data_view():
        data_insert_btn = Button(Appcreator.BtnFrame, text="Insert Data", font="Arial 20 bold", width=10, padx=5, bd=5,
                                 bg="lightblue", anchor="w",
                                 command=lambda: insert_data_screen(dataViewFrame, data_insert_btn, exit_btn,
                                                                    total_item_value, total_sold_item_value))
        #                         fix this command call once delt with  data_view destruction
        data_insert_btn.pack(side=RIGHT)

        dataViewFrame = LabelFrame(Appcreator.root, text=" Items ", bg="#C0C0C0", fg="black",
                                   width=Appcreator.winX / 5 * 4, height=Appcreator.winY)
        dataViewFrame.place(x=0, y=Appcreator.winY / 10)
        dataViewFrame.grid_propagate(FALSE)

        data_show(dataViewFrame, page_counter_variable)

        exit_btn = Button(Appcreator.root, text="Exit", font="Arial 20", width=int(Appcreator.winX / 96), bg="red",
                          command=lambda: Appcreator.root.destroy())
        exit_btn.place(x=Appcreator.winX / 5 * 4.1, y=Appcreator.winY * 0.85)

        total_stored_item_value = total_available_item_stored()
        total_item_value = Label(Appcreator.root,
                                 text="Total value\n of \nstored items : \n " + str(total_stored_item_value),
                                 bg="green", font="Arial 15 bold")
        total_item_value.place(x=Appcreator.winX / 5 * 4.2, y=Appcreator.winY / 10 * 1.8)

        total_sold_item_profit = total_available_item_profit()
        total_sold_item_value = Label(Appcreator.root,
                                      text="Total value\n of \nsold items : \n " + str(total_sold_item_profit),
                                      bg="yellow", font="Arial 15 bold")
        total_sold_item_value.place(x=Appcreator.winX / 5 * 4.2, y=Appcreator.winY / 10 * 3.2)

        total_sold_bought_value = Label(Appcreator.root,
                                        text="Total difference\n of \nsold-bought\n items : \n " + str(
                                            total_sold_item_profit - total_stored_item_value),
                                        bg="white", font="Arial 15 bold")
        total_sold_bought_value.place(x=Appcreator.winX / 5 * 4.2, y=Appcreator.winY / 10 * 4.6)

        next_item_page = Button(Appcreator.root, text="Next", font="Arial 20", width=int(Appcreator.winX / 192),
                                bg="lightblue", command=lambda: (
                increase_page_number(dataViewFrame),
                data_show(dataViewFrame, page_counter_variable)))
        next_item_page.place(x=Appcreator.winX / 5 * 4.5, y=Appcreator.winY / 2 * 1.5)

        prev_item_page = Button(Appcreator.root, text="Prev", font="Arial 20", width=int(Appcreator.winX / 192),
                                bg="lightblue", command=lambda: (
                decrease_page_number(dataViewFrame),
                data_show(dataViewFrame, page_counter_variable)))
        prev_item_page.place(x=Appcreator.winX / 5 * 4.1, y=Appcreator.winY / 2 * 1.5)

    @staticmethod
    def entry_creation(panel, field_name, string_var, xpos, ypos):
        entry_name = Label(panel, text=field_name, font=20, fg="black", bg="#C0C0C0")
        entry_name.place(x=xpos, y=ypos)
        entry = Entry(panel, textvariable=string_var, font="Arial 20", width=25)
        entry.place(x=xpos, y=ypos + 25)

    @staticmethod
    def display_date(var, d):
        if var == 0:
            x = Appcreator.winX / 5 * 4.2
            y = Appcreator.winY / 10 * 1.1
        else:
            x = 4
            y = 4
        date = Label(Appcreator.root, text="Date :", font=20, fg="black", bg="#696969")
        date.place(x=Appcreator.winX / 5 * 4, y=Appcreator.winY / 10 * 1.1)
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        d.set(d1)
        date_entry = Entry(Appcreator.root, textvariable=d, font=20, fg="black", bg="#696969", width=19)
        date_entry.place(x=x, y=y)

    def run_main(self):
        self.root.mainloop()

from calendar import c
from optparse import Values
from re import I
from tkinter import *
from tkinter.tix import Select
import customtkinter as ck
from PIL import ImageTk, Image
from tkcalendar import Calendar, DateEntry
from  datetime import date
import sqlite3

# git push

ck.set_appearance_mode("system")  # Modes: system (default), light, dark
#ck.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


main = Tk()
main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(0, weight=1)
main.title("Lang Too Yen") #Heading
main.iconbitmap('c:/Users/pound/Downloads/LangTooYen/Icon/icon.ico')
main.geometry("480x730")
main.resizable(False, False)
main.config(bg="#ffc700")

# ========== Database ==========
def fridgeingre():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c. execute("""SELECT ingredient_name,
               type,
               quantity,
               quantity_unit,
               expired_date
            from in_fridge
            JOIN ingre 
            on ingre.ingredient_id = in_fridge.ingredient_id
""")
    records = c.fetchall()
    conn.commit()
    conn.close()
    #print(records)
    return records

def menubook():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""SELECT menu_name,
                    
                    ingredient_name,
                    type,
                    amount,
                    quantity_unit
                FROM menu
                join menu_ingre
                ON menu.menu_id = menu_ingre.menu_id
                Join ingre
                On ingre.ingredient_id = menu_ingre.ingredients_id
""")
    records = c.fetchall()
    #print(records)
    conn.commit()
    conn.close()
    return records

def menupic():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""SELECT menu_name,
                    pic_path
                FROM menu
""")
    records = c.fetchall()
    conn.commit()
    conn.close()
    return records

def ingrerowcount():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""SELECT COUNT(*)
                FROM ingre""")
    count = c.fetchall()
    count = count[0][0]
    conn.commit()
    conn.close()
    return count
    
def cartlist():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""SELECT name,quantity,unit
                FROM cart""")
    records = c.fetchall()
    conn.commit()
    conn.close()
    return records

# ========== Page ==========

#first page
def MainPage():
    global a, LANG, TOO, YEN, ButtonMyIn, ButtonKin, ButtonShop, TextEx, Base, ExDate1, Name1, Head

    a = 0

    Base = ck.CTkTextbox(main, 
                       width=1000, 
                       height=1000, 
                       border_spacing=0, 
                       corner_radius=20, 
                       border_width=0, 
                       fg_color="#ffc700", 
                       border_color="#ffc700",
                       state="disabled")
    Base.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

    LANG = ck.CTkLabel(main, 
                   text="LANG", 
                   text_color="#ff4d00", 
                   fg_color="transparent", 
                   font=("Segoe UI Bold", 75))
    LANG.place(relx=0.5, rely=0.08, anchor=ck.CENTER)

    TOO = ck.CTkLabel(main, 
                  text="TOO", 
                  text_color="#ff4d00",  
                  fg_color="transparent",
                  font=("Segoe UI Bold", 75))
    TOO.place(relx=0.5, rely=0.195, anchor=ck.CENTER)

    YEN = ck.CTkLabel(main, 
                  text="YEN", 
                  text_color="#ff4d00", 
                  fg_color="transparent", 
                  font=("Segoe UI Bold", 75))
    YEN.place(relx=0.5, rely=0.31, anchor=ck.CENTER)

    ButtonMyIn = ck.CTkButton(main, 
                          text="My Ingredient", 
                          font=("Segoe UI Bold", 23), 
                          width=300, 
                          height=56, 
                          corner_radius=40, 
                          border_width=2, 
                          fg_color="#ffdd64", 
                          hover_color="#fee692", 
                          border_color="#000000",
                          text_color="#000000", 
                          command=MyIn)                  
    ButtonMyIn.place(relx=0.5, rely=0.42, anchor=ck.CENTER)

    ButtonKin = ck.CTkButton(main, 
                         text="KIN RAI DEE", 
                         font=("Segoe UI Bold", 23), 
                         width=300, 
                         height=56, 
                         corner_radius=40, 
                         border_width=2, 
                         fg_color="#ffdd64", 
                         hover_color="#fee692", 
                         border_color="#000000",
                         text_color="#000000", 
                         command=MenuPageWait)                  
    ButtonKin.place(relx=0.5, rely=0.5075, anchor=ck.CENTER)

    ButtonShop = ck.CTkButton(main, 
                          text="Shopping List", 
                          font=("Segoe UI Bold", 23), 
                          width=300, 
                          height=56, 
                          corner_radius=40, 
                          border_width=2, 
                          fg_color="#ffdd64", 
                          hover_color="#fee692", 
                          border_color="#000000",
                          text_color="#000000",
                          command = shoplist)                  
    ButtonShop.place(relx=0.5, rely=0.595, anchor=ck.CENTER)

    #Textbox for displaying things that will soon expire (top 5 / top 3)
    TextEx = ck.CTkFrame(main, 
                         width=390, 
                         height=210, 
                         corner_radius=20, 
                         border_width=2, 
                         fg_color="#FFA100", 
                         border_color="#000000")
    TextEx.place(relx=0.5, rely=0.8, anchor=ck.CENTER)

    Head = ck.CTkLabel(TextEx, 
                       width = 140,
                       text="About to expire : ", 
                       font=("Segoe UI Bold", 16),
                       fg_color="transparent")
    Head.place(relx=0.23, rely=0.15, anchor=ck.CENTER)
    
    #Ingredient Name
    Name1 = ck.CTkTextbox(main, 
                       width = 170,
                       height = 135,
                       fg_color="#FFA100",
                       text_color = "#000000",
                       corner_radius=0,
                       border_width = 0,
                       border_color = "#FFA100",
                       border_spacing = 0,
                       font=("Segoe UI Bold", 15),
                       activate_scrollbars = False)
    # main page : sort by expired date
    data = fridgeingre()
    sorted_data = sorted(data, key=lambda x: x[4])
    sorted_data = sorted_data[:5]

    if data:
        for i in reversed(sorted_data):
            clean = i[4].split(" ",1)[0]
            d = (i[0],i[1],i[2],i[3],clean)
            Name1.insert(index=1.0,text="{}\n".format(d[0]))
        # Name1.insert(index=1.0,text="{}\t{}\n".format(name))
        Name1.place(relx=0.4, rely=0.82, anchor=ck.CENTER)
        Name1.configure(state="disabled")
    else:
        print("No data")

    #Expired Date
    ExDate1 = ck.CTkTextbox(main, 
                       width = 100,
                       height = 135,
                       fg_color="#FFA100",#FFA100
                       text_color = "#000000",
                       corner_radius=0, 
                       border_width = 0,  
                       border_spacing = 0,
                       border_color = "#FFA100",                    
                       font=("Segoe UI Bold", 15),
                       activate_scrollbars = False)
    ExDate1.place(relx=0.69, rely=0.82, anchor=ck.CENTER)
    for i in reversed(sorted_data):
        d = [i[0],i[1],i[2],i[3],i[4]]
        ExDate1.insert(index=1.0, text="{}\n".format(d[4]))
    ExDate1.configure(state="disabled") 


#My Ingredient Page
def MyIn():
    global ImageLabel1, imgChef, imgBackPage, ImageLabel2, In, ComboCtgr, LabelIn, LabelEd, FrameList, ImageLabel7, Name, ExDate

    DeletePage("Main")

    Base = ck.CTkTextbox(main, 
                       width=1000, 
                       height=1000, 
                       border_spacing=0, 
                       corner_radius=20, 
                       border_width=0, 
                       fg_color="#ffc700", 
                       border_color="#ffc700",
                       state="disabled")
    Base.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

    imgChef = ck.CTkImage(dark_image = Image.open("Icon/chef.png"), 
                          size=(185, 185))
    ImageLabel1 = ck.CTkLabel(main, 
                              image=imgChef, 
                              text="My", 
                              text_color="#ff4d00", 
                              font=("Segoe UI Bold", 60))
    ImageLabel1.place(relx=0.05, rely=0.049)

    imgBackPage = ck.CTkImage(dark_image = Image.open("Icon/BackPage1.png"), 
                          size=(30, 30))
    ImageLabel2 = ck.CTkButton(main, 
                              image=imgBackPage,
                              border_width = 0,
                              width=35, 
                              height=35, 
                              fg_color = "transparent",
                              text = "",
                              hover = False, 
                              command = lambda: BacktoMain("MyIn"))
    ImageLabel2.place(relx=0.015, rely=0.015)

    imgAdd = ck.CTkImage(dark_image = Image.open("Icon/Add.png"), 
                          size=(50, 50))
    ImageLabel7 = ck.CTkButton(main, 
                              image=imgAdd,
                              border_width = 0,
                              width=35, 
                              height=35, 
                              fg_color = "transparent",
                              text = "",
                              hover = False, 
                              command = ADDINGR)
    ImageLabel7.place(relx=0.87, rely=0.003)

    In = ck.CTkLabel(main, 
                     text="Ingredient", 
                     text_color="#ff4d00",  
                     fg_color="transparent",
                     font=("Segoe UI Bold", 50))
    In.place(relx=0.62, rely=0.245, anchor=ck.CENTER)

    #Dropdown List
    ComboStart = ck.StringVar(value="All")
    ComboCtgr = ck.CTkComboBox(main, 
                               values=["All", "Meat", "Spice", "Dairy Product", "Fruit", "Vegetable", "Others"],
                               width = 215,
                               height = 40,
                               corner_radius = 40,
                               border_width=2, 
                               fg_color="#ffdd64", 
                               border_color="#000000",
                               button_color = "#FF7500",
                               button_hover_color = "#FF9A45",
                               dropdown_fg_color = "#ffdd64", 
                               dropdown_hover_color = "#fee692",
                               dropdown_text_color = "#000000", 
                               text_color = "#000000",
                               font =("Segoe UI Bold", 16),
                               dropdown_font = ("Segoe UI", 16),
                               hover = True,
                               variable=ComboStart,
                               state="readonly",
                               command = MyInChoose)  
    #Will add the command function later eg.If you selected Meat, certain information will pop up. 
    ComboCtgr.place(relx=0.7, rely=0.33, anchor=ck.CENTER)

    LabelIn = ck.CTkLabel(main, 
                          text="Ingredients", 
                          fg_color="transparent",
                          text_color = "#000000",
                          font =("Segoe UI Bold", 20))
    LabelIn.place(relx=0.29, rely=0.41, anchor=ck.CENTER)

    LabelEd = ck.CTkLabel(main, 
                          text="Expired Date", 
                          fg_color="transparent",
                          text_color = "#000000",
                          font =("Segoe UI Bold", 20))
    LabelEd.place(relx=0.68, rely=0.41, anchor=ck.CENTER)

    FrameList = ck.CTkScrollableFrame(main, 
                                      width=370, 
                                      height=360,
                                      border_width = 0,
                                      fg_color = "#ffdd64",
                                      border_color = "#000000",
                                      scrollbar_fg_color = "#ffdd64",
                                      scrollbar_button_color = "#dddddd",
                                      scrollbar_button_hover_color = "#000000")
    FrameList.place(relx=0.5, rely=0.7, anchor=ck.CENTER)

    #Ingredient Name Page
    ingre_name, ingre_exp = myin_sortbyexp()
    Name = ck.CTkLabel(FrameList, 
                          width = 180,
                          text = ingre_name, #insert ingredient here
                          fg_color="transparent")
    Name.pack(pady=7, side=LEFT)

    #Expired Date
    ExDate = ck.CTkLabel(FrameList, 
                          width = 180,
                          text = ingre_exp, #insert expired date here
                          fg_color="transparent")
    ExDate.pack(pady=7, side=RIGHT)

    #I separated 2 info so that it'll align better
    

def MenuPageWait():

    Base = ck.CTkTextbox(main, 
                       width=1000, 
                       height=1000, 
                       border_spacing=0, 
                       corner_radius=20, 
                       border_width=0, 
                       fg_color="#ffc700", 
                       border_color="#ffc700",
                       state="disabled")
    Base.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

    main.after(10, MenuPage)


def MenuPage():
    global a, menu, recom, ImageLabel3, SearchMenu, ImageLabel4, ImageLabel5, ImageLabel6, Frame1, outrec, outlinerec, ImageLabel98

    a = 1

    DeletePage("Main")

    menu = ck.CTkLabel(main, 
                       text="Menu", 
                       text_color="#ff4d00",  
                       fg_color="transparent",
                       font=("Segoe UI Bold", 60))
    menu.place(relx=0.5, rely=0.065, anchor=ck.CENTER)

    imgBackPage = ck.CTkImage(dark_image = Image.open("Icon/BackPage1.png"), 
                          size=(30, 30))
    ImageLabel3 = ck.CTkButton(main, 
                              image=imgBackPage,
                              border_width = 0,
                              width=35, 
                              height=35, 
                              fg_color = "transparent",
                              text = "",
                              hover = False, 
                              command = lambda: BacktoMain("Menu"))
    ImageLabel3.place(relx=0.015, rely=0.015)

    imgToCart = ck.CTkImage(dark_image = Image.open("Icon/Cart.png"), 
                          size=(40, 40))
    ImageLabel98 = ck.CTkButton(main, 
                              image=imgToCart,
                              border_width = 0,
                              width=35, 
                              height=35, 
                              fg_color = "transparent",
                              text = "",
                              hover = False, 
                              command = MenuToShopping)
    ImageLabel98.place(relx=0.92, rely=0.043, anchor=ck.CENTER)

    SearchMenu = ck.CTkEntry(main, 
                             width = 390,
                             height = 47,
                             corner_radius = 40,
                             border_width = 2,
                             border_color = "#000000",
                             fg_color = "#FFDD64",
                             text_color = "#000000",
                             placeholder_text_color = "#646464",
                             placeholder_text="enter menu",
                             font=("Segoe UI Bold", 15))
    SearchMenu.place(relx=0.5, rely=0.16, anchor=ck.CENTER)

    imgSe = ck.CTkImage(dark_image = Image.open("Icon/seicon.png"), 
                          size=(25, 25))
    ImageLabel6 = ck.CTkButton(main, 
                              image=imgSe,
                              border_width = 3,
                              corner_radius = 0,
                              width=38, 
                              height=38, 
                              border_color = "#FFDD64",
                              fg_color = "#FFDD64",
                              text = "",
                              hover = False)
    ImageLabel6.place(relx=0.785, rely=0.16, anchor=ck.CENTER)

    imgClear = ck.CTkImage(dark_image = Image.open("Icon/clearicon.png"), 
                          size=(20, 20))
    ImageLabel4 = ck.CTkButton(main, 
                              image=imgClear,
                              border_width = 1,
                              corner_radius = 0,
                              width=36, 
                              height=36,
                              fg_color = "#FFDD64",
                              border_color = "#FFDD64",
                              text = "",
                              hover = False, 
                              command = lambda: ClearOut("Menu"))
    ImageLabel4.place(relx=0.735, rely=0.16, anchor=ck.CENTER)

    imgSearch = ck.CTkImage(dark_image = Image.open("Icon/searchicon.png"), 
                          size=(25, 25))
    ImageLabel5 = ck.CTkButton(main, 
                              image=imgSearch,
                              border_width = 3,
                              corner_radius = 0,
                              width=38, 
                              height=38, 
                              border_color = "#FFDD64",
                              fg_color = "#FFDD64",
                              text = "",
                              hover = False,
                              command = search)
    ImageLabel5.place(relx=0.835, rely=0.159, anchor=ck.CENTER)

    Frame1 = ck.CTkScrollableFrame(main, 
                         width=435 ,
                         height=545,
                         border_width = 0,
                         corner_radius = 0,
                         fg_color = "#ffc700",#ffc700
                         border_color = "#000000",
                         scrollbar_fg_color = "#ffc700",
                         scrollbar_button_color = "#777777",
                         scrollbar_button_hover_color = "#444444")
    Frame1.place(relx=0.52, rely=0.588, anchor=ck.CENTER)

    outrec = ck.CTkFrame(Frame1, 
                         width=120,
                         height=150,
                         border_width = 2,
                         corner_radius = 15,
                         fg_color = "#ffc700",
                         border_color = "#ffc700")
    outrec.pack(fill = 'both')

    outlinerec = ck.CTkFrame(Frame1, 
                         width=400,
                         height=150,
                         border_width = 2,
                         corner_radius = 15,
                         fg_color = "#ffc700",
                         border_color = "#ffc700")
    outlinerec.pack()

    WOW = ck.CTkFrame(Frame1, 
                         width=120,
                         height=15,
                         border_width = 5,
                         corner_radius = 2,
                         fg_color = "#ffc700",
                         border_color = "#ffc700")
    WOW.pack(fill = 'both')

    recom = ck.CTkLabel(outrec, 
                       text="RECOMMENDATION :", 
                       text_color="#000000",  
                       fg_color="transparent",
                       font=("Segoe UI Bold", 19),
                       justify = "right")
    recom.pack(padx= 23, pady=5, side=LEFT)

    MenuSearch()


def ADDINGR():
    global ADD, INGR, ING, entry_ingredient, EXPDATE, entry_expdate, expired_date, button_enter, label_show, Base, ImageLabe20, ImageLabe21, imgClear1, ImageLabel14, ComboCtgr1, CAT, ImageLabe23, QUAN, entry_quan, UNIT, ComboCtgr2, ComboStart1, ComboStart2

    DeletePage("MyIn")
    
    Base = ck.CTkTextbox(main, 
                       width=1000, 
                       height=1000, 
                       border_spacing=0, 
                       corner_radius=20, 
                       border_width=0, 
                       fg_color="#ffc700", 
                       border_color="#ffc700",
                       state="disabled")
    Base.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

    imgBackPage = ck.CTkImage(dark_image = Image.open("Icon/BackPage1.png"), 
                          size=(30, 30))
    ImageLabel14 = ck.CTkButton(main, 
                              image=imgBackPage,
                              border_width = 0,
                              width=35, 
                              height=35, 
                              fg_color = "transparent",
                              text = "",
                              hover = False, 
                              command = MyIn)
    ImageLabel14.place(relx=0.015, rely=0.015)

    #Title "Add ingredient"
    ADD = ck.CTkLabel(main, 
                      text="Add", 
                      text_color="#ff4d00", 
                      fg_color="transparent", 
                      font=("Segoe UI Bold", 75))
    ADD.place(relx=0.5, rely=0.075, anchor=ck.CENTER)

    INGR = ck.CTkLabel(main, 
                       text="Ingredient", 
                       text_color="#ff4d00",  
                       fg_color="transparent",
                       font=("Segoe UI Bold", 75))
    INGR.place(relx=0.5, rely=0.195, anchor=ck.CENTER)

    ING = ck.CTkLabel(main,  
                      text="ingredient: ",
                      text_color = "#000000", 
                      fg_color="transparent", 
                      font=("Segoe UI Bold", 15))
    ING.place(relx=0.135, rely=0.42)
    
    # entry your ingredient
    entry_ingredient = ck.CTkEntry(main, 
                                   placeholder_text="enter your ingredient", 
                                   font=("Segoe UI Bold", 13), 
                                   width=300, height=45, 
                                   corner_radius=40,
                                   fg_color="#FFDD64", 
                                   border_width = 2,
                                   border_color="#000000",
                                   placeholder_text_color="gray", 
                                   text_color = "#000000",
                                   state="normal")# outer, inner
    entry_ingredient.place(relx=0.12, rely=0.465)

    EXPDATE = ck.CTkLabel(main, 
                          text="expired date: ",
                          text_color = "#000000", 
                          fg_color="transparent", 
                          font=("Segoe UI Bold", 15))
    EXPDATE.place(relx=0.135, rely=0.67)

    #entry expired date
    entry_expdate = ck.CTkEntry(main, 
                                placeholder_text=" ", 
                                font=("Segoe UI Bold", 13), 
                                width=300, height=45, 
                                corner_radius=40,
                                fg_color="#FFDD64", 
                                border_width = 2,
                                border_color="#000000",
                                placeholder_text_color="gray", 
                                text_color = "#000000",
                                state="normal")# outer, inner
    entry_expdate.place(relx=0.12, rely=0.715)

    expired_date = ck.CTkButton(main, text="YYYY-MM-DD",
                            width=80, height=30,
                            font=("Segoe UI Bold", 12),
                            text_color="gray",
                            corner_radius=40, 
                            fg_color="#FFDD64",
                            bg_color="#FFDD64",
                            hover = False,
                            command=show_calendar)
    expired_date.place(relx=0.14, rely=0.725)

    #categories
    CAT = ck.CTkLabel(main, 
                      text="  categories: ",
                      text_color = "#000000", 
                      fg_color="transparent", 
                      font=("Segoe UI Bold", 15))
    CAT.place(relx=0.12, rely=0.30)

    ComboStart1 = ck.StringVar(value=" ")
    ComboCtgr1 = ck.CTkComboBox(main, 
                                values=["Meat", "Spice", "Dairy Product", "Fruit", "Vegetable", "Others"],
                                width = 200,
                                height = 43,
                                corner_radius = 40,
                                border_width=2, 
                                fg_color="#ffdd64", 
                                border_color="#000000",
                                button_color = "#FF7500",
                                button_hover_color = "#FF9A45",
                                dropdown_fg_color = "#ffdd64", 
                                dropdown_hover_color = "#fee692",
                                dropdown_text_color = "#000000", 
                                text_color = "#000000",
                                font =("Segoe UI Bold", 13),
                                dropdown_font = ("Segoe UI", 13),
                                hover = True,
                                variable=ComboStart1,
                                state="readonly")
    ComboCtgr1.place(relx=0.33, rely=0.37, anchor=ck.CENTER)

    validation_cmd = main.register(validate_input)  # Register the validation function

    #quantity
    QUAN = ck.CTkLabel(main, text="quantity: ",
                        text_color = "#000000", 
                        fg_color="transparent", 
                        font=("Segoe UI Bold", 15))
    QUAN.place(relx=0.135, rely=0.54)

    entry_quan = ck.CTkEntry(main, 
                             placeholder_text="enter quantity", 
                             font=("Segoe UI Bold", 13), 
                             width=190, height=45, 
                             corner_radius=40,
                             fg_color="#FFDD64", 
                             border_width = 2,
                             border_color="#000000",
                             placeholder_text_color="gray", 
                             text_color = "#000000",
                             state="normal",
                             validate="key", 
                             validatecommand=(validation_cmd, '%P'))
    entry_quan.place(relx=0.12, rely=0.585)

        #unit
    UNIT = ck.CTkLabel(main, text="unit: ",
                        text_color = "#000000", 
                        fg_color="transparent", 
                        font=("Segoe UI Bold", 15))
    UNIT.place(relx=0.60, rely=0.54)

    ComboStart2 = ck.StringVar(value=" ")
    ComboCtgr2 = ck.CTkComboBox(main, 
                                values=["g", "pieces"],
                                width = 150,
                                height = 43,
                                corner_radius = 40,
                                border_width=2, 
                                fg_color="#ffdd64", 
                                border_color="#000000",
                                button_color = "#FF7500",
                                button_hover_color = "#FF9A45",
                                dropdown_fg_color = "#ffdd64", 
                                dropdown_hover_color = "#fee692",
                                dropdown_text_color = "#000000", 
                                text_color = "#000000",
                                font =("Segoe UI Bold", 13),
                                dropdown_font = ("Segoe UI", 13),
                                hover = True,
                                variable=ComboStart2,
                                state="readonly")
    ComboCtgr2.place(relx=0.75, rely=0.6127, anchor=ck.CENTER)

    #Enter button
    button_enter = ck.CTkButton(main, 
                                text="Enter",
                                font=("Segoe UI Bold", 15), 
                                width = 80, height = 55,
                                fg_color="#ff4d00",
                                text_color="#ffffff",
                                hover_color="#ff6f2f",
                                command=submit)
    button_enter.place(relx=0.5, rely= 0.86, anchor=ck.CENTER)

    #show
    label_show = ck.CTkLabel(main, 
                             text="", 
                             text_color="#000000",  
                             fg_color="transparent",
                             font=("Segoe UI Bold", 12))
    label_show.place(relx=0.5, rely=0.93, anchor=ck.CENTER)

    #clear
    imgClear1 = ck.CTkImage(dark_image = Image.open("Icon/clearicon.png"), 
                            size=(15, 15))
    ImageLabe20 = ck.CTkButton(main, 
                                image=imgClear1,
                                border_width = 1,
                                corner_radius = 0,
                                width=36, 
                                height=36,
                                fg_color = "#FFDD64",
                                border_color = "#FFDD64",
                                text = "",
                                hover = False, 
                                command= lambda: ClearOut(1))
    ImageLabe20.place(relx=0.68, rely=0.493, anchor=ck.CENTER)

    ImageLabe23= ck.CTkButton(main, 
                               image=imgClear1,
                               border_width = 1,
                               corner_radius = 0,
                               width=36, 
                               height=36,
                               fg_color = "#FFDD64",
                               border_color = "#FFDD64",
                               text = "",
                               hover = False, 
                               command= lambda: ClearOut(3))
    ImageLabe23.place(relx=0.45, rely=0.615, anchor=ck.CENTER)
    

def shoplist():
    global SHP, FrameList10, INGR, EXP, ImageLabel54, Amount, Name2

    DeletePage("Main")

    Base = ck.CTkTextbox(main, 
                       width=1000, 
                       height=1000, 
                       border_spacing=0, 
                       corner_radius=20, 
                       border_width=0, 
                       fg_color="#ffc700", 
                       border_color="#ffc700",
                       state="disabled")
    Base.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

    imgBackPage = ck.CTkImage(dark_image = Image.open("Icon/BackPage1.png"), 
                          size=(30, 30))
    ImageLabel54 = ck.CTkButton(main, 
                              image=imgBackPage,
                              border_width = 0,
                              width=35, 
                              height=35, 
                              fg_color = "transparent",
                              text = "",
                              hover = False, 
                              command = SpecialBack)
    ImageLabel54.place(relx=0.015, rely=0.015)

    #Title "Add ingredient"
    SHP = ck.CTkLabel(main, text="Shopping List", 
                    text_color="#ff4d00", 
                    fg_color="transparent", 
                    font=("Segoe UI Bold", 60))
    SHP.place(relx=0.5, rely=0.12, anchor=ck.CENTER)

    FrameList10 = ck.CTkScrollableFrame(main, 
                                        width=370, 
                                        height=420,
                                        border_width = 0,
                                        fg_color = "#ffdd64",
                                        border_color = "#000000",
                                        scrollbar_fg_color = "#ffdd64",
                                        scrollbar_button_color = "#dddddd",
                                        scrollbar_button_hover_color = "#000000")
    FrameList10.place(relx=0.5, rely=0.58, anchor=ck.CENTER)

    ClearButt = ck.CTkButton(main, 
                                text="Clear",
                                font=("Segoe UI Bold", 15), 
                                width = 70, 
                                height = 45,
                                fg_color="#ff4d00",
                                text_color="#ffffff",
                                hover_color="#ff6f2f",
                                command=before_clearcart)
    ClearButt.place(relx=0.5, rely= 0.92, anchor=ck.CENTER)

    #list
    INGR = ck.CTkLabel(main, text="Ingredient list ",
                    text_color = "#000000", 
                    fg_color="transparent", 
                    font=("Segoe UI Bold", 20))
    INGR.place(relx=0.195, rely=0.23)
    #amount

    EXP = ck.CTkLabel(main, text="Amount ",
                    text_color = "#000000", 
                    fg_color="transparent", 
                    font=("Segoe UI Bold", 20))
    EXP.place(relx=0.65, rely=0.23)

    #Ingredient Name
    data = cartlist()
    ingredient_totals = {}
    for item in data:
        ingredient_name, quantity, unit = item
        if ingredient_name in ingredient_totals:
            ingredient_totals[ingredient_name] += quantity
        else:
            ingredient_totals[ingredient_name] = quantity
    # print("cartlist: ", data)
    print("ingredient_totals: ".upper())
    print("ingredient_totals: ", ingredient_totals)
    ingredient_name = ''
    quantity = ''
    for i in ingredient_totals:
        if i:
            ingredient_name += str(i+"\n")
            quantity += str(round(ingredient_totals[i],2))+" g"+"\n"
        else:
            print("ingredient_totals: No data")
    Name2 = ck.CTkLabel(FrameList10, 
                          width = 220,
                          text=ingredient_name, #insert ingredient name here
                          fg_color="transparent")
    Name2.pack(pady=7, side=LEFT)

    #Amount
    Amount = ck.CTkLabel(FrameList10, 
                          width = 140,
                          text=quantity,  #insert Amount here
                          fg_color="transparent")
    Amount.pack(pady=7, side=RIGHT)

    #I separated 2 info so that it'll align better


def MenuToShopping():
    DeletePage("Menu")
    shoplist()


def validate_input(P):
    if P.isdigit():
        return True
    elif P == "" or P == "-":
        return True
    else:
        return False
    

def MenuSearch():
    global n

    n = 3  #the recommendation menu amount 1-3
    recommendation(n)

    Menulist()

    

def Menulist():
    global OMG, OMGframes, OMGimgFoodRecs, OMGImagePICs, OMGImageFoodTs, imgSEs, ImageLabelESs, imgSE2s, ImageLabelES2s
    global FoodHaves, FoodMisss, Haves, Misss
    global OMG, OMGimgFoodRec, OMGImagePIC, OMGImageFoodT, imgSE, ImageLabelES, imgSE2, ImageLabelES2
    global FoodHave, FoodMiss, HAVE, MISS
    global box_count

    OMGframes = []  # Create an empty list to store frames
    imgSEs = [] 
    ImageLabelESs = [] 
    imgSE2s = [] 
    ImageLabelES2s = [] 
    OMGimgFoodRecs = []  #Food pic
    OMGImagePICs = []
    OMGImageFoodTs = []  #Food name
    FoodHaves = []
    FoodMisss = []
    Haves = [] #have list
    Misss = [] #miss list
    bigmiss =[]


    menu = menubook()
    ingre = fridgeingre()
    path = menupic()
    sorted_ingre = sorted(ingre, key=lambda x: x[4])
    # print("\nMENU",menu)
    join = []
    if menu:
        for i in sorted_ingre:
            for j in menu:
                if i[0] == j[1]:
                    join.append(j)
    else: print("No Data")
    # print("\n\nJoin".upper(),join)
    subjoin=join[3:]
    m = 5 #number of menu showing
    # for i in range(m):
    #     subjoin.append(join[i])
    box_count = m
    for i in range(m):
        OMG = ck.CTkFrame(Frame1, 
                            width=390,
                            height=220,
                            border_width = 2,
                            corner_radius = 15,
                            fg_color = "#FFDD64",
                            border_color = "#000000")
        OMG.pack(pady = 8)

        imgSE = ck.CTkImage(dark_image = Image.open("Icon/seicon.png"), 
                          size=(25, 200))
        ImageLabelES = ck.CTkButton(OMG, 
                                image=imgSE,
                                border_width = 3,
                                corner_radius = 0,
                                width=38, 
                                height=38, 
                                border_color = "#FFDD64",
                                fg_color = "#FFDD64",
                                text = "",
                                hover = False)
        ImageLabelES.place(relx=0.40, rely=0.5, anchor=ck.CENTER)

        imgSE2 = ck.CTkImage(dark_image = Image.open("Icon/seicon2.png"), 
                          size=(220, 25),)
        ImageLabelES2 = ck.CTkButton(OMG, 
                                image=imgSE2,
                                border_width = 0,
                                corner_radius = 0,
                                width=38, 
                                height=38, 
                                border_color = "#FFDD64",
                                fg_color = "#FFDD64",
                                text = "",
                                hover = False)
        ImageLabelES2.place(relx=0.699, rely=0.5, anchor=ck.CENTER)

        for p in path:
            if subjoin[i][0] == p[0]:
                OMGimgFoodRec = ck.CTkImage(dark_image=Image.open(p[1]), 
                                size=(130, 110))

        # OMGimgFoodRec = ck.CTkImage(dark_image=Image.open(f"Menu/Steak.jpg"), 
        #                         size=(130, 110))
        OMGImagePIC = ck.CTkLabel(OMG, 
                            image=OMGimgFoodRec,
                            text="")
        OMGImagePIC.place(relx=0.2, rely=0.4, anchor=ck.CENTER)

        OMGImageFoodT = ck.CTkLabel(OMG, 
                                text=subjoin[i][0], 
                                text_color="#000000",
                                font=("Segoe UI Bold", 15))
        OMGImageFoodT.place(relx=0.2, rely=0.8, anchor=ck.CENTER)
        
      
        FoodHave = ck.CTkLabel(OMG, 
                                text="REQUIRED", 
                                text_color="#000000",
                                font=("Segoe UI Bold", 15))
        FoodHave.place(relx=0.525, rely=0.11,  anchor=ck.CENTER)

        FoodMiss = ck.CTkLabel(OMG, 
                                text="MISSING", 
                                text_color="#E20000",
                                font=("Segoe UI Bold", 15))
        FoodMiss.place(relx=0.51, rely=0.59, anchor=ck.CENTER)

        h = []
        for j in menu:
            if subjoin[i][0] == j[0]:
                have = (j[1],j[3],j[4])
                h.append(have)
        # print("have: ",h)
        # print("subjoin: ",subjoin)
        ht=''
        for k in h:
            ht += str(k[0])+" "+str(k[1])+" "+str(k[2])+"\n"
        
        missing =[]
        for l in h:
            found = False
            for m in subjoin:
                if l[0] == m[1]:
                    found = True
                    update_tuple = (l[0],l[1]-m[3],l[2])
            if found:
                missing.append(update_tuple)
            if not found:
                missing.append(l)
        missing = [item for item in missing if item[1] > 0]
        print("missing: ".upper())
        print(missing)
        bigmiss.append(missing)
        print("bigmiss: ".upper())
        print(bigmiss)
        mt=''
        for n in missing:
            # print("n in missing: ", n)
            mt += str(n[0])+" "+str(n[1])+" "+str(n[2])+"\n"
        if not missing:
            mt = "You have all required ingredients!"
        HAVE = ck.CTkTextbox(OMG, 
                       width = 205,
                       height = 67,
                       fg_color="#FFDD64",
                       text_color = "#000000",
                       corner_radius=0,
                       border_width = 0,
                       border_color = "#FFDD64",
                       border_spacing = 0,
                       font=("Segoe UI", 11),
                       activate_scrollbars = True)
        HAVE.insert(index=1.0,text=ht)
        HAVE.place(relx=0.7, rely=0.32, anchor=ck.CENTER)
        HAVE.configure(state = "disabled")

        MISS = ck.CTkTextbox(OMG, 
                       width = 205,
                       height = 67,
                       fg_color="#FFDD64",
                       text_color = "#000000",
                       corner_radius=0,
                       border_width = 0,
                       border_color = "#FFDD64",
                       border_spacing = 0,
                       font=("Segoe UI", 11),
                       activate_scrollbars = True)
        MISS.insert(index=1.0,text=mt)
        MISS.place(relx=0.7, rely=0.81, anchor=ck.CENTER)
        MISS.configure(state = "disabled")

        AddToCart = ck.CTkButton(OMG, 
                                text = "Add to Cart",
                                font=("Segoe UI", 10),
                                text_color = "#2F2E2E",
                                border_width = 0,
                                corner_radius = 5,
                                width=38, 
                                height=15, 
                                border_color = "#FFDD64",
                                fg_color = "#FFDD64",
                                hover = True,
                                hover_color = "orange",
                                command =lambda i=i: add_all_to_cart(bigmiss[i]))
        AddToCart.place(relx=0.88, rely =0.59, anchor=ck.CENTER)

        if not missing:
            AddToCart.destroy()

        OMGframes.append(OMG)
        imgSEs.append(imgSE)
        ImageLabelESs.append(ImageLabelES)
        imgSE2s.append(imgSE2)
        ImageLabelES2s.append(ImageLabelES2)
        OMGimgFoodRecs.append(OMGimgFoodRec)
        OMGImagePICs.append(OMGImagePIC)
        OMGImageFoodTs.append(OMGImageFoodT)
        FoodHaves.append(FoodHave)
        FoodMisss.append(FoodMisss)
        Haves.append(HAVE)
        Misss.append(MISS)

'''
    # To access and modify specific elements, use their index
    # is this where you edit info of each recommmendation frame
    #1st
    if i >= 0:
        imgFoodRecs[0] = ck.CTkImage(dark_image=Image.open("Menu/Steak.jpg"), 
                                    size=(100, 88))
        ImagePICs[0].configure(image=imgFoodRecs[0])
        ImageFoodTs[0].configure(text="Menu: Steak")

    #2nd
    if i >= 1:
        imgFoodRecs[1] = ck.CTkImage(dark_image=Image.open("Menu/Burger.jpg"), 
                                    size=(100, 88))
        ImagePICs[1].configure(image=imgFoodRecs[1])
        ImageFoodTs[1].configure(text="Menu: Burger")

    #3rd
    if i >= 2:
        imgFoodRecs[2] = ck.CTkImage(dark_image=Image.open("Menu/Salad.jpg"), 
                                    size=(100, 88))
        ImagePICs[2].configure(image=imgFoodRecs[2])
        ImageFoodTs[2].configure(text="Menu: Salad")
'''

def Menulist2():
    global OMG, OMGframes, OMGimgFoodRecs, OMGImagePICs, OMGImageFoodTs, imgSEs, ImageLabelESs, imgSE2s, ImageLabelES2s
    global FoodHaves, FoodMisss, Haves, Misss
    global OMG, OMGimgFoodRec, OMGImagePIC, OMGImageFoodT, imgSE, ImageLabelES, imgSE2, ImageLabelES2
    global FoodHave, FoodMiss, HAVE, MISS

    OMGframes = []  # Create an empty list to store frames
    imgSEs = [] 
    ImageLabelESs = [] 
    imgSE2s = [] 
    ImageLabelES2s = [] 
    OMGimgFoodRecs = []  #Food pic
    OMGImagePICs = []
    OMGImageFoodTs = []  #Food name
    FoodHaves = []
    FoodMisss = []
    Haves = [] #have list
    Misss = [] #miss list
    bigmiss =[]

    menu = menubook()
    ingre = fridgeingre()
    path = menupic()
    sorted_ingre = sorted(ingre, key=lambda x: x[4])
    searchlist = []
    # print("\nMENU",menu)
    for item in menu:
        if IsSearch == item[0] or IsSearch == item[1]:
            searchlist.append(item)
    print("\n\nsearchlist: ".upper(),searchlist)
    box_count = len(searchlist)
    # print("\n\nbox_count: ".upper(), box_count)

    for i in range(len(searchlist)):
        OMG = ck.CTkFrame(Frame1, 
                            width=390,
                            height=220,
                            border_width = 2,
                            corner_radius = 15,
                            fg_color = "#FFDD64",
                            border_color = "#000000")
        OMG.pack(pady = 8)

        imgSE = ck.CTkImage(dark_image = Image.open("Icon/seicon.png"), 
                          size=(25, 200))
        ImageLabelES = ck.CTkButton(OMG, 
                                image=imgSE,
                                border_width = 3,
                                corner_radius = 0,
                                width=38, 
                                height=38, 
                                border_color = "#FFDD64",
                                fg_color = "#FFDD64",
                                text = "",
                                hover = False)
        ImageLabelES.place(relx=0.40, rely=0.5, anchor=ck.CENTER)

        imgSE2 = ck.CTkImage(dark_image = Image.open("Icon/seicon2.png"), 
                          size=(220, 25),)
        ImageLabelES2 = ck.CTkButton(OMG, 
                                image=imgSE2,
                                border_width = 0,
                                corner_radius = 0,
                                width=38, 
                                height=38, 
                                border_color = "#FFDD64",
                                fg_color = "#FFDD64",
                                text = "",
                                hover = False)
        ImageLabelES2.place(relx=0.699, rely=0.5, anchor=ck.CENTER)

        for p in path:
            if searchlist[i][0] == p[0]:
                OMGimgFoodRec = ck.CTkImage(dark_image=Image.open(p[1]), 
                                size=(130, 110))

        # OMGimgFoodRec = ck.CTkImage(dark_image=Image.open(f"Menu/Steak.jpg"), 
        #                         size=(130, 110))
        OMGImagePIC = ck.CTkLabel(OMG, 
                            image=OMGimgFoodRec,
                            text="")
        OMGImagePIC.place(relx=0.2, rely=0.4, anchor=ck.CENTER)

        OMGImageFoodT = ck.CTkLabel(OMG, 
                                text=searchlist[i][0], 
                                text_color="#000000",
                                font=("Segoe UI Bold", 15))
        OMGImageFoodT.place(relx=0.2, rely=0.8, anchor=ck.CENTER)
        
      
        FoodHave = ck.CTkLabel(OMG, 
                                text="REQUIRED", 
                                text_color="#000000",
                                font=("Segoe UI Bold", 15))
        FoodHave.place(relx=0.525, rely=0.11,  anchor=ck.CENTER)

        FoodMiss = ck.CTkLabel(OMG, 
                                text="MISSING", 
                                text_color="#E20000",
                                font=("Segoe UI Bold", 15))
        FoodMiss.place(relx=0.51, rely=0.59, anchor=ck.CENTER)

        h = []
        for j in menu:
            if searchlist[i][0] == j[0]:
                have = (j[1],j[3],j[4])
                h.append(have)
        # print("have: ",h)
        # print("subjoin: ",subjoin)
        ht=''
        for k in h:
            ht += str(k[0])+" "+str(k[1])+" "+str(k[2])+"\n"
        
        missing =[]
        for l in h:
            found = False
            for m in searchlist:
                if l[0] == m[1]:
                    found = True
                    update_tuple = (l[0],l[1]-m[3],l[2])
            if found:
                missing.append(update_tuple)
            if not found:
                missing.append(l)
        missing = [item for item in missing if item[1] > 0]
        # print("missing: ".upper(), missing)
        bigmiss.append(missing)
        # print("bigmiss: ".upper(),bigmiss)
        
        mt=''
        for n in missing:
            # print("n in missing: ", n)
            mt += str(n[0])+" "+str(n[1])+" "+str(n[2])+"\n"
        if not missing:
            mt = "You have all required ingredients!"
        HAVE = ck.CTkTextbox(OMG, 
                       width = 205,
                       height = 67,
                       fg_color="#FFDD64",
                       text_color = "#000000",
                       corner_radius=0,
                       border_width = 0,
                       border_color = "#FFDD64",
                       border_spacing = 0,
                       font=("Segoe UI", 11),
                       activate_scrollbars = True)
        HAVE.insert(index=1.0,text=ht)
        HAVE.place(relx=0.7, rely=0.32, anchor=ck.CENTER)
        HAVE.configure(state = "disabled")

        MISS = ck.CTkTextbox(OMG, 
                       width = 205,
                       height = 67,
                       fg_color="#FFDD64",
                       text_color = "#000000",
                       corner_radius=0,
                       border_width = 0,
                       border_color = "#FFDD64",
                       border_spacing = 0,
                       font=("Segoe UI", 11),
                       activate_scrollbars = True)
        MISS.insert(index=1.0,text=mt)
        MISS.place(relx=0.7, rely=0.81, anchor=ck.CENTER)
        MISS.configure(state = "disabled")

        AddToCart = ck.CTkButton(OMG, 
                                text = "Add to Cart",
                                font=("Segoe UI", 10),
                                text_color = "#2F2E2E",
                                border_width = 0,
                                corner_radius = 5,
                                width=38, 
                                height=15, 
                                border_color = "#FFDD64",
                                fg_color = "#FFDD64",
                                hover = True,
                                hover_color = "orange",
                                command =lambda i=i: add_all_to_cart(bigmiss[i]))
        AddToCart.place(relx=0.88, rely =0.59, anchor=ck.CENTER)

        if not missing:
            AddToCart.destroy()

        OMGframes.append(OMG)
        imgSEs.append(imgSE)
        ImageLabelESs.append(ImageLabelES)
        imgSE2s.append(imgSE2)
        ImageLabelES2s.append(ImageLabelES2)
        OMGimgFoodRecs.append(OMGimgFoodRec)
        OMGImagePICs.append(OMGImagePIC)
        OMGImageFoodTs.append(OMGImageFoodT)
        FoodHaves.append(FoodHave)
        FoodMisss.append(FoodMisss)
        Haves.append(HAVE)
        Misss.append(MISS)

    

def recommendation(n):
    #global Frame2, Frame3, Frame4, ImagePIC1, ImagePIC2, ImagePIC3, ImageFoodT1, ImageFoodT2, ImageFoodT3
    global frames, imgFoodRecs, ImagePICs, ImageFoodTs

    frames = [] 
    imgFoodRecs = []  #Food pic
    ImagePICs = []
    ImageFoodTs = []  #Food name
    relx_values = [0.17, 0.5, 0.83]  # Define different relx values for frames

    menu = menubook()
    ingre = fridgeingre()
    path = menupic()
    sorted_ingre = sorted(ingre, key=lambda x: x[4])
    # print("\nMENU",menu)
    join = []
    if menu:
        for i in sorted_ingre:
            for j in menu:
                if i[0] == j[1]:
                    join.append(j)
    else: print("No Data")
    join[3:] = []
    print("\n\nJoin".upper(),join)

    for i in range(n):
        frame = ck.CTkFrame(outlinerec, 
                            width=125,
                            height=150,
                            border_width=2,
                            corner_radius=15,
                            fg_color="#FFA100",
                            border_color="#000000")
        frame.place(relx=relx_values[i], rely=0.5, anchor=ck.CENTER)

        for p in path:
            if join[i][0] == p[0]:
                imgFoodRec = ck.CTkImage(dark_image=Image.open(p[1]), 
                                size=(100, 88))
    
        ImagePIC = ck.CTkLabel(frame, 
                            image=imgFoodRec,
                            text="")
        ImagePIC.place(relx=0.4955, rely=0.38, anchor=ck.CENTER)

        ImageFoodT = ck.CTkLabel(frame, 
                                text=join[i][0], 
                                text_color="#000000",
                                font=("Segoe UI Bold", 12))
        ImageFoodT.place(relx=0.5, rely=0.82, anchor=ck.CENTER)

        frames.append(frame)  # Append the frame to the list
        imgFoodRecs.append(imgFoodRec)  # Append imgFoodRec to the list
        ImagePICs.append(ImagePIC)  # Append ImagePIC to the list
        ImageFoodTs.append(ImageFoodT)  # Append ImageFoodT to the list

''' 
    #no longer necesary since we are getting info from the array
    # To access and modify specific elements, use their index
    # is this where you edit info of each recommmendation frame
    #1st
    if i >= 0:
        imgFoodRecs[0] = ck.CTkImage(dark_image=Image.open("Menu/Steak.jpg"), 
                                    size=(100, 88))
        ImagePICs[0].configure(image=imgFoodRecs[0])
        ImageFoodTs[0].configure(text="Menu: Steak")

    #2nd
    if i >= 1:
        imgFoodRecs[1] = ck.CTkImage(dark_image=Image.open("Menu/Burger.jpg"), 
                                    size=(100, 88))
        ImagePICs[1].configure(image=imgFoodRecs[1])
        ImageFoodTs[1].configure(text="Menu: Burger")

    #3rd
    if i >= 2:
        imgFoodRecs[2] = ck.CTkImage(dark_image=Image.open("Menu/Salad.jpg"), 
                                    size=(100, 88))
        ImagePICs[2].configure(image=imgFoodRecs[2])
        ImageFoodTs[2].configure(text="Menu: Salad")
'''    
'''
    Frame2 = ck.CTkFrame(outlinerec, 
                            width=125,
                            height=150,
                            border_width = 2,
                            corner_radius = 15,
                            fg_color = "#FFA100",
                            border_color = "#000000")
    
    #Recommendation menu
    imgFoodRec1 = ck.CTkImage(dark_image = Image.open("Menu/Steak.jpg"), #picture
                            size=(100, 88))
    ImagePIC1 = ck.CTkLabel(frame, 
                                image=imgFoodRec1,
                                text = "")
    ImagePIC1.place(relx=0.4955, rely=0.38, anchor=ck.CENTER)

    ImageFoodT1 = ck.CTkLabel(frame, 
                                text = "Menu: " + "Steak", #food name
                                text_color = "#000000",
                                font =("Segoe UI Bold", 12))
    ImageFoodT1.place(relx=0.5, rely=0.82, anchor=ck.CENTER)
    
    Frame3 = ck.CTkFrame(outlinerec, 
                         width=125,
                         height=150,
                         border_width = 2,
                         corner_radius = 15,
                         fg_color = "#FFA100",
                         border_color = "#000000")
    
    imgFoodRec2 = ck.CTkImage(dark_image = Image.open("Menu/Steak.jpg"), #picture
                          size=(100, 88))
    ImagePIC2 = ck.CTkLabel(Frame3, 
                              image=imgFoodRec2,
                              text = "")
    ImagePIC2.place(relx=0.4955, rely=0.38, anchor=ck.CENTER)

    ImageFoodT2 = ck.CTkLabel(Frame3, 
                              text = "Menu: " + "Steak", #food name
                              text_color = "#000000",
                              font =("Segoe UI Bold", 12))
    ImageFoodT2.place(relx=0.5, rely=0.82, anchor=ck.CENTER)

    Frame4 = ck.CTkFrame(outlinerec, 
                         width=125,
                         height=150,
                         border_width = 2,
                         corner_radius = 15,
                         fg_color = "#FFA100",
                         border_color = "#000000")
    
    imgFoodRec3 = ck.CTkImage(dark_image = Image.open("Menu/Steak.jpg"), #picture
                          size=(100, 88))
    ImagePIC3 = ck.CTkLabel(Frame4, 
                              image=imgFoodRec3,
                              text = "")
    ImagePIC3.place(relx=0.4955, rely=0.38, anchor=ck.CENTER)

    ImageFoodT3 = ck.CTkLabel(Frame4, 
                              text = "Menu: " + "Steak", #food name
                              text_color = "#000000",
                              font =("Segoe UI Bold", 12))
    ImageFoodT3.place(relx=0.5, rely=0.82, anchor=ck.CENTER)

    if n == 1:
        Frame2.place(relx=0.18, rely=0.5, anchor=ck.CENTER)
    elif n == 2:
        Frame2.place(relx=0.18, rely=0.5, anchor=ck.CENTER)
        Frame3.place(relx=0.5, rely=0.5, anchor=ck.CENTER)
    elif n == 3:
        Frame2.place(relx=0.17, rely=0.5, anchor=ck.CENTER)
        Frame3.place(relx=0.5, rely=0.5, anchor=ck.CENTER)
        Frame4.place(relx=0.83, rely=0.5, anchor=ck.CENTER)
    '''


def MyInChoose(choice):
    data = fridgeingre()
    sorted_data = sorted(data, key=lambda x: x[4])
    print(sorted_data)
    if choice == "All":
        name=''
        exp=''
        for i in sorted_data:
            name += str(i[0]+"\n")
            exp += str(i[4]+"\n")
        Name.configure(text=name)
        ExDate.configure(text=exp)
    elif choice == "Meat":
        name=''
        exp=''
        for i in sorted_data:
            if i[1] == "meat":
                name += str(i[0]+"\n")
                exp += str(i[4]+"\n")
        Name.configure(text=name)
        ExDate.configure(text=exp)
    elif choice == "Spice":
        name=''
        exp=''
        for i in sorted_data:
            if i[1] == "spice":
                name += str(i[0]+"\n")
                exp += str(i[4]+"\n")
        Name.configure(text=name)
        ExDate.configure(text=exp)
    elif choice == "Dairy Product":
        name=''
        exp=''
        for i in sorted_data:
            if i[1] == "dairy products ":
                name += str(i[0]+"\n")
                exp += str(i[4]+"\n")
        Name.configure(text=name)
        ExDate.configure(text=exp)
    elif choice == "Fruit":
        name=''
        exp=''
        for i in sorted_data:
            if i[1] == "fruit ":
                name += str(i[0]+"\n")
                exp += str(i[4]+"\n")
        Name.configure(text=name)
        ExDate.configure(text=exp)
    elif choice == "Vegetable":
        name=''
        exp=''
        for i in sorted_data:
            if i[1] == "vegetable ":
                name += str(i[0]+"\n")
                exp += str(i[4]+"\n")
        Name.configure(text=name)
        ExDate.configure(text=exp)
    elif choice == "Others":
        name=''
        exp=''
        for i in sorted_data:
            if i[1] == "others":
                name += str(i[0]+"\n")
                exp += str(i[4]+"\n")
        Name.configure(text=name)
        ExDate.configure(text=exp)

        #I don't know how will you connect all those info but if you uses variable to connect
        # you need to change 'text' to textvariable na
        #textvariable === tkinter.StringVar object
        #text === string
        

def BacktoMain(From):
    DeletePage(From)
    MainPage()


def SpecialBack():
    if a == 0:
        DeletePage("ShopList")
        MainPage()
    if a == 1:
        DeletePage("ShopList")
        MenuPageWait()


def ClearOut(a):
    if a == "Menu":
        SearchMenu.delete(0, END)
        ImageLabel98.destroy()
        OMG.destroy()
        OMGImagePIC.destroy()
        OMGImageFoodT.destroy()
        ImageLabelES.destroy()
        ImageLabelES2.destroy()
        FoodHave.destroy()
        FoodMiss.destroy()
        HAVE.destroy()
        MISS.destroy()
        MenuPage()
    elif a == 1:
        entry_ingredient.configure(state="normal")
        entry_ingredient.delete(0, END)
    elif a == 2:
        entry_expdate.configure(state="normal")
        entry_expdate.delete(0, END)
    elif a == 3:
        entry_quan.configure(state="normal")
        entry_quan.delete(0, END)


def submit():
    ingrename = entry_ingredient.get()
    ingretype = ComboCtgr1.get()
    ingrequan = entry_quan.get()
    ingreunit = ComboCtgr2.get()
    ingredate = cal.get_date()

    if ingretype == "Spice":
        ingretype = 'spice'
    elif ingretype == "Meat":
        ingretype = 'meat'
    elif ingretype == "Dairy Product":
        ingretype = 'dairy products '
    elif ingretype == "Fruit":
        ingretype = 'fruit '
    elif ingretype == "Vegetable":
        ingretype = 'vegetable '
    elif ingretype == "Others":
        ingretype = 'others'

    if ingrename and ingretype and ingrequan and ingreunit and ingredate:
        conn = sqlite3.connect("database.db",timeout=10)
        c = conn.cursor()

        try:
            count = ingrerowcount()
            print("ingre row count: ", count)
            c.execute("INSERT INTO in_fridge VALUES (:item_id, :ingredient_id, :quantity, :unit, :date)",
                    {
                            'item_id': count+1,
                            'ingredient_id': count+1,
                            'quantity': ingrequan,
                            'unit': ingreunit,
                            'date': ingredate
                    }
                    )
            c.execute("INSERT INTO ingre VALUES (:id, :name, :type)",
                    {
                            'id': count+1,
                            'name': ingrename,
                            'type': ingretype
                    }
                    )
                
            conn.commit()
        except Exception as e:
            print("Error: ", e)
            conn.rollback()
        finally:
            conn.close()

            entry_ingredient.configure(state="disabled")
            entry_expdate.configure(state="disabled")
            entry_quan.configure(state="disabled")
            label_show.configure(text=f'{("You added ")+entry_ingredient.get()} {("( ")+ComboCtgr1.get()+(", ")+entry_quan.get()} {ComboCtgr2.get()}{(", exp. ")+cal.get_date()+(" )")}')

            ComboStart1.set(" ")
            ComboStart2.set(" ")
            expired_date.configure(text="YYYY-MM-DD")
            ClearOut(1)
            ClearOut(2)
            ClearOut(3)
    else: label_show.configure(text="Please fill in all the information")


def ADDtoCART(item):
    if item:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO cart VALUES (:name, :quantity, :unit)",
                {
                        'name': item[0],
                        'quantity': item[1],
                        'unit': item[2]
                })
        conn.commit()
        conn.close()
    else: 
        print("ADDtoCART: No item to add")

def add_all_to_cart(missing):
    for item in missing:
        ADDtoCART(item)

def show_calendar():
    global top, cal, set_button, selected_date
    top = Toplevel(main)
    cal = Calendar(top,  
                   firstweekday = "sunday",
                   date_pattern='YYYY-MM-DD')
    cal.pack(padx=20, pady=20)
    
    def set_date():
        global selected_date
        selected_date = cal.get_date()
        expired_date.configure(text=f"{selected_date}")
        top.destroy()
    
    set_button = Button(top, text="Set Date", command=set_date)
    set_button.pack(pady=10)

def before_clearcart():
    global HEHE

    HEHE = Tk()
    HEHE.title("Confirm") #Heading
    HEHE.iconbitmap('c:/Users/pound/Downloads/LangTooYen/Icon/icon.ico')
    HEHE.geometry("350x150")
    HEHE.resizable(False, False)
    HEHE.config(bg="#ffc700")

    DoYou1 = ck.CTkLabel(HEHE, 
                   text="Do you want to clear the cart?", 
                   text_color="#000000", 
                   fg_color="transparent", 
                   font=("Segoe UI Bold", 17))
    DoYou1.place(relx=0.46, rely=0.25, anchor=ck.CENTER)

    DoYou2 = ck.CTkLabel(HEHE, 
                   text="All items in the cart will be deleted.", 
                   text_color="#000000", 
                   fg_color="transparent", 
                   font=("Segoe UI", 12))
    DoYou2.place(relx=0.385, rely=0.45, anchor=ck.CENTER)

    YES = ck.CTkButton(HEHE, 
                                text="Yes",
                                font=("Segoe UI Bold", 15), 
                                width = 70, 
                                height = 35,
                                fg_color="#ff4d00",
                                text_color="#ffffff",
                                hover_color="#FF6F2F",
                                command= after_yes)
    YES.place(relx=0.55, rely= 0.72, anchor=ck.CENTER)

    NO = ck.CTkButton(HEHE, 
                                text="No",
                                font=("Segoe UI Bold", 15), 
                                width = 70, 
                                height = 35,
                                fg_color="#ffdd64",
                                text_color="#000000",
                                hover_color="#fee692",
                                command= after_no)
    NO.place(relx=0.78, rely= 0.72, anchor=ck.CENTER)


def after_yes():
    HEHE.destroy()
    clearcart()


def after_no():
    HEHE.destroy()

def clearcart():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM cart")
    conn.commit()
    conn.close()
    shoplist()

def search():
    getsearch()
    print("\n\nbox_count in search: ".upper(), box_count)
    size = box_count
    if IsSearch:
        outrec.destroy()
        outlinerec.destroy()
        for i in range(size):
            OMGframes[i].destroy()
        Menulist2()
    else: Menulist()

def getsearch():
    global IsSearch
    SearchMenu.configure(state="disabled")
    IsSearch = SearchMenu.get()
    SearchMenu.configure(state="normal")
    print("IsSearch: ", IsSearch)

def myin_sortbyexp():
    data = fridgeingre()
    sorted_data = sorted(data, key=lambda x: x[4])
    ingre_name=''
    ingre_exp=''
    for i in sorted_data:
        ingre_name += str(i[0]+"\n")
        ingre_exp += str(i[4]+"\n")
    return ingre_name, ingre_exp

def DeletePage(page):
    if page == "Main":
        Base.destroy()
        LANG.destroy()
        TOO.destroy()
        YEN.destroy()
        ButtonMyIn.destroy()
        ButtonKin.destroy()
        ButtonShop.destroy()
        TextEx.destroy()
        ExDate1.destroy()
        Name1.destroy()
        Head.destroy()
    elif page == "MyIn":
        Base.destroy()
        ImageLabel1.destroy()
        ImageLabel2.destroy()
        ImageLabel7.destroy()
        In.destroy()
        ComboCtgr.destroy()
        LabelIn.destroy()
        LabelEd.destroy()
        FrameList.destroy()
        Name.destroy()
        ExDate.destroy()
    elif page == "Menu":
        Base.destroy()
        menu.destroy()
        ImageLabel3.destroy()
        SearchMenu.destroy()
        Frame1.destroy()
        recom.destroy()
        ImageLabel4.destroy()
        ImageLabel5.destroy()
        ImageLabel6.destroy()
        outrec.destroy()
        outlinerec.destroy()
        ImageLabel98.destroy()
        OMG.destroy()
        OMGImagePIC.destroy()
        OMGImageFoodT.destroy()
        ImageLabelES.destroy()
        ImageLabelES2.destroy()
        FoodHave.destroy()
        FoodMiss.destroy()
        HAVE.destroy()
        MISS.destroy()
    elif page == "ADDINGR":
        Base.destroy()
        ADD.destroy()
        INGR.destroy()
        ING.destroy()
        entry_ingredient.destroy()
        EXPDATE.destroy()
        entry_expdate.destroy()
        button_enter.destroy()
        label_show.destroy()
        ImageLabel14.destroy()
        ImageLabe20.destroy()
        ImageLabe21.destroy()
        imgClear1.destroy()
        ComboCtgr1.destroy()
        CAT.destroy()
        ImageLabe23.destroy()
        QUAN.destroy()
        entry_quan.destroy()
        UNIT.destroy()
        ComboCtgr2.destroy()
    elif page == "ShopList":
        Base.destroy()
        ImageLabel54.destroy()
        SHP.destroy()
        FrameList10.destroy()
        INGR.destroy()
        EXP.destroy()
        Amount.destroy()
        Name2.destroy()

MainPage()


main.mainloop()
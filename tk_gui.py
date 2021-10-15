from prettytable import PrettyTable
from tkinter import *
from tkinter import messagebox
import noSpoilersModules as nsm

master = Tk()
master.title("No Spoilers")
main_wl_list = []
master.resizable(False , False)  # disables resizeable feature of the window
screen_width = master.winfo_screenwidth()  # fetches the display width
screen_height = master.winfo_screenheight()  # fetches the display height
x_cord = int((screen_width / 2) - (550 / 2))  # lines 12 & 13 determine the centre point on the screen
y_cord = int((screen_height / 2) - (300 / 2))
master.geometry(f"550x300+{x_cord}+{y_cord}")  # ensures the window pops up in the exact centre of the screen

def search():
        '''
        This function is to search and display TV shows
        '''
        try:
                q = query.get()
                if q == '':
                        raise Exception('Error: Please enter a valid query!')
        except Exception:
                messagebox.showerror('Error', 'Please enter a valid query!')

        res = nsm.inputQuery(q)

        try:
                res1 = list(nsm.scrape(res))
        except Exception:
                messagebox.showerror('Error', 'No data receieved for the given show')

        if len(res1) == 0 or len(res1) == 1:
                raise Exception('No data receieved for the given show')

        new_id = nsm.splitID(res1[1])
        temp = res1[2:5]

        search.res2 = [res1[0], new_id]
        for i in range(len(temp)):
                search.res2.append(temp[i])
        res3 = nsm.call(search.res2)
        tb(res3)

def search_again():
        '''
        This function is used to add the search data to the watchlist
        '''
        search()
        try:
                if search.res2 in main_wl_list:
                        raise Exception('Error: show already in watchlist')
                else:
                        main_wl_list.append(search.res2)
                        mytable.add_row(search.res2)
                        try:
                                if search.res2 == []:
                                        raise Exception('Enter a valid query!')
                                else:
                                        messagebox.showwarning('Watchlist', 'Added to watchlist!')
                        except Exception:
                                print('Error: Enter a valid query!')

        except Exception:
                messagebox.showerror('Watchlist', 'Show already in watchlist!')

def tb(a):
        '''
        This function is to clear and insert a new data of TV show
        '''
        tb.textBox.delete(1.0, END)
        tb.textBox.insert(END, a)

def open_top():
        '''
        This function is to display the watchlist
        '''
        top = Toplevel(master)
        top.geometry("525x500")
        top.title('Watchlist')

        textBox1 = Text(top, height=30, width=70)
        textBox1.place(x=0,y=0)

        textBox1.insert(END, mytable)

        top.mainloop()

def open_about_NS():
        '''
        This function is to display About_NS
        '''
        top = Toplevel(master)
        top.geometry("525x500")
        top.title('About NS')

        textBox1 = Text(top, height=30, width=70)
        textBox1.place(x=0,y=0)

        textBox1.insert(END, """No Spoilers is a simple GUI TV show search engine. 
Users can search and store TV shows in watchlists as well 
as get updates on new episodes of a certain show.

Features of NoSpoilers:
>The GUI of NS contains a entry widget where the user
can enter a the exact name or keywords of the particular
show that they want to search for.
>The Search button will search for the show based on the 
keywords entered by the user in the entry widget and will 
display the search results in the text box on the GUI.
>The add to watchlist button will result in adding the 
show shown in the search results to a watchlist, which 
can be viewed by clicking on Watchlist>Open watchlist. 
>The Save watchlist button will ensure that the watchlist 
is saved on the disk in the form a text file named as wlist.txt
for referring to in the future, even after the program is closed.


Requirements for No Spoilers:
>pandas
>prettytable
>requests

Repo source: git@github.com:acmpesuecc/NoSpoilers.git""")

        top.mainloop()

def watchlist_save():
        '''
        This function is to save the watchlist data
        '''
        file = open('wlist.txt', 'a+')
        for i in main_wl_list:
                file.write(', '.join(i) + '\n')
        file.close()
        messagebox.showwarning('Saved', 'Watchlist is saved!')

def quit_ns():
        '''
        This function is to quit the application
        '''
        ans = messagebox.askquestion('Quit', 'Are you sure you want to quit No Spoilers?')
        if ans == 'yes':
                master.destroy()
        else:
                pass

def load_watchlist():
        '''
        This function is to load the saved watchlist everytime the application is opened
        '''
        file = open('wlist.txt', 'r')
        for x in file:
                a = x.split(', ')
                mytable.add_row(a)

menubar = Menu(master)

wList = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Watchlist', menu = wList)
wList.add_command(label = 'Open watchlist', command = open_top)

help = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu = help)
help.add_command(label = 'About NS', command = open_about_NS)

label = Label(master, text='Enter the name of the show')
label.place(x=50,y=20)

query = StringVar()

entry = Entry(master, textvariable=query,width=30)
entry.place(x=230,y=20)

search_button = Button(master, text='Search', command = search)
search_button.place(x=450,y=17)

addtowl_button = Button(master, text='Add to watchlist', command = search_again)
addtowl_button.place(x=100,y=60)

schd_button = Button(master, text='Save watchlist', command = watchlist_save)
schd_button.place(x=250,y=60)

quit_button = Button(master, text='Quit', command = quit_ns)
quit_button.place(x=400,y=60)

mytable = PrettyTable(['Name of the show', 'ID', 'Langauge', 'Genre', 'Status'])

tb.textBox = Text(master, height=10, width=60)
tb.textBox.place(x=30,y=100)

load_watchlist()

master.config(menu = menubar)
master.mainloop()

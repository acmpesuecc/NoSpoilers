from prettytable import PrettyTable
from tkinter import *
from tkinter import messagebox
import noSpoilersModules as nsm

master = Tk()
master.title("No Spoilers")
master.geometry('600x400')
main_wl_list = []

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
        textBox1.pack()

        textBox1.insert(END, mytable)

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
help.add_command(label = 'About NS', command = None)

label = Label(master, text='Enter the name of the show')
label.pack()

query = StringVar()

entry = Entry(master, textvariable=query)
entry.pack()

search_button = Button(master, text='Search', command = search)
search_button.pack()

addtowl_button = Button(master, text='Add to watchlist', command = search_again)
addtowl_button.pack()

schd_button = Button(master, text='Save watchlist', command = watchlist_save)
schd_button.pack()

quit_button = Button(master, text='Quit', command = quit_ns)
quit_button.pack()

mytable = PrettyTable(['Name of the show', 'ID', 'Langauge', 'Genre', 'Status'])

tb.textBox = Text(master, height=10, width=60)
tb.textBox.pack()

load_watchlist()

master.config(menu = menubar)
master.mainloop()

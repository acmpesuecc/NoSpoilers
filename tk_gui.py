from prettytable import PrettyTable
from tkinter import *
from tkinter import messagebox
import noSpoilersModules as nsm
from fuzzywuzzy import process, fuzz

master = Tk()
master.title("No Spoilers")
master.geometry('600x400')
master.configure(bg='#222')
main_wl_list = []
savedupto = 0

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
        top.geometry("700x500")
        top.title('Watchlist')

        def clear():
                filtered_table = mytable
                textBox1.delete('1.0', END)
                textBox1.insert(END, filtered_table)
        def search_update():
                s = searchbar.get()
                if not s.isalnum():
                        clear()
                        print("whitespaces entered")
                        return

                shows=[]
                rows=[]
                for row in mytable:
                        row.border = False
                        row.header = False
                        name = row.get_string(fields=["Name of the show"]).strip()
                        shows.append(name)
                        row_l = [
                                name,
                                row.get_string(fields=['ID']).strip(),
                                row.get_string(fields=['Langauge']).strip(),
                                row.get_string(fields=['Genre']).strip(),
                                row.get_string(fields=['Status']).strip()
                        ]
                        rows.append(row_l)

                filtered_table = PrettyTable(['Name of the show', 'ID', 'Langauge', 'Genre', 'Status'])

                res = process.extract(s, shows)
                print(res)
                for i in res:
                        if i[1] > 70:
                                name  = i[0]
                                for row in rows:
                                        if name in row:
                                                filtered_table.add_row(row)
                textBox1.delete('1.0', END)
                textBox1.insert(END, filtered_table)                                

        search_str = StringVar()
        #search_str.trace_add("write", search_update)

        search_lbl = Label(top, text="Search: ").grid(row=0, column=0, sticky='E')
        searchbar = Entry(top, textvariable=search_str, width=40)
        searchbar.grid(row=0, column=1,)
        search_but = Button(top, text="Search", command=search_update)
        search_but.grid(row=0, column=2, sticky='W')
        clear_but = Button(top, text="Clear", command=clear)
        clear_but.grid(row=0, column=3, sticky='W')

        textBox1 = Text(top, height=30, width=100)
        textBox1.grid(row=1, column=0, columnspan=10)

        filtered_table = mytable
        textBox1.insert(END, filtered_table)

        top.mainloop()

def watchlist_save():
        '''
        This function is to save the watchlist data
        '''
        global savedupto

        file = open('wlist.txt', 'a+')
        for i in main_wl_list[savedupto:]:
                file.write(', '.join(i) + '\n')
        file.close()
        savedupto = len(main_wl_list)
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

label = Label(master, text='Enter the name of the show',bg='#222',fg='white',font=("Poppins Bold",13))
label.pack()

query = StringVar()

entry = Entry(master,width=40, textvariable=query,bg='#444',fg='white')
entry.place(x=180,y=30)

search_button = Button(master, text='Search', command = search ,bg='#6ea3ba',fg='black',font=('Poppins',10))
search_button.place(x=440,y=28)

addtowl_button = Button(master,text='Add to watchlist', command = search_again ,bg='#6ea3ba',fg='black',font=('Poppins',10))
addtowl_button.place(x=20,y=280)


schd_button = Button(master, text='Save watchlist', command = watchlist_save,bg='#6ea3ba',fg='black',font=('Poppins',10))
schd_button.place(x=150,y=280)

quit_button = Button(master,width=5, text='Quit', command = quit_ns, bg='#ff1f48',fg='white',font=('Poppins',10,'bold'))
quit_button.place(x=540,y=330)

mytable = PrettyTable(['Name of the show', 'ID', 'Langauge', 'Genre', 'Status'])

tb.textBox = Text(master, height=10, width=72,bg='#444',fg='white')
tb.textBox.place(x=10,y=70)

load_watchlist()

master.config(menu = menubar)
master.resizable(width=False, height=False)
master.mainloop()

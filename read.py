import os
a=input("enter a word: ")
with open("wlist.txt") as file:
	''' 
	data = file.readline()
	list = data.split (",")
	print(list[0])'''
	data=file.readlines()
	file.close
try:
	f=open("temp.txt","a")
	flag=0
	for i in data:
		list=i.split(',')
		print(list[0])
		if(list[0]!=a):
				f.write(i)
		else:
			flag=1
	f.close()
	if(flag==0):
		os.remove("temp.txt")
		raise Exception("Show doesn't exist on watchlist")
	else:
		os.remove("wlist.txt")
		os.rename("temp.txt","wlist.txt")
finally:
	f.close()
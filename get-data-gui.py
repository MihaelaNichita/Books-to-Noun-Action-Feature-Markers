from tkinter import *
import tkinter.messagebox as messagebox
import nltk
from nltk.tokenize import sent_tokenize
from tkinter import font

content = []
par_no = 0
book_opened = False
list_buttons_pos = []; list_buttons_comb = []; list_buttons_check = []
list_buttons_content = []
list_buttons_chosen = []
nouns = []; verbs = []; adj = []
all_comb = []
under_frame_y = 360


def itsaNoun(event):
	caller = event.widget
	caller.configure(bg='#fed766')
	

def itsaVerb(event):
	caller = event.widget
	caller.configure(bg='#fed766')

	new_button = Button (window,text=caller[text])
	new_button.place(x=size(list_buttons_chosen)*30,y=size(list_buttons_chosen[0]),height=25)

def itsanAdj(event):
	caller = event.widget
	caller.configure(bg='#fed766')

def justaWord(event):
	caller = event.widget
	caller.configure(bg='#999900')

def on_leave(event):
	caller = event.widget
	caller.configure(fg='#0F1626')

def on_enter(event):
	caller = event.widget
	caller.configure(fg='white')

def insert_text(par):
	lastx,lasty = 0,0
	tok_text = nltk.word_tokenize(par)
	for w in tok_text:
		#while w in """.,'?"!:."""
		if lastx + len(w)*10 > 850:
			lastx,lasty = 0,lasty+30

		times14 = font.Font(font='Times',size=14)
		new_button = Button(content_frame, text = w,borderwidth=0, font=times14,fg='#0F1626')
		
		new_button.place(x=lastx, y=lasty, height=25)
		list_buttons_content.append(new_button)
		new_button.bind("<Leave>", on_leave)
		new_button.bind("<Enter>", on_enter)
		new_button.bind("<Button-1>", justaWord)

		if w in nouns:
			new_button.bind("<Button-1>", itsaVerb)
			new_button.configure(bg='#FF533D')

		if w in verbs:
			new_button.bind("<Button-1>", itsaVerb)
			new_button.configure(bg='#AB987A')

		if w in adj:
			new_button.bind("<Button-1>", itsaVerb)
			new_button.configure(bg='#77C9D4')


		content_frame.update_idletasks() 
		lastx += new_button.winfo_width()
		if w in ".:!?,":lastx += 10



def open_book(event):
	global content
	global book_opened
	book_opened = True

	#text.delete(1.0, END)
	removeButtons(list_buttons_content)
	f = open("paragraphs/the-little-prince-paragraphs.txt",'r')

	content = f.readlines()
	getPOS(content[0])
	insert_text(content[par_no])


def removeButtons(list_buttons):
	for e in list_buttons:	
		e.destroy()
	list_buttons = []


def change_par():
	if book_opened == False:
		messagebox.showwarning("Warning","Please open a book first!")
		return

	global par_no, content,all_comb
	all_comb = []

	# Remove previous buttons
	# removeButtons(list_buttons_pos)
	removeButtons(list_buttons_check)
	removeButtons(list_buttons_comb)
	removeButtons(list_buttons_content)

	getPOS(content[par_no])
	insert_text(content[par_no])


def prev_par(event):
	global par_no
	par_no = par_no - 1
	change_par()


def next_par(event):
	global par_no
	par_no = par_no + 1
	change_par()


def getPOS(par):	
	print("Original Paragraph: ",par);print()
	# Remove Punctuation
	par = re.sub(r'[^\w\s]',' ',par)
	par = par.lower() # won't be able to identify NNPs
	
	## Word tokenization
	tok_text = nltk.word_tokenize(par)
	print("Tokenized Paragraph: ",tok_text);print()

	# Removing Stopwords
	from nltk.corpus import stopwords
	stop_words=set(stopwords.words("english"))
	filtered_par=[]
	for w in tok_text:
		if w not in stop_words and w not in filtered_par:
			filtered_par.append(w)
	print("Filterd Paragraph:",filtered_par);print()

	# POS tagging
	parts_of_speech = nltk.pos_tag(filtered_par)
	print(parts_of_speech);print()

	global nouns,verbs,adj
	# Get Nouns
	nouns = [e[0] for e in parts_of_speech if 'NN' in e[1]]
	#createButtons(nouns,700,60,True)
	print("Nouns: ",nouns);print()

	# Get Actions
	verbs = [e[0] for e in parts_of_speech if 'VB' in e[1] or 'RB' in e[1]]
	#createButtons(verbs,800,60,True)
	print("Actions: ",verbs);print()

	# Get Adjectives
	adj = [e[0] for e in parts_of_speech if 'JJ' in e[1]]
	#createButtons(adj,900,60,True)
	print("Adjectives: ",adj);print()


def createButtons(list,xi,yi,col):
	global list_buttons_pos, list_buttons_comb
	i=0
	for item in list:
		new_button = Button(window, text = item)
		if col:
			new_button.place(x=xi, y=yi+i*30,width = 95, height=25)
			list_buttons_pos.append(new_button)
		else:
			new_button.place(x=xi+i*100, y=yi,width = 95, height=25)
			list_buttons_comb.append(new_button)
		i=i+1


def check_comb(event,index):
	print("index = ", index)


def getRand(n):
	import random
	return random.randint(0,n-1)


def genComb(event):
	if book_opened == False:
		messagebox.showwarning("Warning","Please open a book first!")
		return

	global nouns,verbs,adj,all_comb,list_buttons_check
	nn = len(nouns)
	nv = len(verbs)
	na = len(adj)

	print(f"Limit = {nn*nv*na}. When hitting Hint Button, len = ",len(all_comb))

	n = 10
	left = nn*nv*na-len(all_comb)
	print("left : ", left)
	if  11 >= left:
		n = left
		messagebox.showwarning("Warning","These are the last combinations left!")

	for e in range(1,n+1):
		new_button = Button(window, text = str(e+len(all_comb)))
		new_button.place(x=650, y=under_frame_y+e*30,width = 35, height=25)
		list_buttons_check.append(new_button)
		index = list_buttons_check.index(new_button)
		new_button.bind("<Button-1>", check_comb(event,index))

	for i in range(n):
		r = [ getRand(nn),getRand(nv),getRand(na)]
		while r in all_comb:
			print("Duplicat: ",r)
			r = [ getRand(nn),getRand(nv),getRand(na)]
			
		all_comb.append(r)
		print("After Appending r, len = ",len(all_comb))
		createButtons([nouns[r[0]],verbs[r[1]],adj[r[2]]],690,under_frame_y+(i+1)*30,False)
		

def resetColors(event):
	pass


window = Tk()
window.geometry("1100x700")
window.configure(bg='#C5C1C0')

label_paragraph = Label(window, text = "Paragraph:")
label_paragraph.place(x = 30, y = 60, width=100, height=25)
label_paragraph.configure(bg='#003366', fg='white')

button_open_book = Button(window, text = "Open Book")
button_open_book.place(x = 30, y = 30, width=100, height=25)
button_open_book.bind("<Button-1>", open_book)

content_frame = Frame(window,height=300, width=900) #, fg = '#003333'
content_frame.place(x = 140, y = 60)

button_prev_par = Button(window, text = "Previous")
button_prev_par.place(x = 140, y = 30, width=95, height=25)
button_prev_par.bind("<Button-1>", prev_par)

button_next_par = Button(window, text = "Next")
button_next_par.place(x = 240, y = 30, width=95, height=25)
button_next_par.bind("<Button-1>", next_par)

label_nouns1 = Label(window, text = "Nouns:", bg='#FF533D')
label_nouns1.place(x = 140, y = under_frame_y, width=95, height=25)

label_actions1 = Label(window, text = "Actions:",bg='#AB987A')
label_actions1.place(x = 240, y = under_frame_y, width=95, height=25)

label_adjectives1 = Label(window, text = "Adjectives:",bg='#77C9D4')
label_adjectives1.place(x = 340, y = under_frame_y, width=95, height=25)

label_additional1 = Label(window, text="Additional:",bg='#999900')
label_additional1.place(x = 440, y = under_frame_y, width=95, height=25)

label_nouns2 = Label(window, text = "Nouns:", bg='#FF533D')
label_nouns2.place(x = 690, y = under_frame_y, width=95, height=25)

label_actions2 = Label(window, text = "Actions:",bg='#AB987A')
label_actions2.place(x = 790, y = under_frame_y, width=95, height=25)

label_adjectives2 = Label(window, text = "Adjectives:",bg='#77C9D4')
label_adjectives2.place(x = 890, y = under_frame_y, width=95, height=25)

button_hint=Button(window, text="Hint")
button_hint.place(x=545, y=under_frame_y+30, width=100, height=25)
button_hint.bind("<Button-1>", genComb)

label_check = Label(window, text='Check')
label_check.place(x=650, y=under_frame_y,width = 35, height=25)
label_check.configure(bg='#003366', fg='white')

button_reset=Button(window, text="Reset")
button_reset.place(x=30, y=under_frame_y+60, width=100, height=25)
button_reset.bind("<Button-1>", resetColors)

label_chosen = Label(window, text = "Chosen:")
label_chosen.place(x = 30, y = under_frame_y+30, width=100, height=25)
label_chosen.configure(bg='#003366', fg='white')

window.mainloop()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------
# ORT analysis - script GUI prediction - developed by Victor Ibañez
# 03.04.2021
# -------------------------------------------------------------------------------------


# -----------------------------------------------------
# import libraries
# -----------------------------------------------------

from tkinter import *
import tkinter.filedialog as fd
import os

# -----------------------------------------------------
# create GUI
# -----------------------------------------------------

def GUI_correct():

	def call_dic(dic):

		for key, value in dic.items():
			
			for i in range(len(value)):

				if value[i][0] == 'Label':
					lbl=Label(window, text=value[i][1][1])
					lbl.place(x=int(win_w*value[i][1][0]), y=int(win_h*key))
					lbl.config(font=("TkDefaultFont", f_size, "italic"))

				if value[i][0] == 'Button':
					if value[i][1][1] == 'path':
						btn=Button(window, text="search", command=open_path)
					if value[i][1][1] == 'vid':
						btn=Button(window, text="search", command=open_vid)
					if value[i][1][1] == 'vid_path':
						btn=Button(window, text="search", command=source_path)
					if value[i][1][1] == 'submit':
						btn=Button(window, text="start", command=submit)

					btn.place(x=int(win_w*value[i][1][0]), y=int(win_h*key))
					btn.config(font=("TkDefaultFont", f_size, "italic"))

	def open_path():
		global project_path
		project_path = filedialog.askdirectory()
		lbl6=Label(window, text=project_path.ljust(1000))
		lbl6.place(x=int(win_w*0.05), y=int(win_h*0.13))
		lbl6.config(font=("Arial", f_size-2))

	def source_path():
		global source
		source = filedialog.askdirectory()
		lbl7=Label(window, text=os.path.basename(source).ljust(1000))
		lbl7.place(x=int(win_w*0.05), y=int(win_h*0.48))
		lbl7.config(font=("Arial", f_size-2))

	def open_vid():
		global videos

		videos = fd.askopenfilenames()

		name0 = os.path.basename(videos[0]).split('.')[0]
		l = len(name0)
		nb_items = int((win_w/(l+2))/(f_size/1.5))

		for i in range(len(videos)):
			name = os.path.basename(videos[i]).split('.')[0]

			if i < nb_items:
				lbl1=Label(window, text=name.ljust(1000))
				lbl1.place(x=int(win_w*0.05)+(i*int(win_w*0.05)), y=int(win_h*0.28))
				lbl1.config(font=("Arial", f_size-2))
				lbl2=Label(window, text=''.ljust(1000))
				lbl2.place(x=int(win_w*0.05), y=int(win_h*0.31))
				lbl2.config(font=("Arial", f_size-2))
			if i >= nb_items:
				lbl3=Label(window, text=name.ljust(1000))
				lbl3.place(x=int(win_w*0.05)+((i-nb_items)*int(win_w*0.05)), y=int(win_h*0.31))
				lbl3.config(font=("Arial", f_size-2))

	def submit():
		#global project_path
		#global source
		window.destroy()

	
	window=Tk()

	width = window.winfo_screenwidth()
	height = window.winfo_screenheight()
	win_w = int(width/2)
	win_h = int(height/1.15)

	norm_w = 1280
	norm_f_size = 14

	f_size = round((norm_w*norm_f_size)/width)
	
	main = {0.03:[['Label',[0.05,'choose project path:']]],
			0.08:[['Button',[0.05,'path']]],
			0.18:[['Label',[0.05,'choose prediction videos for correction:']]],
			0.23:[['Button',[0.05,'vid']]],
			0.38:[['Label',[0.05,'choose original video path:']]],
			0.43:[['Button',[0.05,'vid_path']]],
			0.94:[['Button',[0.05,'submit']]]}
				

	entries = []
	
	call_dic(main)

	window.title('Create a new Project!')
	window.geometry(str(win_w)+'x'+str(win_h)+'+10+10')
	window.mainloop()

	window=Tk()


	return project_path, videos, source




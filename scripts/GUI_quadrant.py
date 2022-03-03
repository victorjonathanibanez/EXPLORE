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

def GUI_quadrant():

	def get_values():
		return [entry.get() for entry in entries]

	def call_dic(dic):

		for key, value in dic.items():
			
			for i in range(len(value)):

				if value[i][0] == 'Label':
					lbl=Label(window, text=value[i][1][1])
					lbl.place(x=int(win_w*value[i][1][0]), y=int(win_h*key))
					lbl.config(font=("TkDefaultFont", f_size, "italic"))

				if value[i][0] == 'Entry':
					txtfld=Entry(window, bd=2, width=value[i][1][1])
					txtfld.place(x=int(win_w*value[i][1][0]), y=int(win_h*key))
					entries.append(txtfld)

				if value[i][0] == 'Button':
					if value[i][1][1] == 'path':
						btn=Button(window, text="search", command=open_path)
					if value[i][1][1] == 'vid':
						btn=Button(window, text="search", command=open_vid)
					if value[i][1][1] == 'submit':
						btn=Button(window, text="start", command=submit)

					btn.place(x=int(win_w*value[i][1][0]), y=int(win_h*key))
					btn.config(font=("TkDefaultFont", f_size, "italic"))

				if value[i][0] == 'Radiobutton':
					global var
					var = IntVar()
					R1 = Radiobutton(window, text=value[i][1][1], variable=var, value=1,command=sel)
					R1.place(x=int(win_w*value[i][1][0]), y=int(win_h*key))
					R1.config(font=("TkDefaultFont", f_size, "italic"))
					R2 = Radiobutton(window, text=value[i][1][3], variable=var, value=2,command=sel)
					R2.place(x=int(win_w*value[i][1][2]), y=int(win_h*key))
					R2.config(font=("TkDefaultFont", f_size, "italic"))

	def open_path():
		global project_path

		project_path = fd.askdirectory()

		lbl=Label(window, text=project_path.ljust(1000))
		lbl.place(x=int(win_w*0.05), y=int(win_h*0.26))
		lbl.config(font=("Arial", f_size-2))

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
				lbl1.place(x=int(win_w*0.05)+(i*int(win_w*0.05)), y=int(win_h*0.41))
				lbl1.config(font=("Arial", f_size-2))
				lbl2=Label(window, text=''.ljust(1000))
				lbl2.place(x=int(win_w*0.05), y=int(win_h*0.44))
				lbl2.config(font=("Arial", f_size-2))
			if i >= nb_items:
				lbl3=Label(window, text=name.ljust(1000))
				lbl3.place(x=int(win_w*0.05)+((i-nb_items)*int(win_w*0.05)), y=int(win_h*0.44))
				lbl3.config(font=("Arial", f_size-2))

	def sel():
		global selection

		selection =  var.get()

	def submit():
		global video_length
		global project_name
		global project_path
		global background

		entry_list = get_values()
		project_name = entry_list[0]
		video_length = entry_list[1]
		background = var.get()
		window.destroy()

	window=Tk()

	width = window.winfo_screenwidth()
	height = window.winfo_screenheight()
	win_w = int(width/2)
	win_h = int(height/1.15)

	norm_w = 1280
	norm_f_size = 14

	f_size = round((norm_w*norm_f_size)/width)
	
	main = {0.03:[['Label',[0.05,'project name:']],['Label',[0.55,'cutting length videos (min):']]],
			0.08:[['Entry',[0.05,30]],['Entry',[0.55,5]]],
			0.16:[['Label',[0.05,'choose project path:']]],
			0.21:[['Button',[0.05,'path']]],
			0.31:[['Label',[0.05,'choose videos:']]],
			0.36:[['Button',[0.05,'vid']]],
			0.51:[['Label',[0.05,'animals darker than background?']]],
			0.56:[['Radiobutton',[0.05,'yes',0.15,'no']]],
			0.94:[['Button',[0.05,'submit']]]}
				
	entries = []
	
	call_dic(main)

	window.title('Create a new Project!')
	window.geometry(str(win_w)+'x'+str(win_h)+'+10+10')
	window.mainloop()

	return project_path, project_name, videos, video_length, background#, create_plot




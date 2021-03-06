import tkinter as tk
from tkinter import font


from PIL import ImageTk, Image, ImageEnhance

import sys, time, sys, random, platform, time, os
import flickr, settings


# sleep 1; xset +dpms; xset s activate

########################################## go #####################################

# basic code -------------------------------------------------------------------------
class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master = master
		
		pad=0
		self._geom='200x200+0+0'
		master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
		master.configure(background='black')
		master.bind('<Escape>',self.leave) 
		master.attributes('-fullscreen', True)
		master.configure(cursor="none")
		fr = tk.Frame(master)
		fr.pack(expand=1) 

		# font
		helv36 = font.Font(family='Helvetica',size=36, weight='bold')  # you don't have to use Helvetica or bold, this is just an example
		button = tk.Button(fr)
		# design
		button.configure(justify=tk.CENTER)
		button.configure(highlightthickness=0)
		button.configure(bd=0)
		button.configure(borderwidth=0)
		button.configure(compound=tk.CENTER)
		button.configure(font=helv36)
		button.configure(padx=0)
		button.configure(pady=0)
		button.configure(highlightcolor='pink')
		button.configure(highlightbackground='pink')
		button.configure(activebackground='black')
		button.configure(activeforeground='orange')
		button.configure(bg='black')
		button.bind("<Button-3>", self.leave)

		# go
		button.configure(command=lambda: self.update_img(silent = 0))
		button.pack(anchor=tk.CENTER)


		self.button = button
		self.button_image = ""
		self.callback_handle = None
		# choose source, album or all picture
		self.update_img(silent = 1,splash = 1) # show splash
		self.master.update()
		flickr.init()	# get data from flickr

	def update_img(self,silent = 1,splash=0):
		# call it with silent == 0, on button push; else silent == 1 
		recall_time=settings.time_regular_update
		print("")
		print(time.strftime("%H:%M:%S"))
		if(silent != 1):
			print("[GUI] click, non silent update, add 'Loading' label")
			self.button.configure(text = "Loading ...")

			# if there was an old image, show it as grayscale
			if(self.button_image!=""):
				self.button_image_photo = ImageTk.PhotoImage(self.button_image.convert('LA'))
				self.button.configure(image = self.button_image_photo)	
				self.button.image = self.button_image_photo
				self.master.update()
		else:
			print("[GUI] silent update, skipping 'Loading' label")

		if(splash):
			print("[GUI] Loading Splash ...")
			recall_time=settings.time_splash

		self.button_image = resize_img(flickr.get_photo(splash=splash))
		self.button_image_photo = ImageTk.PhotoImage(self.button_image)
		# set it
		self.button.configure(image = self.button_image_photo, text = "")

		# disable callback and restart it
		if(self.callback_handle is not None):
			self.master.after_cancel(self.callback_handle)	
		self.callback_handle = self.master.after(recall_time, self.update_img)

	def leave(self,event):
		self.button.configure(text = "Exiting ...")
		# if there was an old image, show it as grayscale
		if(self.button_image!=""):
			self.button_image_photo = ImageTk.PhotoImage(self.button_image.convert('LA'))
			self.button.configure(image = self.button_image_photo)	
			self.button.image = self.button_image_photo
			self.master.update()
			time.sleep(1)
		exit()


def resize_img(path):
	img = Image.open(path)
	scale_x = root.winfo_screenwidth()/img.size[0]
	scale_y = root.winfo_screenheight()/img.size[1]
	if(scale_x<scale_y):
		scale = scale_x
	else:
		scale = scale_y
	img = img.resize((int(img.size[0]*scale), int(img.size[1]*scale)), Image.ANTIALIAS) 
	return img
	
root=tk.Tk()
app = FullScreenApp(root)
root.mainloop()




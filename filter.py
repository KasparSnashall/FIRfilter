"""
An interative GUI designed for a low pass filter
author: Kaspar Snashall
year: 2016
"""




from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import FileDialog
import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np
import tkMessageBox
import tkFileDialog

np.set_printoptions(suppress=True) # surpress scientific notation

def main():
	root = Tk()
	root.wm_title("FIR low pass filter")
	# making the grid
	
	#main frame
	frame = Frame(root)
	frame.pack(fill=BOTH,expand=YES)
	
	#left side of gui
	leftframe = Frame(frame, bd=20)
	leftframe.pack(side=TOP,fill=X,expand=YES)

	#entry = Entry(leftframe)
        #entry.grid(row=0, columnspan=3, sticky=W+E)


	# add some widgets
	L1 = Label(leftframe, text="Number of coeffs",bd=12,font=("arial", "11", "normal"))
	L1.grid( row = 0, column = 0)
	ttp1 = CreateToolTip(L1, "The number of coefficents that will \n be used in windowing")

	#L2 = Label(leftframe, text="Nqyst freq",bd=12,font=("arial", "11", "normal"))
	#L2.grid( row = 0, column = 1)
	L4 = Label(leftframe, text="Width",bd=12,font=("arial", "11", "normal"))
	L4.grid( row = 0, column = 1)
	ttp2 = CreateToolTip(L4, "The effective width of the transistion region")

	L3 = Label(leftframe, text="Cut off",bd=12,font=("arial", "11", "normal"))
	L3.grid( row = 0, column = 2)
	ttp3 = CreateToolTip(L3, "The cut off point of the window (-3dB)")
	
	
	
	coeff_entry = Entry(leftframe, bd =6,justify='center')
	coeff_entry.grid( row = 1, column = 0)

	#nyqst_entry = Entry(leftframe, bd =6,justify='ctkFileDialogenter')
	#nyqst_entry.grid( row = 1, column = 1)
	
	width_entry = Entry(leftframe, bd =6,justify='center')
	width_entry.grid( row = 1, column = 1)
	
	cutoff_entry = Entry(leftframe, bd =6,justify='center')
	cutoff_entry.grid( row = 1, column = 2)

	

	variable = StringVar(root)
	variable.set("Window") # default value
	w = OptionMenu(leftframe, variable, "boxcar", "triang", "blackman", "hamming", "hann", "bartlett", "flattop", "parzen", "bohman", "blackmanharris", "nuttall", "barthann", 
		"kaiser (needs beta)", "gaussian (needs standard deviation)", "general_gaussian (needs power, width)", 
		"slepian (needs width)", "chebwin (needs attenuation)", "exponential (needs decay scale)", "tukey (needs taper fraction)")
	w.grid(row = 4,column = 0,pady=(10, 10))

	option1_entry = Entry(leftframe, bd =6,justify='center',state=DISABLED)
	option1_entry.grid( row = 4, column = 1,pady=(20, 10))
	option2_entry = Entry(leftframe, bd =6,justify='center',state=DISABLED)
	option2_entry.grid( row = 4, column = 2,pady=(20, 10))	
	
	def option_changed(*args):
		opt = variable.get()
		print opt
		if "kaiser" in opt:
			option1_entry.configure(state = "normal")
			option2_entry.configure(state = "disabled")
			return 0
		if "gaussian" in opt and "_" not in opt:
			option1_entry.configure(state = "normal")
			option2_entry.configure(state = "disabled")
			return 0
		if "general_gaussian" in opt:
			option1_entry.configure(state = "normal")
			option2_entry.configure(state = "normal")
			return 0
		if "slepian" in opt:
			option1_entry.configure(state = "normal")
			option2_entry.configure(state = "disabled")
			return 0
		if "chewbin" in opt:
			option1_entry.configure(state = "normal")
			option2_entry.configure(state = "disabled")
			return 0
		if "exponential" in opt:
			option1_entry.configure(state = "normal")
			option2_entry.configure(state = "disabled")
			return 0
		if "tukey" in opt:
			option1_entry.configure(state = "normal")
			option2_entry.configure(state = "disabled")
			return 0
		else:
			option1_entry.configure(state = "disabled")
			option2_entry.configure(state = "disabled")
	

	variable.trace("w", option_changed)
	def graph(b,a=1):
			#make a graph
			w,h = signal.freqz(b,a)
			h_dB = 20 * np.log10 (abs(h))
			plt.figure()
			#plt.subplot(311)
			plt.plot(w/max(w),h_dB)
			plt.ylim(-150, 5)
			plt.ylabel('Magnitude (db)')
			plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
			plt.title(r'Frequency response')
			plt.show()
			plt.figure()
			l = len(b)
			impulse = np.repeat(0.,l); impulse[0] =1.
			x = arange(0,l)
			response = signal.lfilter(b,a,impulse)
			#plt.subplot(312)
			plt.stem(x, response)
			plt.ylabel('Amplitude')
			plt.xlabel(r'n (samples)')
			plt.title(r'Impulse response')
			plt.show()
			#plt.figure()
			#plt.subplot(313)
			#step = np.cumsum(response)
			#plt.stem(x, step)
			#plt.ylabel('Amplitude')
			#plt.xlabel(r'n (samples)')
			#plt.title(r'Step response')
			#plt.subplots_adjust(hspace=0.5)
			#plt.show()
			return 1

	

	def run():
		"""
		Function of the run button

		"""
		numtaps = coeff_entry.get() # number of coeffs
		# check to see if number
		if numtaps.isdigit() == False:
			tkMessageBox.showinfo( "ERROR","Coefficent entry is not an integer number",icon="error")
			return 0
		else:
			numtaps = float(numtaps)

		mywindow = variable.get() #cut off is the normalised cut off in terms of nqy
		# window is the function
		mywindow = str(mywindow)
		mylist = ["kaiser","slepian","chewbin","exponential","tukey" ]
		if any(x in mywindow for x in mylist):
			for x in mylist:
				if x in mywindow:
					try:
						mynum = float(option1_entry.get())
						mywindow  = (str(x), mynum)
					except:
						tkMessageBox.showinfo( "ERROR","window entry not a number",icon="error")
						return 0

		elif "gaussiantkFileDialog" in mywindow and "general" not in mywindow:
			try:
				mynum = float(option1_entry.get())
				mywindow  = ("gaussian", mynum)
			except:
				tkMessageBox.showinfo( "ERROR","window entry not a number",icon="error")
		elif "general_gaussian" in mywindow:
			try:
				mynum = float(option1_entry.get())
				mynum2 = float(option2_entry.get())
				mywindow  = ("general_gaussian", mynum,mynum2)
			except:
				tkMessageBox.showinfo( "ERROR","one of the window entry not a number",icon="error")
				return 0				
		else:
			mywindow = mywindow
			

		mycutoff = cutoff_entry.get()


		try:
			float(mycutoff)
			mycutoff = float(mycutoff)
		except:
			tkMessageBox.showinfo( "ERROR","Cut off entry is not a floating point number",icon="error")
			return 0

		mywidth = width_entry.get()
		try:
			float(mywidth)
			mycutoff = float(mywidth)
		except:
			tkMessageBox.showinfo( "ERROR","Width entry is not a floating point number",icon="error")
			return 0
		# options = boxcar, triang, blackman, hamming, hann, bartlett, flattop, parzen, bohman, blackmanharris, nuttall, barthann, 
		#kaiser (needs beta), gaussian (needs standard deviation), general_gaussian (needs power, width), 
		#slepian (needs width), chebwin (needs attenuation), exponential (needs decay scale), tukey (needs taper fraction)

		fir_coeff = signal.firwin(numtaps, cutoff = mycutoff, window = mywindow, nyq = 1000, width = mywidth) #
		plt.ion()
		graph(fir_coeff)
		T1.delete("1.0",END) # clear text
		mymulti = Multi_entry.get()
		if mymulti is not None:
			if mymulti.isdigit():
				mymulti = float(mymulti)
				#fir_coeff = fir_coeff.tolist()
				coeff_sum = np.sum(fir_coeff)
				fir_coeff = fir_coeff/coeff_sum
				fir_coeff = np.rint(fir_coeff*mymulti)
				fir_coeff = fir_coeff.astype(int)
				
				#for x in fir_coeff:
				#	print type(x)
				#fir_coeff = [ x*mymulti for x in fir_coeff ]
				
		T1.insert(END, fir_coeff)
		return 1
	
	MultiLabel = Label(leftframe, text="Multiply",bd=12,font=("arial", "11", "normal"))
	MultiLabel.grid( row = 5, column = 0)
	
	Multi_entry = Entry(leftframe, bd =6,justify='center')
	Multi_entry.grid( row = 5, column = 1)		

	run_button = Button(leftframe, text ="Run",command=run)
	run_button.grid(row = 5,column = 2,pady=(20, 10))
	T1 = Text(leftframe, height=7)
	T1.grid(row = 6, column = 0, columnspan = 3)
	S = Scrollbar(leftframe)
	S.grid(row = 6, column = 3, sticky=NS)
	T1.config(yscrollcommand=S.set)
	S.config(command=T1.yview)
	root.mainloop()

	


class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() - 50
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background='lightgrey', relief='solid', borderwidth=3,
                       font=("arial", "12", "normal"))
        label.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


if __name__ == '__main__':
	main() # run the program

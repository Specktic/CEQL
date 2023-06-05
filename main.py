from tkinter import *

login_window = Tk()
login_window.geometry("800x450")
login_window.title("Visualizer")
login_window.config(background="#8e8f99")

login_button = Button(login_window,
                      text="login",
                      command="",
                      font=("Helvetica", 15),
                      fg="black",
                      bg="white",
                      activeforeground="black",
                      activebackground="grey",
                      state=ACTIVE)
login_button.place(x=330, y=350)

register_button = Button(login_window,
                         text="register",
                         command="",
                         font=("Helvetica", 15),
                         fg="black",
                         bg="white",
                         activeforeground="black",
                         activebackground="grey",
                         state=ACTIVE)
register_button.place(x=420, y=350)

login_window.mainloop()

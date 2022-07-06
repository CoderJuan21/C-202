import socket
from threading import Thread
from tkinter import *

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300, bg="#29db38")

        self.pls = Label(self.login, text = "please login to continue", justify = CENTER, bg="blue", font = "Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)
        
        self.labelname = Label(self.login, text = "Name -> ", bg="green", font = "Helvetica 14 bold")
        self.labelname.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryname = Entry(self.login, font = "Helvetica 14 bold")
        self.entryname.place(relheight=0.1, relwidth=0.4, relx=0.35, rely=0.2)
        self.entryname.focus()

        self.go = Button(self.login, text = "CONTINUE",bg="#0bea18", font = "Helvetica 14 bold", command=lambda:self.goahead(self.entryname.get()))
        self.go.place(relx=0.4, rely=0.5)
        self.Window.mainloop()

    def goahead(self,name):
       self.login.destroy()
    #    self.name = name
       self.layout(name)
       rcv = Thread(target = self.receive)
       rcv.start()

    def layout(self,name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("Chat Room")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470,height=550, bg="#7b28d1")
        self.labelHead = Label(self.Window, bg="#0be38a", text=self.name, font="Helvetica 14 bold", pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window, width=250, bg="#f1203d")
        self.line.place(relwidth=1,rely=0.07, relheight=0.012)

        self.textCons = Text(self.Window, width=20, height=2, bg="#10dfc8", padx=5, pady=5, font="Helvetica 14")
        self.textCons.place(relheight=0.7, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window, bg="#cdc834", height=80)
        self.labelBottom.place(relwidth=1, rely=0.8)

        self.entryMessage = Entry(self.labelBottom, font = "Helvetica 13", bg="#2db123")
        self.entryMessage.place(relwidth=0.7, relheight=0.06, rely=0.008, relx=0.01)
        self.entryMessage.focus()

        self.buttonMessage = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, bg="#2839dc", command=lambda:self.sendButton(self.entryMessage.get()))
        self.buttonMessage.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.97)
        scrollbar.config(command=self.textCons.yview)

    def sendButton(self,msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMessage.delete(0,END)
        snd = Thread(target=self.write)
        snd.start()

    def show_message(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message+"\n \n")
        self.textCons.config(state = DISABLED)
        self.textCons.see(END)


    def receive():
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(nickname.encode('utf-8'))
                else:
                    # print(message)
                    self.show_message(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}:{self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break
g = GUI()
# def write():
#     while True:
#         message = '{}: {}'.format(nickname, input(''))
#         client.send(message.encode('utf-8'))

# receive_thread = Thread(target=receive)
# receive_thread.start()
# write_thread = Thread(target=write)
# write_thread.start()

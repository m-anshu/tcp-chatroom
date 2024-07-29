import socket
import threading
import time
from tkinter import *
import pickle
import rsa
import binascii

name=input("enter your name : ")
public, private = rsa.generate_keypair(1024)
msg=pickle.dumps(public)

def set_ip():
    ip = edit_text_ip.get()
    port = edit_text_port.get()


    global client
    client = socket.socket()
    client.connect((ip, int(port)))


    input_root.destroy()

    input_root.quit()


def send():
    if str(edit_text.get()).strip() != "":
        message = str.encode(edit_text.get())
        hex_data   = binascii.hexlify(message)
        plain_text = int(hex_data, 16)
        ctt=rsa.encrypt(plain_text,pkey)
        client.send(str(ctt).encode())

        listbox.insert(END, message)
        edit_text.delete(0, END)


def recv():
    while True:
        response_message =int(client.recv(1024).decode())
        print(response_message)
        decrypted_msg = rsa.decrypt(response_message, private)
  
        listbox.insert(END, name1 +" : "+ str(decrypted_msg))
        edit_text.delete(0, END)



input_root = Tk()
bgimage = PhotoImage(file ="image2.png")
Label(input_root,image=bgimage).place(relwidth=1,relheight=1)
edit_text_ip = Entry()
edit_text_port = Entry()
ip_label = Label(input_root, text="Enter Server IP")
port_label = Label(input_root, text="Enter Server Port")
connect_btn = Button(input_root, text="Connect To Server", command=set_ip, bg='#668cff', fg="white")


ip_label.pack(fill=X, side=TOP)
edit_text_ip.pack(fill=X, side=TOP)
port_label.pack(fill=X, side=TOP)
edit_text_port.pack(fill=X, side=TOP)
connect_btn.pack(fill=X, side=BOTTOM)

input_root.title(name)
input_root.geometry("400x700")
input_root.resizable(width=False, height=False)

input_root.mainloop()

name1=client.recv(1024).decode()
client.send(str.encode(name))
rmsg=client.recv(1024)
pkey=pickle.loads(rmsg)

client.send(msg)

root = Tk()
bgimage2 = PhotoImage(file ="image2.png")
Label(root,image=bgimage2).place(relwidth=1,relheight=1)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack(fill=BOTH, side=TOP)
scrollbar.config(command=listbox.yview)

button = Button(root, text="Send Message", command=send, bg='#4040bf', fg="white")
button.pack(fill=X, side=BOTTOM)
edit_text = Entry(root)
edit_text.pack(fill=X, side=BOTTOM)

root.title(name)
root.geometry("400x700")
root.resizable(width=True, height=True)

threading.Thread(target=recv).start()

root.mainloop()

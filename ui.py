from tkinter import *
import tkinter.messagebox
from aes import aes_encrypt, aes_decrypt


def browsepage():
    root = Tk()
    root.geometry('400x400')
    root.title("AES File Encryption")

    """This is File pointer(Browse and print the content) """
    root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    Button(root, text='Encrypt', command=show_decryption_fields).grid(row=13, column=2, sticky=W, pady=4)
    Button(root, text='Decrypt', command=show_decryption_fields).grid(row=13, column=1, sticky=W, pady=4)
    Label(root, text="Key").grid(row=10,column=1)
    e3 = Entry(root,width=16)
    e3.grid(row=1, column=1)

    #print (root.filename)


def lim(*args):
    value = dayValue.get()
    if len(value) > 16 :
        dayValue.set(value[:16])



def show_entry_fields():
    text = e1.get()
    key = e2.get()
    error = "Please insert 16 character Key"
    if len(key) < 16:
        tkinter.messagebox.showerror("Error", error)
    encrypted = aes_encrypt(text, key)
    print("\n\tEncrypted message is:\n")
    print(encrypted.decode())
    tkinter.messagebox.showinfo("Encrypted Text",encrypted.decode())


def show_decryption_fields():
    text = e1.get()
    key = e2.get()
    error = "Please insert 16 character Key"
    if len(key) < 16:
        tkinter.messagebox.showerror("Error", error)
    decrypted = aes_decrypt(text, key)
    print("\n\tDecrypted message is:\n")
    print(decrypted.decode())
    tkinter.messagebox.showinfo("Decrypted Text",decrypted.decode())


master = Tk()
master.geometry('400x400')
master.title("AES Encryption")
Label(master, text="Plaintext").grid(row=0,column=1)
Label(master, text="Key").grid(row=10,column=1)
dayValue = StringVar()
dayValue.trace('w', lim)
e1 = Entry(master, width=50)
e2 = Entry(master,width=16,textvariable=dayValue)

e1.grid(row=1, column=1)
e2.grid(row=11, column=1)

Button(master, text='Quit', command=master.quit).grid(row=13, column=1, sticky=W, pady=4)
Button(master, text='Encrypt', command=show_entry_fields).grid(row=13, column=2, sticky=W, pady=4)
#Button(master, text='AddFile', command=browsepage).grid(row=1, column=2, sticky=W, pady=4)
Button(master, text='Decrypt', command=show_decryption_fields).grid(row=13, column=3, sticky=W, pady=4)
mainloop( )

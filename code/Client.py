####################################################
#  D1014636 潘子珉                                      									
####################################################
#import sys
import socket
import tkinter as tk

PORT = 6666
BUF_SIZE = 1024			# Receive buffer size

def createWindow():
    window = tk.Tk()
    window.title('Client')
    window.geometry("400x300")
    return window

def createController(window, target):
    frame = tk.Frame(window)
    frame.grid_columnconfigure(0, weight = 1)
    frame.grid_columnconfigure(1, weight = 1)
    ipLabel = tk.Label(frame ,text = "ip")
    ipLabel.grid(row = 0, column = 0)
    ipEntry = tk.Entry(frame)
    ipEntry.grid(row = 0, column = 1)
    ipEntry.insert(0, '127.0.0.1')
    numberLabel = tk.Label(frame ,text = "初始數值")
    numberLabel.grid(row = 1, column = 0)
    numberEntry = tk.Entry(frame)
    numberEntry.grid(row = 1, column = 1)
    start_btn = tk.Button(frame, text='連線', font = ("Times", 11, ""), command = lambda: main(target,ipEntry.get(),int(numberEntry.get())))
    start_btn.grid(row = 2, column = 0, pady = 10)
    clear_btn = tk.Button(frame, text='清除', font = ("Times", 11, ""), command = lambda: delete(target))
    clear_btn.grid(row = 2, column = 1, pady = 10)
    return frame

def createConsole(window):
    frame = tk.Frame(window)
    listbox = tk.Listbox(frame, font = ("Times", 11, ""))
    listbox.pack(side = "left", fill = "both", expand = True)
    scrollbar = tk.Scrollbar(frame, orient = "vertical", command = listbox.yview)
    scrollbar.pack(side = "left", fill = "both", expand = False)
    listbox.configure(yscrollcommand = scrollbar.set)
    return frame, listbox

def delete(listbox):
   listbox.delete(0,tk.END)
   
def append(listbox, txt, color = '#9c7f00'):
    listbox.insert(tk.END, txt)
    listbox.itemconfig(tk.END, { 'bg' :  color, 'fg' : '#fff'})


def main(listbox, serverIP, val1):
    consoleFmt = "%-25s %s"
    """
    if(len(sys.argv) < 2):
        print("Usage: python3 3-TCPClient.py ServerIP")
        exit(1)
    """
    # Get server IP
#    serverIP = socket.gethostbyname(sys.argv[1])

    # Create a TCP client socket
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    append(listbox, consoleFmt % ("[create socket]",""))
    # Connect to server
    print('Connecting to %s port %s' % (serverIP, PORT))
    try:
        cSocket.connect((serverIP, PORT))
    except Exception as msg:
        append(listbox, consoleFmt % ("[socket error]", msg))
        return
    append(listbox, consoleFmt % ("[socket connect]",""))
#    in1 = input('Input a integer: ')
#    val1 = int(in1)
    val1 = val1 - 1
	# Send message to server
    val1Str = str(val1)
    cSocket.send(val1Str.encode('utf-8'))
    append(listbox, consoleFmt % ("[send]", f"data: {val1Str}"), "#009c0d")
    # Receive server reply, buffer size = BUF_SIZE
    
    server_reply = cSocket.recv(BUF_SIZE)
    while server_reply:
        server_utf8 = server_reply.decode('utf-8')
        print(server_utf8)
        append(listbox, consoleFmt % ("[recv]", f"data: {server_utf8}"), "#00609c")
        server_count = int(server_utf8)
        if server_count >= 0:
            server_count = server_count - 1
            val1Str = str(server_count)
            append(listbox, consoleFmt % ("[send]", f"data: {val1Str}"), "#009c0d")
            
            cSocket.send(val1Str.encode('utf-8'))
            server_reply = cSocket.recv(BUF_SIZE)
        else:
            break
    append(listbox, consoleFmt % ("[socket close]",""))
    cSocket.close()

# end of main

def window_init():
    window = createWindow()

    console, listbox = createConsole(window)
    controller = createController(window, listbox)
    controller.pack(fill = "x", side = 'top')
    console.pack(fill = "both", side = 'bottom', expand = True)
    
    window.mainloop()

if __name__ == '__main__':
    window_init()

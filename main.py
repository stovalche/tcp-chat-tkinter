import os
import socket
import _thread
import pathlib
import tkinter as tk
import platform
from tkinter import ttk
from tkinter import messagebox, filedialog
from external_elements import colorscheme

class elements():
  host = "none"
  port = "none"
  username = ""
  user_port = ""
  clients = []
  client_addr = []
  client_namebyaddr = {}
  message_code = ""
  hist = ""
  os = platform.system()
  path = pathlib.Path().resolve()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_payload = (50 * (1024 * 10^3)) # 1 frame data

def create_connection():
  # create a connection to the server
  server_address = (elements.host, int(elements.port))
  sock.connect(server_address)

  # first login message
  message = "12345678login:" + elements.username
  sock.sendall(message.encode('utf-8'))

  hist_writer("chat_room", f"{elements.username} (You) are joined!\n")

  data = sock.recv(data_payload)
  coded_message = data.decode('utf-8')
  if coded_message.split('/')[0] == "12345678initialclients":
    splitted_message = coded_message.split('/')
    for addresses in splitted_message:
      if addresses != '' and addresses != "12345678initialclients":
        addr = addresses.split(':')[0]
        name = addresses.split(':')[1]
        elements.clients.append(name)
        elements.client_addr.append(str(addr))
        elements.client_namebyaddr.update({str(addr): str(name)})

def hist_writer(addr, formatted_message):
  cur_os = elements.os
  if cur_os == "Linux" or cur_os == "Darwin":
    sep = '/'
  elif cur_os == "Windows":
    sep = '\\'
  else:
    sep = '/'
  dirpath = f"{elements.path}{sep}hist"
  if not os.path.exists(dirpath):
    os.mkdir(dirpath)
  file = open(f"{dirpath}{sep}{elements.username}_{addr}.txt", 'a')
  file.write(formatted_message)
  file.close()

def hist_reader(addr):
  cur_os = elements.os
  if cur_os == "Linux" or cur_os == "Darwin":
    sep = '/'
  elif cur_os == "Windows":
    sep = '\\'
  else:
    sep = '/'
  dirpath = f"{elements.path}{sep}hist"
  if not os.path.exists(dirpath):
    os.mkdir(dirpath)
  if os.path.exists(f"{dirpath}{sep}{elements.username}_{addr}.txt"):
    file = open(f"{dirpath}{sep}{elements.username}_{addr}.txt", 'r')
    return f"{file.read()}"; file.close()
  else:
    hist_writer(addr, "")
    return ""

def login_window():
  window = tk.Tk()
  window.configure(background="White")
  window.resizable(True, True)

  server_host = tk.StringVar()
  server_port = tk.StringVar()
  username = tk.StringVar()

  main_frame = tk.Frame(window)
  main_frame.pack(pady=10, padx=10, fill="x", expand=True)

  # server host entry
  server_host_label = tk.Label(main_frame, text="Enter the server's IP:", font=("Hack NF", 10))
  server_host_label.pack(padx=10, pady=5, expand=False)
  server_entry = tk.Entry(main_frame, textvariable=server_host, font=("Hack NF", 10))
  server_entry.pack(padx=10, pady=5, expand=True)

  # server port entry
  server_host_label = tk.Label(main_frame, text="Enter the server's Port:", font=("Hack NF", 10))
  server_host_label.pack(padx=10, pady=5, expand=False)
  server_entry = tk.Entry(main_frame, textvariable=server_port, font=("Hack NF", 10))
  server_entry.pack(padx=10, pady=5, expand=True)

  # username entry
  server_host_label = tk.Label(main_frame, text="Enter your name:", font=("Hack NF", 10))
  server_host_label.pack(padx=10, pady=5, expand=False)
  server_entry = tk.Entry(main_frame, textvariable=username, font=("Hack NF", 10))
  server_entry.pack(padx=10, pady=5, expand=True)

  # log in button
  def _on_login_pressed():
    data_1 = str(server_host.get())
    data_2 = str(server_port.get())
    data_3 = str(username.get())
    if data_1 == "" or data_2 == "" or data_3 == "":
      messagebox.showinfo("Tk", "There is something wrong!\n")
      exit(0)
    else:
      elements.host = data_1
      elements.port = data_2
      elements.username = data_3
      create_connection()
      window.destroy()
      
  login_button = tk.Button(main_frame, text="log-in", command=_on_login_pressed, font=("Hack NF", 10))
  login_button.pack(padx=10, pady=10, expand=True)

  window.mainloop()


def session_window():
  # first defined hist file
  elements.hist = "chat_room"
  color = colorscheme.dark
  window = tk.Tk()
  window.configure(bg=color["base02"])
  window.resizable(True, True)
  window.title("Tcpchat")

  def header():
    # window label
    header_frame = tk.Frame(window, background=color["base00"])
    header_frame.pack(fill="both")
    label = tk.Label(header_frame, text="Tcpchat", background=color["base00"], foreground=color["base2"], font=("Hack NF", 14))
    label.pack(side=tk.LEFT, padx=10, pady=10, fill="x")

  def body():
    # body frame
    body_frame = tk.Frame(window, background=color["base03"])
    body_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def outputframe(user, message):
      if user != "":
        return f"{user} : {message}"
      else:
        return f"{message}"
      
    # users frame
    users_frame = tk.Frame(body_frame, background=color["base03"], border=0)
    users_frame.pack(side=tk.LEFT, fill="x", pady=10, padx=5, expand=True)
    users_title_frame = tk.Frame(users_frame, border=0)
    users_title_frame.pack(fill='y', pady=10)
    users_label = tk.Label(users_title_frame, text="Chat", font=("Hack NF", 13), foreground=color["base2"], background=color["base03"])
    users_label.pack(side=tk.RIGHT, fill='y')
    users_canvas = tk.Canvas(users_frame, background=color["base00"], border=0, width=160)
    ##---------- scrollregion has to be larger than canvas size
    ##           otherwise it just stays in the visible canvas
    users_canvas.pack(side=tk.LEFT, expand=True, fill="y")
    users_canvas_scrollable = ttk.Scrollbar(users_frame, orient="vertical", command=users_canvas.yview)
    users_canvas_scrollable.pack(side=tk.RIGHT, fill="y")
    users_canvas.configure(yscrollcommand=users_canvas_scrollable.set)

    def max_char(string):
      max_char_named = ""
      if len(string) > 15:
        for i in range(18):
          if i < 15:
            max_char_named += string[i]
          else:
            max_char_named += '.'
      else:
        max_char_named = string
      return max_char_named

    def _on_contact_pressed(addr):
      elements.message_code = f"12345678private:{addr}:"
      elements.hist = str(addr)
      chat_label.config(text=f"{elements.client_namebyaddr[str(addr)]}")
      chat_text.configure(state=tk.NORMAL)
      chat_text.delete("1.0", tk.END)
      chat_text.insert(tk.END, f"{hist_reader(str(addr))}")
      chat_text.yview_pickplace(tk.END)
      chat_text.configure(state=tk.DISABLED)

    def user_update():
      users_canvas.delete('all')
      index = 1
      def _on_chat_room_pressed():
        elements.message_code = ""
        elements.hist = "chat_room"
        chat_label.config(text="Chat room")
        chat_text.configure(state=tk.NORMAL)
        chat_text.delete("1.0", tk.END)
        chat_text.insert(tk.END, f"{hist_reader('chat_room')}")
        chat_text.yview_pickplace(tk.END)
        chat_text.configure(state=tk.DISABLED)
      users_canvas.config(scrollregion=( 0, 0, 0, 0))
      users_button = tk.Button(users_canvas, height=1, text="Chat room", background=color["blue"], foreground=color["base2"])
      users_button.config(command=_on_chat_room_pressed)
      users_button.pack(fill='x')
      users_canvas.create_window(0, 0, anchor='nw', window=users_button, width=160)
      for client_addr in elements.client_addr:
        def _on_contact_pressed_caller(x = str(client_addr)):
          return _on_contact_pressed(x)
        if client_addr != "":
          client_name = elements.clients[index - 1]
          shorted_client_name = max_char(client_name)
          users_canvas.config(scrollregion=( 0, 0, (index*30), (index*30 + (3 * index))))
          users_button = tk.Button(users_canvas, height=1, text=shorted_client_name, background=color["blue"], foreground=color["base2"])
          users_button.config(command=_on_contact_pressed_caller)
          users_button.pack(fill='x')
          users_canvas.create_window(0, (30*index), anchor='nw', window=users_button, width=160)
        index += 1

    # to check if there was some users or not
    user_update()

    # chat frame
    chat_frame = tk.LabelFrame(body_frame, background=color["base03"], border=0)
    chat_frame.pack(side=tk.RIGHT, fill='x', expand=True, pady=10, padx=5)
    chat_title_frame = tk.Frame(chat_frame, border=0)
    chat_title_frame.pack(fill='y', pady=10)
    chat_label = tk.Label(chat_title_frame, text="Chat room", font=("Hack NF", 13), foreground=color["base2"], background=color["base03"])
    chat_label.pack(side=tk.RIGHT, fill='y')
    chat_text = tk.Text(chat_frame, height=15, width=80, font=("Hack NF", 10), foreground=color["base2"], background=color["base01"], border=4)
    chat_text.pack(side=tk.LEFT, expand=True, fill="both")
    chat_box_scrollable = ttk.Scrollbar(chat_frame, orient="vertical", command=chat_text.yview)
    chat_box_scrollable.pack(side=tk.RIGHT, fill="y")
    chat_text.configure(cursor="arrow", state=tk.DISABLED, yscrollcommand=chat_box_scrollable.set)

    def chat_text_update(addr, message):
      hist_writer(f"{addr}", message)
      if str(elements.hist) == str(addr):
        chat_text.configure(state=tk.NORMAL)
        chat_text.delete("1.0", tk.END)
        chat_text.insert(tk.END, f"{hist_reader(str(addr))}")
        chat_text.yview_pickplace(tk.END)
        chat_text.configure(state=tk.DISABLED)

    # first open the hist file
    chat_text_update("chat_room", "")

    def file_receiver(private, coded_message):
      if private == 1:
        index = 1
      else:
        index = 0
      addr = coded_message.split(':')[index+1]
      filename = coded_message.split(':')[index+2]
      full_data = ""
      for i in range(index+3, coded_message.split(':').__len__()):
        if i > index+3:
          full_data += ':'
        full_data += coded_message.split(':')[i]
      cur_os = elements.os
      if cur_os == "Linux" or cur_os == "Darwin":
        sep = '/'
      elif cur_os == "Windows":
        sep = '\\'
      else:
        sep = '/'
      dirpath = f"{elements.path}{sep}received"
      if not os.path.exists(dirpath):
        os.mkdir(dirpath)
      file = open(f"{dirpath}{sep}{filename}", 'w')
      file.write(full_data)
      file.close()
      if private == 1:
        chat_text_update(addr, f"{elements.client_namebyaddr[str(addr)]} : █ {filename}\n")
      else:
        chat_text_update("chat_room", f"{elements.client_namebyaddr[str(addr)]} : █ {filename}\n")

    def receive_handler():
      while True:
        data = sock.recv(data_payload)
        message = data.decode('utf-8')
        if message.split(':')[0] == "12345678newuser":
          addr = message.split(':')[1]
          name = message.split(':')[2]
          full_message = message.split(':')[3] + "\n"
          elements.client_namebyaddr.update({str(addr): name})
          elements.client_addr.append(str(addr))
          elements.clients.append(name)
          user_update()
          chat_text_update("chat_room", outputframe("", full_message))
        elif message.split(':')[0] == "12345678private":
          if message.split(':')[1] == "12345678file":
            file_receiver(1, message)
          else:
            addr = str(message.split(':')[1])
            name = elements.client_namebyaddr[addr]
            full_message = ""
            for i in range(2, message.split(':').__len__()):
              if i > 2:
                full_message += ':'
              full_message += message.split(':')[i]
            chat_text_update(addr, outputframe(name, full_message))
        elif message.split(':')[0] == "12345678logout":
          addr = str(message.split(':')[1])
          name = str(message.split(':')[2])
          del elements.client_namebyaddr[addr]
          elements.clients.remove(name)
          elements.client_addr.remove(str(addr))
          full_message = f"{name} <{addr}> is exited!\n" 
          if elements.client_addr.__len__() == 0:
            elements.hist = "chat_room"
            chat_label.config(text="Chat room")
          user_update()
          chat_text_update("chat_room", outputframe("", full_message))
        else:
          if message.split(':')[0] == "12345678file":
            file_receiver(0, message)
          else:
            if message != "":
              addr = str(message.split(':')[0])
              name = elements.client_namebyaddr[addr]
              full_message = ""
              for i in range(1, message.split(':').__len__()):
                if i > 1:
                  full_message += ':'
                full_message += message.split(':')[i]
              chat_text_update("chat_room", outputframe(name, full_message))

    _thread.start_new_thread(receive_handler, ())

    # entry frame
    def _on_send_action():
      if entry.get("1.0", tk.END) == "\n":
        return messagebox.showinfo("Warning", "Empty message cannot be sent..!")
      message = entry.get("1.0", tk.END)
      entry.delete("1.0", tk.END)
      chat_text_update(elements.hist, outputframe(f"{elements.username} (You)", message))
      try:
        coded_message = elements.message_code + message
        sock.sendall(coded_message.encode('utf-8'))
      except socket.error as e:
        print ("Socket error: %s" %str(e))

    entry_frame = tk.Frame(window, background=color["base03"])
    entry_frame.pack(padx=10, fill="x", expand=True)

    def _on_cancel_file():
      entry.configure(state=tk.NORMAL)
      file_send_button.configure(text="File", command=_on_file_action)
      entry.delete("1.0", tk.END)
      text_send_button.configure(command=_on_send_action)

    def _on_file_action():
      file = filedialog.askopenfilename(initialdir=os.getenv("HOME"), title="Select A File")
      def _on_send_file():
        file_send_button.configure(text="File", command=_on_file_action)
        filename = file.split('/')
        file_data = open(file, 'r')
        data_readed = file_data.read()
        filename = filename[filename.__len__() - 1]
        entry.configure(state=tk.NORMAL)
        entry.delete("1.0", tk.END)
        chat_text_update(elements.hist, outputframe(f"{elements.username} (You)", f"█ {filename}\n"))
        sock.send(f"{elements.message_code}12345678file:{filename}:{data_readed}".encode('utf-8'))
        file_data.close()
        text_send_button.configure(command=_on_send_action)
      if f"{file}" != "()" and f"{file}" != "":
        entry.delete("1.0", tk.END)
        entry.insert(tk.END, f"Send file: █ {file}")
        entry.configure(state=tk.DISABLED)
        file_send_button.configure(text="Cancel", command=_on_cancel_file)
        text_send_button.configure(command=_on_send_file)

    # file send button
    file_send_button = tk.Button(entry_frame, text="File", command=_on_file_action, font=("Hack NF", 13), foreground=color["base3"], background=color["yellow"])
    file_send_button.pack(side=tk.LEFT,padx=10,pady=10,fill="x",expand=True)

    # entry text box
    entry = tk.Text(entry_frame, height=2,  font=("Hack NF", 10), foreground=color["base2"], background=color["base01"])
    entry.pack(side=tk.LEFT, pady=5, expand=False)
    entry.focus()

    # text send Button
    text_send_button = tk.Button(entry_frame, text="Send", command=_on_send_action, font=("Hack NF", 13),  foreground=color["base3"], background=color["yellow"])
    text_send_button.pack(side=tk.RIGHT, padx=10,pady=10,fill="x",expand=True)

  # exit Button
  def footer():
    def _on_exit_pressed():

      full_message = f"{elements.username} (You) are exited!\n" 
      hist_writer("chat_room", full_message)

      sock.send(f"12345678exit".encode('utf-8'))
      sock.close()
      exit(0)

    exit_button = tk.Button(window, text="Exit", command=_on_exit_pressed, font=("Hack NF", 13),  foreground=color["base3"], background=color["yellow"])
    exit_button.pack(pady=20, expand=True)

  header()
  body()
  footer()
  window.mainloop()

if __name__ == "__main__":
  login_window()
  session_window()

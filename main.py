import os
import tkinter as tk
from tkinter import messagebox, filedialog
from assets import colorscheme
from assets import icon
import socket
import _thread

class elements():
  host = "none"
  port = "none"
  username = ""
  clients = []
  client_connbyaddr = {}
  client_namebyaddr = {}
  status_message = ""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_payload = (50 * (1024 * 10^3)) # 1 frame data

def create_connection():
  # create a connection to the server
  server_address = (elements.host, int(elements.port))
  sock.connect(server_address)

  # first login message
  message = "12345678login:" + elements.username
  sock.sendall(message.encode('utf-8'))

  data = sock.recv(data_payload)
  coded_message = data.decode('utf-8')
  if coded_message.split('/')[0] == "12345678initialclients":
    splitted_message = coded_message.split('/')
    for addresses in splitted_message:
      if addresses != '' and addresses != "12345678initialclients":
        addr = addresses.split(':')[0]
        conn = addresses.split(':')[1]
        name = addresses.split(':')[2]
        elements.clients.append(name)
        elements.client_connbyaddr.update({str(addr): str(conn)})
        elements.client_namebyaddr.update({str(addr): str(name)})

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
    # print with buble chat
    def outputframe(message, user):
      hor_line = "\u2500"

      term_size = 60
      header = term_size - 2 - len(user)
      if header % 2 == 1:
        half_left = (header + 1) / 2
        le_left = hor_line * int(half_left)
        le_right = hor_line * int(header - half_left)
      else:
        half_left = header / 2
        le_left = hor_line * int(half_left)
        le_right = hor_line * int(header - half_left)

      if user != "":
        head_string = hor_line + "\u257C " + user + " \u257E" + le_left + le_right + hor_line
      else:
        head_string = hor_line + hor_line + hor_line + le_left + le_right + hor_line
      foot_string = hor_line + (hor_line * term_size) + hor_line
      term_size = int(term_size * 9 / 6 + 1)
      sep_string = '-' + ('-' * term_size) + '-'
      value = f"{head_string}\n{message}{foot_string}\n{sep_string}\n"

      return value

    # chat frame
    body_frame = tk.Frame(window, background=color["base03"])
    body_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # users frame
    users_frame = tk.Frame(body_frame, background=color["base03"])
    users_frame.pack(side=tk.LEFT, fill="x")
    users_title_frame = tk.Frame(users_frame, background=color["base03"])
    users_title_frame.pack(fill='y')
    users_icon = tk.Label(users_title_frame, text=icon.users_icon, font=("Hack NF", 20), foreground=color["base2"], background=color["base03"])
    users_icon.pack(side=tk.LEFT, fill='x')
    users_label = tk.Label(users_title_frame, text="Users:", font=("Hack NF", 10), foreground=color["base2"], background=color["base03"])
    users_label.pack(side=tk.RIGHT, fill='x', pady=10)
    users_text = tk.Text(users_frame, width=15, height=15, font=("Hack NF", 10), foreground=color["base2"], background=color["base01"], border=0)
    users_text.pack(side=tk.LEFT, padx=5, pady=10, expand=True, fill="y")
    users_text_scrollable = tk.Scrollbar(users_frame, orient="vertical", command=users_text.yview, background=color["base02"], border=0)
    users_text_scrollable.pack(side=tk.LEFT, fill="y")
    users_text.configure(cursor="arrow", state=tk.DISABLED, yscrollcommand=users_text_scrollable.set)

    def user_update():
      users=""
      for i in elements.clients:
        if i != "":
          users = f"{users}- {i}\n"
      users_text.configure(state=tk.NORMAL)
      users_text.delete("1.0", tk.END)
      users_text.insert(tk.END, f"{users}")
      users_text.configure(state=tk.DISABLED)

    # your username update for the first time
    user_update()

    # chat frame
    chat_frame = tk.LabelFrame(body_frame, background=color["base03"], border=0)
    chat_frame.pack(side=tk.RIGHT, fill='both', expand=True, pady=10, padx=5)
    chat_title_frame = tk.Frame(chat_frame, border=0)
    chat_title_frame.pack(fill='y')
    chat_icon = tk.Label(chat_title_frame, text=icon.chat_icon, font=("Hack NF", 24), foreground=color["base2"], background=color["base03"])
    chat_icon.pack(side=tk.LEFT, fill='y')
    chat_label = tk.Label(chat_title_frame, text="Chat room:", font=("Hack NF", 10), foreground=color["base2"], background=color["base03"])
    chat_label.pack(side=tk.RIGHT, fill='y')
    chat_text = tk.Text(chat_frame, height=15, width=70, font=("Hack NF", 10), foreground=color["base2"], background=color["base01"], border=0)
    chat_text.pack(side=tk.LEFT, padx=5, pady=10, expand=True, fill="y")
    chat_box_scrollable = tk.Scrollbar(chat_frame, orient="vertical", command=chat_text.yview, background=color["base02"], border=0)
    chat_box_scrollable.pack(side=tk.RIGHT, fill="y")
    chat_text.configure(cursor="arrow", state=tk.DISABLED, yscrollcommand=chat_box_scrollable.set)

    def receive_handler():
      while True:
        data = sock.recv(data_payload)
        message = data.decode('utf-8')
        if message.split(':')[0] == "12345678newuser":
          addr = message.split(':')[1]
          conn = message.split(':')[2]
          name = message.split(':')[3]
          full_message = message.split(':')[4]
          elements.client_connbyaddr.update({str(addr): str(conn)})
          elements.client_namebyaddr.update({str(addr): name})
          elements.clients.append(name)
          user_update()
          chat_text.configure(state=tk.NORMAL)
          chat_text.insert(tk.END, outputframe(f"{full_message}\n", ""))
          chat_text.yview_pickplace(tk.END)
          chat_text.configure(state=tk.DISABLED)
        elif message.split(':')[0] == "12345678private":
          pass
        elif message.split(':')[0] == "12345678logout":
          addr = str(message.split(':')[1])
          name = str(message.split(':')[2])
          del elements.client_connbyaddr[addr]
          del elements.client_namebyaddr[addr]
          elements.clients.remove(name)
          user_update()
          chat_text.configure(state=tk.NORMAL)
          chat_text.insert(tk.END, outputframe(f"{name} <{addr}> is exited!\n", ""))
          chat_text.yview_pickplace(tk.END)
          chat_text.configure(state=tk.DISABLED)
        else:
          full_message = ""
          sender = elements.client_namebyaddr[str(message.split(':')[0])]
          for i in range(1, message.split(':').__len__()):
            if i > 1:
              full_message += ':'
            full_message += message.split(':')[i]
          chat_text.configure(state=tk.NORMAL)
          chat_text.insert(tk.END, outputframe(f"{full_message}", sender))
          chat_text.yview_pickplace(tk.END)
          chat_text.configure(state=tk.DISABLED)

    _thread.start_new_thread(receive_handler, ())

    # entry frame
    def _on_send_action():
      if entry.get("1.0", tk.END) == "\n":
        return messagebox.showinfo("Warning", "Empty message cannot be sent..!")
      message = entry.get("1.0", tk.END)
      chat_text.configure(state=tk.NORMAL)
      chat_text.insert(tk.END, outputframe(message, f"{elements.username}(You)"))
      entry.delete("1.0", tk.END)
      chat_text.yview_pickplace(tk.END)
      chat_text.configure(state=tk.DISABLED)
      try:
        sock.sendall(message.encode('utf-8'))
      except socket.error as e:
        print ("Socket error: %s" %str(e))


    entry_frame = tk.Frame(window, background=color["base03"])
    entry_frame.pack(padx=10,pady=10,fill="x",expand=True)

    def _on_cancel_file():
      entry.configure(state=tk.NORMAL)
      file_send_button.configure(text=icon.file_icon, command=_on_file_action)
      entry.delete("1.0", tk.END)

    def _on_file_action():
      file = filedialog.askopenfilename(initialdir=os.getenv("HOME"), title="Select A File")
      def _on_send_file():
        file_send_button.configure(text=icon.file_icon, command=_on_file_action)
        filename = file.split('/')
        filename = filename[filename.__len__() - 1]
        entry.configure(state=tk.NORMAL)
        entry.delete("1.0", tk.END)
        chat_text.configure(state=tk.NORMAL)
        chat_text.insert(tk.END, outputframe(f"{icon.file_icon} {filename}\n", f"{elements.username}(You)"))
        chat_text.configure(state=tk.DISABLED)
        chat_text.yview_pickplace(tk.END)
        text_send_button.configure(command=_on_send_action)
      if f"{file}" != "()" and f"{file}" != "":
        entry.delete("1.0", tk.END)
        entry.insert(tk.END, f"Send file: {file}")
        entry.configure(state=tk.DISABLED)
        file_send_button.configure(text=icon.cancel_icon, command=_on_cancel_file)
        text_send_button.configure(command=_on_send_file)

    # file send button
    file_send_button = tk.Button(entry_frame, text=icon.file_icon, command=_on_file_action, font=("Hack NF", 17), foreground=color["base3"], background=color["yellow"])
    file_send_button.pack(side=tk.LEFT,padx=10,pady=10,fill="x",expand=True)

    # entry text box
    entry = tk.Text(entry_frame, height=2, width=70, font=("Hack NF", 10), foreground=color["base2"], background=color["base01"])
    entry.pack(side=tk.LEFT, padx=5, pady=5, expand=False)
    entry.focus()

    # text send Button
    text_send_button = tk.Button(entry_frame, text=icon.send_icon, command=_on_send_action, font=("Hack NF", 17),  foreground=color["base3"], background=color["yellow"])
    text_send_button.pack(side=tk.RIGHT, padx=10,pady=10,fill="x",expand=True)

  # exit Button
  def footer():
    def _on_exit_pressed():
      sock.send(f"12345678exit".encode('utf-8'))
      sock.close()
      exit(0)

    exit_button = tk.Button(window, text="Exit", command=_on_exit_pressed, font=("Hack NF", 10),  foreground=color["base3"], background=color["yellow"])
    exit_button.pack(padx=10, pady=10, expand=True)



  header()
  body()
  footer()
  window.mainloop()

if __name__ == "__main__":
  login_window()
  session_window()

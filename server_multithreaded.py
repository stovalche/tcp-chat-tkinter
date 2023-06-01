import socket
import _thread

data_payload = (50 * (1024 * 10^3)) # 1 frame data maksimal 50 mb
backlog = 100 # jumlah maksimal koneksi dalam satu waktu
server_address = (socket.gethostbyname(socket.gethostname()), 9900)
client_connection = []
client_name = {}
client_addr = {}
client_connectionbyaddr = {}

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enable reuse address/port
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the Socket to the port
print("Starting up echo server on %s, port %s\n" %server_address)
sock.bind(server_address)
# Listen to clients, backlog arguments specifies the max no of queued connections
sock.listen(backlog)


def remove_client(connection):
  addr = client_addr[connection]
  name = client_name[connection]
  for client in client_connection:
    if client != connection:
      try:
        coded_message = f"12345678logout:{addr}:{name}"
        client.send(coded_message.encode('utf-8'))
      except socket.error:
        print("# remove_client exception!")
        remove_client(client)
  for client in client_connection:
    if client == connection:
      print(f"{client_name[connection]} <{client_addr[connection]}> is exited!")
      del client_connectionbyaddr[str(client_addr[connection])]
      del client_name[connection]
      del client_addr[connection]
      client_connection.remove(connection)
      connection.close()

def broadcast(client_sender, full_message):
  for client in client_connection:
    if client != client_sender:
      try:
        message = ""
        if full_message.split(':')[0] == "12345678file":
          filename = full_message.split(':')[1]
          filedata = full_message.split(':')[2]
          message = f"12345678file:{client_addr[client_sender]}:{filename}:{filedata}"
        else:
          message = f"{client_addr[client_sender]}:{full_message}"
        client.send(message.encode('utf-8'))
      except socket.error:
        print("# broadcast exception!")
        remove_client(client)

def private(sender, coded_message):
  filename = ""
  filedata = "" 
  full_message = ""
  client_addr_target = coded_message.split(':')[1]
  client_conn_target = client_connectionbyaddr[str(client_addr_target)]
  if coded_message.split(':')[2] == "12345678file":
    filename = coded_message.split(':')[3]
    for i in range(4, coded_message.split(':').__len__()):
      if i > 4:
        filedata += ':'
      filedata += coded_message.split(':')[i]
  else:
    for i in range(2, coded_message.split(':').__len__()):
      if i != 2:
        full_message += ':'
      full_message += coded_message.split(':')[i]
  for client in client_connection:
    if str(client) == str(client_conn_target):
      if coded_message.split(':')[2] == "12345678file":
        message = f"12345678private:12345678file:{client_addr[sender]}:{filename}:{filedata}"
      else:
        message = f"12345678private:{client_addr[sender]}:{full_message}"
      client.send(message.encode('utf-8'))

def update_new_user(new_client, addr, name, full_message):
  if client_connection.__len__() > 0:
    initial_message = "12345678initialclients/"
    for client in client_connection:
      initial_message += f"{client_addr[client]}:{client_name[client]}/"
    new_client.send(initial_message.encode('utf-8'))
  else:
    new_client.send("12345678nothing".encode('utf-8'))
  client_name.update({new_client: name})
  client_addr.update({new_client: addr})
  client_connectionbyaddr.update({str(addr): new_client})
  client_connection.append(new_client)
  for client in client_connection:
    if client != new_client:
      try:
        client.send(f"12345678newuser:{addr}:{name}:{full_message}".encode('utf-8'))
      except socket.error:
        print("# update_new_user exception!")
        remove_client(client)

def client_thread(client, name):
  while True:
    try:
      data = client.recv(data_payload)
      if data:
        message = data.decode('utf-8')
        if message.split(':')[0] == "12345678private":
          private(client, message)
        elif message == "12345678exit":
          remove_client(client)
          _thread.exit()
        else:
          broadcast(client, message)
    except socket.error:
      print(f"# client_thread exception! for user named {name}")
      remove_client(client)
      _thread.exit()

    # connection check
    try:
      data = client.recv(data_payload, socket.MSG_DONTWAIT | socket.MSG_PEEK)
      if len(data) == 0:
        remove_client(client)
        _thread.exit()
    except BlockingIOError and ConnectionResetError:
      print(f"# connection checker exception! for user named {name}")
      remove_client(client)
      _thread.exit()
    except Exception:
      pass

if __name__ == "__main__":
  while True:
    connection, addr = sock.accept()
    data_client = connection.recv(data_payload).decode('utf-8')
    login_message = data_client.split(':')[0]
    name = data_client.split(':')[1]
    if login_message == "12345678login":
      new_user_info = f"{name} <{addr}> is joined!"
      print(new_user_info)
      update_new_user(connection, addr, name, new_user_info)
      _thread.start_new_thread(client_thread, (connection, name))

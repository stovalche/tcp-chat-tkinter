import socket
import _thread

data_payload = (50 * (1024 * 10^3)) # 1 frame data
client_connection = {}

def echo_client(host, port):
  print ("Connection with %s port %s\n" %(host, port))
  # Create a TCP/IP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Connect the socket to the server
  server_address = (host, port)
  sock.connect(server_address)

  # first login message
  name = input("Enter your name: ")
  message = "12345678login:" + name
  sock.sendall(message.encode('utf-8'))

  data = sock.recv(data_payload)
  client_connection = data.decode('utf-8')
  print("\n\n:" + client_connection)

  def receive_handler():
    while True:
      data = sock.recv(data_payload)
      if data:
        print ("\n" + data.decode('utf-8'))

  _thread.start_new_thread(receive_handler, ())

  while True:
    try:
      # Send data
      message = input("Client : ")
      sock.sendall(message.encode('utf-8'))
    except socket.error as e:
      print ("Socket error: %s" %str(e))

echo_client('', 9900)

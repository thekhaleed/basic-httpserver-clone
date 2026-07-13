"""
A basic http server
"""

import socket

def handle_request(request:str) -> tuple:
	lines = request.split("\r\n")

	# Get the different parts of the first line
	method, path, httpVersion = lines[0].split(" ")

	if path == '/':
		fileName = 'index.html'
	else:
		fileName = path.lstrip('/')

	try:
		with open("htdocs/" + fileName) as file:
			fileContent = file.read()

		return 200, fileContent
	except FileNotFoundError:
		return 404, "<h1>File Not Found</h1>"

def build_response(status: int, body:str)-> str:
	if status == 200:
		status_text = "OK"
	elif status == 400:
		status_text = "NOT FOUND"
	else:
		status_text = "INTERNAL SERVER ERROR"

	# Adding the different response headers
	response = f"HTTP/1.1 {status} {status_text}\r\n"
	response += "Content-Type: text/html\r\n"
	response += f"Content-Length: {len(body.encode())}\r\n\r\n"
	response += body
	return response

HOST = "127.0.0.1"
PORT = 8080

# Create socket
server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(10) # The integer is backlog which defines the number of connections that can wait in a queue while one is being processed
print(f"Listening on port {PORT}...\n")

while True:
	# Wait for connection to socket
	client_socket, client_addr = server_socket.accept()
	#print(f"Client Socket: {client_socket}")
	#print(f"Client Addr: {client_addr}")

	# Get client request
	request = client_socket.recv(1024).decode()
	print(request + "\n")

	# Send a response
	status, body = handle_request(request)
	response = build_response(status, body)
	client_socket.sendall(response.encode())
	print(response)

	client_socket.close()

server_socket.close()

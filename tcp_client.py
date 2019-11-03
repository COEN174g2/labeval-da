import socket                   # Import socket module


server_ip = "10.0.0.137" 
port = 60000      

s = socket.socket()             
host = server_ip    
        
message = "Hello server!"
s.connect((host, port))
s.send(message.encode())

with open("data_analytics.html", "wb") as f:
    while True:
        print("receiving data...")
        data = s.recv(1024)
        print("data=%s", (data))
        if not data:
            break
        f.write(data)

f.close()
print("Successfully get the file")
s.close()
print("Connection closed")


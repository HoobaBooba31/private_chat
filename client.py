import socket
import threading
import json

nickname = input("Введите своё имя: ")
room = int(input("Введите номер Комнаты: "))

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            print(msg.decode("utf-8"))
        except:
            break
    
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12345))

client.send(json.dumps({
    "username": nickname,
    "room_number": room
}).encode("utf-8"))

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

while True:
    message = input()
    client.send(json.dumps(
        {
            "username":nickname,
            "message": message
        }
    ).encode("utf-8"))
import socket
import threading
import json

rooms = {}

def handle_client(client: str, room_number: int):
    while True:
        try:
            msg = client.recv(1024)
            json_str = msg.decode("utf-8")
            data = json.loads(json_str)
            if not msg:
                break
            for member in rooms[room_number]:
                member.send(f'{data["username"]}|{room_number}:{data["message"]}'.encode("utf-8"))
        except Exception as e:
            print(f"Ошибка с клиентом: {e}")
            break

    rooms[room_number].remove(client)
    client.close()
    
def entering(username: str, room_number: int):
    for member in rooms[room_number]:
        member.send(f"{username} вошёл в чат!".encode("utf-8"))




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen()

print("Server started")

while True:
    client, addr = server.accept()
    print(f"{addr} подключился")

    # Для простоты допустим, что первый месседж клиента - это имя комнаты
    msg = client.recv(1024)
    if not msg:
        client.close()
        continue
    data = json.loads(msg.decode("utf-8"))

    room_number = data["room_number"]
    if room_number not in rooms:
        rooms[room_number] = []
    rooms[room_number].append(client)

    entering(username=data["username"], room_number=data["room_number"])

    # Создаём отдельный поток для клиента
    threading.Thread(target=handle_client, args=(client, data["room_number"]), daemon=True).start()
import tkinter as tk
import socket
import threading

UDP_MAX_SIZE = 65535


def listen(host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    members = []

    # Создаем графический интерфейс
    root = tk.Tk()
    root.title("Server")
    log_text = tk.Text(root, width=50, height=15)
    log_text.pack()

    # Отображаем сообщение о прослушивании порта
    log_text.insert(tk.END, f'Прослушивается {host}:{port}\n')

    def receive_messages():
        while True:
            msg, addr = s.recvfrom(UDP_MAX_SIZE)

            if addr not in members:
                members.append(addr)

            if not msg:
                continue

            client_id = addr[1]
            if msg.decode('utf-8') == "__подключился__к__чату__":
                log_text.insert(tk.END, f'Client{client_id} присоединился к чату\n')

            msg = f'client{client_id}: {msg.decode("utf-8")}'
            for member in members:
                if member == addr:
                    continue

                s.sendto(msg.encode('utf-8'), member)

            # Обновляем окно Tkinter для отображения новых сообщений
            root.update()

    threading.Thread(target=receive_messages, daemon=True).start()

    root.mainloop()


if __name__ == "__main__":
    listen()

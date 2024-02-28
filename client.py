import tkinter as tk
import threading
import socket

UDP_MAX_SIZE = 1024


def listen(s: socket.socket, text_widget: tk.Text):
    while True:
        msg = s.recv(UDP_MAX_SIZE)
        text_widget.insert(tk.END, msg.decode('utf-8') + '\n')
        text_widget.see(tk.END)  # Прокрутка вниз, чтобы видеть новые сообщения


def connect(host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, port))

    # Создание окна
    window = tk.Tk()
    window.title("Client")

    # Создание текстового виджета для отображения сообщений
    chat_history = tk.Text(window)
    chat_history.pack(expand=True, fill=tk.BOTH)

    def send_message():
        msg = message_entry.get()
        if msg:
            s.send(msg.encode('utf-8'))
            chat_history.insert(tk.END, 'you: ' + msg + '\n')
            message_entry.delete(0, tk.END)

    # Создание поля для ввода сообщений
    message_entry = tk.Entry(window)
    message_entry.pack(fill=tk.X)

    # Создание кнопки "Отправить"
    send_button = tk.Button(window, text="Отправить", command=send_message)
    send_button.pack()

    # Вывод приветствия
    chat_history.insert(tk.END, "Добро пожаловать в чат\n")

    threading.Thread(target=listen, args=(s, chat_history), daemon=True).start()

    s.send('__подключился__к__чату__'.encode('utf-8'))

    window.mainloop()


if __name__ == "__main__":
    connect()

import socket
from guizero import App, Text, TextBox, PushButton, Combo, info


# Создаем функцию сканера. В параметрах принимаем адрес хоста и список с портами
def scan_ports(host, ports):
    port_vidget.value = ""
    finish_vidget.value = ""
    host = host.value
    # Считаем колличество открытых портов
    p = 0
    # В цикле перебираем порты из списка
    for port in ports:
        # Создаем сокет
        s = socket.socket()
        # Ставим тайм-аут в одну cекунду
        s.settimeout(1)
        # Ловим ошибки
        try:
            # Пробуем соединиться, хост и порт передаем как список
            s.connect((host, port))
        # Если соединение вызвало ошибку
        except socket.error:
            # тогда ничего не делаем
            pass
        else:
            port_vidget.value += f"\n{port} port is active"
            # Закрываем соединение
            s.close()
            # Считаем колличество открытых портов
            p += 1
    finish_vidget.value = f"\n{host}: Active ports found: {p} \nThe scan is complete!"



# Принимаем список портов, ввденный пользователем
def input_porta():
    global one_port_list
    one_port_list.clear()
    # Ловим ошибки ввода. Если ввод не число - список ports остается пустым
    try:
        # преобразуем str в int(list)
        x = one_port.value.split()
        for i in x:
            one_port_list.append(int(i))
    except:
        try:
            # если пользователь ввел не int, удаляем элемент из list
            one_port_list.pop()
        except:
            pass
    # удаляем дубликаты из списка
    one_port_list = list(set(one_port_list))
    # вызываем функцию создания списка с полученными от пользователя портами
    create_ports_list(one_port_list)
    # Отправляем результат функции go на проверку функции scan_button
    scan_button_active()



# Создание списка портов
def create_ports_list(value):
    global ports
    ports.clear()
    ports += value



# Выбор из списка портов (GUI) (Пометка GUI в описании говорит что функция влияет на графический интерфейс)
def go():
    one_port.value = ""
    # изменения в GUI
    if ports_choise.value == "Standard ports":
        lable_00.hide()
        lable_01.show()
        one_port.enabled=False
        one_port.value = "80, 443...and more"
        # вызываем функцию создания списка с портами
        create_ports_list(ports_pop)
    elif ports_choise.value == "User input:":
        one_port.enabled=True
        lable_00.show()
        lable_01.hide()
        # вызываем функцию создания списка с портами
        one_port_list.clear()
        create_ports_list(one_port_list)
    else:
        one_port.enabled=False
    # Отправляем результат функции go на проверку функции scan_button
    scan_button_active()



# Активация кнопки Scan (GUI)
def scan_button_active():
    # Если поля host и port не пусты, то кнопка становится активна
    if host.value != "" and ports != []:
        scan_button.enabled=True
    else:
        scan_button.enabled=False
    #print(host.value, ports)


# About (GUI)
def about():
    info("info", "Created by Aleksan149 \n2022")

# Списки портов для сканирования
ports_pop = [20, 21, 22, 23, 25, 42, 43, 53, 67, 69, 80, 110, 115, 123, 137, 138, 139, 143, 161, 179, 443, 445, 514,
             515, 993, 995, 1080, 1194, 1433, 1702, 1723, 3128, 3268, 3306, 3389, 5432, 5060, 5900, 5938, 8080, 10000,
             20000]
one_port_list = []
ports = []

# Ставим список стандартных портов при запуске
create_ports_list(ports_pop)



# GUI
# Главное окно приложения с лейблами
app = App(title="Simple GUI Port Scanner", height=600)

# Лейбл
start_vidget = Text(app, text="SCAN THIS!", size=30, color="blue")

# Лейбл
ip_vidget = Text(app, text="\n\nEnter the IP or website address without http/https:", size=17)

# Поле ввода ip адреса цели
host = TextBox(app, width=20, command=scan_button_active)

# Лейбл
start2_vidget = Text(app, text=f"\nWhich ports will we scan?", size=17)

# Виджет выбора портов для сканирования
ports_choise = Combo(app, options=["Standard ports", "User input:"], height=1, width=15, command=go)

# Лейбл
lable_00 = Text(app, text="Enter one or more ports with a 'space'", visible=False, color="gray")

# Поле пользовательского ввода порта
one_port = TextBox(app, width=17, enabled=False, command=input_porta, text="80, 443...and more")

# Пустые лейблы для отступа
lable_01 = Text(app)
lable_02 = Text(app)

# Кнопка Scan
scan_button = PushButton(app, text="Scan", padx=20, pady=10, command=scan_ports, args=[host, ports], enabled=False)

# Лейбл открытых портов
port_vidget = Text(app)

# Лейбл итоговый
finish_vidget = Text(app)

# Кнопка инфо
info_butoon = PushButton(app, text="about", command=about, align="bottom", padx=3, pady=3)
info_butoon.text_color = "blue"

# Запуск GUI
app.display()

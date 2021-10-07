import socket
import select






massages = []
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8820))
client_sockets = []
server_socket.listen()
count = 0
turn_list = []
turn_i = 0
end = 1
first = 1
acpt = True
host = None
won_list = []
fin = False

while not fin:


    rlist, wlist, elist = select.select([server_socket] + client_sockets ,client_sockets,[])

    #check if stop accpeting clients and start the game


    for current_socket in rlist:
        if current_socket is server_socket and acpt:

            conn, addrres = server_socket.accept()
            print("new client has joined")
            client_sockets.append(conn)
            conn.send(("cl*" + str(count)).encode())
            if count == 0:
                host = conn
            turn_list.append(count)
            count += 1


        elif current_socket is host and acpt:


            data = host.recv(1024).decode()
            acpt = False
            massages.append((data, current_socket))



        elif not acpt:
            data = current_socket.recv(1024).decode()


            if data[:3] == "won":
                won_list[int(data.split('*')[1])] = 1
            else:
                massages.append((data, current_socket))

            if data == "exit":
                fin = True

    if not acpt and first == 0:
        end = 1
        for i in won_list:
            if i == 0:
                end = 0

        if end == 1:
            massages.append(("move/", None))

    for msg in massages:

        data, cl = msg

        for client in client_sockets:
            if client is not cl:

                client.send(data.encode())
        massages.remove(msg)




    if not acpt:
        if end == 1:
            first = 0
            turn = turn_list[turn_i]
            massages.append(("turn*" + str(turn) + '*', None))
            end = 0
            won_list = []
            for i in range(len(turn_list)):
                if i!= turn_i:
                    won_list.append(0)
                else:
                    won_list.append(1)
            turn_i = (turn_i + 1) % len(turn_list)


for client in client_sockets:
    client.close()

server_socket.close()





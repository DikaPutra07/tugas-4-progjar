import socket
import json
import base64
import logging

server_address=('0.0.0.0',6666)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False
    
def remote_upload(path="", name=""):
    with open(path, 'rb') as f:
        file_contents = f.read()
        encoded_contents = base64.b64encode(file_contents)
            
    command_str = f"UPLOAD {encoded_contents} {name}"
    hasil = send_command(command_str)
    
    if hasil.get('status') == 'OK':
        print(hasil)
        return True
    else:
        print(hasil)
        return False
    
def remote_delete(filename=""):
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("File berhasil dihapus")
        return True
    else:
        print(hasil)
        return False

if __name__=='__main__':
    server_address=('localhost',6666)
    remote_list()
    # remote_get('get_file_server.jpg')
    # remote_upload("donalbebek.jpg","bebek_server.jpg")
    remote_delete("bebek_server.jpg")
    remote_list()
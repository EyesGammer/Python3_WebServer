#!/bin/python3

import socket, sys, os, os.path, threading, re, functions, settings
from os import path

if __name__ == "__main__":
    global show, errors, predefined, files, functions_post, functions_get
    errors = settings.errors
    predefined = settings.predefined
    files = settings.files
    functions_post = functions.post_files
    functions_get = functions.get_files
    try:
        args = {element.split("=")[0]: element.split("=")[1] for element in sys.argv[1:]}
    except Exception:
        pass
    host = args.get("host") or args.get("h") or "localhost"
    port = args.get("port") or args.get("p") or "80"
    numa = args.get("accept") or args.get("a") or "5"
    show = args.get("show-requests") or args.get("sr") or "1"

class client_handle(threading.Thread):
    def __init__(self, connexion, informations):
        threading.Thread.__init__(self)
        self.connexion, self.informations = connexion, informations
    def run(self):
        packet = self.connexion.recv(2048)
        method, path, get_datas, post_datas = handle_packet(packet)
        returned = get_file(path)
        to_send = processing(returned)
        path = path.split("/")[-1] if path.split("/")[-1] != "" else "index.html"
        to_send = handle_method(method, path, get_datas, post_datas, to_send)
        self.connexion.sendall(to_send.encode("utf8"))
        self.connexion.close()

def dynamics_pages(file_path, dict_matchs={}):
    with open(file_path, "r") as file_read:
        file_content = file_read.read()
    to_replace = {element.group(): element.span() for element in re.finditer("{{\w+}}", file_content)}
    for key, item in dict_matchs.items():
        for key_file, item_file in to_replace.items():
            if "{{" + key + "}}" == key_file:
                file_content = file_content.replace(str(key_file), item)
    return file_content

def processing(returned):
    if type(returned) == str:
        use_file = returned.split("/")[-1]
        content = dynamics_pages(returned, files.get(use_file)) if type(files.get(use_file)) != type(None) else dynamics_pages(returned)
    elif type(returned) == tuple:
        file_path, files_list = returned
        content_list = ""
        for element in files_list[:-1]:
            content_list += f'<li><a href="{element}">{element}</a></li>'
        content = dynamics_pages(file_path, {"path": files_list[-1], "content": content_list})
    return content

def get_file(path_file):
    path_list = path_file.split("/")
    if "." in path_list[-1] and path_list[-1].count(".") == 1:
        if path.exists(path_file[1:]):
            return_file = path_file[1:]
        else:
            return_file = errors.get(404)
    elif len(path_list) == 2 and path_list[0] == '' and path_list[1] == '':
        return_file = predefined.get("index")
    else:
        try:
            directory_content = os.listdir(path_file[1:])
            directory_content.append(path_file)
            return_file = predefined.get("list-dir")
            return return_file, directory_content
        except FileNotFoundError:
            return_file = errors.get(404)
    return return_file

def method_identifier(packet):
    try:
        method = packet[:20].split(" ")[0]
        path = packet.split("\r\n")[0].split(" HTTP")[0].split(f"{method}")[1][1:]
        return method, path
    except ValueError:
        return "ERROR"

def get_post_datas(packet):
    datas = packet.split("\r\n\r\n")[-1].split("&")
    datas_unpack = {element.split("=")[0]: element.split("=")[-1] for element in datas}
    return datas_unpack, packet.split("\r\n\r\n")[-1]

def handle_method(method, path, get_datas, post_datas, returned):
    if method == "POST" and post_datas != "":
        returned = functions_post.get(path)(post_datas, returned)
        if get_datas != "":
            returned = functions_get.get(path)(get_datas, returned)
    if method == "GET" and get_datas != "":
        returned = functions_get.get(path)(get_datas, returned)
    return returned

def handle_packet(packet):
    packet = packet.decode("utf8")
    method, path = method_identifier(packet)
    additionnal, datas, post_printer = "", {}, ""
    if "?" in path:
        path, additionnal = path.split("?")
        additionnal = "?" + additionnal
    if method == "POST":
        datas, post_printer = get_post_datas(packet)
    if int(show):
        print(packet)
    else:
        print(f"\x1b[1;34m{method}\x1b[0m \x1b[1;32m{path}\x1b[0m\x1b[1;33m{additionnal}\x1b[0m \x1b[1;31m{post_printer}\x1b[0m")
    return method, path, additionnal, datas

def start_server(host, port, numa, show):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, int(port)))
    server.listen(int(numa))
    print(f"\x1b[1;36m--- Server started on {host}:{port} for {numa} clients ---\x1b[0m")
    try:
        while True:
            connexion, informations = server.accept()
            new_client = client_handle(connexion, informations)
            new_client.start()
        return
    except KeyboardInterrupt:
        server.close()
        print("\x1b[1;36m--- Server Stopped ---\x1b[0m")

start_server(host, port, numa, show)

import copy
import multiprocessing
# 시간을 나타내기 위해서 사용

from _thread import start_new_thread

from __configure.mubby_value import CLIENT, CLIENT_LIST, REQUEST_ADDR
from __function.default import *
from __utils.socket_module import Socket
from __utils.action_thread import action_thread


class RequestProcess(multiprocessing.Process):
    def __init__(self):
        super(RequestProcess, self).__init__()
        self.__request_process = None

    def run(self):
        self.__request_process = Handler()


class Handler:
    def __init__(self):
        self.__request_socket = Socket(REQUEST_ADDR).getting_server()

        print(" SERVER is running {}".format('-'*10))
        self.handler()

    def handler(self):
        primary_key = 1

        while self.__request_socket:
            # 00. Initialize a client_info
            client_info = copy.deepcopy(CLIENT)
            # 로그로 수정해야하는 부분
            print("-")
            try:
                # 01. First connect for setting request_socket_from_client
                request_socket_from_client, client_ip = self.__request_socket.accept()
                Socket.setting_socket_option(request_socket_from_client)

                # 02. Comparison a client_serial_number and DB_records
                #   - if the same : return primary key
                exist_in_a_db = False
                if not exist_in_a_db:
                    #       >> Add client information at DB
                    if primary_key == 1:
                        primary_key = 0
                    else:
                        primary_key = 1

                    if primary_key not in CLIENT_LIST:
                        #       >> Add a new client_info at CLIENT_LIST
                        client_info['request_socket_from_client'] = request_socket_from_client
                        client_info['folder_path'] = "__user_audio/" + "{}".format(primary_key) + "/"
                        # 방 주소를 ip로 하지 않고 primary key로 생성해야 할 것 같다.
                        make_user_dir(primary_key)
                        # print('client ip > {}'.format(primary_key))
                        # print('client_info ip > {}'.format(client_info['request_socket_from_client'].getpeername()[1]))

                        CLIENT_LIST[primary_key] = client_info
                    #   - else: insert it than return the primary key
                    else:
                        CLIENT_LIST[primary_key]['request_socket_from_client'] = request_socket_from_client

                # 03. Start thread
                start_new_thread(action_thread, (CLIENT_LIST[primary_key],))

            except Exception as e:
                self.__request_socket = None
                print('\t★ RequestProcess error >> {}'.format(e))

            finally:
                pass
                # HAVE TO SAVE A CLIENT_LIST VALUE
                # YOU CAN USE A "PICKLE" MODULE#
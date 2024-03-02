import socket

# TODO which port to use?
SERVER_PORT = 19132

def get_own_ip():
    """ Get own ip for network multiplayer """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('123.123.123.123', 1))
        IP = s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()
    return IP

def check_ip_running_server(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, SERVER_PORT))
    if result == 0:
        print ("Port is open")
    else:
        print("Port is closed")

    sock.close()
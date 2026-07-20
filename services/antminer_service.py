import socket
import json


def antminer_request(ip, command="summary", port=4028):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        sock.connect((ip, port))

        request = json.dumps({
            "command": command
        })

        sock.send(request.encode())

        response = sock.recv(4096)

        sock.close()

        return json.loads(response.decode())

    except Exception as e:
        return {
            "error": str(e)
        }


def get_summary(ip):
    return antminer_request(ip, "summary")


def get_stats(ip):
    return antminer_request(ip, "stats")


def get_pools(ip):
    return antminer_request(ip, "pools")


def get_antminer_status(ip):

    return {
        "summary": get_summary(ip),
        "stats": get_stats(ip),
        "pools": get_pools(ip)
    }

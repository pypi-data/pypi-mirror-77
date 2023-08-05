try:
    from pypsrp.client import Client
except Exception as err:
    from core.exception import AwdExceptions
    raise AwdExceptions(str(err))

def WinRmUpload(host, username, password, src_path, dst_path):
    try:
        client = Client(host, username=username, password=password, ssl=False, auth="ntlm")
        client.copy(src_path, dst_path)
        return True
    except Exception as e:
        return False

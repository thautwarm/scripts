# utility file
from bs4 import BeautifulSoup, Tag
from typing import Optional, Type
import socket
import socks
import ssl
import types
import io

Pending = object()


def async_apply(fn, arg, hang_on: Type[OSError] = BlockingIOError):
    _Pending = Pending
    while True:
        try:
            return fn(arg)
        except hang_on:
            yield _Pending


def async_socket_sendall(self: socket.socket, data, flags=0):
    """
    This is the async version implementation of SSLSocket.sendall.
    """
    self._checkClosed()

    count = 0

    if self._sslobj:
        if flags != 0:
            raise ValueError(
                "non-zero flags not allowed in calls to sendall() on %s" %
                self.__class__)

        send = self.send
    else:
        send = types.MethodType(socket.socket.send, self)

    with memoryview(data) as view, view.cast("B") as byte_view:
        amount = len(byte_view)
        while count < amount:
            v = yield from async_apply(send, byte_view[count:])
            count += v


def async_hand_shake(ssl_sock):
    count = 0
    while True:
        try:
            count += 1
            ssl_sock.do_handshake()
            break
        except ssl.SSLError:
            pass


def async_https_get(url, use_proxy=True, hand_shake_on_connect=False):
    if use_proxy and socks.socksocket is not socket.socket:
        socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1080)
        socket.socket = socks.socksocket

    _, _, host, path = url.split('/', 3)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 443))
    with ssl.wrap_socket(
            sock,
            keyfile=None,
            certfile=None,
            do_handshake_on_connect=hand_shake_on_connect,
            server_side=False,
            cert_reqs=ssl.CERT_NONE,
            ssl_version=ssl.PROTOCOL_SSLv23) as ssl_sock:
        host, path = map(str.encode, (host, path))
        request = b'GET /' + path + b' HTTP/1.0\r\nHost: ' + host + b'\r\n\r\n'
        if hand_shake_on_connect:
            ssl_sock.setblocking(False)
            async_hand_shake(ssl_sock)
            yield from async_socket_sendall(ssl_sock, request)
        else:
            ssl_sock.sendall(request)
            ssl_sock.setblocking(False)

        while True:
            received = yield from async_apply(
                ssl_sock.recv, 1024, hang_on=ssl.SSLError)
            if received:
                yield received
            else:
                break


class Section:
    def __init__(self, *_, **__):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def find_recent_tweets(name='bing'):
    _Pending = Pending
    with io.BytesIO() as ios:
        for produced in async_https_get(f'https://twitter.com/{name}'):
            if produced is _Pending:
                yield
            else:
                ios.write(produced)
        text = ios.getvalue()
        record: Optional[Tag] = BeautifulSoup(text).find(
            'div', attrs={'class': 'js-tweet-text-container'})

    if not record:
        return "<Twits no thing!>"

    return record.text

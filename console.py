import argparse

import qrcode

from local_net import get_local_ip


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor to VR")
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument("--play-from", help="Read the media from a file and sent it."),
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--verbose", "-v", action="count")
    return parser.parse_args()


def print_qr(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii()


def print_connection_information(ssl_context, args):
    url = "http://"
    if ssl_context:
        url = "https://"
    url = url + str(get_local_ip())
    url = url + f":{args.port}/"
    print(url)
    print_qr(url)

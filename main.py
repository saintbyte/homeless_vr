import asyncio
import json
import logging
import platform
import ssl

from aiohttp import web
from aiortc import RTCConfiguration
from aiortc import RTCPeerConnection
from aiortc import RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
from aiortc.contrib.media import MediaRelay

from console import channel_log
from console import parse_args
from console import print_connection_information
from constants import DATA_CHANNEL_NAME
from web_responses import index
from web_responses import javascript
from web_responses import style

relay = None
webcam = None
pcs = set()


def create_webcam_track():
    options = {"framerate": "25", "video_size": "640x480"}
    if platform.system() == "Darwin":
        webcam = MediaPlayer("default:none", format="avfoundation", options=options)
    elif platform.system() == "Windows":
        webcam = MediaPlayer("video=Integrated Camera", format="dshow", options=options)
    else:
        webcam = MediaPlayer("/dev/video2", format="v4l2", options=options)

    return webcam


def create_local_tracks():
    relay = MediaRelay()
    webcam = create_webcam_track()
    return None, relay.subscribe(webcam.video)


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection(configuration=RTCConfiguration(iceServers=[]))
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    audio, video = create_local_tracks()

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == "audio" and audio:
            pc.addTrack(audio)
        elif t.kind == "video" and video:
            pc.addTrack(video)
    # ---------
    channel = pc.createDataChannel(DATA_CHANNEL_NAME)
    channel_log(channel, "-", "created by local party")

    @channel.on("open")
    def on_open():
        channel_log(channel, "-", "OPEN CHANNEL")
        # asyncio.ensure_future(send_pings())

    @channel.on("message")
    def on_message(message):
        channel_log(channel, "<", message)

    # ---------
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


def get_ssl_context(args):
    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None
    return ssl_context


def set_logging_level(args):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def main():
    args = parse_args()
    set_logging_level(args)
    ssl_context = get_ssl_context(args)
    print_connection_information(ssl_context, args)
    app = web.Application()
    app.on_shutdown.append(on_shutdown)

    app.router.add_get("/client.js", javascript)
    app.router.add_get("/style.css", style)
    app.router.add_post("/offer", offer)
    app.router.add_get("/", index)
    web.run_app(app, host=args.host, port=args.port, ssl_context=ssl_context)


if __name__ == "__main__":
    main()

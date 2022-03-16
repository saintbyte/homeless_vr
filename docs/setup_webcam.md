## Настройка трансляции экран в linux
1.
```
sudo modprobe v4l2loopback
```
и в дев появлятся новый файл /dev/video2

2. проверяем
```
sudo v4l2-ctl -d /dev/video2 --all
```

```
Driver Info:
        Driver name      : v4l2 loopback
        Card type        : Dummy video device (0x0000)
        Bus info         : platform:v4l2loopback-000
        Driver version   : 5.13.19
        Capabilities     : 0x85208003
                Video Capture
                Video Output
                Video Memory-to-Memory
                Read/Write
                Streaming
                Extended Pix Format
                Device Capabilities
        Device Caps      : 0x05208003
                Video Capture
                Video Output
                Video Memory-to-Memory
                Read/Write
                Streaming
                Extended Pix Format
```

3. Стартуем вебку:
https://unix.stackexchange.com/questions/528400/how-can-i-stream-my-desktop-screen-to-dev-video1-as-a-fake-webcam-on-linux

```
ffmpeg -f x11grab -r 15 -s 1280x720 -i :0.0+0,0 -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video2
```

```
ffmpeg -f x11grab -r 15 -s 1366x768 -i :0.0+0,0 -vcodec rawvideo -pix_fmt yuvj422p -threads 0 -f v4l2 /dev/video2
```
```
sudo ffmpeg -f x11grab -r 30 -s 1365x766 -i :0.0 -vcodec rawvideo -fflags nobuffer,low_delay -framedrop -strict experimental -avioflags direct  -pix_fmt yuv420p -threads 0 -f v4l2 -vf 'scale=640x480' /dev/video2
```

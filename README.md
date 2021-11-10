# SimpleStreamer
This is a basic Flask app for streaming webcam which I'm using for Docker practice. Currently investigating how to pass the webcam to the container
from a Windows 10 machine.

### Build
```docker build -t python-streamer .```

### Run
Assuming Linux host machine:

```docker run -p 5700:5700 --device=/dev/video0:/dev/video2 python-streamer```

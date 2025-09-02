# How to get things to work on MacOS

## Setup instructions for MacOS


If you are using macOS you should be able to use docker directly on your host system. In many cases this works flawlessly as well. 
We routinely use docker on the latest macOS.

On the latest macOS:
* [Install Docker](https://www.docker.com)
* [Install XQuarz](https://www.xquartz.org)

__IMPORTANT:__ 
* In XQuarz, go to security settings and set both security options.
* In Docker, 
  * go to Settings --> Resources --> Network and enable host networking

Then, use 

```bash 
ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' 
``` 
to find your IP adress.

start a terminal and run
```bash
xhost +
```
This will start XQuarz, and it will open up your unix window system for world-wide access :-)

Make sure that XQuarz is running when starting your Docker container.

When you want to run your container, you need to mount the host’s X11 socket directory (/tmp/.X11-unix). 
Therefore, you need to use
```bash
  docker compose run --env="DISPLAY=10.0.1.15:0"  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" base
```
and replace 10.0.1.15 with your own IP adress. Note the ":0" after the ip-adress.

You can then open new terminals and attach to the currently running container from a different terminal using the command:
```bash
docker compose exec base bash
```
as explained on the main page.

* Special settings are needed when you are starting the FlexBE UI with the finite state machines. There you need to run in your docker shell:
```bash
export QT_QPA_PLATFORM=xcb          # normal X11 backend
export QT_QUICK_BACKEND=software    # Qt-Quick → raster, no OpenGL shaders
export LIBGL_ALWAYS_SOFTWARE=1      # force Mesa llvmpipe
ros2 run flexbe_webui webui_client
``` 



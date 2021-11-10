# bfs-camera-driver
Simple camera driver for Blackfly cameras from FLIR. Images are provided in the form of the publish-subscribe pattern.
(Tested with [Blackfly USB3 BFLY-U3-05S2C-CS](https://www.flir.de/products/blackfly-usb3/?model=BFLY-U3-05S2C-CS).)

## Usage-Docker
A docker file is provided for easy use of the camera-publisher.
* The docker file uses the calibration.ymal file for undistortion. Depending on the setup choose the right calibration data.
* Build DockerImage: sudo docker build ./ --tag  bfs-image-publisher
* Run DockerImage: sudo docker run -t --privileged -v /dqev/bus/usb:/dev/bus/usb -p 5557:5557 -p 5556:5556 bfs-image-publisher

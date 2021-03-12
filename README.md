# bfs-camera-driver
Simple camera driver for Blackfly cameras from FLIR. Images are provided in the form of the publish-subscribe pattern.
(Tested with [Blackfly USB3 BFLY-U3-05S2C-CS](https://www.flir.de/products/blackfly-usb3/?model=BFLY-U3-05S2C-CS).)

## Usage-Docker
A docker file is provided for easy use of the camera-publisher.
* Download the [Spinnaker SDK](https://meta.box.lenovo.com/v/link/view/a1995795ffba47dbbe45771477319cc3) in Version 2.2.0.48 to the Folder ./docker. 
  * spinnaker-2.2.0.48-Ubuntu20.04-amd64-pkg.tar.gz 
  * spinnaker_python-2.2.0.48-cp38-cp38-linux_x86_64.tar.gz
* Build DockerImage: sudo docker build ./ --tag  bfs-image-publisher
* Run DockerImage: sudo docker run -t --privileged -v /dqev/bus/usb:/dev/bus/usb -p 5557:5557 -p 5556:5556 bfs-image-publisher

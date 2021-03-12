#!/bin/bash

set -o errexit
#"$confirm" = "y"
echo "Installing Spinnaker packages..."
yes | sudo dpkg -i libspinnaker_*.deb || true
yes | sudo dpkg -i libspinnaker-dev_*.deb || true
yes | sudo dpkg -i libspinnaker-c_*.deb || true
yes | sudo dpkg -i libspinnaker-c-dev_*.deb || true
yes | sudo dpkg -i libspinvideo_*.deb || true
yes | sudo dpkg -i libspinvideo-dev_*.deb || true
yes | sudo dpkg -i libspinvideo-c_*.deb || true
yes | sudo dpkg -i libspinvideo-c-dev_*.deb || true
yes | sudo dpkg -i spinview-qt_*.deb || true
yes | sudo dpkg -i spinview-qt-dev_*.deb || true
yes | sudo dpkg -i spinupdate_*.deb || true
yes | sudo dpkg -i spinupdate-dev_*.deb || true
yes | sudo dpkg -i spinnaker_*.deb || true
yes | sudo dpkg -i spinnaker-doc_*.deb || true
yes | sudo dpkg -i libgentl_*.deb || true


#sudo sh configure_spinnaker.sh
sudo sh configure_usbfs.sh
sudo sh configure_spinnaker_paths.sh
ARCH=$(ls libspinnaker_* | grep -oP '[0-9]_\K.*(?=.deb)' || [[ $? == 1 ]])
if [ "$ARCH" = "amd64" ]; then
    BITS=64
elif [ "$ARCH" = "i386" ]; then
    BITS=32
fi
if [ -z "$BITS" ]; then
    echo "Could not automatically add the FLIR GenTL Producer to the GenTL environment variable."
    echo "To use the FLIR GenTL Producer, please follow the GenTL Setup notes in the included README."
else
    echo "Launching GenTL path configuration script..."
    sudo sh configure_gentl_paths.sh $BITS
fi
exit 0

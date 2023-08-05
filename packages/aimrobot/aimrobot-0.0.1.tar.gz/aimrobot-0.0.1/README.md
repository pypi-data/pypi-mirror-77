# AIM.Robot

AIM.Robot is a Python library to run Robotic Assembly Digital Model (RADM) files directly on Universal Robots.

## Requirements

 - Universal Robot (tested on a UR5e and UR10e).
 - Python 3.8 or newer
 - A valid RADM file

## Installation

The easiest way to install AIM.Robot is using pip:

    pip install aimrobot

## Getting Started

First of all, you need to test the connection to the robot:

    aimrobot --networktest 192.168.1.1

If the connection is established, you can load and run a RADM file:

    aimrobot --file runme.radm
  
 This will execute all the steps using the wait time  set in the file. If you want to have manual control, you can add the flag --manual
 

    aimrobot --file runme.radm --manual
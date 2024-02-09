# Home Assistant configuration


## The key software I run is

* [Home Assistant](https://home-assistant.io/)
* [Docker-CE](https://docs.docker.com/get-docker/) for all containers
* [nginx](https://nginx.org/en/) to provide remote access, in conjunction with [Let's Encrypt](https://letsencrypt.org/) via [Linuxserver/SWAG](https://hub.docker.com/r/linuxserver/swag/)
* [Mosquitto](https://hub.docker.com/_/eclipse-mosquitto) for the MQTT broker
* [MariaDB](https://hub.docker.com/_/mariadb) for the database
* [Zigbee2MQTT](https://hub.docker.com/r/koenkk/zigbee2mqtt/) for communicating with my Zigbee Mesh
* [InfluxDB](https://hub.docker.com/_/influxdb) for recording time-series history
* [Grafana](https://hub.docker.com/r/grafana/grafana/) for displaying InfluxDB data



* [Debian13](https://www.debian.org/) for my primary storage and containers\vms
* [Debian13](https://www.debian.org) for my secondary backup and container host

* [OPNSense](https://opnsense.org/) for routing and firewalling


## My experiences

* Repairing computers since 1993
* Started building computers in 1995
* Started working with Linux in 1997
* Played around with routing and networking since 1998
* Got into Windows system administration in 2004
* Moved on to Enterprise consulting on storage, *nix, networking and more in 2007
* Trained electronic repairs technician, enjoys building stuff and repairing stuff
* No higher education, currently having fun doing certifications on whim 
  * N+ 
  * VMWare VCP-DCV 5-5.5-6-6.5-7-2022 
  * VMware VCP-NV 2021
  * VMware VCAP-DCV Deploy+Design 2023
  * SUSE Linux Administrator 
  * ITILv3 
  * AWS Pracitioner 
  * Azure AZ900+SC900+MS900+AZ800
  * HPE ASE Compute+Storage
  * HPE VTP Hybrid Solutions
  * Certified Kubernetes Administrator
  * CCNA 2023
  * Aruba ACSA + ACNSA

## Does and don'ts
* Does not want to run Home Assistant OS as I find the software limiting, as such I run in native docker
* I don't trust mDNS, and I think it is a shitty protocol, as such I create DNS entries for all my network devices and use hostnames whenever possible to access services (OPNsense also creates DNS entries dynamically for all DHCP clients)
* I find discovery a bad idea, if I had no intention of adding it to Home Assistant, I shouldn't be using a discovery service
* If there is no value in my professional life from running a software, I see no point in running it, as such I mostly run software that I gain knowledge I can use in my worklife from (i.e Docker, ESXi, etc)


## Hardware

* 104 and counting Zigbee devices (needs updating)
  * 4 Xiaomi Door and Window Sensors
  * 3 Xiaomi Movement sensors
  * 2 Xiaomi Double Wireless Switches
  * 4 Xiaomi Single mini button
  * 2 Xiaomi Magic Cube
  * 1 IKEA On Off Switch
  * 1 IKEA RGB E27 Bulb
  * 9 IKEA E14 Bulbs
  * 5 IKEA CT E14 Bulbs
  * 19 IKEA CT GU10 Bulbs
  * 8 IKEA CT E27 Bulbs
  * 1 Gledopto RGBWW Controller
  * 1 Gledopto RGBCCT Controller
  * 2 Philips Hue E14 Mingion Bulbs
  * 3 Philips Hue E27 Bulbs
  * 1 Philips Hue Filament E27 Bulb
  * 3 Philips Hue Wireless Dimmer Switches
* 4 ESPhome self built devices
  * Garage Door opener
  * Greenhouse Monitor
  * Soil Moisture Sensor
  * Sonoff Bridge with hack implemented
* 3 Tasmota OTA flashed devices
  * Tumbledrier power monitor
  * Greenhouse heating power monitor
  * Garage rack power monitor
* 2 Yeelight WiFi RGB E27 Bulbs
* 1 Yeelight WiFi RGB Led Strip
* Xiaomi Roborock S5
* 2x WebOS TV
* Samsung Smart Exclusive Heat Pump
* Broadlink RM3 Mini controlling a older Samsung Plasma, Yamaha Reciever, Toshiba Heat Pump, Sanyo Heat Pump

* Production servers \ systems
  * DL380 Gen9 (24 cores \ 128GB RAM \ 2x 10G \ Tesla P4)
  * Mini-ITX server running Debian
  * HPE Edgeline 300 running OPNSense
  * Cisco 2970 as core
  * Aruba 2530 POE as distribution switch
  * Cheap $20 POE Cameras from Aliexpress

* Lab servers \ switches
  * 5x DL380 Gen8 (24 cores \ 384GB RAM \ 4x 10G)
  * RX4640
  * RX3600
  * C3000 with BL860c, BL460c G7 and DS2000
  * 2x HPE Edgeline 1000
  * 2x HPE 5900AF
  * 1x Procurve 1800

## Todos

* Actually finishing my daughters lightning lamp, started out as a Arduino project with sound detection and IR, then I discovered HA, wanted to make it smart, and here we are today, current plan is to integrate with WWLN and make it reactive to when lightning is nearby
* Get my IoT greenhouse operational, started with a wifi relay board that controlled fans and relays last year, that borked, currently building v2 with ESP32, soil moisture sensors and bigger solenoid valves 

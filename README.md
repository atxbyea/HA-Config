# Home Assistant configuration


## The key software I run is

* [Home Assistant](https://home-assistant.io/)
* [nginx](https://nginx.org/en/) to provide remote access, in conjunction with [Let's Encrypt](https://letsencrypt.org/) via [Linuxserver/SWAG](https://hub.docker.com/r/linuxserver/swag/)
* [Mosquitto](https://hub.docker.com/_/eclipse-mosquitto) for the MQTT broker
* [MariaDB](https://hub.docker.com/_/mariadb) for the database
* [Zigbee2MQTT](https://hub.docker.com/r/koenkk/zigbee2mqtt/) for communicating with my Zigbee Mesh
* [InfluxDB](https://hub.docker.com/_/influxdb) for recording time-series history
* [Grafana](https://hub.docker.com/r/grafana/grafana/) for displaying InfluxDB data
* [Node-RED](https://hub.docker.com/r/nodered/node-red) for testing
* [Debian11.2](https://www.debian.org/) for my primary storage and containers\vms
* [Debian11.2](https://www.debian.org) for my secondary backup and container host
* [Docker-CE](https://docs.docker.com/get-docker/) for all containers
* [OPNSense](https://opnsense.org/) for routing and firewalling


## My experiences

* Repairing computers since 1993
* Started building computers in 1995
* Started working with Linux in 1997
* Played around with routing and networking since 1998
* Got into Windows system administration in 2004
* Moved on to Enterprise consulting on storage, *nix, networking and more in 2007
* Trained electronic repairs technician, enjoys building stuff and repairing stuff
* No higher education, certified N+, VMWare VCP 5-5.5-6-6.5, VMware VCP-NV 2021, SUSE Linux Administrator, ITILv3, AWS Pracitioner, Azure AZ900+SC900

## Does and don'ts
* Does not want to run Home Assistant OS as I find the software limiting, as such I run in native docker
* I don't trust mDNS, and I think it is a shitty protocol, as such I create DNS entries for all my network devices and use hostnames whenever possible to access services (OPNsense also creates DNS entries dynamically for all DHCP clients)
* I find discovery a bad idea, if I had no intention of adding it to Home Assistant, I shouldn't be using a discovery service
* If there is no value in my professional life from running a software, I see no point in running it, as such I mostly run software that I gain knowledge I can use in my worklife from (i.e Docker, ESXi, etc)


## Hardware

* 85 and counting Zigbee devices (needs updating)
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
* 5 433MHz temperature sensors
  * Deep freezer sensor
  * Outdoor temp sensor
  * Indoor Living Room sensor
  * Greenhouse temperature sensor backup
  * Secondary outdoor sensor I seem to be picking up from somewhere
* 2 Yeelight WiFi RGB E27 Bulbs
* 1 Yeelight WiFi RGB Led Strip
* Xiaomi Roborock S5
* WebOS TV
* Samsung Smart Exclusive Heat Pump
* Broadlink RM3 Mini controlling a older Samsung Plasma, Yamaha Reciever, Toshiba Heat Pump, Sanyo Heat Pump
* DELL R510 running Debian with ZFS and docker + KVM
* Mini-ITX server running Debian
* HPE Edgeline 300 running OPNSense
* Cisco 2970 as core
* Aruba 2530 POE as distribution switch
* Cheap $20 POE Cameras from Aliexpress


## Todos

* Actually finishing my daughters lightning lamp, started out as a Arduino project with sound detection and IR, then I discovered HA, wanted to make it smart, and here we are today, current plan is to integrate with WWLN and make it reactive to when lightning is nearby
* Get my IoT greenhouse operational, started with a wifi relay board that controlled fans and relays last year, that borked, currently building v2 with ESP32, soil moisture sensors and bigger solenoid valves 

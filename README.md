# Home Assistant configuration
This is my current configuration for Home Assistant

![Setup](https://github.com/atxbyea/HA-Config/blob/master/images/Setup-1.png)

## The key software I run is

* [Home Assistant](https://home-assistant.io/)
* [nginx](https://nginx.org/en/) to provide remote access, in conjunction with [Let's Encrypt](https://letsencrypt.org/)
* [Mosquitto](https://mosquitto.org/) for the MQTT broker
* MariaDB for the database
* [Zigbee2MQTT](https://www.zigbee2mqtt.io/) for communicating with my Zigbee Mesh
* [Zigbee2MQTTAssistant](https://github.com/yllibed/Zigbee2MqttAssistant) for initiating updates of Zigbee devices
* InfluxDB for recording time-series history
* Grafana for displaying InfluxDB data
* Letsencrypt container with nginx as a proxy server
* Node-RED for testing
* FreeNAS 11.3U2 for my primary storage and jails
* OpenSUSE Tumbleweed for my docker host
* Docker-CE for all containers
* OPNSense for routing and firewalling


## My experiences

* Repairing computers since 1993
* Started building computers in 1995
* Started working with Linux in 1997
* Played around with routing and networking since 1998
* Got into Windows system administration in 2004
* Moved on to Enterprise consulting on storage, *nix, networking and more in 2007
* Trained electronic repairs technician, enjoys building stuff and repairing stuff
* No higher education

## Does and don'ts
* Does not want to run Home Assistant Supervised as I find the software limiting, as such I run in venv (and part of the time docker)
* I don't trust mDNS, and I think it is a shitty protocol, as such I create DNS entries for all my network devices and use hostnames whenever possible to access services
* I find discovery a bad idea, if I had no intention of adding it to Home Assistant, I shouldn't be using a discovery service
* If there is no value in my professional life from running a software, I see no point in running it, as such I mostly run software that I gain knowledge I can use in my worklife from (i.e Docker, ESXi, etc)


## Hardware

* 85 and counting Zigbee devices
* 4 ESPhome self built devices
* 3 Tasmota OTA flashed devices
* 5 433MHz temperature sensors
* Xiaomi Roborock S5
* WebOS TV
* Onkyo Reciever
* Samsung Smart Exclusive Heat Pump
* Broadlink RM3 Mini controlling a older Samsung Plasma, Yamaha Reciever, Toshiba Heat Pump
* DELL R510 running Freenas
* Mini-ITX server running OpenSuSE Tumbleweed
* Mini-computer from Aliexpress running OPNSense
* Pair of HPE 5900AF 40G switches in core
* Aruba 2530 POE and distribution swithces
* Cheap $20 POE Cameras


## Todos

* Actually finishing my daughters lightning lamp, started out as a Arduino project with sound detection and IR, then I discovered HA, wanted to make it smart, and here we are today, current plan is to integrate with WWLN and make it reactive to when lightning is nearby
* Get my IoT greenhouse operational, started with a wifi relay board that controlled fans and relays last year, that borked, currently building v2 with ESP32, soil moisture sensors and bigger solenoid valves 

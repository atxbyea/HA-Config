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

#!/bin/bash
echo "pushing charms to nexus"
curl -v -u admin:admin123 --upload-file /charms/amf-operator/amf_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/amf_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/mongodb-operator/mongodb_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/mongodb_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/nrf-operator/nrf_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/nrf_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/pcf-operator/pcf_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/pcf_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/udm-operator/udm_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/udm_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/ausf-operator/ausf_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/ausf_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/smf-operator/smf_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/smf_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/udr-operator/udr_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/udr_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/upf1-operator/upf1_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/upf1_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/webui-operator/webui_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/webui_ubuntu-20.04-amd64.charm;
curl -v -u admin:admin123 --upload-file /charms/natapp-operator/natapp_ubuntu-20.04-amd64.charm http://18.221.164.72:6081/repository/5g/charms/natapp_ubuntu-20.04-amd64.charm;
echo " Now pushing images to Nexus";

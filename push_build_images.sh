#!/bin/bash
echo "Free5gc Images Tag"
docker tag localhost:32000/free5gc-natapp:1.0 18.221.164.72:6083/repository/osm/free5gc-natapp:1.0;
docker tag localhost:32000/free5gc-webui:1.0 18.221.164.72:6083/repository/osm/free5gc-webui:1.0;
docker tag localhost:32000/free5gc-udr:1.0 18.221.164.72:6083/repository/osm/free5gc-udr:1.0;
docker tag localhost:32000/free5gc-udm:1.0 18.221.164.72:6083/repository/osm/free5gc-udm:1.0;
docker tag localhost:32000/free5gc-smf:1.0 18.221.164.72:6083/repository/osm/free5gc-smf:1.0;
docker tag localhost:32000/free5gc-pcf:1.0 18.221.164.72:6083/repository/osm/free5gc-pcf:1.0;
docker tag localhost:32000/free5gc-nssf:1.0 18.221.164.72:6083/repository/osm/free5gc-nssf:1.0;
docker tag localhost:32000/free5gc-ausf:1.0 18.221.164.72:6083/repository/osm/free5gc-ausf:1.0;
docker tag localhost:32000/free5gc-amf:1.0 18.221.164.72:6083/repository/osm/free5gc-amf:1.0;
docker tag localhost:32000/free5gc-nrf:1.0 18.221.164.72:6083/repository/osm/free5gc-nrf:1.0;
docker tag localhost:32000/free5gc-mongo:1.0 18.221.164.72:6083/repository/osm/free5gc-mongo:1.0;
docker tag localhost:32000/free5gc-upf-1:1.0 18.221.164.72:6083/repository/osm/free5gc-upf-1:1.0;
echo "Image Taging Done";
echo "Pushing Docker Images To Nexus";
docker push 18.221.164.72:6083/repository/osm/free5gc-natapp:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-webui:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-udr:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-udm:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-smf:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-pcf:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-nssf:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-ausf:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-amf:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-nrf:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-mongo:1.0;
docker push 18.221.164.72:6083/repository/osm/free5gc-upf-1:1.0;
echo "Images Push To Nexus";

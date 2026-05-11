sudo adduser --gecos "" --disabled-password splunk
cd /opt
sudo tar -xzf splunkforwarder-8.2.6.1.tgz
sudo /opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --seed-passwd 29jclpbp


sudo /opt/splunkforwarder/bin/splunk stop
sudo chown -R splunk:splunk /opt/splunkforwarder/
sudo /opt/splunkforwarder/bin/splunk enable boot-start  -user splunk


sudo sed -i 's|"/opt/splunkforwarder/bin/splunk" start --no-prompt --answer-yes|su - ${USER} -c '\''"/opt/splunkforwarder/bin/splunk" start --no-prompt --answer-yes'\''|g' /etc/init.d/splunk
sudo sed -i 's|"/opt/splunkforwarder/bin/splunk" stop|su - ${USER} -c '\''"/opt/splunkforwarder/bin/splunk" stop'\''|g' /etc/init.d/splunk
sudo sed -i 's|"/opt/splunkforwarder/bin/splunk" restart|su - ${USER} -c '\''"/opt/splunkforwarder/bin/splunk" stop'\''|g' /etc/init.d/splunk
sudo sed -i 's|"/opt/splunkforwarder/bin/splunk" status|su - ${USER} -c '\''"/opt/splunkforwarder/bin/splunk" stop'\''|g' /etc/init.d/splunk

sudo systemctl daemon-reload

cd /tmp
unzip --qq Configurations-Base.zip

sudo cp -r Configurations-Base/org_all_deploymentclient /opt/splunkforwarder/etc/apps
sudo mv /opt/splunkforwarder/etc/apps/org_all_deploymentclient /opt/splunkforwarder/etc/apps/ap3_all_deploymentclient

sudo sed -i 's|targetUri = deploymentserver\.splunk\.mycompany\.com:8089|targetUri = xx.xx.xxx.xxx:8089|g' /opt/splunkforwarder/etc/apps/ap3_all_deploymentclient/local/deploymentclient.conf
sudo chown -R splunk:splunk /opt/splunkforwarder/
sudo chown -R splunk:splunk  /tmp/Configurations-Base/
sudo service splunk start
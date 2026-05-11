sudo adduser --gecos "" --disabled-password splunk
sudo mkdir /opt/splunkdata
sudo chown -R splunk:splunk /opt/splunkdata/
cd /opt
sudo tar -xzf splunk-8.2.6.1.tgz
sudo /opt/splunk/bin/splunk start --accept-license --answer-yes --seed-passwd 29jclpbp


sudo /opt/splunk/bin/splunk stop
sudo chown -R splunk:splunk /opt/splunk/
sudo /opt/splunk/bin/splunk enable boot-start  -user splunk


sudo sed -i 's|"/opt/splunk/bin/splunk" start --no-prompt --answer-yes|su - ${USER} -c '\''"/opt/splunk/bin/splunk" start --no-prompt --answer-yes'\''|g' /etc/init.d/splunk
sudo sed -i 's|"/opt/splunk/bin/splunk" stop|su - ${USER} -c '\''"/opt/splunk/bin/splunk" stop'\''|g' /etc/init.d/splunk
sudo sed -i 's|"/opt/splunk/bin/splunk" restart|su - ${USER} -c '\''"/opt/splunk/bin/splunk" stop'\''|g' /etc/init.d/splunk
sudo sed -i 's|"/opt/splunk/bin/splunk" status|su - ${USER} -c '\''"/opt/splunk/bin/splunk" stop'\''|g' /etc/init.d/splunk

sudo systemctl daemon-reload

cd /tmp
unzip --qq Configurations-Base.zip

sudo cp -r Configurations-Base/org_all_deploymentclient /opt/splunk/etc/apps
sudo mv /opt/splunk/etc/apps/org_all_deploymentclient /opt/splunk/etc/apps/ap3_all_deploymentclient

sudo sed -i 's|targetUri = deploymentserver\.splunk\.mycompany\.com:8089|targetUri = xx.xx.xxx.xxx:8089|g' /opt/splunk/etc/apps/ap3_all_deploymentclient/local/deploymentclient.conf

sudo cp -r Configurations-Base/org_all_indexer_base /opt/splunk/etc/apps
sudo mv /opt/splunk/etc/apps/org_all_indexer_base /opt/splunk/etc/apps/ap3_all_indexer_base


sudo chown -R splunk:splunk /opt/splunk/
sudo chown -R splunk:splunk  /tmp/Configurations-Base/
sudo service splunk start

sudo -H -u splunk /opt/splunk/bin/splunk display listen
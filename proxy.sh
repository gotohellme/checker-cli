#!/bin/bash

wget https://raw.githubusercontent.com/serverok/squid-proxy-installer/master/squid3-install.sh -O squid3-install.sh
sudo bash squid3-install.sh

mkdir /etc/squid
# Add a user for the proxy (replace 'h3h3' and 'h3h3' with your desired username and password)
sudo htpasswd -bc /etc/squid/passwords h3h3 h3h3

# # Backup the original Squid configuration file
sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.bak

# Create a new Squid configuration file with your settings
cat <<EOL | sudo tee /etc/squid/squid.conf
auth_param basic program /usr/lib/squid3/basic_ncsa_auth /etc/squid/passwords
auth_param basic realm proxy
acl authenticated proxy_auth REQUIRED
http_access allow authenticated
http_port 3128
EOL

# Enable Squid to start on boot
sudo systemctl restart squid
sudo systemctl reload squid

# Allow incoming traffic on port 587 (TCP and UDP)
sudo ufw allow 587/tcp -y
sudo ufw allow 587/udp -y

# Print proxy information
echo "Proxy is http://h3h3:h3h3@$(hostname -I | awk '{print $1}'):3128"

echo "Squid proxy installation and configuration completed."

export DEBIAN_FRONTEND=noninteractive

echo "Set Time Zone"
timedatectl set-timezone America/Los_Angeles

echo "Add Ubuntu Dependencies"
apt-get update
apt-get upgrade -y
xargs apt-get install -y < /vagrant/project.d/requirements-dev.txt

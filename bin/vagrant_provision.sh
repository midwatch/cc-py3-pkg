export DEBIAN_FRONTEND=noninteractive

echo "Set Time Zone"
timedatectl set-timezone America/Los_Angeles

echo "Add Ubuntu Dependencies"
apt-get update
apt-get upgrade -y
apt-get install -y build-essential \
                   git \
                   git-flow \
                   tig

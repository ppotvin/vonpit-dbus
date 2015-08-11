# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/vivid64"

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y dbus-x11 python3.4-venv
    echo export PATH=/vagrant/test-scripts:\\$PATH >> /home/vagrant/.bashrc
  SHELL
end

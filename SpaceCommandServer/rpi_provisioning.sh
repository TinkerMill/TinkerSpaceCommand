#!/bin/bash

ARG1=${1:-no_args_passed}

apt-get update

apt-get install -y git

apt-get install -y emacs

apt-get install -y mongodb python3-pymongo

if [ $ARG1 = "install_vim" ]
then
	apt-get install -y vim

	# Configure vim
	echo "----------- Install Pathogen -----------"
	mkdir /home/pi/.vim/
	mkdir /home/pi/.vim/autoload/
	mkdir /home/pi/.vim/bundle/
	# Fix CURL certifications path
  export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
	curl -LSso /home/pi/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

	echo "---------------- Install Nerdtree ----------"
	# Install Nerdtree
	git clone https://github.com/scrooloose/nerdtree.git /home/pi/.vim/bundle/nerdtree

	echo "--------- Install Vundle --------"
  echo "--------- Launch vim and run :PluginInstall to finish the install -----------"
	# Install Vundle
	git clone https://github.com/VundleVim/Vundle.vim.git /home/pi/.vim/bundle/Vundle.vim


	echo "---------- Copy vimrc to home directory --------"
	cp "$PWD/provisioning_files/vimrc" /home/pi/.vimrc

  # Install coloschemes
  echo "----------- Download colorschemes for vim -----------------"
  echo " Vundle manages colorscheme, run :PluginInstall when first starting vim to load "
  
  # Add a line to .bashrc to enable 256 color in terminal
  
  echo -e "\n#Enable 256 color in terminal\nexport TERM=xterm-256color" >> /home/pi/.bashrc # sets up terminal so advanced colorschemes will work


fi




# -------------- Python ------------------------
echo "---------- Install Python Packages -------------"
pip3 install --upgrade pip
pip3 install zeroconf
pip3 install paho-mqtt
pip3 install pyyaml
pip3 install rx
pip3 install flask
pip3 install flask-cors
pip3 install influxdb


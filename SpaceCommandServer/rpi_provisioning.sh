#!/bin/bash

ARG1=${1:-no_args_passed}

#apt-get update

#apt-get install -y git


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
	git clone https://github.com/scrooloose/nerdtree.git /home/pi/.vim/bundle

	echo "--------- Install Vundle --------"
  echo "--------- Launch vim and run :PluginInstall to finish the install -----------"
	# Install Vundle
	git clone https://github.com/VundleVim/Vundle.vim.git /home/pi/.vim/bundle/Vundle.vim


	echo "---------- Copy vimrc to home directory --------"
	cp "$PWD/provisioning_files/vimrc" /home/pi/.vimrc
fi


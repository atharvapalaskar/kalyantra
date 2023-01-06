#! /usr/bin/env bash

#startup audio 
espeak -a 140 -g 10 "Powered On, Initializing"

#executing with pyenv python3.11
/home/atharvap/.pyenv/versions/3.11.1/bin/python3 --version
/home/atharvap/.pyenv/versions/3.11.1/bin/python3 /home/atharvap/Proj/kalyantra/pyserver/thebot/app.py
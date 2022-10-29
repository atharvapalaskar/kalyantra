#! /usr/bin/env bash

#startup audio 
espeak -a 140 -g 10 "Powered On, Initializing"

#IMP*: comment out below if you're going to use kalyantrast.service

#Give pi a bit time to setup after boot
sleep 5
 
#Path to main index file
espeak -a 100 "starting server"

node /home/atharvap/Proj/kalyantra/server/main/index.js

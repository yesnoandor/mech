#!/bin/bash

mkdir -p ./mech-II/release/log
~/anaconda3/bin/python3 py2so.py  mech-II
cp ./mech-II/main.py ./mech-II/release/
cp -rf ./mech-II/res ./mech-II/release/


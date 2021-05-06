#!/bin/sh

cd $HOME
python3 clear-term.py --term 2021-1

cd $HOME/my-klas-gatling
./gradlew clean gatlingRun

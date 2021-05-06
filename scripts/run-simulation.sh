#!/bin/sh

cd $HOME
python3 init-data.py --clear --create-students --term 2021-1

cp registrations.csv my-klas-gatling/src/gatling/resources/

cd $HOME/my-klas-gatling
./gradlew clean gatlingRun

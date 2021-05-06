#!/bin/sh

cd $HOME
python3 init-data.py --clear --create-students --term 2018-1
cp registrations.csv my-klas-gatling/src/gatling/resources/
cd $HOME/my-klas-gatling
./gradlew clean gatlingRun

cd $HOME
python3 init-data.py --term 2018-2
cp registrations.csv my-klas-gatling/src/gatling/resources/
cd $HOME/my-klas-gatling
./gradlew clean gatlingRun

cd $HOME
python3 init-data.py --term 2019-1
cp registrations.csv my-klas-gatling/src/gatling/resources/
cd $HOME/my-klas-gatling
./gradlew clean gatlingRun

cd $HOME
python3 init-data.py --term 2019-2
cp registrations.csv my-klas-gatling/src/gatling/resources/
cd $HOME/my-klas-gatling
./gradlew clean gatlingRun

cd $HOME
python3 init-data.py --term 2020-1
cp registrations.csv my-klas-gatling/src/gatling/resources/
cd $HOME/my-klas-gatling
./gradlew clean gatlingRun

cd $HOME
python3 init-data.py --term 2020-2
cp registrations.csv my-klas-gatling/src/gatling/resources/
cd $HOME/my-klas-gatling
./gradlew clean gatlingRun

cd $HOME
python3 init-data.py --term 2021-1
cp registrations.csv my-klas-gatling/src/gatling/resources/

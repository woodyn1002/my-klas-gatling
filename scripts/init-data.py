import requests
import logging
import math
import random
import json
import csv
import time
import argparse

BASE_URI = 'http://15.165.226.60:8080'
NUM_STUDENTS = 2000
NUM_LECTURES = 1200
NUM_POPULAR_LECTURES = 10
NUM_LECTURES_PER_STUDENT = 6

requestLogger = logging.getLogger("request")
mainLogger = logging.getLogger("main")

def request(method, path, headers=None, body=None, check_status=True):
    global BASE_URI
    global requestLogger

    requestLogger.info(f"sending {method} {path}:")
    with requests.Session() as session:
        res = session.request(method=method, url=BASE_URI + path, json=body, headers=headers)
        requestLogger.info(f"response={{ status={res.status_code}, body={res.text} }}")

        if check_status:
            res.raise_for_status()
    
        try:
            return res.json()
        except json.decoder.JSONDecodeError:
            return None

def random_student_number():
    return str(random.randrange(2012, 2022)) + str(random.randrange(1, 1000000)).zfill(6)

def random_lecture_number(level):
    return str(random.randrange(1, 10)) + f'000-{level}-' + str(random.randrange(1, 10000)).zfill(4) + '-' + str(random.randrange(1, 10)).zfill(2)

def random_term():
    return str(random.randrange(2017, 2022)) + '-' + str(random.randrange(1, 3))

def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Init data')
    parser.add_argument('--clear', action='store_true')
    parser.add_argument('--create-students', action='store_true')
    parser.add_argument('--term')

    args = parser.parse_args()

    logging.info("waiting for server...")
    while True:
        try:
            requests.request(method='GET', url=BASE_URI + '/')
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    logging.info("..connected!")
    
    if args.clear:
        request('POST', '/admin/clear')

    studentIds = []

    if args.create_students:
        for i in range(NUM_STUDENTS):
            student = request('POST', '/students', body={ 'studentNumber': random_student_number()})
            studentIds.append(student['id'])
    else:
        students = request('GET', '/students')
        for student in students:
            studentIds.append(student['id'])
    
    lectureIds = []
    for i in range(NUM_LECTURES):
        level = i
        lecture = request('POST', '/lectures', body={
            'lectureNumber': random_lecture_number(level=level),
            'term': args.term,
            'name': f"test-{str(i)}",
            'subject': f"test-{str(i)}",
            'level': level,
            'credit': 3,
            'capacity': 10,
            'schedules': []})
        lectureIds.append(lecture['id'])

    popLectureIds = lectureIds[:NUM_POPULAR_LECTURES]

    with open('registrations.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["studentId", "lectureIds"]) # Header

        for studentId in studentIds:
            registLectureIds = []
            if NUM_POPULAR_LECTURES > 0 and random.random() < 0.5:
                registLectureIds.append(random.choice(popLectureIds))
            
            while len(registLectureIds) < NUM_LECTURES_PER_STUDENT:
                registLectureIds.append(random.choice(lectureIds))

            mainLogger.info(f"student #{str(studentId)} will register: {', '.join(str(id) for id in registLectureIds)}")
            spamwriter.writerow([str(studentId), ' '.join(str(id) for id in registLectureIds)])

    mainLogger.info("-" * 10)
    mainLogger.info("Initialization has been completed!")
    mainLogger.info(f"- inserted {NUM_STUDENTS} students")
    mainLogger.info(f"- inserted {NUM_LECTURES} lectures")
    mainLogger.info(f"- {NUM_POPULAR_LECTURES} popular lectures: {', '.join(str(id) for id in popLectureIds)}")
    mainLogger.info(f"- wrote registrations.csv (each students will register {NUM_LECTURES_PER_STUDENT} lectures)")
    mainLogger.info("-" * 10)

if __name__ == '__main__':
    main()

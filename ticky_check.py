#!/usr/bin/env python3
import csv
import re
import operator

with open("syslog.log", "r") as file:
    errors = {}
    for line in file.readlines():
        result = re.search(r"(ERROR|INFO) (\w.+) ", line)
        check = result.group(1)
        error = result.group(2)
        if check == "ERROR":
            if error not in errors:
                errors[error] = [1]
            else:
                errors[error][0] += 1
        else:
            pass

sorted_error = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)

with open('error_message.csv', "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Error", "Count"])
for log in sorted_error:
    key, value = log
    with open('error_message.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([key, value[0]])

with open("syslog.log", "r") as file:
    per_user = {}
    for line in file.readlines():
        result = re.search(r": (INFO|ERROR) .+\((\w+.*)\)", line)
        type_ = result.group(1)
        user = result.group(2)
        if user not in per_user:
            per_user[user] = [0, 0]
            if type_ == "ERROR":
                per_user[user][0] += 1
            else:
                per_user[user][1] += 1
        else:
            if type_ == "ERROR":
                per_user[user][0] += 1
            else:
                per_user[user][1] += 1

sorted_puser = sorted(per_user.items())

with open('user_statistics.csv', "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Username", "INFO", "ERROR"])
for log in sorted_puser:
    key, value = log
    with open('user_statistics.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([key, value[0], value[1]])

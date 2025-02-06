import json
import csv
import datetime
import time
import random
import os

while True:
    input_data = csv.DictReader(open('sample_data.csv'))
    flag = 0
    temp = 0

    for line in input_data:
        # Ingest data to Kinesis Firehose in 0 ~ 1 second
        temp += 1
        if(temp % 100 == 0):
            flag += 1

        time.sleep(random.random())

        dt = datetime.datetime.now()
        timestamp = dt.isoformat()

        raw_data = {}
        raw_data.update(line)

        # Add current time to source data
        raw_data['OccurenceTime'] = timestamp
        raw_data['Row ID'] = int(raw_data['Row ID'])
        raw_data['Postal Code'] = int(raw_data['Postal Code'])
        raw_data['Sales'] = float(raw_data['Sales'])
        raw_data['Quantity'] = int(raw_data['Quantity'])
        raw_data['Discount'] = float(raw_data['Discount'])
        raw_data['Profit'] = float(raw_data['Profit'])

        # Write json file to /tmp/anhyobin-analytics-log/
        filename = '/tmp/clickstream-log/' + str(flag) + '_clickstream.json'
        with open(filename, 'a') as logFile:
            json.dump(raw_data, logFile)
            # Kinesis Agent parsed from each file based on \n
            logFile.write('\n')
            os.chmod(filename, 0o777)

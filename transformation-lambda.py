import base64

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8')

        # Replace 'Ship Mode' to 'Shipping Option'
        new_payload = payload.replace('Ship Mode', 'Shipping Option')
        print(new_payload)

        # Record Payload
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(new_payload.encode('utf-8')).decode('utf-8')
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))
    return {'records': output}

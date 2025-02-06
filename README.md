
## 1. EC2 로그가 저장될 디렉토리 설정

```
mkdir /tmp/clickstream-log
chmod 777 /tmp/clickstream-log
```

## 2. CSV 파일 (`sample_data.csv`) 다운로드 혹은 복사

curl이나 wget을 이용하여, `Download raw file` 버튼에서 주어지는 링크를 이용해서 다운로드

## 3. 클릭스트림 생성기 Python 스크립트 (`clickstream-generator.py`) 실행

`sample_data.csv`와 같은 디렉토리에 위치해 있어야 하며, 실행 후 아무런 output도 나오지 않으나, `/tmp/clickstream-log` 디렉토리로 이동하면 파일이 생성되고 있음을 확인할 수 있음

## 4. Amazon Linux에 aws-kinesis-agent를 설치

```
yum install aws-kinesis-agent
```

[참고](https://docs.aws.amazon.com/ko_kr/firehose/latest/dev/download-install.html)

## 5. Firehose 스트림 생성

소스는 Direct PUT

## 6. aws-kinesis-agent 환경설정 및 서비스 실행

`/etc/aws-kinesis/agent.json` 파일을 다음과 같이 수정

```
{
  "cloudwatch.emitMetrics": true,
  "kinesis.endpoint": "",
  "firehose.endpoint": "firehose.<리전>.amazonaws.com",
  "flows": [
    {
      "filePattern": "/tmp/clickstream-log/*.json",
      "deliveryStream": "<Firehose 스트림 이름>"
    }
  ]
}
```

`sudo service aws-kinesis-agent start`로 서비스 실행하며, 로그는 `/var/log/aws-kinesis-agent/aws-kinesis-agent.log`에서 확인 가능

## 7. EC2에 IAM 역할 부여

클릭스트림이 생성되는 EC2에 IAM 역할이 없다면, aws-kinesis-agent는 권한 에러를 발생시킴. 
따라서 다음 사용자 정의 정책을 추가한 후, 이를 활용하는 역할을 추가해야 함

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "firehose:*",
                "logs:*",
                "sns:*",
                "cloudwatch:*",
                "kinesis:*"
            ],
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Condition": {
                "StringLike": {
                    "iam:AWSServiceName": "events.amazonaws.com"
                }
            },
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "arn:aws:iam::*:role/aws-service-role/events.amazonaws.com/AWSServiceRoleForCloudWatchEvents*",
            "Effect": "Allow"
        }
    ]
}
```

새 역할을 추가할 때, 신뢰 대상은 EC2로 설정

## 8. aws-kinesis-agent 다시 실행

다음과 같은 로그가 확인되면, Destination (s3 bucket)에 파일이 생성되어있는 것을 확인할 수 있음.

```
2025-02-06 01:59:23.802+0000  (FileTailer[fh:my-streaming-processor:/tmp/clickstream-log/*.json].MetricsEmitter RUNNING) com.amazon.kinesis.streaming.agent.tailing.FileTailer [INFO] FileTailer[fh:my-streaming-processor:/tmp/clickstream-log/*.json]: Tailer Progress: Tailer has parsed 3158 records (1728214 bytes), transformed 0 records, skipped 0 records, and has successfully sent 3148 records to destination.
```

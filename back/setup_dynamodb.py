import boto3


def create_table():
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url="http://localhost:8000",
        region_name='us-west-2',
        aws_access_key_id='dummyAccessKeyId',
        aws_secret_access_key='dummySecretAccessKey'
    )

    table = dynamodb.create_table(
        TableName='Tasks',
        KeySchema=[
            {
                'AttributeName': 'task_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'task_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName='Tasks')
    print("Table created successfully.")


create_table()

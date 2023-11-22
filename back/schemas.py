import datetime
import uuid
import graphene
from graphql_models import StatusEnum, Task
import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://localhost:8000",
    region_name='us-west-2',
    aws_access_key_id='dummyAccessKeyId',
    aws_secret_access_key='dummySecretAccessKey'
)


def get_dynamodb_table():
    return dynamodb.Table('Tasks')


class Query(graphene.ObjectType):
    tasks = graphene.List(Task, status=StatusEnum())
    task = graphene.Field(Task, id=graphene.ID(required=True))

    def resolve_tasks(self, info, status=None):
        table = get_dynamodb_table()
        if status:
            response = table.query(
                IndexName='StatusIndex',
                KeyConditionExpression=Key('status').eq(status)
            )
        else:
            # Fetch all tasks
            response = table.scan()

        tasks = []
        for item in response.get('Items', []):
            tasks.append(Task(
                id=item.get('task_id'),
                title=item.get('title'),
                description=item.get('description'),
                status=item.get('status'),
                created_at=item.get('created_at'),
                updated_at=item.get('updated_at')
            ))

        return tasks

    def resolve_task(self, info, id):
        table = get_dynamodb_table()
        response = table.get_item(
            Key={'task_id': id}
        )
        item = response.get('Item')
        if not item:
            return None

        return Task(
            id=item.get('task_id'),
            title=item.get('title'),
            description=item.get('description'),
            status=item.get('status'),
            created_at=item.get('created_at'),
            updated_at=item.get('updated_at')
        )


class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()

    task = graphene.Field(Task)

    def mutate(self, info, title, description=None):
        current_time = datetime.datetime.utcnow()
        task_id = str(uuid.uuid4())

        table = dynamodb.Table('Tasks')

        # Item structure
        item = {
            'task_id': task_id,
            'title': title,
            'description': description if description else '',
            'status': 'TO DO',
            'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat()
        }

        table.put_item(Item=item)

        return CreateTask(task=Task(
            id=task_id,
            title=title,
            description=description,
            status='TO DO',
            created_at=current_time,
            updated_at=current_time
        ))


class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        status = graphene.Argument(StatusEnum)

    task = graphene.Field(Task)

    def mutate(self, info, id, title=None, description=None, status=None):
        table = dynamodb.Table('Tasks')

        # Update expression components
        update_expression = []
        expression_attribute_values = {}

        if title:
            update_expression.append("title = :t")
            expression_attribute_values[':t'] = title
        if description:
            update_expression.append("description = :d")
            expression_attribute_values[':d'] = description
        if status:
            update_expression.append("status = :s")
            expression_attribute_values[':s'] = status

        update_expression_str = "SET " + ", ".join(update_expression)

        response = table.update_item(
            Key={'task_id': id},
            UpdateExpression=update_expression_str,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )

        updated_attributes = response.get('Attributes', {})

        return UpdateTask(task=Task(
            id=id,
            title=updated_attributes.get('title', ''),
            description=updated_attributes.get('description', ''),
            status=updated_attributes.get('status', ''),
            created_at=updated_attributes.get('created_at', ''),
            updated_at=updated_attributes.get('updated_at', '')
        ))


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

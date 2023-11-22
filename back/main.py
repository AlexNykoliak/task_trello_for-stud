import datetime
import uuid
from fastapi import FastAPI
from models import TaskCreate, TaskUpdate
import boto3
from starlette_graphene3 import GraphQLApp
from fastapi import Depends
from fastapi import FastAPI, Request
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from schemas import schema
from schemas import schema

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://localhost:8000",
    region_name='us-west-2',
    aws_access_key_id='dummyAccessKeyId',
    aws_secret_access_key='dummySecretAccessKey'
)


def get_dynamodb_table():
    return dynamodb.Table('Tasks')


app = FastAPI()


@app.route("/graphql", methods=["GET", "POST"])
async def graphql(request: Request):
    if request.method == "GET":
        return make_graphiql_handler()(request)
    elif request.method == "POST":
        app = GraphQLApp(schema=schema)
        return await app.handle_graphql(request=request)


@app.post("/tasks/")
async def create_task(task: TaskCreate, table=Depends(get_dynamodb_table)):
    current_time = datetime.datetime.utcnow().isoformat()
    task_id = str(uuid.uuid4())
    print("Generated task_id:", task_id)

    response = table.put_item(
        Item={
            'task_id': task_id,
            'title': task.title,
            'description': task.description,
            'status': 'TO DO',
            'created_at': current_time,
            'updated_at': current_time
        }
    )
    print("DynamoDB response:", response)
    return {"task_id": task_id, **task.dict()}


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: TaskUpdate, table=Depends(get_dynamodb_table)):
    update_expression = "SET "
    expression_attribute_values = {}
    expression_attribute_names = {}

    if task.title is not None:
        update_expression += "#title = :title, "
        expression_attribute_values[':title'] = task.title
        expression_attribute_names['#title'] = 'title'

    if task.description is not None:
        update_expression += "#description = :description, "
        expression_attribute_values[':description'] = task.description
        expression_attribute_names['#description'] = 'description'

    if task.status is not None:
        update_expression += "#status = :status, "
        expression_attribute_values[':status'] = task.status
        expression_attribute_names['#status'] = 'status'

    update_expression = update_expression.rstrip(", ")

    response = table.update_item(
        Key={'task_id': task_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names,
        ReturnValues="UPDATED_NEW"
    )
    return response


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, table=Depends(get_dynamodb_table)):
    response = table.delete_item(
        Key={'task_id': task_id}
    )
    return response

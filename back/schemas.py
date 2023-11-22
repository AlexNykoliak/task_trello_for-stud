import datetime
import uuid
import graphene
from graphql_models import StatusEnum, Task


class Query(graphene.ObjectType):
    tasks = graphene.List(Task, status=StatusEnum())
    task = graphene.Field(Task, id=graphene.ID(required=True))

    def resolve_tasks(self, info, status=None):
        pass

    def resolve_task(self, info, id):
        pass


class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()

    task = graphene.Field(Task)

    def mutate(self, info, title, description=None):
        current_time = datetime.datetime.utcnow()
        new_task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            status="TO DO",
            created_at=current_time,
            updated_at=current_time
        )
        return CreateTask(task=new_task)


class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        status = graphene.Argument(StatusEnum)

    task = graphene.Field(Task)

    def mutate(self, info, id, title=None, description=None, status=None):
        pass


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

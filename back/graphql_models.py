import graphene
from datetime import datetime


class StatusEnum(graphene.Enum):
    TO_DO = "TO DO"
    IN_PROGRESS = "IN PROGRESS"
    DONE = "DONE"


class Task(graphene.ObjectType):
    id = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String()
    status = graphene.Field(StatusEnum)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

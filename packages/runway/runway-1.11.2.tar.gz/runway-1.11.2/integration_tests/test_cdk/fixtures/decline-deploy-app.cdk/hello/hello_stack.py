from aws_cdk import aws_iam as iam
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
from aws_cdk import aws_sqs as sqs
from aws_cdk import core

from .hello_construct import HelloConstruct


class MyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hello = HelloConstruct(self, "MyHelloConstruct", num_buckets=1)
        user = iam.User(self, "MyUser")
        hello.grant_read(user)

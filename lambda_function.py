# -*- coding: utf-8 -*-

import datetime

import boto3
from slacker import Slacker

SLACK_API_TOKEN = '(your api token)'
SLACK_CHANNEL = '(any channel or user)'


def lambda_handler(event, context):
    message = "Currenct balance: `$%s` " % (billing_amount_this_month())

    slack = Slacker(SLACK_API_TOKEN)
    slack.chat.post_message(
        SLACK_CHANNEL, message,
        username='AWS Bill Collector',
        icon_emoji=':money_with_wings:')


def billing_amount_this_month():
    start_date = datetime.datetime.today() - datetime.timedelta(days=1)
    end_date = datetime.datetime.today()

    return billing_amount(start_date, end_date)


def billing_amount(start_date, end_date):
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        MetricName='EstimatedCharges',
        Namespace='AWS/Billing',
        Period=86400,
        StartTime=start_date,
        EndTime=end_date,
        Statistics=['Maximum'],
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
            }
        ]
    )

    return response['Datapoints'][0]['Maximum']

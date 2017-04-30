import sys
import os

import botocore
from boto3 import session
from bush import color


def create_session(options):
    # Bush looks for credentials this order.
    #   1. Environment variables
    #   2. AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    #   3. ~/.aws/credentials with profile
    #   4. ~/.aws/credentials with default profile
    access_key = os.environ.get('AWS_ACCESS_KEY_ID') or options.access_key
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY') or options.secret_key
    params = {}
    if options.region:
        params['region_name'] = options.region

    if access_key and secret_key:
        params['aws_access_key_id'] = access_key
        params['aws_secret_access_key'] = secret_key

    if options.profile:
        params['profile_name'] = options.profile

    try:
        return session.Session(**params)
    except botocore.exceptions.ProfileNotFound as error:
        print(color.red(error))
        sys.exit(2)

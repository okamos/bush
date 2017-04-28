from optparse import OptionParser
from boto3 import session

import __init__
import os
import botocore
import color


parser = OptionParser()

parser.add_option("-p", "--profile",
                  action="store", type="string", dest="profile",
                  help="Use a specific profile from your credential file")
parser.add_option("--access_key_id",
                  action="store", type="string", dest="access_key",
                  help="Use a specific AWS_ACCESS_KEY_ID")
parser.add_option("--secret_key",
                  action="store", type="string", dest="secret_key",
                  help="Use a specific AWS_SECRET_ACCESS_KEY")
parser.add_option("-r", "--region",
                  action="store", type="string", dest="region",
                  help="Use a specific region")
parser.add_option("-v", "--version",
                  action="store_true", dest="version",
                  help="Display version")

(options, args) = parser.parse_args()

if options.version:
    print(__init__.__version__)

# Bush looks for credentials this order.
#   1. Environment variables
#   2. AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
#   3. ~/.aws/credentials with profile
#   4. ~/.aws/credentials with default profile
access_key = os.environ.get('AWS_ACCESS_KEY_ID') or options.access_key
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY') or options.secret_key
if access_key and secret_key:
    session.Session(aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key)
elif options.profile:
    try:
        session.Session(profile_name=options.profile)
    except botocore.exceptions.ProfileNotFound as error:
        print(color.red(error))
else:
    session.Session(profile_name=options.profile)

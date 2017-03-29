#!/usr/bin/python26

import sys
from os.path import dirname, abspath
import time
import boto
from boto.ec2.regioninfo import RegionInfo

sys.path.insert(0, abspath(dirname(__file__)) + '/../../libs')
from common.aws import get_aws_env

aws_env = get_aws_env()
AWS_ACCCESS_KEY = aws_env.key
AWS_SECRET_KEY = aws_env.secret
REGION_ENDPOINT = 'ec2.ap-northeast-1.amazonaws.com'

inst_dict = {
            "mugicha":["i-xxxxxxxxxxxx", "111.222.333.444"], 
            "milktea":["i-xxxxxxxxxxxx", "555.666.777.888"]
          }

region = RegionInfo(endpoint=REGION_ENDPOINT)
ec2 = boto.connect_ec2(AWS_ACCCESS_KEY, AWS_SECRET_KEY,region=region)

for k, v in inst_dict.items():
    version = k
    instance_id = v[0]
    eip = v[1]
    inst = ec2.get_all_instances(instance_id)[0].instances[0]
    if inst.state != 'stopped':
       print('The %s is already starting.' % version)

    else:
        try:
            inst.start()
            print('Start %s. Please wait until running.' % version)
        
            while True:
              inst.update() 
              if inst.state == "running":
                break
              else:
                pass
        
            ec2.associate_address(instance_id=instance_id, public_ip=eip)
            print('Associated EIP to the %s.' % version)
    
        except ValueError:
            print ('Error!!')

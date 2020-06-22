import tempfile
from datetime import datetime as dt
from Enumeration.setting import AWS, SLACK
from Enumeration.core.util import push_slack, temp_file
from Enumeration.core.lib import AwsScanner
from Enumeration.core.db import SubDomainData


def _commit(domain, subdomains:list, errors:list, logger):
    DB = SubDomainData(domain)
    DB.insert_domains(subdomains)
    new_sub = DB.new_sub

    # slack update
    msg = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "domain: `{}`\nnew_count: `{}`\n total_count: `{}`\n".format(domain, len(new_sub), len(subdomains))
                }
            }
        ]
    
    # Upload file with new domain to s3
    if len(new_sub) > 0 and AWS['upload']:
        file_name = "{}_{}.txt".format(domain, str(dt.timestamp(dt.now())))
        aws_up = AwsScanner(AWS['upload_bucket'], False)
        aws_up.file_to_upload = temp_file(new_sub)
        aws_up.upload(file_name)
        msg.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "https://{}.s3.amazonaws.com/{}".format(AWS['upload_bucket'], file_name)
                }
            })
        logger.info('{} - File uploaded to s3-bucket Name: {}'.format(domain, file_name))
        

    if len(errors) > 0:
        msg.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join([err for err in errors])
                }
            })

    # Pushing updates to slack
    push_slack(SLACK['report_hook'], msg, domain)
    logger.info('{} - Enumeration job finished'.format(domain))
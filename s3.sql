select
	title,
	region,
	bucket_policy_is_public 
from 
aws_s3_bucket
group by title,region,bucket_policy_is_public

#/usr/local/bin/steampipe query "select i.instance_id,i.region,i.title,i.vpc_id,i.subnet_id,s.tags ->> 'Name' as subnet_name from aws_ec2_instance as i, aws_vpc_subnet as s where i.subnet_id = s.subnet_id order by vpc_id,subnet_id,title;" --search-path=$1 --output=csv
/usr/local/bin/steampipe query "select region,name as title,vpc_id,'' as subnet_id, '' as subnet_name from aws_ec2_application_load_balancer" --search-path=$1 --output=csv
#/usr/local/bin/steampipe query "select i.region,i.title,i.vpc_id,i.subnet_id,s.tags ->> 'Name' as subnet_name from aws_ec2_instance as i, aws_vpc_subnet as s where i.subnet_id = s.subnet_id and i.instance_state = 'running' and i.title like 'BK%' order by vpc_id,subnet_id,title;" --search-path=$1 --output=csv

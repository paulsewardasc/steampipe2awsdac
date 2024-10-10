select
	region,
  db_instance_identifier as title,
	engine,
  sub ->> 'SubnetIdentifier' as subnet_id,
	vpc_id
from
  aws_rds_db_instance
  cross join jsonb_array_elements(subnets) as sub
group by region,db_instance_identifier,engine,sub ->> 'SubnetIdentifier', vpc_id;

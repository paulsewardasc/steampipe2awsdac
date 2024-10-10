with aws_ec2_instances as (
  select title,
    instance_id,
    region,
    account_id,
    arn
  from
    aws_ec2_instance ),
aws_ec2_target_groups as (
  select
    target_health_descriptions,
    load_balancer_arns
  from
    aws_ec2_target_group ),
aws_ec2_application_load_balancers as (
  select
    arn, title
  from
    aws_ec2_application_load_balancer )
select lb.title as alb_title, region, i.instance_id as ec2_instance_id
from
  aws_ec2_instances as i,
  aws_ec2_target_groups as target,
  jsonb_array_elements(target.target_health_descriptions) as health_descriptions,
  jsonb_array_elements_text(target.load_balancer_arns) as l,
  aws_ec2_application_load_balancers as lb
where
  health_descriptions -> 'Target' ->> 'Id' = i.instance_id
  and l = lb.arn
group by lb.title, region, i.instance_id;

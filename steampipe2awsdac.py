import csv
import json
import sys
import re
import os

def getfname(filename,ftype):
  base_directory = '.'
  base = os.path.abspath(base_directory)
  fname = os.path.abspath(os.path.join(base_directory, f'{filename}-{ftype}.csv'))
  fname = os.path.normpath(os.path.join(base_directory, fname))
  if fname.startswith(base):
    return(fname)
  else:
    print('[-] An attempt to circumvent secruity has been made, exiting...')
    sys.exit()

def process_csv(filename):
    data = {}
    data_alb = {}
    subnet = {}
    ec2 = {}

    fname = getfname(filename,'main')
    with open(fname, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            instance_id = row['instance_id']
            region = row['region']
            state = row['instance_state']
            instance_type = row['instance_type']
            vpc_id = f'{row["region"]}-{row["vpc_id"]}'
            subnet_id = row['subnet_id']
            subnet_name = row['subnet_name']
            title = row['title']
            title = title.replace(' ','_')
            if instance_id not in ec2:
              ec2[instance_id] = {'title': title, 'state': state, 'instance_type': instance_type}
            if region not in data:
                data[region] = {'Type': 'AWS::Region', 'Children': []}
            if vpc_id not in data:
                data[vpc_id] = {'Type': 'AWS::EC2::VPC', 'Children': []}
            if subnet_id not in data:
                data[subnet_id] = {'Type': 'AWS::EC2::Subnet', 'Children': []}

            if subnet_id not in subnet:
              subnet[subnet_id] = subnet_name

            if vpc_id not in data[region]['Children']:
              data[region]['Children'].append(vpc_id)
            if subnet_id not in data[vpc_id]['Children']:
              data[vpc_id]['Children'].append(subnet_id)
            if instance_id not in data[subnet_id]['Children']:
              data[subnet_id]['Children'].append(instance_id)
            data[instance_id] = {'Type': 'AWS::EC2::Instance'}

    # Read in ALB file for reference
    try:
      fname = getfname(filename,'alb')
      with open(fname, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
          region = row['region']
          vpc_id = f'{row["region"]}-{row["vpc_id"]}'
          subnet_id = row['subnet_id']
          subnet_name = row['subnet_name']
          title = row['title']
          if region not in data:
            data[region] = {'Type': 'AWS::Region', 'Children': []}
          if vpc_id not in data:
            data[vpc_id] = {'Type': 'AWS::EC2::VPC', 'Children': []}
          if title not in data[vpc_id]['Children']:
            data[vpc_id]['Children'].append(title)
          data[title] = {'Type': 'AWS::ElasticLoadBalancingV2::LoadBalancer'}
    except Exception as e:
      print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
      sys.exit()

    # Read in RDS file for reference
    try:
      fname = getfname(filename,'rds')
      with open(fname, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
          region = row['region']
          vpc_id = f'{row["region"]}-{row["vpc_id"]}'
          subnet_id = row['subnet_id']
          engine = row['engine']
          title = row['title']
          title = f'{title} / {engine}'
          if region not in data:
            data[region] = {'Type': 'AWS::Region', 'Children': []}
          if vpc_id not in data:
            data[vpc_id] = {'Type': 'AWS::EC2::VPC', 'Children': []}
          if title not in data[vpc_id]['Children']:
            data[vpc_id]['Children'].append(title)
          data[title] = {'Type': 'AWS::RDS::DBInstance'}
    except Exception as e:
      print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
      sys.exit()

    # Read in S3 file for reference
    try:
      fname = getfname(filename,'s3')
      with open(fname, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
          region = row['region']
          title = row['title']
          public = row['bucket_policy_is_public']
          if public == 'true':
            title = f'{title} - PUBLIC'
          if region not in data:
            data[region] = {'Type': 'AWS::Region', 'Children': []}
          if title not in data[region]['Children']:
            data[region]['Children'].append(title)
          data[title] = {'Type': 'AWS::S3::Bucket'}
    except Exception as e:
      print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
      sys.exit()

    #print(json.dumps(data, indent=2))
    #sys.exit()

    # Read in ALB Links
    links = {}
    try:
      fname = getfname(filename,'alb-links')
      with open(fname, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
          source = row['alb_title']
          target = row['ec2_instance_id']
          if source not in links:
            links[source] = {'Targets': [target]}
          else:
            links[source]['Targets'].append(target)
    except Exception as e:
      print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
      sys.exit()

#    print(json.dumps(data, indent=2))
#    sys.exit()

    # Output the data in the desired format
    print('Diagram:')
    print('  DefinitionFiles:')
    print('    - Type: URL')
    print('      Url: "https://raw.githubusercontent.com/awslabs/diagram-as-code/main/definitions/definition-for-aws-icons-light.yaml"')

    print('  Resources:')
    print('    Canvas:')
    print('      Type: AWS::Diagram::Canvas')
    print('      Direction: vertical')
    print('      Align: left')
    print('      Children:')
    print('        - AWSCloud')
    print('    AWSCloud:')
    print('      Type: AWS::Diagram::Cloud')
    print('      Direction: vertical')
    print(f'      Title: {mainTitle}')
    print('      Align: left')
    print('      Preset: AWSCloudNoLogo')
    print('      Children:')
    print('        - Regions')
    print('    Regions:')
    print('      Type: AWS::Diagram::VerticalStack')
    print('      Children:')
    for key, value in data.items():
      if "Region" in value['Type']:
        print(f'        - {key}')
    for key, value in data.items():
        if 'AWS::EC2::Instance' in value['Type']:
          fillcolor = "rgba(0,0,0,0)"
          title = ec2[key]['title']
          instance_type = ec2[key]['instance_type']
          if ec2[key]['state'] == 'stopped':
            fillcolor = "rgba(255,115,166,75)"
        else:
          title = key
        print(f"    {key}:")
        if 'Region' in value['Type']:
          print('      Direction: vertical')
          print('      Align: center')
        if 'VPC' in value['Type']:
          print('      Direction: left')
        if 'Subnet' in value['Type']:
          print('      Direction: horizontal')
        for k, v in value.items():
            if k == 'Children':
                print(f"      {k}:")
                for child in v:
                    print(f"        - {child}")
            else:
                print(f"      {k}: {v}")
                if 'VPC' in value['Type']:
                  title = re.sub('.*?vpc', 'vpc', title)
                if 'Subnet' in value['Type']:
                  title = f'{title} / {subnet[title]}'
                if 'AWS::EC2::Instance' in value['Type']:
                  print(f"      Title: {title} / {instance_type}")
                  print(f"      FillColor: {fillcolor}") 
                else:
                  print(f"      Title: {title}")
    print('  Links:')
    for source, v in links.items():
      source = source.replace(' ','_')
      #print(f'source: {source}, v: {v}')
      for target in v['Targets']:
        target = target.replace(' ','_')
        print(f'    - Source: {source}')
        print(f'      SourcePosition: N')
        print(f'      Target: {target}')
        print(f'      TargetPosition: S')
        print(f'      TargetArrowHead:')
        print(f'        Type: Open')


def get_csv_filename():
  """
  Reads the command line parameter and returns it as the CSV filename,
  or defaults to "ec2.csv" if no parameter is provided.

  Returns:
      str: The CSV filename.
  """
  if len(sys.argv) > 1:
      csv_file = sys.argv[1]
  else:
      csv_file = "ec2.csv"
  return csv_file

if __name__ == "__main__":
    csv_file = get_csv_filename()
    mainTitle = csv_file
    mainTitle = mainTitle.replace('awsdac-','')
    process_csv(csv_file)

#!/bin/bash

step1() {
  # commands for step 1
  echo "Executing step EC2..."
	./make_awsdac.sh $acc > awsdac-$acc-main.csv
}

step2() {
  # commands for step 2
  echo "Executing step ALB..."
	./make_awsdac_alb.sh $acc > awsdac-$acc-alb.csv
}

step3() {
  # commands for step 3
  echo "Executing step ALB Links..."
	./make_awsdac_alb_links.sh $acc > awsdac-$acc-alb-links.csv
}

step4() {
  # commands for step 4
  echo "Executing step RDS..."
	./make_awsdac_rds.sh $acc > awsdac-$acc-rds.csv
}

step5() {
  # commands for step 5
  echo "Executing step S3..."
	./make_awsdac_s3.sh $acc > awsdac-$acc-s3.csv
}

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <step_number> [<step_number> ...] or $0 all"
  exit 1
fi

if [[ "$1" == "all" ]]; then
  step1
  step2
  step3
  step4
  step5
else
  for i in "$@"; do
    case "$i" in
      1) step1 ;;
      2) step2 ;;
      3) step3 ;;
      4) step4 ;;
      5) step5 ;;
      *) echo "Invalid step number: $i" ;;
    esac
  done
fi


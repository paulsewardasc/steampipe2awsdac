  i=$1
  echo $i
	./make_awsdac.sh $i > awsdac-$i.csv
	./make_awsdac_alb.sh $i > awsdac-$i-alb.csv
	./make_awsdac_alb_links.sh $i > awsdac-$i-alb-links.csv




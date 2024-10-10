  i=$1
  echo $i
	echo "[+] Step 1"
	./make_awsdac.sh $i > awsdac-$i.csv
	echo "[+] Step 2"
	./make_awsdac_alb.sh $i > awsdac-$i-alb.csv
	echo "[+] Step 3"
	./make_awsdac_alb_links.sh $i > awsdac-$i-alb-links.csv
	echo "[+] Step 4"
	./make_awsdac_rds.sh $i > awsdac-$i-rds.csv




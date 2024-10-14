cd ~/awsdac
for i in $(ls -1 *main.csv | perl -pe 's{-main.csv}{}')                                       
do
  python steampipe2awsdac.py $i > $i.yaml; awsdac $i.yaml -o $i.png
done

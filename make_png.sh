cd ~/awsdac
for i in $(ls -1 *main.csv | perl -pe 's{-main.csv}{}')                                       
do
  python ec2s_to_dac.py $i > $i.yaml; awsdac $i.yaml -o $i.png
done

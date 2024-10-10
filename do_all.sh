for i in $(cat ~/.steampipe/config/aws.spc | grep "^connection" | awk '{print $2}' | perl -pe "s{\"}{}g" | grep "futures")
do 
export acc=$i
./do_each.sh $1
done


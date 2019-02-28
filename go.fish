#!/usr/bin/fish
# usage: ./go.fish threads > shit.log


for i in (seq $argv[1])
    python -u hust_wsxk.py $i &
end

for j in (jobs -p)
    if [ $j = 'Process' ]
        continue
    end
    wait $j
end



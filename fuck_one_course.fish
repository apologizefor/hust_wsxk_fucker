#!/usr/bin/fish
#

set log_fname (mktemp)

function fuck
    curl -s 'http://wsxk.hust.edu.cn/zxqstudentcourse/zxqcoursesresult.action' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Origin: http://wsxk.hust.edu.cn' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: http://wsxk.hust.edu.cn/zxqstudentcourse/coursesandclassroom.action?markZB=6&ggkdl=&GGKDLBH=0&skZC=&skJC=&kcmc=%E6%98%93%E7%BB%8F' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9' -H 'Cookie: _gscu_1399484133=45466154wop59714; BIGipServerpool6_http=352979466.20480.0000; JSESSIONID=00001gprsedNAbzR0_9x_Dgce72:190ld4dfl' --data 'kcbh=1438094&kczxf=2&ktbh=201821438094001&ktrl=200&ktrs=200&markZB=6&kcmc=%E6%98%93%E7%BB%8F%E4%B8%8E%E4%B8%AD%E5%9B%BD%E6%96%87%E5%8C%96' --compressed > $log_fname
    if grep '选课失败，课堂人数已满！' $log_fname
        echo 'Failed.'$log_fname
    else
        echo 'Success.'$log_fname
        cat $log_fname > succ.$log_fname.log

    end
end

while true
    fuck
end



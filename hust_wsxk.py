
## enable debug
#import http.client as http_client
#import logging
#http_client.HTTPConnection.debuglevel = 1
## You must initialize logging, otherwise you'll not see debug output.
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

FORCE_FUCK = False # Only try to select course if there's a seat.

blacklist = ['自然科学类','艺术类','中级俄语']

cookie_str = '_gscu_1399484133=45466154wop59714; BIGipServerpool6_http=352979466.20480.0000; JSESSIONID=00001gprsedNAbzR0_9x_Dgce72:190ld4dfl'

##################################################################################

import requests
import sys

try:
    MY_MAGIC = sys.argv[1]
except:
    MY_MAGIC = 0
MAGIC_HEAD = '[{}] '.format(MY_MAGIC)

cookie = {}
for c in cookie_str.split('; '):
    cookie[c.split('=')[0]] = c.split('=')[1]

def fetch_course_page(pageNo):
    wsxk_get_url = 'http://wsxk.hust.edu.cn/zxqstudentcourse/coursesandclassroom.action?markZB=6&page=' + str(pageNo)
    resp = requests.get(wsxk_get_url, cookies=cookie)
    if resp.status_code != 200:
        raise RuntimeError("resp.status code not 200. ")
    cont = resp.text
    return cont

from bs4 import BeautifulSoup

def parse_page_html(cont):
    parsed = BeautifulSoup(cont, features='lxml')
    mainlist = parsed.body.find_all('tr', attrs={'class':'tablelist'})
    #print(mainlist)
    return mainlist

def check_and_fuck_a_course(cont):
    global succ,tried,checked

    for keyword in blacklist:
        if str(cont).find(keyword) != -1:
            return

    checked += 1

    shit = str(cont.find('input'))
    # <input disabled="" id="201821434234001" onclick="selectKT(this.id,'200','200','大学生健康教育','1434234','2');" type="button" value="选课"/>

    id_index_beg = shit.find('id="') + 4
    id_index_end = shit.find('"', id_index_beg) - 1
    my_id = shit[id_index_beg : id_index_end+1]
    #print(my_id,id_index_beg,id_index_end)
    assert(len(my_id) == len("201821434234001"))

    shit = shit.replace('this.id', my_id)

    arg_list_beg = shit.find('(') + 1
    arg_list_end = shit.find(')')
    arg_list = shit[arg_list_beg:arg_list_end]

    ktbh,ktrl,ktrs,kcmcl,kczxf,kcbh = arg_list.replace('\'','').split(',')

    if ktrl == ktrs:
        # class full
        if not FORCE_FUCK:
            return
    
    if not FORCE_FUCK:
        print(MAGIC_HEAD, 'FIRE!!!', shit)
    tried += 1

    data_dict = {
        'ktbh':ktbh,
        'ktrl':ktrl,
        'ktrs':ktrs,
        'kcmc1':kcmcl,
        'kczxf':kczxf,
        'kcbh':kcbh,
        'markZB':'6'
    }
    data2 = 'ktbh={}&ktrl={}&ktrs={}&kcmc1={}&kczxf={}&kcbh={}&markZB=6'.format(ktbh,ktrl,ktrs,kcmcl,kczxf,kcbh).encode('utf-8')

    post_url = 'http://wsxk.hust.edu.cn/zxqstudentcourse/zxqcoursesresult.action'
    resp = requests.post(post_url, data=data_dict, cookies=cookie)

    if resp.status_code != 200:
        print(MAGIC_HEAD, 'err: post resp code not 200')
        return

    if resp.text.count('选课失败，课堂人数已满') != 0:
        print(MAGIC_HEAD, 'fuck. course is full. course info:', data_dict)
    else:
        print(MAGIC_HEAD, 'good!', shit, ',checked=', checked, '\n', resp.text)
        succ += 1
        print(MAGIC_HEAD, data_dict)
        with open('save-' + str(checked) + '.log', 'w+') as f:
            f.write(shit)
            f.write(resp.text)

checked = 0
succ = 0
tried = 0
while True:
    for pageNo in range(34):
        try:
            fetched = fetch_course_page(pageNo+1)
        except:
            continue
        ls = parse_page_html(fetched)
        if ls == []:
            print(MAGIC_HEAD, 'Warning: empty class list')

        try:
            for course in ls:
                check_and_fuck_a_course(course)
        except:
            continue

        print(MAGIC_HEAD, 'checked', checked, 'courses. succ', succ, ',tried', tried, file=sys.stderr)
    print(MAGIC_HEAD, 'new round!')








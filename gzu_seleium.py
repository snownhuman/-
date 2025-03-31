#此处使用Edge
import requests.cookies
from selenium import webdriver
from selenium.webdriver.common.by import  By
from time import sleep
from chaojiying import Chaojiying_Client
import requests
from PIL import Image
from lxml import etree

#用户输入
name=input('请输入您的学号')
passwd=input('请输入您的账号')
chaoji_name=input('请输入您的超级鹰账号')
chaoji_passwd=input('请输入您的超级鹰密码')
chaoji_key=input('请输入您的超级鹰key')

#初始网页驱动对象
option=webdriver.EdgeOptions()
option.add_argument('--headless')
drievr=webdriver.Edge(options=option)
#填入你的网页登录url
url='#####'
drievr.get(url)


#获取网页验证码图片
drievr.save_screenshot('page.jpg')
ce=drievr.find_element(by=By.ID,value='icode')
left=ce.location['x']
top=ce.location['y']
right=ce.size['width']+left
height=ce.size['height']+top
#将图片保存到page.jpg
im=Image.open('page.jpg')
img=im.crop((left,top,right,height))
img.save('page.jpg')





#使用超级鹰对验证码进行识别
if __name__ == '__main__':
    chaojiying = Chaojiying_Client(chaoji_name, chaoji_passwd, chaoji_key)	#用户中心>>软件ID 生成一个替换 96001
    im = open('page.jpg', 'rb').read()
    yanzhengma=chaojiying.PostPic(im, 1902)#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    New_yanzhengma=yanzhengma['pic_str']										#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    #print chaojiying.PostPic(base64_str, 1902)  #此处为传入 base64代码

#定位网页标签实现自动填写
scrcetcode=drievr.find_element(by=By.ID,value='txtSecretCode')
scrcetcode.send_keys(New_yanzhengma)
username=drievr.find_element(by=By.ID,value='txtUserName')
username.send_keys(name)
passwd=drievr.find_element(by=By.ID,value='TextBox2')
passwd.send_keys(passwd)
yanzheng=drievr.find_element(by=By.ID,value='txtSecretCode')
button=drievr.find_element(by=By.ID,value='Button1')
button.click()
sel_cookie=drievr.get_cookies()
# print(sel_cookie)
jar=requests.cookies.RequestsCookieJar()
for i in sel_cookie:
      jar.set(i['name'], i['value'],domain=i['domain'],path=i['path']) 
      
      
#将session对象的cookie值进行更改使其可以访问下一级页面后续更方便对网页数据爬取
session=requests.Session()
session.cookies.update(jar)
print (session.cookies)
url = 'https://jw.gzu.edu.cn/xs_main.aspx?xh='+name
headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36 Edg/134.0.0.0'}
req = requests.Request(method='GET', url=url, headers=headers)
rpe = session.send(session.prepare_request(req), 
                    verify=False,# verify设置为False来规避SSL证书验证
                    timeout=10)  
# print (session.cookies)
urls='https://jw.gzu.edu.cn/xs_main.aspx?xh='+name+'#a' 
response=session.get(url=urls,headers=headers).text
#成功定位到下一级页面后面对数据进行爬取
tree=etree.HTML(response)
# kemu=tree.xpath('/html/body/form/div/div/span/table[2]/tbody/tr[3]/td[3]/text()')
# print(kemu)
# print(response)
#此处session已更改
sleep(100)
drievr.close()

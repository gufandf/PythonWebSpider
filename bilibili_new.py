import re
from bs4 import BeautifulSoup
import requests


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55"}
f = """
<local:MyCard 	Title="{0}" Margin="0,5,0,5" CanSwap="True" IsSwaped="True">
    <StackPanel Margin="15,35,0,15 " Orientation="Horizontal" HorizontalAlignment="Left">
        <Image 	Height="180" HorizontalAlignment="Center " 
        		Source="{1}" />
        <StackPanel HorizontalAlignment="Center">
			<TextBlock Margin="15,5,15,0" HorizontalAlignment="Center" 
                        Padding="0,0,0,0" Text="UP: {2}" />
            <TextBlock TextWrapping="Wrap" FontSize="15" Margin="0,0,0,4" 
                        HorizontalAlignment="Center" Text="{3}" />
            <TextBlock TextWrapping="Wrap" Width="200" Height="100" FontSize="12" Margin="0,0,0,4" 
                        HorizontalAlignment="Center" Text="{4}" />
            <local:MyButton Margin="15,5,15,0" Width="200" Height="35" 
                        HorizontalAlignment="Center" Padding="13,0,13,0" ColorType="Highlight" 
                        Text="打开详情" ToolTip="{5}" EventType="打开网页" EventData="{5}" />
        </StackPanel>
    </StackPanel>
</local:MyCard>
"""
def GetMainUrl():
    htmls = requests.get("https://www.bilibili.com/",headers=headers)
    htmls = BeautifulSoup(htmls.text,"lxml")
    div = (htmls.find_all("div",class_="info-box"))
    inf = []
    for i in div :
        url = "https:"+str(i).split('"')[3]
        title = str(i).split('"')[7]
        img_url = "https:"+str(i).split('"')[9].split('@')[0]
        up = re.findall('</i>(.*?)</p><p',str(i))[0]
        inf.append({"title":title,"url":url,"img_url":img_url,"up":up})
    return inf


def GetMovieInf(url):
    print(url)
    d = {}
    l = ["like","coin","collect","share","info","up-card","tit"]
    htmls = requests.get(url,headers=headers) #like_coin_collect_share
    htmls = BeautifulSoup(htmls.text,"lxml")
    for i in l:
        div = (htmls.find_all("span",class_=i))
        if i == "like":
            d[i] = str(div[0]).split('>')[-2][0:-11]
        elif i == "coin":
            d[i] = str(div[0]).split('>')[-2][7:-11]
        elif i == "collect":
            d[i] = str(div[0]).split('>')[-2][0:-11]
        elif i == "share":
            d[i] = str(div[0]).split('>')[-3][0:-14]
        elif i == "tit tr-fix":
            d["title"] = str(div[0])[25:-7]
        elif i == "info" :
            d[i] = str(htmls.find_all("div",class_=i)[0])[23:-6]
        # elif i == "up-card":
        #     ups = []
        #     up_l = htmls.find_all("div",class_="up-card")
        #     if up_l == None:
        #         up = htmls.find_all("a",report-id="name")
        #     else:
        #         for r in up_l:
        #             print(str(r).split('>'))
        #             up_name = str(r).split('>')[-4][:-3]
        #             up_act = str(r).split('>')[-9][:-6]
        #             up_url = "https:"+str(r).split('"')[9]
        #             ups.append({"up_name":up_name,"up_url":up_url,"up_act":up_act})
        #             d["up"] = ups
    return d

div = GetMainUrl()
f_up = open("E:\%recreation\PCL\PCL\Customs\Custom_up.xaml","r",encoding='utf-8')
f_up = f_up.read()
fo = f_up
#print(div)

for i in div:
    inf = GetMovieInf(i["url"])
    fo = fo+f.format(re.sub(r'[\"\<\>]', "", i["title"]),
    i["img_url"],
    re.sub(r'[\"\<\>]', "", i["up"]),
    "点赞: "+str(inf["like"]),
    re.sub(r'[\"\<\>]', "", inf["info"]),i["url"])

f = open("E:\%recreation\PCL\PCL\Custom.xaml","w",encoding='utf-8')
f.write(fo)
f.close()
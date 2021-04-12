import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib


def send_email(content):
    my_email = "XXX@gmail.com"
    password = "XXX"
    target_email = "XXX"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=target_email,
            msg=f"Subject:Webwork close!!!\n\n"
                f"{content}")


URL = "http://webwork.math.ntu.edu.tw/webwork2/1092MATH4008_07?user=XXX&passwd=XXX"
data = requests.get(URL).text
soup = BeautifulSoup(data, "html.parser")
table = soup.find("table")
raw_data = table.find_all("td")

chapter = []
raw_date = []
t = 0
for i in raw_data:
    t += 1
    if t % 3 == 2:
        chapter.append(i.string)
    if t % 3 == 0:
        raw_date.append(i.string[10:20])

date = []
for d in raw_date:
    try:
        date.append(datetime.strptime(d, "%m/%d/%Y"))
    except ValueError:
        pass

t = -1
notify_dict = {}
for time in date:
    t += 1
    difference = time - datetime.today()
    print(difference)
    if difference.days < 7:
        notify_dict[chapter[t]] = time.strftime("%m/%d")

if notify_dict is not None:
    string = "Morning BoBo:\n\n" \
             "Have you finished your webwork?\n" \
             "Here are the chapters and the dates!!\n"
    for (key, value) in notify_dict.items():
        string += f"{key} {value}\n"

    string += "Please do it now!!\n\n" \
              "Yours,\n" \
              "Luke"
    send_email(string)
    print("send!")

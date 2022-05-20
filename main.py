import requests
from bs4 import BeautifulSoup
import smtplib
from config import mail, token, chat_id, sword
import time

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) firefox/92.0.4515.159 Safari/537.36'}
locality = ['семилуки','девица','стрелица','орлово','петино','латная','Cемилуки','Девица','Стрелица','Орлово','Петино','Латная','Устье','Подпольное','Дмитриевка','Еманча 1','Заречье','Гремячье']
old_name = []
class Dom:
    def __init__(self):

        url = 'https://www.avito.ru/voronezhskaya_oblast/doma_dachi_kottedzhi/prodam/dom-ASgBAQICAUSUA9AQAUDYCBTOWQ?bt=1&f=ASgBAQECAUSUA9AQAUDYCBTOWQJFkAkYeyJmcm9tIjpudWxsLCJ0byI6MTQ1NTZ9wBMYeyJmcm9tIjpudWxsLCJ0byI6MTQ2NTJ9&p=5&q=%D0%B4%D0%BE%D0%BC&s=104'
        self.get_html(url)


    def get_html(self, url):
        r = requests.get(url, headers=headers)
        self.work(r.text)

    def work(self, html):
        global old_name
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all('div', class_="iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum")
          
        if len(items) == 0:
            self.send_bot('Restore link!')
            raise SystemExit.exit()  
        for self.i in items:
            name = self.i.find('span', class_="geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL").text.strip('с.').strip('пос.').strip(' ')
            
            
            if name in locality:
                if name == old_name:
                    self.send_bot('Not new.')
                    break

                old_name = name
                self.send_mail(self.get_href())
                self.send_bot(name)    
                break
            
                



    def get_href(self):
        href = 'https://www.avito.ru'+self.i.find('a', class_="link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH").get('href')
        return href

    def send_mail(self, href):
        global sword
        sender = mail
        sword = sword

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        try:
            server.login(sender, sword)
            server.sendmail(sender, 'iwan.marjanoff@yandex.ru', f"Subject:Link from Avito!!!{href}")
            return "The message send successfully!"

        except Exception as ex:
            return f"{ex}\n Check your login or passeword please." 

    def send_bot(self,message):
        try:
            URL = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
            r = requests.get(URL)
            return "The message to Bot successfully!"
        except Exception as f:
            return f'{f} the wrong!'  
    print('Please Wait')

def main():
    while True:
        b = Dom()
        time.sleep(60*10)

if __name__ == '__main__':
    main()

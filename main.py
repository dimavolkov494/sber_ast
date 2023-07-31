from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import re

class Lot:
	def __init__(self, torg_n, lot, money, link, prop, vin):
		self.lot = lot.text.replace('                                    ','')
		self.lot = self.lot.replace('\n', '')
		self.money = money.text
		self.link = link
		self.properties = prop
		self.torg_n = torg_n
		self.vin = vin

		self.libra = {"Номер на торгах" : str(self.torg_n),
						"Лот" : self.lot.split('Лот: ')[1],
						"Цена" : float(self.money.replace(" ","")),
						"VIN номер" : self.vin,
						"Ссылка" : self.link,
						"Описание" : self.properties
						}

	def show(self):
		print(self.libra)	
		return 0	

def parse(url):

	browser = webdriver.Edge()
	browser.get(url)

	bs = BeautifulSoup(browser.page_source, 'html.parser')

	table = bs.find_all('div', {'content':'node:hits', 'class': 'purch-reestr-tbl-div'})
	arrayoflots = []
	for elem in table:
		lot = elem.find('div', {'class': 'SelBidNameSpan'})
		money =  elem.find('span', {"content":"leaf:purchAmount","format":"money", "class":"es-el-amount"})
		link = elem.find('a', {'class':'link-button STRView', 'target':'_blank'})
		link = link.get('href')
		torg_number = elem.find('span', {"content":"leaf:purchCodeTerm", "class":"es-el-code-term"})
		torg_number = torg_number.text

		#time.sleep(1)
		newbrowser = webdriver.Edge()
		newbrowser.get(link)
		time.sleep(2)

		new_bs = BeautifulSoup(newbrowser.page_source, 'html.parser')
		prop = new_bs.find_all('span', {"content":"leaf:DebtorBidName","id":"DynamicControlBidInfo_DebtorBidName", "name":"DynamicControlBidInfo_DebtorBidName"})
		
		if len(prop) == 0:
			propt = '123'
		else:	
			propt = prop[0].text


		match = re.search(r'[A-Za-z0-9]{16}', propt)

		# Если ключевая строка найдена, вывод ее на экран
		if match:
			key_string = match.group()
			vin = key_string
		else:
			vin = "Не удалось найти VIN"

		obj = Lot(torg_number, lot, money, link, propt, vin)
		obj.show()
		arrayoflots.append(obj)
		for lot in arrayoflots:
			lot.show()


	

	return 0


if __name__ == "__main__":
	url = "https://utp.sberbank-ast.ru/Bankruptcy/List/BidListTransport"
	parse(url)

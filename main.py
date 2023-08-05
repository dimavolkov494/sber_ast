from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import re

class Lot:
	def __init__(self, torg_n, lot, money, link, prop, vin, region):
		self.lot = lot.text.replace('                                    ','')
		self.lot = self.lot.replace('\n', '')
		self.money = money.text
		self.link = link
		self.properties = prop
		self.torg_n = torg_n
		self.vin = vin
		self.region = region

		self.libra = {"Номер на торгах" : str(self.torg_n),
						"Лот" : self.lot.split('Лот: ')[1],
						"Цена" : float(self.money.replace(" ","")),
						"VIN номер" : self.vin,
						"Ссылка" : self.link,
						#"Описание" : self.properties,
						"Описание" : "Временно отключено",
						"Регион" : self.region
						}

	def show(self):
		print("{")
		print("	"+"Номер на торгах : " +self.libra.get("Номер на торгах"))
		print("	"+"Лот : " +self.libra.get("Лот"))
		print("	"+"Цена : " +str(self.libra.get("Цена")))
		print("	"+"VIN номер : " +self.libra.get("VIN номер"))
		print("	"+"Ссылка : " +self.libra.get("Ссылка"))
		print("	"+"Описание : " +self.libra.get("Описание"))
		print("	"+"Регион : " + self.libra.get("Регион"))
		print("}")	
		return 0	

def beautiful_drow(array):
	for elem in array:
		elem.show()


def parse(url):

	browser = webdriver.Chrome()
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

		#properties
		new_bs = BeautifulSoup(newbrowser.page_source, 'html.parser')
		prop = new_bs.find_all('span', {"content":"leaf:DebtorBidName","id":"DynamicControlBidInfo_DebtorBidName", "name":"DynamicControlBidInfo_DebtorBidName"})
		region = new_bs.find_all('span', {"content":"leaf:BidRegion","id":"DynamicControlBidInfo_BidRegion", "name":"DynamicControlBidInfo_BidRegion"})

		#properties
		if len(prop) == 0:
			propt = '123'
		else:	
			propt = prop[0].text

		#city
		if len(region) == 0:
			region_str = '123'
		else:	
			region_str = region[0].text

		#vin
		match = re.search(r'[A-Za-z0-9]{16}', propt)

		# Если ключевая строка найдена
		if match:
			key_string = match.group()
			vin = key_string
		else:
			vin = "Не удалось найти VIN"




		obj = Lot(torg_number, lot, money, link, propt, vin, region_str)
		obj.show()
		arrayoflots.append(obj)
	
	beautiful_drow(arrayoflots)

	return 0


if __name__ == "__main__":
	url = "https://utp.sberbank-ast.ru/Bankruptcy/List/BidListTransport"
	parse(url)

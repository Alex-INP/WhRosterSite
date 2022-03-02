from bs4 import BeautifulSoup
import requests
links = ["https://wahapedia.ru/wh40k9ed/factions/adeptus-mechanicus/Belisarius-Cawl",
		 "https://wahapedia.ru/wh40k9ed/factions/adeptus-mechanicus/Kataphron-Destroyers",
		 "https://wahapedia.ru/wh40k9ed/factions/adeptus-mechanicus/Archaeopter-Fusilave"]
for link in links:
	data = requests.get(link).content
	soup = BeautifulSoup(data, "html.parser")
	h3 = soup.h3
	print(h3.contents[0].text)
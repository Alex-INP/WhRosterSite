from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json
import re

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_segment_links(doc):
	all_results = []
	all_roles = []
	link_segment = doc.find_all("div", {"style": "margin-bottom:8px;"})
	for segment in link_segment:
		result = {"role": None, "units": []}
		role = segment.find("b", {"class": "BatRole"}).text
		if role not in all_roles:
			all_roles.append(role)
			result["role"] = role
			units = segment.find_all("div", {"class": "i15"})
			for i in units:
				result["units"].append(i.a["href"])
			all_results.append(result)
	return all_results


def replace_data(data, replace_strings):
	for key, val in data.items():
		if type(val) == dict:
			replace_data(val, replace_strings)
			continue
		elif val is None:
			continue
		elif type(val) == list:
			if type(val[0]) == dict:
				for i in val:
					replace_data(i, replace_strings)
				continue
			for ind, value in enumerate(val):
				for strings in replace_strings:
					val[ind] = value.replace(strings[0], strings[1])
			continue
		for strings in replace_strings:
			data[key] = str(val).replace(strings[0], strings[1])


def get_model_data(unit_element):
	all_results = []
	result = {
		"model_data": {
			"name": None,
			"price": None
		},
		"model_profiles_data": [],
		"model_count_restrictions": {
			"min": None,
			"max": None
		}
	}
	data_table_elements = unit_element.find("table", {"class": "wTable pTable_no_dam pTable_border"}) \
		.find_all("tbody", {"class": "bkg"})

	profile_position = 1
	for element in data_table_elements:
		if price := element.find("div", {"class": "PriceTag"}):
			result = {
				"model_data": {
					"name": None,
					"price": None
				},
				"model_profiles_data": [],
				"model_count_restrictions": {
					"min": None,
					"max": None
				}
			}
			profile_position = 1
			result["model_data"]["name"] = element.find("span", {"class": "pTable2_long"}).contents[1]
			result["model_data"]["price"] = price.text

		columns = element.find("tr", {"class": None}).findChildren(recursive=False)
		if profile_position == 1:
			count_restrictions = columns[0].text
			if "‑" in count_restrictions:
				count_restrictions = count_restrictions.split("‑")
				result["model_count_restrictions"]["min"] = count_restrictions[0]
				result["model_count_restrictions"]["max"] = count_restrictions[1]
			else:
				result["model_count_restrictions"]["min"] = count_restrictions
				result["model_count_restrictions"]["max"] = count_restrictions

		result["model_profiles_data"].append({
			"position": profile_position,
			"movement": columns[2].text.replace("\"", ""),
			"weapon_skill": columns[3].text.replace("+", ""),
			"ballistic_skill": columns[4].text.replace("+", ""),
			"strength": columns[5].text,
			"toughness": columns[6].text,
			"wounds": columns[7].text,
			"attacks": columns[8].text,
			"leadership": columns[9].text,
			"saving_throw": columns[10].text.replace("+", ""),
			"base": columns[11].text,
		})
		profile_position += 1
		all_results.append(result)
	return all_results


def normalize_abilities(abilities):
	for ind, value in enumerate(abilities):
		if "Description in Codex" in value and "," in value:
			splitted_abilities = value.split(":")[0].split(",")
			del abilities[ind]
			for i in splitted_abilities:
				abilities.insert(0, f'{i}: Description in Codex')


def get_unit_weapon_data(doc, unit_name):
	weapons_data = []

	weapon_table = doc.find("div", {"class": "wtOuterFrame"}).table
	for weapon_el in weapon_table.find_all("tbody", {"class": "bkg"}):
		weapon = {
			"weapon_data": {
				"name": None,
				"price": None
			},
			"weapon_profiles_data": []
		}
		if len(weapon_el.findChildren(recursive=False)) <= 3:
			if price := weapon_el.find("div", {"class": "PriceTag"}):
				weapon["weapon_data"]["price"] = price.text.replace("+", "")
				try:
					weapon["weapon_data"]["name"] = weapon_el.find("span", {"class": None}).contents[
														1] + f" ({unit_name})"
				except TypeError:
					weapon["weapon_data"]["name"] = weapon_el.find("span",
																   {"class": "tt kwbu"}).parent.text + f" ({unit_name})"

			else:
				weapon["weapon_data"]["price"] = "0"
				weapon["weapon_data"]["name"] = weapon_el.find("tr", {"class": "wTable2_long"}).td.span.text


			# stats = weapon_el.find("tr", {"class": ""}).findChildren(recursive=False)
			try:
				stats = weapon_el.findChildren(recursive=False)[2].findChildren(recursive=False)

				# print(f"{stats=}")
				weapon["weapon_profiles_data"].append({
					"name": "single",
					"weapon_range": stats[1].text.replace("\"", ""),
					"weapon_type": stats[2].text,
					"strength": stats[3].text,
					"armor_penetration": stats[4].text.replace("-", ""),
					"damage": stats[5].text,
					"abilities": stats[6].text,
				})
			except:
				stats = weapon_el.findChildren(recursive=False)[1].findChildren(recursive=False)

				# print(f"{stats=}")
				weapon["weapon_profiles_data"].append({
					"name": "single",
					"weapon_range": stats[1].text.replace("\"", ""),
					"weapon_type": stats[2].text,
					"strength": stats[3].text,
					"armor_penetration": stats[4].text.replace("-", ""),
					"damage": stats[5].text,
					"abilities": stats[6].text,
				})
		else:
			if price := weapon_el.find("div", {"class": "PriceTag"}):
				weapon["weapon_data"]["price"] = price.text.replace("+", "")
				try:
					weapon["weapon_data"]["name"] = weapon_el.find("div", {"class": "pad2626"}).contents[
														1] + f" ({unit_name})"
				except:
					weapon["weapon_data"]["name"] = weapon_el.find("span",
																   {"class": "tt kwbu"}).parent.text + f" ({unit_name})"
			else:
				weapon["weapon_data"]["price"] = "0"
				weapon["weapon_data"]["name"] = weapon_el.find("div", {"class": "pad2626"}).text
				if weapon["weapon_data"]["name"] == "Melee":
					weapon["weapon_data"]["name"] = weapon_el.find("td", {"class": "wTable2_short pad2626"}).text

			for element in weapon_el.find_all("td", {"class": "wTable2_short pad2626"}):
				stats = element.parent.find("div", {"class": "ct pad2626"}).parent.parent.findChildren(recursive=False)

				weapon["weapon_profiles_data"].append({
					"name": stats[0].text[3:],
					"weapon_range": stats[1].text.replace("\"", ""),
					"weapon_type": stats[2].text,
					"strength": stats[3].text,
					"armor_penetration": stats[4].text.replace("-", ""),
					"damage": stats[5].text,
					"abilities": stats[6].text,
				})
		weapons_data.append(weapon)
	return weapons_data


def get_unit_other_wargear(doc, unit_name):
	all_results = []
	all_tables = doc.find_all("table", {"class": "wTable"})
	for table in all_tables:
		if el := table.find("div", {"class": "wTable1"}):
			try:
				txt = el.text.lower()
			except:
				continue
			if txt == "other wargear":
				for element in table.find_all("tbody", {"class": "bkg"}):
					result = {
						"name": None,
						"price": None,
						"description": None
					}
					entry = element.findChildren(recursive=False)
					if price := entry[0].find("div", {"class": "PriceTag"}):
						result["price"] = price.text.replace("+", "")
					else:
						result["price"] = "0"
					if result["price"] != "0":
						result["name"] = entry[0].find("div", {"class": "pad2626"}).span.text + f" ({unit_name})"
					else:
						result["name"] = entry[0].find("div", {"class": "pad2626"}).text
					result["description"] = entry[2].find("td", {"colspan": "7"}).text
					all_results.append(result)
				break

	return all_results if all_results else None


def get_unit_data(driver, site_name, link):
	replace_strings = []
	result = {
		"unit_data": {
			"name": None,
			"codex_faction": None,
			"wargear_options": None,
			"description": None,
			"power_rating": None,
			"picture_search_link": None,
			"abilities": None,
			"transport": None,
			"psyker": None,
			"faction_keywords": None,
			"keywords": None,
			"weapons": None,
			"other_wargear": None,
			"warlord_trait": None
		}
	}
	full_link = site_name + link
	# data = requests.get(full_link).content
	driver.get(full_link)
	data = driver.page_source

	doc = BeautifulSoup(data, "html.parser")
	result["unit_data"]["power_rating"] = doc.find("div", {"class": "img-opa PowerPrice"}).text
	result["unit_data"]["name"] = doc.find("h3", {"class": "pTable_h3 pTable_no_dam"}).div.text
	result["unit_data"]["description"] = doc.find("div", {"style": "padding:4px;"}).getText()
	result["unit_data"]["picture_search_link"] = doc.find("a", {"class": "tooltip"})["href"]

	table_elements = doc.find("tr", {"class": "abVisChk dsAbilityHeader_long"}).parent.findChildren(recursive=False)
	# pprint(table_elements)

	def add_keyw(element, result, keyw_header):
		keywords = element.find("span", {"class": "dsKeywordData"}).getText().split(",")
		for ind, keyw in enumerate(keywords):
			if keyw[0] == " ":
				keywords[ind] = keyw[1:]
			if search_result := re.search(r"<.+>", keyw):
				keywords[ind] = search_result.group()
				replace_strings.append([keyw, keywords[ind]])
		if keyw_header.text[:-2].lower() == "faction keywords":
			result["unit_data"]["faction_keywords"] = keywords
		elif keyw_header.text[:-2].lower() == "keywords":
			result["unit_data"]["keywords"] = keywords

	trait = False
	for element in table_elements:
		# print("---"*20)
		# print(element)
		# print("---" * 20)
		if header := element.find("div", {"class": "dsHeader"}):
			if header.text.lower() == "wargear options":
				wargear_options = element.find("td", {"class": "dsAbilityData"})
				if wargear_options:
					all_options = []
					for option in wargear_options.findChildren(recursive=False):
						all_options.append(option.text[3:])
					result["unit_data"]["wargear_options"] = all_options
			elif header.text.lower() == "abilities":
				abilities = element.find("td", {"class": "dsAbilityData"})
				if abilities:
					all_abilities = []
					for abilitiy in abilities.find_all("div", {"class": "BreakInsideAvoid abVisChk2"}):
						if abilitiy.b:
							all_abilities.append(f"{abilitiy.b.getText()}: Description in Codex")
					for abilitiy in abilities.find_all("div", {"class": "BreakInsideAvoid abVis"}):
						if abilitiy.b:
							all_abilities.append(abilitiy.getText())
					normalize_abilities(all_abilities)
					result["unit_data"]["abilities"] = all_abilities
			elif header.text.lower() == "transport":
				if transport_data := element.find("td", {"class": "dsAbilityData"}):
					result["unit_data"]["transport"] = transport_data.text.strip()
			elif header.text.lower() == "psyker":
				if psyker_data := element.find("td", {"class": "dsAbilityData"}):
					result["unit_data"]["psyker"] = psyker_data.text.strip()
			elif header.text.lower() == "warlord trait!" and not trait:
				trait = True
			elif trait:
				warlord_trait = element.find("td", {"class": "dsAbilityData"})
				result["unit_data"]["warlord_trait"] = warlord_trait.text.strip()
				trait = False

		elif keyw_header := element.find("span", {"class": "dsKeywordHeader"}):
			add_keyw(element, result, keyw_header)
		if result["unit_data"]["keywords"] is None:
			for el in doc.find("tr", {"class": "abVisChk dsAbilityHeader_long"}).parent.parent.findChildren(recursive=False)[1:]:
				if header := el.find("div", {"class": "dsHeader"}):
					if header.text.lower() == "transport":
						if transport_data := el.find("td", {"class": "dsAbilityData"}):
							result["unit_data"]["transport"] = transport_data.text.strip()
					elif header.text.lower() == "psyker":
						if psyker_data := el.find("td", {"class": "dsAbilityData"}):
							result["unit_data"]["psyker"] = psyker_data.text.strip()
						elif header.text.lower() == "warlord trait!" and not trait:
							trait = True
						elif trait:
							warlord_trait = element.find("td", {"class": "dsAbilityData"})
							result["unit_data"]["warlord_trait"] = warlord_trait.text.strip()
							trait = False
				elif el.find("span", {"class": "dsKeywordHeader"}):
					for i in el.findChildren(recursive=False):
						keyw_header = i.find("span", {"class": "dsKeywordHeader"})
						add_keyw(i, result, keyw_header)

	result["unit_data"]["other_wargear"] = get_unit_other_wargear(doc, result["unit_data"]["name"])
	result["unit_data"]["weapons"] = get_unit_weapon_data(doc, result["unit_data"]["name"])
	unit_model_data = get_model_data(doc)

	result["models_data"] = unit_model_data
	return result, replace_strings

def add_to_data(where_to, what_to, data):
	if what_to not in data[where_to]:
		data[where_to].append(what_to)


def restructure(data):
	with open(file_name, "w", encoding="utf-8") as file:
		content = {}
		for i in ["codex_faction_data",
				  "battlefield_role_data",
				  "weapon_data",
				  "weapon_profile_data",
				  "ability_data",
				  "keyword_data",
				  "faction_keyword_data",
				  "unit_model_data",
				  "unit_data",
				  "unit_model_profile_data",
				  "other_wargear"]:
			content[i] = []

		for entry in data:
			# for key, val in entry["unit_data"]:
			add_to_data("battlefield_role_data", {"name": entry["unit_data"]["battlefield_role"]}, content)
			add_to_data("codex_faction_data", {"name": entry["unit_data"]["codex_faction"]}, content)
			for weapon in entry["unit_data"]["weapons"]:
				add_to_data("weapon_data", {
					"name": weapon["weapon_data"]["name"],
					"price": weapon["weapon_data"]["price"]
				}, content)
				for p in weapon["weapon_profiles_data"]:
					add_to_data("weapon_profile_data", {
						"name": p["name"],
						"weapon_range": p["weapon_range"],
						"weapon_type": p["weapon_type"],
						"strength": p["strength"],
						"armor_penetration": p["armor_penetration"],
						"damage": p["damage"],
						"abilities": p["abilities"],
						"weapon": weapon["weapon_data"]["name"]
					}, content)
			for i in entry["unit_data"]["abilities"]:
				ability_splitted = i.split(":")
				name, descr = ability_splitted[0], ":".join(ability_splitted[1:])
				dict_to_add = {
					"name": name,
					"description": descr,
					"price": None
				}
				try:
					price = re.search(r"\+\d+", descr).group()
					dict_to_add["price"] = price[1:]
					dict_to_add["description"] = dict_to_add["description"].replace("+" + dict_to_add["price"], "")
				except AttributeError:
					price = "0"
					dict_to_add["price"] = price

				if dict_to_add["name"][:1] == " ":
					dict_to_add["name"] = dict_to_add["name"][1:]
				if dict_to_add["description"][:1] == " ":
					dict_to_add["description"] = dict_to_add["description"][1:]

				add_to_data("ability_data", dict_to_add, content)

			for i in entry["unit_data"]["keywords"]:
				add_to_data("keyword_data", {
					"name": i
				}, content)
			for i in entry["unit_data"]["faction_keywords"]:
				add_to_data("faction_keyword_data", {
					"name": i
				}, content)

			for ind, val in enumerate(entry["unit_data"]["abilities"]):
				if match_str := re.search(r"\+\d+", val):
					match_str = match_str.group(0)
					entry["unit_data"]["abilities"][ind] = entry["unit_data"]["abilities"][ind].replace(match_str, "")
			dict_to_add = {
				"battlefield_role": entry["unit_data"]["battlefield_role"],
				"name": entry["unit_data"]["name"],
				"codex_faction": entry["unit_data"]["codex_faction"],
				"wargear_options": entry["unit_data"]["wargear_options"],
				"other_wargear": [w["name"] for w in entry["unit_data"]["other_wargear"]] if entry["unit_data"][
					"other_wargear"] else None,
				"description": entry["unit_data"]["description"],
				"power_rating": entry["unit_data"]["power_rating"],
				"picture_search_link": entry["unit_data"]["picture_search_link"],
				"transport": entry["unit_data"]["transport"],
				"faction_keywords": entry["unit_data"]["faction_keywords"],
				"keywords": entry["unit_data"]["keywords"],
				"psyker": entry["unit_data"]["psyker"],
				"warlord_trait": entry["unit_data"]["warlord_trait"],
				"weapons": [w["weapon_data"]["name"] for w in entry["unit_data"]["weapons"]],
				"abilities": [{"name": ab.split(":")[0], "description": ":".join(ab.split(":")[1:])[1:]} for ab in entry["unit_data"]["abilities"]]
			}

			for el in dict_to_add["abilities"]:
				# print(f"{el=}")
				if el["name"][:1] == " ":
					el["name"] = el["name"][1:]
				if el["description"][:1] == " ":
					el["description"] = el["description"][1:]
			add_to_data("unit_data", dict_to_add, content)

			for i in entry["models_data"]:
				add_to_data("unit_model_data", {
					"name": i["model_data"]["name"],
					"price": i["model_data"]["price"],
					"unit_count_restrictions": i["model_count_restrictions"],
					"unit_affinity": entry["unit_data"]["name"]
				}, content)
				for pr in i["model_profiles_data"]:
					add_to_data("unit_model_profile_data", {
						"position": pr["position"],
						"movement": pr["movement"],
						"weapon_skill": pr["weapon_skill"],
						"ballistic_skill": pr["ballistic_skill"],
						"strength": pr["strength"],
						"toughness": pr["toughness"],
						"wounds": pr["wounds"],
						"attacks": pr["attacks"],
						"leadership": pr["leadership"],
						"saving_throw": pr["saving_throw"],
						"base": pr["base"],
						"unit_model": i["model_data"]["name"]
					}, content)
			if entry["unit_data"]["other_wargear"]:
				for i in entry["unit_data"]["other_wargear"]:
					add_to_data("other_wargear", {"name": i["name"], "description": i["description"], "price": i["price"]}, content)

		json.dump(content, file)


if __name__ == "__main__":
	site_name = "https://wahapedia.ru"
	# links = ["https://wahapedia.ru/wh40k9ed/factions/adeptus-mechanicus/"]
	links = ["https://wahapedia.ru/wh40k9ed/factions/chaos-daemons/"]
	final_data = []
	file_name = "data_daemons.json"

	for link in links:
		options = Options()
		options.add_argument("start-maximized")
		driver = webdriver.Chrome(service=Service("./chromedriver.exe"), options=options)
		driver.implicitly_wait(20)
		driver.get(link)
		data = driver.page_source

		# headers = {
		# 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
		# data = requests.get(link, headers=headers).content
		# print(data.decode())
		doc = BeautifulSoup(data, "html.parser")

		faction = doc.find("span", {"class": "page_header_span"}).text
		unit_links = get_segment_links(doc)

		for unit_link in unit_links:
			role = unit_link["role"]
			if role == "Fortifications":
				continue
			for i in unit_link["units"]:
				print(f"Processing link: {i}")
				unit_data, replace_strings = get_unit_data(driver, site_name, i)

				replace_data(unit_data, replace_strings)

				unit_data["unit_data"]["codex_faction"] = faction
				unit_data["unit_data"]["battlefield_role"] = role

				final_data.append(unit_data)
				print("Processing done.")
	pprint(final_data, sort_dicts=False)
	restructure(final_data)
	# pprint(final_data, sort_dicts=False)

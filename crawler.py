import requests
import json
import calculator
import re

base_url="https://api.torn.com"

fliter_list = ['bank', 'player_id', 'job', 'items', 'company', 'stats', 'stocks', "merits", "company_employees", "strength", "speed", "dexterity", "defense", "faction_perks"]
stats_fliter_list = ['points_averagecost']
stocks_fliter_list = ['1', '2', '4', '5', '6', '7', '9', '10', '12', '15', '16', '17', '18', '19', '24', '32', '35']

def fliter_func(key):
    if key in fliter_list:
        return True
    return False

def crawl_template(url="",key="",headers={}):
    try:
        data=requests.get(f"{base_url}{url}&key={key}&comment=Torn-BS-Helper", headers=headers).json()
        if "error" in data.keys():
            raise ValueError(data["error"]["error"])
        return data
    except Exception as e:
        raise ValueError(e)

def crawlers(object, key):
    try:
        d = {}
        d.update(crawl_template("/torn/?selections=bank,stats",key))
        d["stats"] = {k:v for (k,v) in d["stats"].items() if k in stats_fliter_list}
        d.update(crawl_template("/user/?selections=merits,stocks,profile,battlestats,perks",key))
        d["stocks"] = {k:v for (k,v) in d["stocks"].items() if k in stocks_fliter_list}
        d.update(crawl_template("/torn/106,329,330,331,364,365,366,367,368,369,370,817,818,530,532,533,553,554,555,985,986,987?selections=items",key))
        d.update(crawl_template("/company/?selections=profile,employees",key))
        d = {k:v for (k,v) in d.items() if k in fliter_list}

        TCI = d["stocks"].get("2", None)
        if TCI and TCI["benefit"]["ready"]:
            object.TCI.set(True)
        else:
            object.TCI.set(False)
        
        object.bank_rate = d["bank"]
        object.bank_merits.set(d["merits"]["Bank Interest"])
        
        if d["job"]:
            company_id = d["job"].get("company_id", 0)
            if company_id:
                position = d['job'].get("position", None)
                if position == "Director":
                    object.salary.set(object.salary.get()+calculator.calculate_director(d["company"], d["company_employees"], crawl_template("/company/?selections=detailed", key)["company_detailed"]))
                else:
                    object.salary.set(object.salary.get()+d["company_employees"][str(d["player_id"])]["wage"])
        
        object.STR.set(d["strength"])
        object.SPD.set(d["speed"])
        object.DEX.set(d["dexterity"])
        object.DEF.set(d["defense"])

        for k,v in d["stocks"].items():
            if "dividend" in v.keys():
                object.stock_dict[k][0].set(True)
                object.stock_dict[k][1].set(v["dividend"]["increment"])

        for k,v in d["items"].items():
            object.item_value[k] = v["market_value"]
        
        object.pts_value = d["stats"]["points_averagecost"]

        perks = d.get("faction_perks", None)
        if perks:
           for i in perks:
               x = re.match(r"\+ ([0-9]{1,2})\% energy gain from energy drinks", i)
               if x:
                   object.energy_perks = x.group(1)

    except Exception as e:
        raise ValueError(e)
import cityu
import polyu
import eventbrite
import hku
import hkbu

# Configuration for title filter words
title_filter_config = {
    "hku": ["漢字","Lyrics","Periodontal","clinical", "Cadaveric","Buddhism","20th Hong Kong International Orthopaedic Forum","12th Hong Kong Pathology Forum","Shostakovich Preludes and Fugues","Printmakers","ISMS"],
    "hkbu": ["PhD programme"],
    "eventbrite": ["Book Club","Weekly Social HackJam","AIA", "Eats Out", "Drink","瑜伽","Meditation","展覽","Testing","NETMHK","Live Music","創意工作坊","SALSA FEVER","護手霜","Fringe Club","Kizomba","Hive x Starring","校舍參觀","香港私人物業","BOLLYWOOD NIGHT","PATIENTS FOR YOUR CLINIC","Board Games","Comedy Night"]
}
# title_filter_config = {
#     "hku": [],
#     "hkbu": [],
#     "eventbrite": []
# }

def run():
    print("=============== CityU ===============")
    cityu.fetch_events()
    
    print("=============== PolyU ===============")
    polyu.fetch_events()
    
    print("=============== hku ===============")
    hku.fetch_events(title_filter_words=title_filter_config["hku"])
    
    print("=============== hkbu ===============")
    hkbu.fetch_events(title_filter_words=title_filter_config["hkbu"])
    
    print("=============== Eventbrite next_month===============")
    eventbrite.fetch_events("next_month", title_filter_words=title_filter_config["eventbrite"])
    print("=============== Eventbrite this_month===============")
    eventbrite.fetch_events("this_month", title_filter_words=title_filter_config["eventbrite"])

if __name__ == "__main__":
    run()

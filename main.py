import cityu
import polyu
import eventbrite
import hku
import hkbu
import gdg_hk
import cityu_mba
import luma
import meetup  # Add this import for the new module

# Configuration for title filter words
title_filter_config = {
    "hku": ["導賞","音樂節","中學","Endoscopy","Tubular Structures","Thyroid","Retreat","HKSGO","Orthodontic","漢字","Lyrics","Periodontal"
            ,"Infectious","Orthopaedic","Musculoskeletal","Surgery","Infection","dental","O&G Centenary","Perio Implant","Esophageal Cancer","HKUMAA 25th","CAAD Futures","Certificate in Infection","clinical", "Cadaveric","Buddhism","20th Hong Kong International Orthopaedic Forum","12th Hong Kong Pathology Forum","Shostakovich Preludes and Fugues","Printmakers","ISMS"],
    "hkbu": ["PhD programme","比賽","特展","崇拜","Choir"],
    "meetup": ["HKMechworks", "Coffee & Connections", "Meditation", "Yoga", "瑜伽", "Dance", "Board Games", "Comedy Night", "Book Club", "Hiking"],
    "eventbrite": ["新體驗","Public Social HackJam","How to prepare IPO successfully","Startup Legal Tech","健脊及伸展","頸椎問題的影響","佛山","One Sai Day",
                   "Nook Bar","Networking Night","Art Pop-Up","Free (face-to-face) English Classes","Dancing Group","Kids English","舞蹈工作坊","運動科學資訊日",
                   "Yogathon","Animal Flow","Ascension","Improv Auditions","獨奏會","夢幻與泡影","中原地產","YMCA","Spanish Movie Night","創作者導賞團","Dubai Property","動優惠卷","embrace your Colours","Legal Workshops","小學部","Open Day at Oxbridge School","YWCA CLLE","The Psychology of Money","Summer Sizzler","Dubai Real Estate","Book Club","Weekly Social HackJam","AIA", "Eats Out", "Drink","瑜伽","Meditation","展覽","Testing","NETMHK","Live Music","創意工作坊","SALSA FEVER","護手霜","Fringe Club","Kizomba","Hive x Starring","校舍參觀","香港私人物業","BOLLYWOOD NIGHT","PATIENTS FOR YOUR CLINIC","Board Games","Comedy Night"]
}

def run():
    print("=============== Luma ===============")
    luma.fetch_events()

    print("=============== GDG HK ===============")
    gdg_hk.fetch_events()
    
    print("=============== hku ===============")
    hku.fetch_events(title_filter_words=title_filter_config["hku"])
    
    print("=============== Eventbrite next_month===============")
    eventbrite.fetch_events("next_month", title_filter_words=title_filter_config["eventbrite"])
    print("=============== Eventbrite this_month===============")
    eventbrite.fetch_events("this_month", title_filter_words=title_filter_config["eventbrite"])
    
    print("=============== CityU ===============")
    cityu.fetch_events()
    
    print("=============== CityU MBA ===============")
    cityu_mba.fetch_events()
    
    print("=============== PolyU ===============")
    polyu.fetch_events()
    
    print("=============== hkbu ===============")
    hkbu.fetch_events(title_filter_words=title_filter_config["hkbu"])

    print("=============== Meetup ===============")
    meetup.fetch_events(title_filter_words=title_filter_config["meetup"])

if __name__ == "__main__":
    run()

import cityu
import polyu
import eventbrite
import hku
import hkbu

def run():
    print("=============== CityU ===============")
    cityu.fetch_events()
    print("=============== PolyU ===============")
    polyu.fetch_events()
    print("=============== hku ===============")
    hku.fetch_events()
    print("=============== hkbu ===============")
    hkbu.fetch_events()
    
    print("=============== Eventbrite next_month===============")
    eventbrite.fetch_events("next_month")
    print("=============== Eventbrite this_month===============")
    eventbrite.fetch_events("this_month")
    

if __name__ == "__main__":
    run()

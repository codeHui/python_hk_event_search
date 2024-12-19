import cityu
import polyu
import eventbrite

def run():
    print("=============== CityU ===============")
    cityu.fetch_events()
    print("=============== PolyU ===============")
    polyu.fetch_events()
    print("=============== Eventbrite ===============")
    eventbrite.fetch_events()

if __name__ == "__main__":
    run()

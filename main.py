import cityu
import polyu

def run():
    print("=============== CityU ===============")
    cityu.fetch_events()
    print("=============== PolyU ===============")
    # Assuming the main logic in polyu.py is not encapsulated in a function
    # and runs when the script is executed.
    polyu.fetch_events()

if __name__ == "__main__":
    run()

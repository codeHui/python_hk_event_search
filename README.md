# HK Event Search

HK Event Search is a Python script that allows you to search for events from various universities and event platforms in Hong Kong with a single command. It filters out events that occur during working hours, saving you time and effort.

## Features

- Fetch events from CityU, PolyU, HKU, and Eventbrite.
- Filters out events during working hours.
- Filter out events by keywords in their titles by modifying `title_filter_words` in the code.
- Easy to use and extend.

## Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/codeHui/python_hk_event_search.git
cd python_hk_event_search
pip install requests-html beautifulsoup4 lxml
```

## Usage

Run the script to fetch and display events:

```bash
python main.py
```

The print result will be like
```
=============== CityU ===============
Title: CityUHK MBA Masterclass & Info Session in Shanghai (11 January 2025)
Date: 11 Jan 2025 (Sat)
Time: 2:30 PM - 5:30 PM
Venue: The Westin Bund Center Shanghai
URL: https://cap.cityu.edu.hk/postpublic.aspx?id=M10k0520e245412O738312
----------------------------------------
=============== PolyU ===============
Title: 30th Annual Graduate Education and Graduate Student Research Conference in Hospitality & Tourism
Start Date: 2025-01-02 08:00:00, Thursday
End Date  : 2025-01-04 18:00:00, Saturday
URL: https://www.polyu.edu.hk/en/events/2025/1/20250102-30th-Annual-Graduate-Education-and-Graduate-Student-Research-Conference

=============== hku ===============
Title: [GUIDED TOUR 導賞] Perckhammer’s Peking: A Photographic Documentation of China’s Capital City in the 1920s 京城舊影：1920年代奧地利攝影家佩克哈默的攝影紀錄
Date: 26 Jan - 26 Jan 2025 (Sunday)
Time: 15:30-15:50
Venue: Drake Gallery, 1/F Fung Ping Shan Building, University Museum and Art Gallery, The University of Hong Kong, 90 Bonham Road, Pokfulam, Hong Kong  
URL: http://hkuems1.hku.hk/hkuems/ec_hdetail.aspx?guest=Y&UEID=97992
----------------------------------------
=============== Eventbrite ===============
Title: HKU MBA Open House
Start Date: 2025-01-18 02:30:00, Saturday
End Date  : 2025-01-18 17:30:00, Saturday
URL: 8 Connaught Place, Hong Kong SAR China, HKI
URL: https://www.eventbrite.com/e/hku-mba-open-house-tickets-1118454901719
```

## Contributing

We welcome contributions! Please feel free to fork the repository, submit issues, and send pull requests. Join the discussion in the Discussions tab.

## License

This project is licensed under the MIT License.

## Acknowledgements

Thanks to all contributors and the open-source community for their support.

## Contact

For any questions or suggestions, please open an issue or start a discussion.

If you like this project, please give it a star!

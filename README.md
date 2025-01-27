# HK Event Search

python_hk_event_search allows you to search for Hong Kong events from various universities and event platforms with a single command. It filters out events that occur during working hours and the topics you are not interested in, saving you time and effort.

## Features

- Fetch events from Eventbrite, CityU, PolyU, HKU, and HKBU.
- Filters out events during working hours.
- Filter out topics by keywords in their titles by modifying `title_filter_config` in the `main.py`.
- Easy to use and extend.


## Usage

Run the script (see Installation below for detail):

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

## Installation

### To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/codeHui/python_hk_event_search.git
cd python_hk_event_search
```

### Conda Environment
To initialize the conda environment from the environment.yml file:
```bash
conda env create -f environment.yml
conda activate python_hk_event_search
python main.py
```
### If you are Running in VS Code  
Make sure you have selected the correct Python interpreter (e.g., python_hk_event_search),   
Show and Run Commands (Ctrl + SHift +P ) -> Python: Select Interpreter

### Other conda command you may need
> Note: If you see an error asking to run 'conda init' before 'conda activate', run:
```bash
conda init
```
then restart your shell.

> Windows PowerShell users may need to run:
```bash
conda init powershell
```
then close and reopen PowerShell, and run:
```bash
conda activate python_hk_event_search
```

> Updating the environment 
```bash
conda deactivate python_hk_event_search
conda env remove -n python_hk_event_search
conda env create -f environment.yml
conda activate python_hk_event_search
```


## Contributing

Please feel free give it a star, fork the repository, and send pull requests. Join the discussion in the Discussions tab.

## License

This project is licensed under the MIT License and free to use.

## Contact

For any questions or suggestions, please open an issue or start a discussion.

If you like this project, please give it a star!

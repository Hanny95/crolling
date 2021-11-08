import folium
import pandas as pd
import webbrowser

clinicGeoData = pd.read_csv('./resources/clinic_geo.shp.csv',
            encoding='cp949',
            engine='python')

clinic_map = folium.Map(location=[37.560284, 126.975334], zoom_start= 10)

clinic_icon = './resources/health-clinic.png'

for i, store in clinicGeoData.iterrows():
    folium.Marker(location = [store['위도'], store['경도']],
                  popup=store['name'],
                  icon=folium.Icon(color='beige', icon='star')).add_to(clinic_map)

clinic_map.save('C:/chh_scraping/map/clinic_map.html')


chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

url = 'C:/chh_scraping/map/clinic_map.html'

webbrowser.get(chrome_path).open(url)

# CoperDBAPI

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Framework.png)

- [CoperDBAPI](#coperdbapi)
    - [Example Usage](#example-usage)
    - [ProducerWave](#producerwave)
    - [ProducerWind](#producerwind)
    - [API](#api)
      - [Request](#request)
      - [Response](#response)

---

### Example Usage

In the same folder with docker-compose.yml

```sh
docker-compose up --build
```

To ensure there are no orphan containers, you can use

```sh
docker-compose up --build --remove-orphans
```

To run in background as deamon

```sh
docker-compose up --build --remove-orphans -d
```

When Docker is first launched, the following items are inserted into the respective collections of the database, so with the following request, if run locally, the following should be displayed.
```sh
http://localhost:5000/data?dateMin=2024-03-12T00:00:00&dateMax=2024-03-12T22:00:00&latitude=43.173814&longitude=27.917171&radius=20
```
```json
[
    {
        "waveData": [
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "12/03/2024 12:00:00",
                "vhm0": 0.6299999952316284,
                "vmdr": 86.0999984741211,
                "vtm10": 6.37999963760376
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "12/03/2024 15:00:00",
                "vhm0": 0.5999999642372131,
                "vmdr": 85.3499984741211,
                "vtm10": 6.019999980926514
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "12/03/2024 18:00:00",
                "vhm0": 0.550000011920929,
                "vmdr": 85.74000549316406,
                "vtm10": 6.159999847412109
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "12/03/2024 21:00:00",
                "vhm0": 0.5199999809265137,
                "vmdr": 87.05000305175781,
                "vtm10": 6.099999904632568
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "12/03/2024 12:00:00",
                "vhm0": 0.6299999952316284,
                "vmdr": 86.0999984741211,
                "vtm10": 6.37999963760376
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "12/03/2024 15:00:00",
                "vhm0": 0.5999999642372131,
                "vmdr": 85.3499984741211,
                "vtm10": 6.019999980926514
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "12/03/2024 18:00:00",
                "vhm0": 0.550000011920929,
                "vmdr": 85.74000549316406,
                "vtm10": 6.159999847412109
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "12/03/2024 21:00:00",
                "vhm0": 0.5199999809265137,
                "vmdr": 87.05000305175781,
                "vtm10": 6.099999904632568
            }
        ]
    },
    {
        "windData": [
            {
                "direction": 134.1752185718333,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.887032302336219,
                "time": "12/03/2024 00:00:00",
                "u10": -2.787826509766614,
                "v10": 2.708697744460926
            },
            {
                "direction": 131.65970101406833,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.0852380626135645,
                "time": "12/03/2024 01:00:00",
                "u10": -3.052105407717172,
                "v10": 2.7154783387849415
            },
            {
                "direction": 131.09734368420956,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.869301889604879,
                "time": "12/03/2024 02:00:00",
                "u10": -2.9158821788618625,
                "v10": 2.5434480989191988
            },
            {
                "direction": 131.56924028342664,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.4688136116430126,
                "time": "12/03/2024 03:00:00",
                "u10": -2.595208225425166,
                "v10": 2.3016433561708474
            },
            {
                "direction": 135.72998165508946,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.4990158458371106,
                "time": "12/03/2024 04:00:00",
                "u10": -2.4424554113411605,
                "v10": 2.5054986435896294
            },
            {
                "direction": 137.50480325283522,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.086868571286054,
                "time": "12/03/2024 05:00:00",
                "u10": -2.7607957762749824,
                "v10": 3.01338703134329
            },
            {
                "direction": 132.8101900444412,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.987847811702837,
                "time": "12/03/2024 06:00:00",
                "u10": -3.6591301170274493,
                "v10": 3.3896006519015573
            },
            {
                "direction": 136.6916005331812,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.005373427494936,
                "time": "12/03/2024 07:00:00",
                "u10": -4.119235983510908,
                "v10": 4.36994335384467
            },
            {
                "direction": 140.88500443190614,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.567891610711149,
                "time": "12/03/2024 08:00:00",
                "u10": -4.1435441970825195,
                "v10": 5.095904404212629
            },
            {
                "direction": 146.82139535213233,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.7572793998190175,
                "time": "12/03/2024 09:00:00",
                "u10": -3.697926025887741,
                "v10": 5.655631529217631
            },
            {
                "direction": 150.51258850832522,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.164192048273712,
                "time": "12/03/2024 10:00:00",
                "u10": -3.034214562528466,
                "v10": 5.365706439653688
            },
            {
                "direction": 155.17133068390297,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.089444165664456,
                "time": "12/03/2024 11:00:00",
                "u10": -2.556995713690593,
                "v10": 5.52658150821218
            },
            {
                "direction": 163.74414919744214,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.122976948356248,
                "time": "12/03/2024 12:00:00",
                "u10": -1.7139868670271134,
                "v10": 5.878188133239746
            },
            {
                "direction": 166.91125822854514,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 5.729231466181619,
                "time": "12/03/2024 13:00:00",
                "u10": -1.297441319263982,
                "v10": 5.580388805105978
            },
            {
                "direction": 162.77590219369836,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.843963877539972,
                "time": "12/03/2024 14:00:00",
                "u10": -1.434345178099297,
                "v10": 4.6267310227606036
            },
            {
                "direction": 167.60994338716006,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.090979120068913,
                "time": "12/03/2024 15:00:00",
                "u10": -0.8777843201636847,
                "v10": 3.9956982929288585
            },
            {
                "direction": 168.02186100041263,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.6401222410745815,
                "time": "12/03/2024 16:00:00",
                "u10": -0.7554653894713366,
                "v10": 3.5608653407952335
            },
            {
                "direction": 166.76931475702065,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 2.770198510562419,
                "time": "12/03/2024 17:00:00",
                "u10": -0.6340215544675665,
                "v10": 2.696667657757028
            },
            {
                "direction": 172.5546377476847,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 2.4564346322807227,
                "time": "12/03/2024 18:00:00",
                "u10": -0.31830647659947897,
                "v10": 2.4357241407070207
            },
            {
                "direction": 188.84602224762565,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 2.879656272951848,
                "time": "12/03/2024 19:00:00",
                "u10": 0.442832306754814,
                "v10": 2.8454032751870404
            },
            {
                "direction": 211.24631336524436,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.105333881060079,
                "time": "12/03/2024 20:00:00",
                "u10": 1.6107933524435936,
                "v10": 2.6548904475671273
            },
            {
                "direction": 237.71925301942457,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 2.635802543730374,
                "time": "12/03/2024 21:00:00",
                "u10": 2.2284164428710938,
                "v10": 1.4076985496466392
            },
            {
                "direction": 257.8136366662268,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 1.6348963362448974,
                "time": "12/03/2024 22:00:00",
                "u10": 1.5980558485320695,
                "v10": 0.3451138004186962
            }
        ]
    },
    {
        "weatherData": [
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99950.41054316147,
                "sea_temp": 281.2021484375,
                "temperature": 281.5177712119097,
                "time": "12/03/2024 03:00:00",
                "total_cloud_cover": 99.15631044097071,
                "total_rain_water": 0.0,
                "total_snow_water": 0.17701392405935334
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99935.4852917614,
                "sea_temp": 281.2021484375,
                "temperature": 281.31876428649036,
                "time": "12/03/2024 04:00:00",
                "total_cloud_cover": 99.75108381053175,
                "total_rain_water": 0.0007095979682254956,
                "total_snow_water": 0.3757753792188977
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99927.18011154686,
                "sea_temp": 281.2021484375,
                "temperature": 281.74651765295835,
                "time": "12/03/2024 05:00:00",
                "total_cloud_cover": 97.56940662048655,
                "total_rain_water": 0.01694375820115836,
                "total_snow_water": 0.3873937129974365
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99870.51832044544,
                "sea_temp": 281.2021484375,
                "temperature": 282.3270990858546,
                "time": "12/03/2024 06:00:00",
                "total_cloud_cover": 96.00269883971582,
                "total_rain_water": 0.038085244596004486,
                "total_snow_water": 0.21331543109448903
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99864.04870542322,
                "sea_temp": 281.2021484375,
                "temperature": 282.75790901365116,
                "time": "12/03/2024 07:00:00",
                "total_cloud_cover": 99.97576475234386,
                "total_rain_water": 0.011639498859639844,
                "total_snow_water": 0.05470897415359971
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99830.13588621381,
                "sea_temp": 281.2021484375,
                "temperature": 282.80326177498586,
                "time": "12/03/2024 08:00:00",
                "total_cloud_cover": 100.0,
                "total_rain_water": 0.009748399933672795,
                "total_snow_water": 0.07182402959031176
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99814.2477153686,
                "sea_temp": 281.2021484375,
                "temperature": 282.70470832458096,
                "time": "12/03/2024 09:00:00",
                "total_cloud_cover": 99.96415202950864,
                "total_rain_water": 0.017325581186518023,
                "total_snow_water": 0.12507858342381334
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99814.18753290328,
                "sea_temp": 281.2021484375,
                "temperature": 282.6417596831657,
                "time": "12/03/2024 10:00:00",
                "total_cloud_cover": 97.21042201458002,
                "total_rain_water": 0.016389330304608707,
                "total_snow_water": 0.21877165059307574
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99727.49469160577,
                "sea_temp": 281.2021484375,
                "temperature": 283.299002978573,
                "time": "12/03/2024 11:00:00",
                "total_cloud_cover": 98.79833563704985,
                "total_rain_water": 0.01130591226360263,
                "total_snow_water": 0.0784027375117254
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99666.6502191644,
                "sea_temp": 281.2021484375,
                "temperature": 283.5878893290053,
                "time": "12/03/2024 12:00:00",
                "total_cloud_cover": 91.92057431263517,
                "total_rain_water": 0.008643612269793459,
                "total_snow_water": 0.05719117793397477
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99644.77389301955,
                "sea_temp": 281.2021484375,
                "temperature": 283.90048468217543,
                "time": "12/03/2024 13:00:00",
                "total_cloud_cover": 95.47760180716618,
                "total_rain_water": 0.008104875728806533,
                "total_snow_water": 0.09092369084676423
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99551.31052437323,
                "sea_temp": 281.2021484375,
                "temperature": 284.05760845641686,
                "time": "12/03/2024 14:00:00",
                "total_cloud_cover": 93.51858595496174,
                "total_rain_water": 0.0051386283661341865,
                "total_snow_water": 0.06507752700775385
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99533.88770066226,
                "sea_temp": 281.2021484375,
                "temperature": 284.25578928417985,
                "time": "12/03/2024 15:00:00",
                "total_cloud_cover": 94.0371192746045,
                "total_rain_water": 0.0015005585208503133,
                "total_snow_water": 0.04808976407259949
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99524.7399659332,
                "sea_temp": 281.2021484375,
                "temperature": 283.9519505661672,
                "time": "12/03/2024 16:00:00",
                "total_cloud_cover": 87.53399448687428,
                "total_rain_water": 0.0010245874021142937,
                "total_snow_water": 0.029250473842060476
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99543.66735127722,
                "sea_temp": 281.2021484375,
                "temperature": 282.9353547902393,
                "time": "12/03/2024 17:00:00",
                "total_cloud_cover": 84.16882936962102,
                "total_rain_water": 0.00016679329801860474,
                "total_snow_water": 0.015005285713194677
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99542.43361073811,
                "sea_temp": 281.2021484375,
                "temperature": 282.68686461520343,
                "time": "12/03/2024 18:00:00",
                "total_cloud_cover": 72.84137559534092,
                "total_rain_water": 0.00016679329801860474,
                "total_snow_water": 0.008218280971050235
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99544.3895408611,
                "sea_temp": 281.2021484375,
                "temperature": 282.1433749670781,
                "time": "12/03/2024 19:00:00",
                "total_cloud_cover": 73.12664465629337,
                "total_rain_water": 0.0,
                "total_snow_water": 0.027919688598502745
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99559.01387993454,
                "sea_temp": 281.2021484375,
                "temperature": 281.8910021330573,
                "time": "12/03/2024 20:00:00",
                "total_cloud_cover": 78.41144334830986,
                "total_rain_water": 0.0,
                "total_snow_water": 0.036552434613233764
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99508.67124769201,
                "sea_temp": 281.2021484375,
                "temperature": 281.64631200724074,
                "time": "12/03/2024 21:00:00",
                "total_cloud_cover": 87.46482305085573,
                "total_rain_water": 0.0,
                "total_snow_water": 0.027653531549791194
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99459.53226475594,
                "sea_temp": 281.248046875,
                "temperature": 281.56824577871384,
                "time": "12/03/2024 22:00:00",
                "total_cloud_cover": 90.48362608702335,
                "total_rain_water": 0.0,
                "total_snow_water": 0.02499774708547381
            }
        ]
    }
]
```
![Sublime's custom image](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-24%20at%205.32.18%20PM.png)

### ProducerWave

The first time it will pull data from Copernicus is when the docker compose is first uploaded. After that, it will retrieve data every 3 hours. Duplicates do not exist because the time range for pulling data from Copernicus is: `current_time - 3 hours + 1 second`

Copernicus updates information every 3 hours starting at 00:00. If the program starts at 05:00 o'clock, that means that the first time it retrieves data is at: `5 - (5%3) = 2` --> 02:00 o'clock.

We obtain the information as a .nc file from Copernicus, refactor it into JSON, and push it into the Kafka topic `wave_topic` and into MongoDB in a collection named `waveData` with the following format:

```json
{
  "time": "Fri, 26 Jan 2024 01:00:00 GMT",
  "latitude": 35,
  "longitude": 18.916666666666657,
  "vhm0": 0.25999999046325684,
  "vmdr": 322.69000244140625,
  "vtm10": 3.4600000381469727
}
```

The information is analyzed below:

| Variable | Description                  | Unit |
|----------|------------------------------|------|
| vhm0     | Significant Wave Height      |meters|
| vmdr     | Wave Direction               |      |
| vtm10    | Wave Period Mean Value       |      |

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-25%20at%208.24.36%20AM.png)

The horizontal resolution is: `0.083° x 0.083°`

---

### ProducerWind

The first time it will pull data from Copernicus is when the docker compose is first uploaded. After that, it will retrieve data every day. The earliest data that we can get from Copernicus is from 6 days ago. The available time values are as follows:

```json
'time': [
  '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
  '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
  '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
  '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',
]
```

We obtain the information as a .nc file from Copernicus, refactor it into JSON, and push it into the Kafka topic `wind_topic` and into MongoDB in a collection named `windData` with the following format:

```json
{
  "time": "Fri, 26 Jan 2024 01:00:00 GMT",
  "latitude": 50.150001525878906,
  "longitude": -27.1200008392334,
  "u10": -4.6063704822533245,
  "v10": -0.529921079222938,
  "speed": 4.636751596751709,
  "direction": 83.43748990096958
}
```
We add some extra features at the .nc file from Copernicus, refactor it into JSON, and push it into the Kafka topic `weather_topic` and into MongoDB in a collection named `weatherData` with the following format:

```json
    {
        "humidity": 96.38448804707079,
        "latitude": 43.24399948120117,
        "longitude": 27.92099952697754,
        "pressure": 102227.77759296843,
        "sea_temp": 279.388671875,
        "temperature": 273.9269860137408,
        "time": "Wed, 31 Jan 2024 00:00:00 GMT",
        "total_cloud_cover": 59.96673923146837,
        "total_rain_water": -1.3552527156068805e-20,
        "total_snow_water": 0.0008333513378112866,
        "wind_direction": 359.40557106573124,
        "wind_speed": 5.3438242696397555
    }
```
The information is analyzed below:

| Variable           | Description                                                                                                         |  Unit  |
|--------------------|---------------------------------------------------------------------------------------------------------------------|--------|
| u10                | East Wind Component                                                                                                 |  m/s   |
| v10                | North Wind Component                                                                                                |  m/s   |
| direction / wind_direction | The Direction Of The Wind                                                                                   |   ˚    |
| speed / wind_speed | Combination of the above two components                                                                             |  m/s   |
| temperature        | The temperature of air at 2m above the surface of land, sea or in-land waters                                       |   K    |
| sea_temp           | The temperature of the sea                                                                                          |   K    |
| humidity           | A Combination of temperature, dewpoint temperature and pressure                                                     |   %    |
| sea_temp           | This parameter is the temperature of sea water near the surface                                                     |   K    |
| pressure           | Pressure                                                                                                            |   Pa   |
| total_cloud_cover  | This parameter is the proportion of a grid box covered by cloud                                                     |   %    |
| total_rain_water   | Water in droplets of raindrop size in a column extending from the surface of the Earth to the top of the atmosphere | kg/m^2 |
| total_snow_water   | Snow in a column extending from the surface of the Earth to the top of the atmosphere                               | kg/m^2 |

Speed information:

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-25%20at%208.25.32%20AM.png)

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-25%20at%208.25.44%20AM.png)

The horizontal resolution is: `0.25° x 0.25°`

---

### API

#### Request

`GET /data?dateMin=2023-07-19T04:00:00&dateMax=2023-07-19T07:00:00&latitude=35&longitude=18&radius=20`

Users must provide 5 variables: `dateMin`, `dateMax`, `latitude`, `longitude`, `radius`.

![CoperDBAPI](https://github.com/ArtemisStefanidou/APIs/blob/main/photos/Screenshot%202023-07-25%20at%2011.53.06%20AM.png)

#### Response

If the user provides a date older or newer than those in the collections, an empty list is returned.

When a valid date is provided, we check if data exists for the specified latitude and longitude. If data exists, information from both collections is returned.

```json
[
  {
    "waveData": [
      {
                "time": "26/01/2024 01:00:00",
                "latitude": 35,
                "longitude": 18.916666666666657,
                "vhm0": 0.25999999046325684,
                "vmdr": 322.69000244140625,
                "vtm10": 3.4600000381469727
      },
      {...}
    ]
  },
  {
    "windData": [
      {
                "direction": 84.4351874836367,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 0.09072748381317144,
                "time": "31/01/2024 20:00:00",
                "u10": -0.0902998980297362,
                "v10": -0.008797996072318348
      },
      {...}
    ]
  }
  {
    "weatherData": [
      {
                "humidity": 96.38448804707079,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 102227.77759296843,
                "sea_temp": 279.388671875,
                "temperature": 273.9269860137408,
                "time": "31/01/2024 00:00:00",
                "total_cloud_cover": 59.96673923146837,
                "total_rain_water": -1.3552527156068805e-20,
                "total_snow_water": 0.0008333513378112866
      },
      {...}
    ]
   }
]
```

If not, an empty list is returned.

#### Requests

The AIS data we receive is divided into two categories: static, which includes messages of type 24 and 5, and dynamic, which includes types 1, 2, 3, and 18. These data are stored in the respective Kafka topics and collections in our database: ais_cyprus_dynamic for dynamic data and ais_cyprus_static for static data.

`GET /ais_static?dateMin=2024-04-25T10:04:08&dateMax=2024-04-25T12:04:08`

`GET /ais_cyprus_dynamic?dateMin=2024-01-31T00:00:00&dateMax=2024-01-31T14:00:00`

Users must provide 2 variables: `dateMin`, `dateMax`.


#### Response

The two most recent hours will be displayed.

```json
For static
[
    {
        "_id": {
            "$oid": "662a2a994da5c77d915f3db5"
        },
        "ais_type": 24,
        "bow": 20,
        "call_sign": "P3AY8",
        "destination": null,
        "draught": null,
        "imo": null,
        "mmsi": 212983012,
        "port": 4,
        "ship_name": null,
        "ship_type": 60,
        "starboard": 4,
        "stern": 4,
        "timestamp": "25/04/2024 10:04:09"
    },
    {
        "_id": {
            "$oid": "662a2a9b4da5c77d915f3dc5"
        },
        "ais_type": 24,
        "bow": 15,
        "call_sign": "MCTA7",
        "destination": null,
        "draught": null,
        "imo": null,
        "mmsi": 232014380,
        "port": 4,
        "ship_name": null,
        "ship_type": 36,
        "starboard": 0,
        "stern": 0,
        "timestamp": "25/04/2024 10:04:11"
    },
    {
        "_id": {
            "$oid": "662a2a9f4da5c77d915f3df4"
        },
        "ais_type": 24,
        "bow": null,
        "call_sign": null,
        "destination": null,
        "draught": null,
        "imo": null,
        "mmsi": 232050147,
        "port": null,
        "ship_name": "LADY LUCK 2",
        "ship_type": null,
        "starboard": null,
        "stern": null,
        "timestamp": "25/04/2024 10:04:15"
    },
    {
        "_id": {
            "$oid": "662a2aa04da5c77d915f3df9"
        },
        "ais_type": 24,
        "bow": 6,
        "call_sign": "METI3",
        "destination": null,
        "draught": null,
        "imo": null,
        "mmsi": 232020668,
        "port": 2,
        "ship_name": null,
        "ship_type": 37,
        "starboard": 2,
        "stern": 5,
        "timestamp": "25/04/2024 10:04:16"
    }
...
]
```


```json
For dynamic
[
    {
        "_id": {
            "$oid": "65ba3aad5ee1c64a559eb046"
        },
        "ais_type": 18,
        "cog": 162.4,
        "heading": 511,
        "latitude": 34.64899166666667,
        "longitude": 32.694395,
        "mmsi": 0,
        "nav_status": null,
        "sog": 0.1,
        "timestamp": "31/01/2024 12:18:53"
    },
    {
        "_id": {
            "$oid": "65ba3aad5ee1c64a559eb047"
        },
        "ais_type": 18,
        "cog": 41.300000000000004,
        "heading": 511,
        "latitude": 35.052238333333335,
        "longitude": 33.98875666666667,
        "mmsi": 0,
        "nav_status": null,
        "sog": 0.2,
        "timestamp": "31/01/2024 12:18:53"
    },
    {
        "_id": {
            "$oid": "65ba3aae5ee1c64a559eb048"
        },
        "ais_type": 18,
        "cog": 162.4,
        "heading": 511,
        "latitude": 34.64899,
        "longitude": 32.694395,
        "mmsi": 0,
        "nav_status": null,
        "sog": 0.2,
        "timestamp": "31/01/2024 12:18:54"
    }
]
```



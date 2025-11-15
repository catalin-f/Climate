#!/usr/bin/python3
import time
import board
import adafruit_dht
import json
import requests
import paho.mqtt.publish as pub



dhtDevice = adafruit_dht.DHT22(board.D4)
data = {"temp":0, "hum":0, "out_temp":0, "out_nebulozitate":" ", "out_presiune":" ", "out_hum":0, "setTemp":15, "modeType":"", "heat":"off", "auto":"off"} 



def heat_stop(state, temp_val, temp_set):
    print(state, temp_val, temp_set)
    if (state =="on"):
        if temp_val > (temp_set +1):
            #relay connected in the opposote way
            pub.single("eu/releu", "ON", hostname="localhost", port = 1883)


def get_anm(oras):
    url = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        for i in data["features"]:
            if i["properties"]["nume"]==oras:
                print(oras)
                print(i["properties"]["tempe"])
                return i["properties"]["tempe"], i["properties"]["umezeala"], i["properties"]["nebulozitate"],i["properties"]["presiunetext"]
    except requests.exceptions.RequestException as e:
     print(f"Error fetching data: {e}")


def get_temp():
    count =0
    temp_data=0
    data["out_temp"], data["out_hum"], data["out_nebulozitate"], data["out_presiune"]=get_anm("BUCURESTI FILARET")
    while True:
        try:
            # Print the values to the serial port
            with open("/home/pi/work/centrala/temp.json","r") as f:
              temp_data = json.load(f)
            temperature_c = dhtDevice.temperature
            heat_stop(temp_data["heat"], temperature_c, temp_data["setTemp"])
            data["temp"]= temperature_c
            humidity = dhtDevice.humidity
            data["hum"]=humidity 
            if (len(temp_data)!=0):
                data["setTemp"] = temp_data["setTemp"]
                if len(temp_data["modeType"]):
                    data["modeType"] = temp_data["modeType"]
            with  open("temp.json", "w") as f:
                json.dump(data,f)
            print(f"Temp:  {temperature_c:.1f} C    Humidity: {humidity}% ")
            
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(60.0)
            continue
            #except Exception as error:
            #    dhtDevice.exit()
            #     raise error
        if count >10:
            data["out_temp"], data["out_hum"], data["out_nebulozitate"],data["out_presiune"]=get_anm("BUCURESTI FILARET")
            count =0
        count = count +1
        time.sleep(300.0)

if __name__=='__main__':
    adafruit_dht.DHT22(board.D4).exit()
    temp_file=0
    with open("/home/pi/work/centrala/temp.json", "r") as f:
        temp_file=json.load(f)
        print(temp_file["heat"])
    if len(temp_file)==0:
        with open("/home/pi/work/centrala/temp.json","w") as f2:
            json.dump(data,f2)
    get_temp()

from tkinter import *
from datetime import datetime
# from PIL import ImageTk,Image
import requests
import json 


root = Tk()
root.title("weather-statation")
root.iconbitmap("./assets/icons8-surf-16.ico")
root.geometry("900x300")
root.config(background="green")

current_area = "Snowdon Summit - 3308"

# //gets the value of the select list 
def handle_value(value):
    global current_area
    value = default.get()
    current_area = value


# gets the snowdonia weather locations 
try:
    locations_api_request = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=5275bfb9-bbc4-4e89-9515-3ea51fc7b58a")
    locations_api = json.loads(locations_api_request.content)
    LOCATIONS=[]
    for location in locations_api["Locations"]["Location"]:
        #only get national parks
        if location.get("nationalPark") == 'Snowdonia National Park':
            LOCATIONS.append(location["name"] +" - " + location["id"])
        else:
           pass

    default = StringVar(root)
    default.set("Snowdon Summit - 3308")
    #add locations to list
    area = OptionMenu(root, default, *LOCATIONS, command=handle_value)
    area.grid(row=0, column=0)

except Exception as e:
    print("Error!")



# when button is clicked fetches data on the area 
def checkArea():
    try:
        #split value of weatherstation and return id
        area_id = str(current_area).split(" ").pop()

        #get current time in iso format 
        current_time = datetime.now().isoformat("T", "hours") 
       
        #use id in api key
        area_api_request = requests.get(f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{area_id}?res=3hourly&key=5275bfb9-bbc4-4e89-9515-3ea51fc7b58a")
        area_api_response = json.loads(area_api_request.content)
        response_key = area_api_response["SiteRep"]["Wx"]["Param"]
        response_area = area_api_response["SiteRep"]["DV"]["Location"]
        
      
       
        
        location = response_area.get("name")
        elevation = response_area.get("elevation")
        temp = response_area["Period"][0]["Rep"][0]["T"]
        feel_like_temp = response_area["Period"][0]["Rep"][0]["F"]
        wind_speed = response_area["Period"][0]["Rep"][0]["S"]
        percip_percent = response_area["Period"][0]["Rep"][0]["Pp"]
        vis = response_area["Period"][0]["Rep"][0]["V"]

        forcast = f'{location} | elevation {elevation}m '
        
        als_tip = "Al's top tip: "
        if (int(feel_like_temp) >= 0 and int(feel_like_temp) < 25) and int(percip_percent) < 10 and (vis =="EX" or vis == "VG"):
            als_tip += " PERFECT!!! Get out there now"
            als_color = "green"
        elif (int(percip_percent) > 60) and int(temp) < 5 and (vis !="EX" and vis != "VG" and vis != "GO"):
            als_tip += " Horrible conditions!! Go if you want a miserable time!!"
            als_color = "red"
        else: 
            als_tip += " double check but should be OK"
            als_color = "#FFBF00"
    

        temp_warning = f"Feels like {feel_like_temp}C || "
        if int(feel_like_temp) >= 0 and int(feel_like_temp) < 15:
             temp_warning += "be bold start cold"
             temp_color = "orange"
        elif int(feel_like_temp) < 0:
             temp_warning += "put on some layers"
             temp_color = "#C8E9E9"
        elif int(feel_like_temp) >= 15:
            temp_color = "red"
            temp_warning += "shorts and t-shit, bring water!!!"
        
        rain_warning = f"{percip_percent}% chance of rain || "
        if int(percip_percent) < 10:
            rain_warning += " dont bother with a coat"
            rain_color = "#FFE87C"
        elif int(percip_percent) >= 10 and int(percip_percent) < 50:
            rain_warning += " I would risk not bringing a coat"
            rain_color = "#AFBFD6"
        elif int(percip_percent) >= 50:
            rain_warning += " definatley bring a coat!!" 
            rain_color =  "#243492"
        
        wind_warning = f"{wind_speed}mph wind || "
        if int(wind_speed) < 8:
            wind_warning += " not scary"
            wind_color = "green"
        elif int(wind_speed) >= 8 and int(wind_speed) < 20:
            wind_warning += " watch out for wind"
            wind_color = "#FFBF00"
        elif int(wind_speed) >= 20:
            wind_warning += " wooooah! Stay low to the ground!!!"
            wind_color = "red"


        vis_warning = f"vis is {vis} || "
        if vis == "VP": 
            vis_color = "#0E4D64"
            vis_warning += " wont see a bloody thing!!"
        elif vis == "OP":
            vis_color = "#0E4D64"
            vis_warning += " stay at home if you want veiws...."
        elif vis == "MO":
            vis_color = "#137177"
            vis_warning += " you might see something"
        elif vis == "GO":
            vis_color = "#39A96B"
            vis_warning += " nice veiws"
        elif vis == "VG":
            vis_color = "#BFE1B0"
            vis_warning += " profile picture day"
        elif vis == "EX":
            vis_color = "#99D492"
            vis_warning += " amazing veiw, get out there!!!"
        else:
            vis_color = "grey"
            vis_warning += " who knows"
        
        root.config(background=als_color)
            
        
        forcast_label = Label(root, text=forcast, font=("Helvetica", 16))
        forcast_label.grid(row=0, column=2, sticky="W" )
        als_tip_label = Label(root, text=als_tip, font=("Helvetica", 16), background=als_color)
        als_tip_label.grid(row=1, column=0, columnspan=2, sticky="W", pady=10, )

        temp_warning_label = Label(root, text=temp_warning, font=("Helvetica", 16), background=temp_color )
        temp_warning_label.grid(row=4, column=0, columnspan=2, sticky="W", pady=3)
        rain_warning_label = Label(root, text=rain_warning, font=("Helvetica", 16), background=rain_color )
        rain_warning_label.grid(row=5, column=0, columnspan=2, sticky="W", pady=3)
        wind_warning_label = Label(root, text=wind_warning, font=("Helvetica", 16), background=wind_color )
        wind_warning_label.grid(row=6, column=0, columnspan=2, sticky="W", pady=3)
        vis_warning_label = Label(root, text=vis_warning, font=("Helvetica", 16), background=vis_color )
        vis_warning_label.grid(row=7, column=0, columnspan=2, sticky="W", pady=3)
    except Exception as e:
        print("Error!")
        

submit_area = Button(root, text="check weather", command=checkArea)
submit_area.grid(row=0, column=1, sticky="W")

root.mainloop()

#https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=89129&distance=5&API_KEY=A3305BCC-EB0F-432D-B3FB-87ADCBF5E47A



# 5275bfb9-bbc4-4e89-9515-3ea51fc7b58a
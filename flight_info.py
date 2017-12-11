import json
import requests
from datetime import datetime
from enum import Enum
import argparse

info_type = Enum('info_type', 'arrival departure')
url_departure="https://api.laminardata.aero/v1/aerodromes/VIDP/departures?user_key=9d674a1c8ba9c96de6ec62d513a2cb93"
url_arrival="https://api.laminardata.aero/v1/aerodromes/VIDP/arrivals?user_key=9d674a1c8ba9c96de6ec62d513a2cb93"

def parseFlighStatData(url,data_file, verbose, chosen_info_type):
    
    # try retrieving live flight data from API first, otherwise use sample json files.
    response=requests.get(url,headers={"accept":"application/json"})
    flight_data=None
    
    if(response.status_code==200):
        flight_data=response.json()
        print("API works")
    else:
        print("API does not work, parsing from sample file instead")
        with open(data_file) as file:
            flight_data = json.load(file)
    
    #stores the data of flights arriving or departing betweeb 1200 and 1800 IST, keyed by date     
    parsed_data={}
    if(flight_data!=None):
        for item in flight_data['features']:
            try:
                #flight arrival or departure time
                time = item['properties'][chosen_info_type.name]['runwayTime']['initial']
            except KeyError:
                continue
            time = time.replace('T', ' ').replace('Z', '')
            day = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").day
            hour = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").hour
            minute = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").minute
            
            #API uses UTC time, therefore between 0630 and 1230 UTC (IST=UTC+530)
            if( ((hour==6 and minute>=30) or (hour >= 7)) and ((hour < 12) or (hour == 12 and minute <= 29)) ):
                if(day not in parsed_data):
                    parsed_data[day]=[]
                try:
                    airline=item['properties']['airline']
                except KeyError:
                    pass
                arrival=item['properties']['arrival']['aerodrome']['scheduled']
                departure=item['properties']['departure']['aerodrome']['scheduled']
                parsed_data[day].append({ 'arrival':arrival , 'departure':departure,  
                                       'airline':airline, 'time':time})
        
        #print the number of flights between out interval keyed by date
        for key in parsed_data.keys():
            num=len(parsed_data[key])
            print("No. of flight {0} or scehduled on {1} Dec on delhi airport in our interval is {2}".format(chosen_info_type.name,key,num))
        
        #print the flight info as well
        if(verbose):
            for key in parsed_data.keys():
                num=len(parsed_data[key])
                print("Flight scheddule for {0} Dec".format(key))
                for flight in parsed_data[key]:
                    print("Departure: {} Arrival:{} Airline:{} Time:{}"
                          .format(flight["departure"],flight["arrival"],flight["airline"],flight["time"]))    

def getCommandLineParser():
    parser = argparse.ArgumentParser(description='FlightInfo')
    parser.add_argument('--t',required=False,default="arrival",
        help='--t arrival for displaying arrival, --t departure for displaying departure')
    parser.add_argument('--v',required=False,default="true",
        help='--v true for detailed flight output, false for just count')
    return parser

def printDelhiArrival(verbose):
    parseFlighStatData(url_arrival,"data_arrival.json",verbose,info_type.arrival)

def printDelhiDeparture(verbose):
    parseFlighStatData(url_departure,"data_departure.json",verbose,info_type.departure)


if __name__ == '__main__':

    # Command Line Argumnent
    #    --t arrival for displaying flight arrivals, --t departure for displaying fligh departures (default=arrival)
    #    --v true for displaying flight info, false for just displaying counts (default= true)
    parser=getCommandLineParser()
    args = parser.parse_args()
    
    if(args.t=="arrival"):
        printDelhiArrival(args.v == "true")
    elif(args.t=="departure"):
        printDelhiDeparture(args.v == "true")

# delhiAirportFlightChart

## Requirements
Python3
</br>
Python Requests library

## Usage
To display detailed flight info for only arrival flights
```shell
python3 flight_info.py
python3 flight_info.py --t arrival --v true
```
To display detailed flight info for only departure flights
```shell
python3 flight_info.py --t departure --v false
```
*The data is only for Delhi Aiport between 1200 and 1800 IST

## Example
```
No. of flight arrival or scehduled on 12 Dec on delhi airport in our interval is 191
No. of flight arrival or scehduled on 13 Dec on delhi airport in our interval is 193
No. of flight arrival or scehduled on 14 Dec on delhi airport in our interval is 4
Flight scheddule for 12 Dec
Departure: VISR Arrival:VIDP Airline:IGO Time:2017-12-12 11:15:00
.
.
Flight scheddule for 13 Dec
Departure: VABB Arrival:VIDP Airline:GOW Time:2017-12-14 06:35:00
.
.
Flight scheddule for 14 Dec
Departure: VICG Arrival:VIDP Airline:JAI Time:2017-12-14 06:50:00
.
.
```
## API
We used the flight departure and arrival API from Laminar data available at <br>
https://developer.laminardata.aero/documentation/flightdata <br>
It provides only the current data (+/- 1 day)

The only source for accurate historical flight info at delhi airport we found was at <br>
https://developer.flightstats.com/api-docs/historical-flight-status/v3 <br>
However, the use of this API is not free.

The same provider also provides scehduled flight data at <br>
https://developer.flightstats.com/api-docs/scheduledFlights/v1 <br>
However, the request for API key has not been approved for this.

There were some other possible options too, for instance, <br>
https://www.flightstats.com/go/FlightStatus/flightStatusByFlight.do <br>
provides data of airport upto +/- 3 days, however, our used API was still a convenient option than scrapping the data from this website






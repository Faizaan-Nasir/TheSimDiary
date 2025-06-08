
from __future__ import print_function

from metar import Metar
def giveWeather(info):
    print(info)
    code = info
    summary=""
    temp=""
    obs = Metar.Metar(code)
    print(obs)
    if obs.time:
        temp+="Time: "+obs.time.ctime()

    if obs.temp:
        summary+=" Temperature: "+obs.temp.string("C")+"|"

    if obs.dewpt:
        summary+=" Dew Point: "+obs.dewpt.string("C")+"|"

    if obs.wind_speed:
        summary+=" Winds: "+str(obs.wind_dir)+" at "+str(obs.wind_speed)+"|"
    
    if obs.wind_gust:        
        summary=summary.rstrip("|")+" gusting "+str(obs.wind_gust)+"|"

    if obs.wind_speed_peak:
        print()
    if obs.vis:
        summary+=" Visibility: "+obs.visibility()+"|"

    if obs.runway:
        summary+=" Visual Range: "+obs.runway_visual_range()+"|"

    if obs.press:
        summary+=" Pressure: "+obs.press.string("hpa")+"|"

    if obs.precip_1hr:
        summary+=" Precipitation: "+obs.precip_1hr.string("in")+"|"

    if obs.present_weather():
        summary+=" Weather: "+obs.present_weather()+"|"

    if obs.sky_conditions():
        summary+=" Sky: "+obs.sky_conditions(" ")+"|"

    if obs._remarks:
        summary+=" Remarks: "+obs.remarks(" ")
    
    return summary.strip("| ")
def giveTime(info):
    obs=Metar.Metar(info)
    return (obs.time.time())

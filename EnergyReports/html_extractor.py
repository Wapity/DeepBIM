import re

"""Extactor of heating/cooling load and parameters for one building from html Revit 'detailed' report"""

def html_single_extractor(text, get_keys = False):
    dict_result = {}
    index_temp = 0
    index_cool = 0
    index_heat = 0
    wall_area = []
    door_area = []

    # Unique conditions for parameter and not particular to a building

    for i in range(len(text)):
        #Latitude
        if 'Latitude' in text[i]:
            dict_result['Latitude'] = int(re.findall(r'\d+', text[i+1])[0])
        #Longitude
        elif "Longitude" in text[i] :
            dict_result['Longitude'] = int(re.findall(r'\d+', text[i+1])[0])
        #Mean daily_range
        elif text[i]=='Range':
            dict_result['Mean_daily_range'] = int(re.findall(r'\d+', text[i+1])[0])
        #Area
        elif 'Family' in text[i] and 'Area' in text[i]:
            dict_result['Area'] = int(re.findall(r'\d+', text[i+1])[0])
        #Humidity
        elif 'Humidity' in text[i]:
            dict_result['Relative_humidity'] = int(re.findall(r'\d+', text[i])[0])
        #Supply air temperature
        elif text[i]=='Temperature' and index_temp==0 : #first temperature for supply air temperature
            dict_result['Supply_air_temperature'] = int(re.findall(r'\d+', text[i+1])[0])
            index_temp+=1
        #Wall Area
        elif 'Wall' in text[i] and text[i+1] == 'Area':
            wall_area.append(int(re.findall(r'\d+', text[i+2])[0]))
        #Door Area
        elif 'Door' in text[i] and text[i+1] == 'Area':
            door_area.append(int(re.findall(r'\d+', text[i+2])[0]))

        #Peak cooling total load
        elif text[i]=='Total' and text[i+1] == 'Load' and index_cool ==0:
            dict_result['Cooling_load'] = int(re.findall(r'\d+', text[i+2])[0]+re.findall(r'\d+', text[i+2])[1])
            index_cool+=1
        #Peak heating load
        elif text[i]=='Heating' and text[i+1] == 'Load' and index_heat ==0:
            dict_result['Heating_load'] = int(re.findall(r'\d+', text[i+2])[0]+re.findall(r'\d+', text[i+2])[1])
            index_heat+=1

    dict_result['Wall_area'] = sum(wall_area)
    dict_result['Door_area'] = sum(door_area)


    keys = list(dict_result.keys())
    items = list(dict_result.values())
    # print(keys)

    if get_keys :
        return keys, items

    return items

import urllib.request
import xml.etree.ElementTree as ElementTree


def fetch_departures_from_station():
    response = urllib.request.urlopen("http://www2.vvs.de/widget/XML_DM_REQUEST?locationServerActive=1"
                                      "&lsShowTrainsExplicit=1&stateless=1&language=de&SpEncId=0"
                                      "&anySigWhenPerfectNoOtherMatches=1&limit=10&depArr=departure&type_dm=any"
                                      "&anyObjFilter_dm=2&deleteAssignedStops=1&name_dm=5006027&mode=direct").read()
    tree = ElementTree.fromstring(response)
    departures = tree.findall('./itdDepartureMonitorRequest/itdDepartureList/itdDeparture')
    departures = sorted(departures, key=lambda x: (-int(x.get('platform')), int(x.get('countdown'))))

    counter_platform_1 = 0
    counter_platform_2 = 0
    departure_list = []

    for departure in departures:
        countdown = departure.get('countdown')
        line_info = departure.find('itdServingLine')
        line = line_info.get('number')
        destination = line_info.get('direction')

        platform = int(departure.get('platform'))

        if platform == 1:
            counter_platform_1 += 1
            if counter_platform_1 <= 3:
                departure_list.append(_construct_departure_string(line, destination, countdown))
        elif platform == 2:
            counter_platform_2 += 1
            if counter_platform_2 <= 3:
                departure_list.append(_construct_departure_string(line, destination, countdown))

    return departure_list


def _construct_departure_string(line, destination, countdown):
    minute_string = 'Minute' if countdown == '1' else 'Minuten'
    if destination == 'Flughafen/Messe':
        destination = 'Flughafen'
    return line + ' ' + destination + '\n\r' + countdown + ' ' + minute_string

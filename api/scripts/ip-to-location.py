import geoip2.database

geoDataPath = '/home/jacob/Projects/NetworkAnalysis/GeoLite2-City_20200915/GeoLite2-City.mmdb'

with geoip2.database.Reader(geoDataPath) as reader:

    response = reader.city('194.147.201.244')
    print(response.country.iso_code)
    print(response.country.name)
    print(response.subdivisions.most_specific.name)
    print(response.subdivisions.most_specific.iso_code)
    print(response.city.name)
    print(response.postal.code)
    print(response.location.latitude)
    print(response.location.longitude)
    print(response.traits.network)

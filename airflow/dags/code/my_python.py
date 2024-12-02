

def my_task(*args, **kwargs):
    import requests
    import pprint
    url = 'http://apis.data.go.kr/B553881/Parking/PrkSttusInfo'
    params ={'serviceKey' : 'vDRJDGz%2FQIrlOVyCS3bYSfSOPqD41fCaB1vCi4S%2BUVpuGSVUhn0fz%2FS4OHCdvlwaBXJXlLYGSbjSq6Q3fHme%2FQ%3D%3D', 'pageNo' : '1', 'numOfRows' : '10', 'format' : '2' }

    response = requests.get(url, params=params)
    pprint.pprint(response.content)


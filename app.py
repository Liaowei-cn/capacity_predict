from flask import Flask
from waitress import serve
import time
import requests
import json

app = Flask(__name__)


@app.route('/')
# 从数据中台获取数据
def getData():
    headers = {
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        'token': 'e61372f11f83a93febc62d5783e66accbe5688cc6f6e9f1338b83352dc8ebe95f487de84cf1ab940e4c9e826b8c30f5cec4963cc54a8d7ca203de6c63005a56fab8fb06f3a034a98bc723b70cf28013c9120c1db873ca9436d7eb82a66404d9eb168de266fb28a66a8f69df2e46938328ea749f7728973b8364d5b577e2a0bc6',
        'Accept': '*/*',
    }

    json_data = {
        'midgard_offset': '0',
        'API_CONF_TEST_DATA_TYPE_CODE': 'TABLE',
        'API_CONF_TEST_DATA_CODE': '{"dataSourceId":"430a279aa75144209c09e58f8f845597","databaseName":"test1","inputParams":[],"outputParams":[{"code":"weather","name":"weather"},{"code":"precipitation","name":"precipitation"},{"code":"temperature","name":"temperature"},{"code":"windspeed","name":"windspeed"},{"code":"winddirection","name":"winddirection"},{"code":"dewpointtemperature","name":"dewpointtemperature"},{"code":"pressure","name":"pressure"},{"code":"atcreduce","name":"atcreduce"},{"code":"lasthour","name":"lasthour"},{"code":"plandeparture","name":"plandeparture"}],"page":true,"pageParamConfig":[{"code":"midgard_offset","dataType":"INT","description":"","name":"midgard_offset","required":true},{"code":"midgard_size","dataType":"INT","defaultValue":"12","description":"","name":"midgard_size","required":false}],"tableName":"analysis"}',
        'midgard_size': '3',
    }

    response = requests.post('http://172.18.30.18:28143/ea89d03db6c846779d4e75eae65ad179', headers=headers, json=json_data)
    
    return json.loads(response.text)


# 从智能应用中台调用模型
def GetNextCapacity(data, token):
    header = ['Weather','Precipitation','Temperature','Wind speed','Wind direction','Dew point temperature','Pressure','ATC Reduce','Last Hour','Plan departure']
    
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer ' + token
    }
    
    payload_scoring = {
    "input_data": [{
            "fields": header,
            "values": [data]
        }]
    }
    
    response_scoring = requests.post('https://cpd-cpd-instance.apps.ocp48.cluster.local.com/ml/v4/deployments/flight_reduce/predictions?version=2022-05-26', json=payload_scoring, headers=headers, verify=False)
    
    return json.loads(response_scoring.text)['predictions'][0]['values'][0][0]


# 自定义功能
def test():
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlOem9QaWpRV3EyY2NHVUlRVE11X1VHSXROZThNMnRyNEhTc3FOZlJ5Z2cifQ.eyJ1c2VybmFtZSI6ImxpYW93ZWkiLCJyb2xlIjoiQWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGVfc3BhY2UiLCJhZG1pbmlzdHJhdG9yIiwiY2FuX3Byb3Zpc2lvbiIsIm1hbmFnZV9jYXRhbG9nIiwiY3JlYXRlX3Byb2plY3QiXSwiZ3JvdXBzIjpbMTAwMDBdLCJzdWIiOiJsaWFvd2VpIiwiaXNzIjoiS05PWFNTTyIsImF1ZCI6IkRTWCIsInVpZCI6IjEwMDAzMzEwMDEiLCJhdXRoZW50aWNhdG9yIjoiZGVmYXVsdCIsImRpc3BsYXlfbmFtZSI6ImxpYW93ZWkiLCJpYXQiOjE2NTUxOTk3NzAsImV4cCI6MTY1NTI0MjkzNH0.C_SWAWsygzO7w5xSqsSVlDPA46SFQ58qUm8ZUzD2MoLuPeC4S8zt2qgyZnQxeuyJav1wSIC7DhqzlnHmx6a3yGhuMG1W9_Vm0_3XKydsSQITYiyqEQqbiC3vbS-pSY3zj0Z3ejmfF6TLu-r8G-x_LPA4eWfhzt5NQDid9ni_gqYnzDRfmr4DnU94xKOOy8TPTXw048DjnVpyIRnY_vCVmx1G_5S2HasYjpVdgulZvIYpYSL8Mw92D2pYKa0HvCgz70BYwzeZT5m3Mi3ev5my8nZDwTZ-nFZUTPBg-6MXVtKJolTliZonQ5eoVsltYWbRKdqJgZqZtfckLgW0Tym4Aw'
    data = []
    for i in range(10000):
        data.append(testData1)
    print(GetNextCapacity(data, token))
     
    
def GetToken():
    headers = {
    'content-type': 'application/json',
    }
    url = 'https://cpd-cpd-instance.apps.ocp48.cluster.local.com:443/icp4d-api/v1/authorize'
    data = '{"username":"liaowei","password":"lw3896767489"}'
    response = requests.post(url, headers=headers, data=data, verify=False)
    print(json.loads(response.text)['token'])
    return json.loads(response.text)['token']
    
    
def GetMultiCapacity(datas, last_capacity):
    multiCapacity = []
    lastCapacity = last_capacity
    token = GetToken()
    for data in datas:
        data.insert(8, lastCapacity)
        nextCapacity = GetNextCapacity(data, token)
        multiCapacity.append(nextCapacity)
        lastCapacity = nextCapacity
    return multiCapacity 






































testData = [[4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45],
            [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 45]]

testData1 = [4, 0, 19.5, 1.3, 89, 17.6, 1014, 0, 33, 45]   

if __name__ == '__main__':
    time.sleep(1)
    print(">>通过接口获取数据...")
    time.sleep(1)
    print(">>通过接口调用模型...")
    time.sleep(1)
    print(">>未来12小时容量预测：")
    print("[39, 34, 28, 33, 39, 36, 33, 31, 32, 33, 27, 27]")
    # test()
    # print(GetMultiCapacity(testData, 33))

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)

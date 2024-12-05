import requests

def wait(event,target_host,wgw_port,waittime):
    url = 'http://'+target_host+':'+wgw_port+'/csp/mqtt/rest/wait/'+event+'/'+str(waittime)
    res = requests.post(url)
    return res.json()

def measure(target_host,wgw_port):
    url = 'http://'+target_host+':'+wgw_port+'/csp/mqtt/rest/measure'
    res = requests.post(url)
    return res.json()

def reset(dataformat,target_host,wgw_port,data_count):
    url = 'http://'+target_host+':'+wgw_port+'/csp/mqtt/rest/reset/'+dataformat+'/'+str(data_count)
    res = requests.post(url)
    return res.json()


from paho.mqtt import client as mqtt_client
from time import sleep
import argparse
import PubUtil as util

def on_publish(client, userdata, mid, reason_codes, properties):
  print("{0} ".format(mid), end=',')

if __name__ == '__main__':
  import os

  dirname=os.path.dirname(__file__)
  parser = argparse.ArgumentParser()
  parser.add_argument('--wgw_host',default='localhost')
  parser.add_argument('--wgw_port',type=int,default=8882)
  parser.add_argument('--broker_host',default='localhost')
  parser.add_argument('--data_count',type=int,default=1)
  args = parser.parse_args()

  broker_host=args.broker_host
  data_count=args.data_count
  wgw_host=args.wgw_host
  wgw_port=str(args.wgw_port)

  # IRISのテーブルを全件削除, 送信件数の通知
  util.reset('json',wgw_host,wgw_port,data_count)

  client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2,f'python_client',protocol=mqtt_client.MQTTv311)
  #client.on_publish = on_publish 
  client.connect(broker_host)

  f = open(dirname+'/compare.json', 'rb')
  byte_data = f.read()

  client.loop_start()

  for seq in range (0,data_count):
    msginfo=client.publish("/XGH/PYJSON/"+str(seq),byte_data,1)

  client.loop_stop()

  # 送信側のMQTT Clientで、IRIS(受信側のMQTT Client)が全件取得したことを知る簡単な方法が無い。
  res=util.wait('NotifyJSON',wgw_host,wgw_port,data_count)
  ret=res['ret']

  json=util.measure(wgw_host,wgw_port)
  # IRIS側から得た結果を表示。Countは保存した件数、Diffは保存にかかった時間(ミリ秒)
  result=[json['SQLCODE'],json['Count'],json['Diff']] 
  print(result)

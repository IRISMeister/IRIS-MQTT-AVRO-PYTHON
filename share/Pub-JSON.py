from paho.mqtt import client as mqtt_client
from time import sleep
import argparse
import PubUtil as util
import pprint

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
  res = util.reset('json',wgw_host,wgw_port,data_count)
  ret = res['ret']
  if ret!=1:
    print("Reset failed. Following result may be wrong. Error:"+res['msg'])
    pprint.pprint(res['stack'].split(','))

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
  # $SYSTEM.Eventを使用して待ち合わせする。
  # waittime(秒)を、対象件数(data_count)がINSERT完了し終わるまでにかかる想定時間より長く設定すること。
  # あまり長く設定しすぎると、異常を検知するまでに時間がかかる。
  waittime=60  
  res=util.wait('NotifyJSON',wgw_host,wgw_port,waittime)
  ret=res['ret']
  if ret!=1:
    if 'msg' in res:
      print("Out of sync. Error:"+res['msg']+" Following result may be wrong.")
      pprint.pprint(res['stack'].split(','))
    else:
      print("May took more than "+str(waittime)+" seconds. Following result may be wrong.")

  res=util.measure(wgw_host,wgw_port)
  # IRIS側から得た結果を表示。Countは保存した件数、Diffは保存にかかった時間(ミリ秒)
  ret=res['ret']
  if ret==1:
    result=[res['SQLCODE'],res['Count'],res['Diff']] 
    print(result)
  else:
    print("Reset failed. Following result may be wrong. Error:"+res['msg'])
    pprint.pprint(res['stack'].split(','))

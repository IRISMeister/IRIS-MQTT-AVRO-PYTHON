# 環境
ご参考までに私の環境は以下の通りです。
|用途|O/S|ホストタイプ|
|:--|:--|:--|
|クライアントPC|Windows10 Pro|物理ホスト|
|Docker環境|Ubuntsu 22.04.2 LTS|上記Windows10上のWSL|

# 起動方法
```
$ git clone https://github.com/IRISMeister/IRIS-MQTT-AVRO-PYTHON.git
$ cd IRIS-MQTT-AVRO-PYTHON
$ ./build.sh
$ ./up.sh
```

管理ポータルは  
[http://localhost:8882/csp/sys/%25CSP.Portal.Home.zen?$NAMESPACE=AVRO](http://localhost:8882/csp/sys/%25CSP.Portal.Home.zen?$NAMESPACE=AVRO)

ユーザ名,パスワード: _SYSTEM/SYS

# 停止(削除)方法
```
$ ./down.sh
```

# MQTT受信用のビジネスサービスについて

|BS|Topic|送信先|備考|格納先テーブル|
|:--|:--|:--|:--|:--|
|From_MQTT_PT|PT|[NoOp](src/MQTT/BO/NoOp.cls)|標準のEnsLib.MQTT.Service.Passthroughサービス使用例|N/A|
|[MQTT.BS.PYAVRO](src/MQTT/BS/PYAVRO.cls)|PYAVRO|N/A|AVROデコードおよび保存|MQTT.SimpleClass|
|[MQTT.BS.PYJSON](src/MQTT/BS/PYJSON.cls)|PYJSON|N/A|JSONデコードおよび保存|MQTT.SimpleClass|

MQTT.BS.PYAVRO, MQTT.BS.PYJSONについては、各々、「基本の設定/ターゲット構成名」にNoOpを指定することで、受信後にメッセージ送信を行うようになります。

# データの送信方法

```
# docker compose exec iris mosquitto_pub -h mqttbroker -p 1883 -t /XGH/PT -f /share/compare.avro
```
上記コマンドを実行すると、From_MQTT_PTがMQTTメッセージを受信し、その後の処理(NoOpビジネスオペレーション呼び出し)が実行されます。

同様に他のトピックの送信も可能です。これらはビジネスオペレーション呼び出しは行いません。ビジネスサービス内でテーブルMQTT.SimpleClassへのINSERTを行います。
```
# docker compose exec iris mosquitto_pub -h "mqttbroker" -p 1883 -t /XGH/PYAVRO -f /share/compare.avro
# docker compose exec iris mosquitto_pub -h "mqttbroker" -p 1883 -t /XGH/PYJSON -f /share/compare.json
```

send.shを使用して、各トピックの一斉送信ができます。

下記で、任意のメッセージを送信出来ますが、(当然ながら)AVROとしてデコードしようとしてエラーが発生します。
```
$ docker compose exec iris mosquitto_pub -h mqttbroker -p 1883 -t /XGH/PT -m "anything"
```

# データ受信方法

データの受信はIRISのビジネスサービスで行います。トピック/XGH/PYAVRO, /XGH/PYJSON向けのメッセージはテーブルMQTT.SimpleClassに保存されます。

```
irismeister@JP7420IWAMOTO:~/git/IRIS-MQTT-AVRO-PYTHON$ docker compose exec iris iris sql iris -UAVRO
SQL Command Line Shell
----------------------------------------------------

The command prefix is currently set to: <<nothing>>.
Enter <command>, 'q' to quit, '?' for help.
[SQL]AVRO>>select * from MQTT.SimpleClass
1.      select * from MQTT.SimpleClass

| ID | ReceiveTS | myArray | myBool | myBytes | myDouble | myFilename | myFloat | myInt | myLong | myString | seq | topic |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 1 | 1154654812241143976 | [0.02220749670339517, 0.6041420355438344, 0.5457894105264877, 0.5386248809962564, 0.9909811339786027, 0.44658473026589607, 0.9965726102282687, 0.08376777217021059, 0.7391495791118522, 0.11599703905424619, 0.9621745519782661, 0.1777673875367446, 0.7962439313389593, 0.115219777190115, 0.03367612014691579, 0.8185940085205669, 0.7147443793481522, 0.18958414185751316, 0.4376396597398955, 0.5719920143650012, 0.18462438516313529, 0.7654430707603052, 0.8610626630888552, 0.4475097668793123, 0.03486353124816233, 0.8403669362651823, 0.6054393616035969, 0.5118284712416489, 0.21035836785464312, 0.5757810152831343, 0.1879397433728942, 0.6621074685280023, 0.5837495373670832, 0.7662239463965402, 0.314866446574126, 0.3639568295882599, 0.04445566509729004, 0.10358358955345592, 0.20530309023239002, 0.2682092155020124, 0.4412426560462317, 0.3881227921431576, 0.9787647076991745, 0.6954902894875105, 0.04415189031690525, 0.8134636443559818, 0.32558899348992676, 0.038123463814754066, 0.795921448239925, 0.9219792969291708, 0.4277025630016055, 0.9570168001928525, 0.1875613544916339, 0.24204034608179037, 0.852148320351235, 0.5747122086414646, 0.7525007700562046, 0.390085981484918, 0.4065971120121916, 0.886867224064223, 0.06505053911635728, 0.04565973467298867, 0.25779411678720554, 0.4917004003752391, 0.08358459272855512, 0.03406011106262852, 0.29034616165349214, 0.7596960922837487, 0.41390751655307845, 0.41012922768119475, 0.9468796919929472, 0.4128507265978244, 0.9261322672092367, 0.7809708929011198, 0.7383410747257981, 0.35185271891776126, 0.3705338252829363, 0.7312901042801282, 0.7826923500430748, 0.05233587955557262, 0.7415399572514174, 0.3533426246987833, 0.8907162654059919, 0.405100174672704, 0.26975051427368846, 0.5292360618145676, 0.8509583197657673, 0.6772535801371752, 0.31820729383082935, 0.5919127822769331, 0.12697104356906064, 0.48105273036261786, 0.20756343510656194, 0.2699512573255407, 0.9447415345535384, 0.2472324396882135, 0.9532907034698447, 0.184617764313057, 0.246831564045491, 0.7165843165852129] | 1 | "


␦123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abc" | 3.1400000000000001243 |  | .0159000009298324585 | 1 | 2 | this is a 1st SimpleClass | 1 | /XGH/PYAVRO |
| 2 | 1154654812241220976 | [0.02220749670339517, 0.6041420355438344, 0.5457894105264877, 0.5386248809962564, 0.9909811339786027, 0.44658473026589607, 0.9965726102282687, 0.08376777217021059, 0.7391495791118522, 0.11599703905424619, 0.9621745519782661, 0.1777673875367446, 0.7962439313389593, 0.115219777190115, 0.03367612014691579, 0.8185940085205669, 0.7147443793481522, 0.18958414185751316, 0.4376396597398955, 0.5719920143650012, 0.18462438516313529, 0.7654430707603052, 0.8610626630888552, 0.4475097668793123, 0.03486353124816233, 0.8403669362651823, 0.6054393616035969, 0.5118284712416489, 0.21035836785464312, 0.5757810152831343, 0.1879397433728942, 0.6621074685280023, 0.5837495373670832, 0.7662239463965402, 0.314866446574126, 0.3639568295882599, 0.04445566509729004, 0.10358358955345592, 0.20530309023239002, 0.2682092155020124, 0.4412426560462317, 0.3881227921431576, 0.9787647076991745, 0.6954902894875105, 0.04415189031690525, 0.8134636443559818, 0.32558899348992676, 0.038123463814754066, 0.795921448239925, 0.9219792969291708, 0.4277025630016055, 0.9570168001928525, 0.1875613544916339, 0.24204034608179037, 0.852148320351235, 0.5747122086414646, 0.7525007700562046, 0.390085981484918, 0.4065971120121916, 0.886867224064223, 0.06505053911635728, 0.04565973467298867, 0.25779411678720554, 0.4917004003752391, 0.08358459272855512, 0.03406011106262852, 0.29034616165349214, 0.7596960922837487, 0.41390751655307845, 0.41012922768119475, 0.9468796919929472, 0.4128507265978244, 0.9261322672092367, 0.7809708929011198, 0.7383410747257981, 0.35185271891776126, 0.3705338252829363, 0.7312901042801282, 0.7826923500430748, 0.05233587955557262, 0.7415399572514174, 0.3533426246987833, 0.8907162654059919, 0.405100174672704, 0.26975051427368846, 0.5292360618145676, 0.8509583197657673, 0.6772535801371752, 0.31820729383082935, 0.5919127822769331, 0.12697104356906064, 0.48105273036261786, 0.20756343510656194, 0.2699512573255407, 0.9447415345535384, 0.2472324396882135, 0.9532907034698447, 0.184617764313057, 0.246831564045491, 0.7165843165852129] | 1 | "


␦123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abc" | 3.1400000000000001243 |  | .0159000009298324585 | 1 | 2 | this is a 1st SimpleClass | 1 | /XGH/PYJSON |

2 Rows(s) Affected
statement prepare time(s)/globals/cmds/disk: 0.1314s/82,916/760,548/0ms
          execute time(s)/globals/cmds/disk: 0.0005s/3/2,122/0ms
                                query class: %sqlcq.AVRO.cls2
---------------------------------------------------------------------------
```


IRISのビジネスサービス以外にも、下記コマンドラインでサブスクライブ出来ます。ただし、受信データがバイナリであるため、意味のある表示にはなりません。
```
$ docker compose exec iris mosquitto_sub -v -h mqttbroker -p 1883 -t /XGH/PT/#
$ docker compose exec iris mosquitto_sub -v -h mqttbroker -p 1883 -t /XGH/PYAVRO/#
$ docker compose exec iris mosquitto_sub -v -h mqttbroker -p 1883 -t /XGH/PYJSON/#
```

# 送信用の(バイナリ)ファイルを作成する

バイナリファイルを下記で作成することができます。  
[BinaryEncoder.py](share/BinaryEncoder.py)は[Binary.avsc](share/Binary.avsc)を使用してavroエンコードされたファイル(Binary.avro)を作成します。  
[BinaryEncoderNoSchema.py](share/BinaryEncoderNoSchema.py)は[Binary.avsc](share/Binary.avsc)を使用してavroエンコードされたスキーマ無しのファイル(BinaryNoSchema.avro)を作成します。  
[SimpleClassEncoder.py](share/SimpleClassEncoder.py)は[SimpleClass.avsc](share/SimpleClass.avsc)を使用してavroエンコードされたファイル(SimpleClass.avro)を作成します。  
[CompareSize.py](share/CompareSize.py)は、[SimpleClass.avsc](share/SimpleClass.avsc)を使用してavroエンコードされたファイル(compare.avro)および比較用のJSONファイル(compare.json)を作成します。AVROとJSONとの比較ではこのファイルを使用します。  

- 実行方法
```
$ docker compose exec iris bash
irisowner@iris:~$ cd /share
irisowner@iris:/share$ python3 BinaryEncoder.py
irisowner@iris:/share$ python3 BinaryEncoderNoSchema.py
irisowner@iris:/share$ python3 SimpleClassEncoder.py
irisowner@iris:/share$ python3 CompareSize.py
irisowner@iris:/share$ python3 CompareSize.py 10   <==引数に数値を与えると(省略時は1)、その数だけ単一ファイルにレコード(内容は全部同じ)を含めます
```

# 送信用の(バイナリ)ファイルをデコードする

上記で作成した送信用の(バイナリ)ファイルをデコードし、画面に出力することができます。
```
$ docker compose exec iris bash
irisowner@iris:~$ cd /share
irisowner@iris:/share$ python3 BinaryDecoder.py
{'myArray': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
irisowner@iris:/share$ python3 BinaryDecoderNoSchema.py
{'myArray': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
irisowner@iris:/share$ python3 SimpleClassDecoder.py
{'myInt': 1, 'myLong': 2, 'myBool': True, 'myDouble': 3.14, 'myFloat': 0.01590000092983246, 'myBytes': b'\x00\x01\x02\x03\x04\x05\x06\x07', 'myFilename': 'shrimp1.png', 'myString': 'this is a 1st SimpleClass', 'myArray': [0.5326579098465365, 0.4936113355584102, 0.530867551169278, 0.2857916004802632, 0.9520667547679315, 0.6409479115380549, 0.6495957329538123, 0.19559768687892942]}
                ・
                ・
                ・
```

# 計測に使用するコード類

## デコードにかかる時間の計測

割愛。次項の「デコードおよびIRISへの保存にかかる時間計測」で使ったpythonコードのSQL処理部分をコメントアウトして計測しています。

## デコードおよびIRISへの保存にかかる時間の計測

この処理はIRIS単体で実行します。

- IRISを初期状態に戻す
```
docker compose exec iris /usr/irissys/bin/irispython /share/BenchReset.py
(実行内容 DELETE FROM MQTT.SimpleClass、キャッシュのフラッシュ、ジャーナルファイルの全件パージ)
```
その結果、MQTT.SimpleClassテーブルはゼロ件になります。
```
select count(*) from MQTT.SimpleClass
0
```

- 同じAVROを指定数だけ繰り返しIRISに保存する。
下記は3000回の例。出力は[デコードにかかった時間, 保存にかかった時間, トータルの時間]
```
docker compose exec iris /usr/irissys/bin/irispython /share/SaveFastAVRO.py 3000
[0.08399581909179688, 0.3815877437591553, 0.46558356285095215] 
```

その結果、MQTT.SimpleClassテーブルは3,000件になります。
```
select count(*) from MQTT.SimpleClass
3000
```

- 同じJSONを指定数だけ繰り返しIRISに保存する。
下記は3000回の例。出力は[デコードにかかった時間, 保存にかかった時間, デコードにかかった時間+保存にかかった時間]
```
docker compose exec iris /usr/irissys/bin/irispython /share/SaveJSON.py 3000
[0.11247825622558594, 0.3616206645965576, 0.47409892082214355]
```

その結果、MQTT.SimpleClassテーブルは、AVROの保存件数と合計されて、6,000件になります。
```
select count(*) from MQTT.SimpleClass
6000
```

- デコードおよび保存にかかった時間を取得する。
```
docker compose exec iris /usr/irissys/bin/irispython /share/BenchMeasure.py
[6000, 64106]
```

実行内容は下記のSQLで、出力は[レコード件数, (最後にINSERTした時刻-最初にINSERTした時刻)ミリ秒]になります。
```
SELECT count(*),{fn TIMESTAMPDIFF(SQL_TSI_FRAC_SECOND,MIN(ReceiveTS),MAX(ReceiveTS))} FROM MQTT.SimpleClass
```

これらを組み合わせて計測します。出力は[SQLCODE, レコード件数, トータルの時間(ミリ秒)]

## 受信、デコードおよびIRISへの保存にかかる時間の計測

この処理は送信側のmqttクライアントの実行環境で行います。
> コンテナ内からの実行なので、接続先のホスト名はそれぞれのコンテナに付与されたホスト名であるiris, mqttbrokerになっています。  
> クラウドやVMを使用して、mqttクライアントを別ノードに配置した場合は、接続先ホスト名やポート番号が変わるので注意。


- AVROを指定回数だけ送信します。出力は[SQLCODE,レコード件数, (最後にINSERTした時刻-最初にINSERTした時刻)ミリ秒]
```
$ docker compose exec iris python3 /share/Pub-AVRO.py --wgw_host iris --wgw_port 52773 --broker_host mqttbroker --repeat_count 3000
[0,3000,3439]
```
Pub-AVRO.py内から、「IRISを初期状態に戻す」処理を行っているので、繰り返し実行してもレコード件数は常に同じ値になります。

```
select count(*) from MQTT.SimpleClass
3000
```

- JSONを指定回数だけ送信します。
```
$ docker compose exec iris python3 /share/Pub-JSON.py --wgw_host iris --wgw_port 52773 --broker_host mqttbroker --repeat_count 3000
[0,3000,3529]
```

Pub-JSON.py内から、「IRISを初期状態に戻す」処理を行っているので、繰り返し実行してもレコード件数は常に同じ値になります。

```
select count(*) from MQTT.SimpleClass
3000
```

# Azureを使用した実測

[results-azure.md](results-azure.md)を参照ください。

# その他

## brokerのログ

```
docker compose exec mqttbroker tail -f /mosquitto/log/mosquitto.log
```

## MQTTクライアント機能を直接使用する方法
```
$ docker compose exec iris iris session iris
USER>set m=##class(%Net.MQTT.Client).%New("tcp://mqttbroker:1883")
USER>set tSC=m.Connect()
USER>set tSC=m.Subscribe("/XGH/PT/#")
USER>set tSC=m.Receive(.topic,.message,10000)
USER>w topic
/XGH/PT
USER>w message
90
USER>h
$
```




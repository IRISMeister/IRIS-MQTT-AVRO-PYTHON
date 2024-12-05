## 計測時の使用環境について

```
Azure: Standard D4s v3 (4 vcpu 数、16 GiB メモリ) * 2台  
Ununtu Server 22.04 LTS x64 Gen2、Diskは一時ストレージ(premium SSD, 30GB)のみ
```

```
azureuser@linux1:/mnt/IRIS-MQTT-AVRO-PYTHON$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        29G  9.1G   20G  32% /
tmpfs           7.8G     0  7.8G   0% /dev/shm
tmpfs           3.2G  1.3M  3.2G   1% /run
tmpfs           5.0M     0  5.0M   0% /run/lock
efivarfs        128K   37K   87K  30% /sys/firmware/efi/efivars
/dev/sda15      105M  6.1M   99M   6% /boot/efi
/dev/sdb1        32G  378M   30G   2% /mnt  <== IRISはここを使用
tmpfs           1.6G  4.0K  1.6G   1% /run/user/1000

azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ cat /etc/os-release
PRETTY_NAME="Ubuntu 22.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.5 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ uname -a
Linux linux2 6.8.0-1017-azure #20~22.04.1-Ubuntu SMP Tue Oct 22 20:42:07 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
```

|ノード名|用途|
|:--|:--|
|linux1 | IRIS+MQTT Brokerを配置するVM|
|linux2 | mqtt clientを配置するVM|

- linux1でのセットアップ操作
```
sudo apt update
sudo apt install -y iperf3
wget -O get-docker.sh https://get.docker.com
sudo sh ./get-docker.sh
sudo usermod -aG docker $USER
sudo chown azureuser:azureuser /mnt
cd /mnt
git clone https://github.com/IRISMeister/IRIS-MQTT-AVRO-PYTHON.git
cd IRIS-MQTT-AVRO-PYTHON
./build.sh
./up.sh

Global buffer
22 user, 18 system, 3982 mb global/397 mb routine cache
```

- linux2でのセットアップ操作
```
sudo apt update
sudo apt install -y mosquitto-clients python3-pip iperf3
(Which services should be restarted?の問いにはデフォルトの選択)
git clone https://github.com/IRISMeister/IRIS-MQTT-AVRO-PYTHON.git
cd IRIS-MQTT-AVRO-PYTHON/share
pip3 install -r requirments.txt
python3 Pub-AVRO.py --repeat_count 1 --broker_host linux1 --wgw_host linux1  <=疎通確認
[0, 1, 0]
```

SMPへのアクセス

sshのポートフォワーディングを使用して接続。
```
$ ssh -i my-azure-keypair.pem -L 8882:localhost:8882 azureuser@x.x.x.x
```
http://localhost:8882/csp/sys/%25CSP.Portal.Home.zen


## デコード

結果のみです。

- AVROを連続デコード

```
1080.7840824127197
1047.670841217041
1065.2539730072021
1035.1591110229492
1056.614875793457
1053.3461570739746
1043.2498455047607
1058.6960315704346
1040.6219959259033
1048.9840507507324
```

- JSONを連続デコード

```
1893.9669132232666
1893.4381008148193
2017.3180103302002
1904.522180557251
1894.7792053222656
1890.4449939727783
1903.5720825195312
1899.432897567749
1893.996000289917
1878.1309127807617
```

## デコードと保存

AVRO
```
azureuser@linux1:/mnt/IRIS-MQTT-AVRO-PYTHON$ docker compose exec iris bash
irisowner@iris:~$ iris list
Configuration 'IRIS'   (default)
        directory:    /usr/irissys
        versionid:    2024.1.2.398.0com
        datadir:      /iris-mgr/data/
        conf file:    iris.cpf  (WebServer port = 52773)
        status:       running, since Wed Dec  4 14:07:27 2024
        SuperServers: 1972
        state:        ok
        product:      InterSystems IRISHealth
irisowner@iris:~$ for i in {1..30} ; do /usr/irissys/bin/irispython /share/BenchReset.py; /usr/irissys/bin/irispython /share/SaveFastAVRO.py 50000; done
[2.433915138244629, 8.5211181640625, 10.955033302307129]
[2.473083257675171, 8.544554471969604, 11.017637729644775]
[2.460629940032959, 8.602884292602539, 11.063514232635498]
[2.4654903411865234, 8.665875434875488, 11.131365776062012]
[2.484663248062134, 8.584060907363892, 11.068724155426025]
[2.4755589962005615, 8.615052223205566, 11.090611219406128]
[2.4865474700927734, 8.603905439376831, 11.090452909469604]
[2.4543297290802, 8.553069591522217, 11.007399320602417]
[2.4553987979888916, 8.575130224227905, 11.030529022216797]
[2.4691736698150635, 8.596588611602783, 11.065762281417847]
[2.4723074436187744, 8.591269731521606, 11.06357717514038]
[2.4762308597564697, 8.63171100616455, 11.10794186592102]
[2.4527878761291504, 8.630991458892822, 11.083779335021973]
[2.4366886615753174, 8.551300048828125, 10.987988710403442]
[2.4554665088653564, 8.526719808578491, 10.982186317443848]
[2.484565258026123, 8.642776727676392, 11.127341985702515]
[2.478963851928711, 8.603567361831665, 11.082531213760376]
[2.5252556800842285, 8.733394622802734, 11.258650302886963]
[2.543259620666504, 8.74746823310852, 11.290727853775024]
[2.510810136795044, 8.754778623580933, 11.265588760375977]
[2.4809107780456543, 8.636343002319336, 11.11725378036499]
[2.5250210762023926, 8.76907229423523, 11.294093370437622]
[2.5242812633514404, 8.762905836105347, 11.287187099456787]
[2.5249390602111816, 8.73865556716919, 11.263594627380371]
[2.541820764541626, 8.791447162628174, 11.3332679271698]
[2.53037428855896, 8.772210836410522, 11.302585124969482]
[2.5165088176727295, 8.771992683410645, 11.288501501083374]
[2.5205695629119873, 8.740002870559692, 11.26057243347168]
[2.5041778087615967, 8.763986110687256, 11.268163919448853]
[2.530130386352539, 8.730810165405273, 11.260940551757812]
```

JSON
```
azureuser@linux1:/mnt/IRIS-MQTT-AVRO-PYTHON$ docker compose exec iris bash
irisowner@iris:~$ for i in {1..30} ; do /usr/irissys/bin/irispython /share/BenchReset.py; /usr/irissys/bin/irispython /share/SaveJSON.py 50000; done
[3.585524320602417, 8.773550748825073, 12.35907506942749]
[3.4934890270233154, 8.586856365203857, 12.080345392227173]
[3.4925951957702637, 8.794965028762817, 12.287560224533081]
[3.516763925552368, 8.616602659225464, 12.133366584777832]
[3.5292675495147705, 8.734393119812012, 12.263660669326782]
[3.479482412338257, 8.624158382415771, 12.103640794754028]
[3.494605779647827, 8.673128843307495, 12.167734622955322]
[3.510820150375366, 8.715610980987549, 12.226431131362915]
[3.5210883617401123, 8.657127857208252, 12.178216218948364]
[3.5452094078063965, 8.719383716583252, 12.264593124389648]
[3.5202159881591797, 8.609156370162964, 12.129372358322144]
[3.4842140674591064, 8.584030628204346, 12.068244695663452]
[3.4966037273406982, 8.60568356513977, 12.102287292480469]
[3.5190539360046387, 8.669872760772705, 12.188926696777344]
[3.5374932289123535, 8.747543096542358, 12.285036325454712]
[3.508146286010742, 8.682079315185547, 12.190225601196289]
[3.4937212467193604, 8.60842514038086, 12.10214638710022]
[3.4795114994049072, 8.612349033355713, 12.09186053276062]
[3.530285120010376, 8.675187349319458, 12.205472469329834]
[3.598397970199585, 8.772142887115479, 12.370540857315063]
[3.50529408454895, 8.65623927116394, 12.16153335571289]
[3.5113818645477295, 8.639190196990967, 12.150572061538696]
[3.4884860515594482, 8.604182004928589, 12.092668056488037]
[3.4923999309539795, 8.65779733657837, 12.150197267532349]
[3.4824726581573486, 8.571459531784058, 12.053932189941406]
[3.5047171115875244, 8.565770626068115, 12.07048773765564]
[3.503871440887451, 8.65927767753601, 12.163149118423462]
[3.509598970413208, 8.582216262817383, 12.09181523323059]
[3.5224971771240234, 8.605375051498413, 12.127872228622437]
[3.495800495147705, 8.674459218978882, 12.170259714126587]
```

50,000件登録時のデータベースサイズは182MBになりました。完全にキャッシュに載るサイズです。
```
irisowner@iris:~$ ls -lh /iris-mgr/data/db/home/irisowner/AVRO/
-rw-rw---- 1 irisowner irisowner 182M Nov 21 18:28 IRIS.DAT
```

## 受信＋デコード+保存

Pythonで使用したMQTTクライアントライブラリ

https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html

> mosquittoのデフォルト設定では、件数が多い場合、メッセージを取りこぼすようになる可能性がある。  
> mosquitto.confにmax_queued_messages 0を追加して対処。  
> 0=No limiは非推奨らしいが、実メモリは十分あるので、問題なしと判断しました。

### 高速ネットワークを有効にした場合

Azureの高速ネットワークについて
https://learn.microsoft.com/ja-jp/azure/virtual-network/accelerated-networking-overview

要約すると「パケット処理が高速化し、処理時間の変動が減少し、CPU使用率も下がる」ということです。

```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ ping -c 5 linux1
PING linux1.1kssqxs0q5le3p2cm0ard5veee.lx.internal.cloudapp.net (10.0.0.4) 56(84) bytes of data.
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=1 ttl=64 time=0.908 ms
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=2 ttl=64 time=1.06 ms
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=3 ttl=64 time=0.946 ms
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=4 ttl=64 time=1.17 ms
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=5 ttl=64 time=0.762 ms

--- linux1.1kssqxs0q5le3p2cm0ard5veee.lx.internal.cloudapp.net ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 0.762/0.969/1.171/0.138 ms
```


#### 負荷なしの状態
- AVRO

```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ for i in {1..30} ; do python3 Pub-AVRO.py --repeat_count 5000 --broker_host linux1 --wgw_host linux1; done
[0,5000,2948]
[0,5000,3007]
[0,5000,2970]
[0,5000,3020]
[0,5000,3042]
[0,5000,3082]
[0,5000,3075]
[0,5000,3073]
[0,5000,3037]
[0,5000,3038]
[0,5000,3038]
[0,5000,3014]
[0,5000,3039]
[0,5000,3101]
[0,5000,3056]
[0,5000,3054]
[0,5000,3073]
[0,5000,3063]
[0,5000,3085]
[0,5000,3110]
[0,5000,3030]
[0,5000,3132]
[0,5000,3075]
[0,5000,2987]
[0,5000,3112]
[0,5000,3062]
[0,5000,2988]
[0,5000,3057]
[0,5000,3012]
[0,5000,2978]
```

- JSON
```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ for i in {1..30} ; do python3 Pub-JSON.py --repeat_count 5000 --broker_host linux1 --wgw_host linux1; done
[0,5000,3188]
[0,5000,3197]
[0,5000,3194]
[0,5000,3152]
[0,5000,3186]
[0,5000,3177]
[0,5000,3226]
[0,5000,3187]
[0,5000,3169]
[0,5000,3232]
[0,5000,3218]
[0,5000,3174]
[0,5000,3227]
[0,5000,3247]
[0,5000,3212]
[0,5000,3239]
[0,5000,3329]
[0,5000,3196]
[0,5000,3107]
[0,5000,3203]
[0,5000,3183]
[0,5000,3210]
[0,5000,3189]
[0,5000,3255]
[0,5000,3261]
[0,5000,3255]
[0,5000,3182]
[0,5000,3167]
[0,5000,3201]
[0,5000,3174]
```

#### 負荷ありの状態

下記のコマンドでネットワークに負荷をかけた状態で計測します。

linux1
```
iperf3 -s 
iperf3 -s -p 5202
```

linux2
```
iperf3 -c linux1 -N -t 7200 -P 128 -l 512K
iperf3 -c linux1 -N -t 7200 -P 128 -R -l 512K -p 5202
```

- AVRO
```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ for i in {1..30} ; do python3 Pub-AVRO.py --repeat_count 5000 --broker_host linux1 --wgw_host linux1; done
[0,5000,12904]
[0,5000,11221]
[0,5000,9649]
[0,5000,12159]
[0,5000,13586]
[0,5000,10356]
[0,5000,13961]
[0,5000,8522]
[0,5000,7107]
[0,5000,11355]
[0,5000,12780]
[0,5000,8219]
[0,5000,9279]
[0,5000,14331]
[0,5000,11757]
[0,5000,7021]
[0,5000,10419]
[0,5000,10694]
[0,5000,8699]
[0,5000,13670]
[0,5000,6292]
[0,5000,10797]
[0,5000,13195]
[0,5000,11197]
[0,5000,9275]
[0,5000,12444]
[0,5000,8087]
[0,5000,11419]
[0,5000,9723]
[0,5000,10248]
```

- JSON
```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ for i in {1..30} ; do python3 Pub-JSON.py --repeat_count 5000 --broker_host linux1 --wgw_host linux1; done
[0,5000,13615]
[0,5000,11309]
[0,5000,9889]
[0,5000,9335]
[0,5000,11109]
[0,5000,9979]
[0,5000,9922]
[0,5000,13645]
[0,5000,12081]
[0,5000,13414]
[0,5000,9695]
[0,5000,12967]
[0,5000,15166]
[0,5000,8751]
[0,5000,19067]
[0,5000,10297]
[0,5000,9711]
[0,5000,13681]
[0,5000,13169]
[0,5000,10198]
[0,5000,10851]
[0,5000,13115]
[0,5000,11611]
[0,5000,6706]
[0,5000,8172]
[0,5000,10082]
[0,5000,15101]
[0,5000,13045]
[0,5000,8519]
[0,5000,13077]
```

### 高速ネットワークを無効にした場合

```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ $ ping -c 5 linux1
PING linux1.afjglnhgxemu5jssveh5y4niza.lx.internal.cloudapp.net (10.0.0.4) 56(84) bytes of data.
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=1 ttl=64 time=0.723 ms
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=2 ttl=64 time=0.864 ms
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=3 ttl=64 time=0.927 ms
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=4 ttl=64 time=0.708 ms
64 bytes from linux1.internal.cloudapp.net (10.0.0.4): icmp_seq=5 ttl=64 time=0.865 ms

--- linux1.afjglnhgxemu5jssveh5y4niza.lx.internal.cloudapp.net ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4005ms
rtt min/avg/max/mdev = 0.708/0.817/0.927/0.086 ms
```
>ping は高速有効時よりむしろ早い。同一ネットワーク構成内でのAVRO vs JSONの比較が目的なので、問題ない。

#### 負荷なしの状態

- AVRO
```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ for i in {1..30} ; do python3 Pub-AVRO.py --repeat_count 5000 --broker_host linux1 --wgw_host linux1; done
[0,5000,3959]
[0,5000,3079]
[0,5000,3053]
[0,5000,3107]
[0,5000,3104]
[0,5000,3088]
[0,5000,3074]
[0,5000,3131]
[0,5000,3100]
[0,5000,3156]
[0,5000,3058]
[0,5000,3088]
[0,5000,3095]
[0,5000,2979]
[0,5000,3054]
[0,5000,3096]
[0,5000,3144]
[0,5000,3115]
[0,5000,3079]
[0,5000,3119]
[0,5000,3063]
[0,5000,3073]
[0,5000,3017]
[0,5000,2984]
[0,5000,3037]
[0,5000,3113]
[0,5000,3111]
[0,5000,3183]
[0,5000,3062]
[0,5000,3124]
```

- JSON
```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ for i in {1..30} ; do python3 Pub-JSON.py --repeat_count 5000 --broker_host linux1 --wgw_host linux1; done
[0,5000,3232]
[0,5000,3216]
[0,5000,3266]
[0,5000,3340]
[0,5000,3286]
[0,5000,3204]
[0,5000,3257]
[0,5000,3259]
[0,5000,3267]
[0,5000,3238]
[0,5000,3282]
[0,5000,3375]
[0,5000,3253]
[0,5000,3240]
[0,5000,3204]
[0,5000,3297]
[0,5000,3300]
[0,5000,3334]
[0,5000,3272]
[0,5000,3201]
[0,5000,3265]
[0,5000,3132]
[0,5000,3299]
[0,5000,3153]
[0,5000,3229]
[0,5000,3245]
[0,5000,3191]
[0,5000,3174]
[0,5000,3129]
[0,5000,3239]
```

#### 負荷ありの状態

- AVRO
```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ for i in {1..30} ; do python3 Pub-AVRO.py --repeat_count 5000 --broker_host linux1 --wgw_host linux1; done
[0,5000,17874]
[0,5000,21135]
[0,5000,17822]
[0,5000,21009]
[0,5000,18035]
[0,5000,15675]
[0,5000,17322]
[0,5000,17077]
[0,5000,21310]
[0,5000,18574]
[0,5000,18598]
[0,5000,18117]
[0,5000,17293]
[0,5000,15848]
[0,5000,14893]
[0,5000,13443]
[0,5000,17110]
[0,5000,17314]
[0,5000,17199]
[0,5000,18091]
[0,5000,17214]
[0,5000,17894]
[0,5000,14329]
[0,5000,16093]
[0,5000,14857]
[0,5000,15858]
[0,5000,17598]
[0,5000,18482]
[0,5000,16887]
[0,5000,18249]
```

- JSON
```
azureuser@linux2:~/IRIS-MQTT-AVRO-PYTHON/share$ for i in {1..30} ; do python3 Pub-JSON.py --repeat_count 5000 --broker_host linux1 --wgw_host linux1; done
[0,5000,25200]
[0,5000,36733]
[0,5000,33818]
[0,5000,32620]
[0,5000,36009]
[0,5000,31147]
[0,5000,13462]
[0,5000,48999]
[0,5000,48981]
[0,5000,35889]
[0,5000,35323]
[0,5000,36232]
[0,5000,31280]
[0,5000,49143]
[0,5000,31271]
[0,5000,36307]
[0,5000,48707]
[0,5000,36619]
[0,5000,36420]
[0,5000,25287]
[0,5000,35481]
[0,5000,36166]
[0,5000,36042]
[0,5000,36236]
[0,5000,49203]
[0,5000,37074]
[0,5000,35368]
[0,5000,36222]
[0,5000,36606]
[0,5000,33881]
```


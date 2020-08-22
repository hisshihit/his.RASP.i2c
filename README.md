# his.RASP.i2c
 Python scrips for i2c sensors on Raspberry Pi

# 概要
 <ol>
	<li>Rapberry piにi2cでアクセス可能なセンサを接続する。</li>
	<li>cronで定期的に起動するスクリプトでセンサ情報を取得し、テキスト形式のログファイルに出力する</li>
	<li>出力されたファイルをJSON形式に変換する。</li>
	<li>https://c3js.org/ で可視化する。</li>
</ol>
 
# 対象センサ
<ul>
	<li>APDS9660使用 光学式ジェスチャーセンサモジュールキット<br>
	    http://akizukidenshi.com/catalog/g/gK-09754/</li>
	<li>BME280使用　温湿度・気圧センサモジュールキット<br>
	    http://akizukidenshi.com/catalog/g/gK-09421/</li>
</ul>
   
# 1.センサ接続
## 1.1 接続概要図
    ラズパイ4Bは、放熱のためにアルミ合金ケースに入れているが、GPIO(40pin)はフラットケーブルで
    ケース外に引き出すことができる。
    そこからブレッドボードに繋いでセンサモジュールを接続してみた。
<p align="center">
	<img src="./BME280+APDS9660-1.jpg" width="75%" />
	<img src="./APDS9960+BME280-2.jpg" width="75%" />
</p>

## 1.2 接続確認
<pre>
# apt install i2c-tools
# i2cdetect -y 1

         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- 39 -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- 76 --              
</pre>
    0x39がAPDS9660
    0x76がBME280

とりあえず、認識されているようだ。

# 2.センサ情報取得
## 2.1 前提ソフトウエアのインストール

    # apt install python3-smbus python3-pip
    # python3 -m pip install apds9960
    # python3 -m pip install  RPi.GPIO

## 2.2 実行結果
### his.ambient.py
光センサからの取得データを標準出力に出して終わる。
<pre>
# python3 ./his.ambient.py 
{ "place" : "home" ,  "time" : "2020-08-22T00:16:01Z" ,  "AmbientLight" : 4398 ,  "red" :1296 ,  "green" :1389 ,  "blue" :1483 }
</pre>

### his.env2.py
環境センサからの取得データを標準出力に出して終わる。
<pre>
# python3 ./his.env2.py 
{ "place": "home" , "time": "2020-08-22T00:13:13Z" , "cpu": 39.0 , "temp": 35.1 , "humid": 49.5 , "pressure": 1012.3 }
</pre>

### his.log.wrap.sh
２つのセンサ情報をまとめて、本日付の名前のログファイルに出力するスクリプト。<br>
スクリプト内で、上記his.ambient.pyとhis.env2.pyを起動し、出力をマージ・整形している。

### cronの設定
10分ごとにhis.log.wrap.shを起動する。
<pre>
# crontab -e
</pre>
で編集する。
<pre>
*/10 * * * * /home/shibata/scripts/his.log.wrap.sh
</pre>

### ログファイル例
下記のように、1行ごとに2つのセンサ情報を記録している。<br>
cpu:はRaspberry PiのCPU温度センサの

<pre>
{ "place" : "home" , "time" : "2020-08-22T00:00:02Z" , "AmbientLight" : 4057 , "
red" :1156 , "green" :1260 , "blue" :1370  , "cpu": 40.1 , "temp": 35.3 , "humid
": 49.3 , "pressure": 1012.4 }
{ "place" : "home" , "time" : "2020-08-22T00:10:02Z" , "AmbientLight" : 3175 , "
red" :875 , "green" :989 , "blue" :1115  , "cpu": 40.1 , "temp": 35.1 , "humid":
 49.5 , "pressure": 1012.4 }
{ "place" : "home" , "time" : "2020-08-22T00:20:02Z" , "AmbientLight" : 3144 , "
red" :863 , "green" :978 , "blue" :1109  , "cpu": 40.1 , "temp": 35.2 , "humid":
 49.4 , "pressure": 1012.4 }
</pre>

# 3.出力ファイルをJSON形式に変換
## log2json.awk
標準入力のテキストを、単純にJSON形式に変換して標準出力するawkスクリプト。<br>
ファイル形式のチェックは行なっていない。つまり、たいしたことはやってない。

## cronの設定
毎時07分に上記スクリプトを起動し、所望の場所にファイル出力する。
<pre>
7 * * * * cat /home/shibata/his.SensorLogs/Log-2*|/home/shibata/scripts/log2json.awk > /var/www/html/Log.txt
</pre>

# 4.JSON形式ファイルの内容を可視化
## index.html
c3.jsを使ったグラフ表示を行うための入り口

## c3-test.js
JavaScriptによるグラフ表示スクリプト

# 今後の予定
表示対象のデータ範囲を指定できるようにする。

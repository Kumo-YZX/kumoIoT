--setting wifi...
ssid="your_wifi_ssid"
passw="your_wifi_password"

print('Init starts...')
wifi.setmode(wifi.STATION)
print('wifi mode:'..wifi.getmode()..'\n')
print('mac address:', wifi.sta.getmac())
print('chip id:',node.chipid())

wifi_conf={}
wifi_conf.ssid=ssid
wifi_conf.pwd=passw
wifi.sta.config(wifi_conf)

dofile("main.lua")
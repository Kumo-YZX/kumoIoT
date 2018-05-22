
print("main starts...")
consta = 0
gpio.mode(2, gpio.INPUT)

tmr.alarm(1,5000,tmr.ALARM_AUTO,function ()
    gp4 = gpio.read(2)
    print("gpio4 (2) status : "..gp4)
    if gp4 == 1 then
        if consta == 1 then
            status, temp, humi, td, hd = dht.read(5)
            print("temp : "..temp.." humi : "..humi)
            tmr.delay(2000000)
            srv = net.createConnection(net.TCP, 0)
            srv:on("receive", function(sck, c)
                print("start to receive data...")
                print(c)
            end)
            srv:on("connection", function(sck, c)
                sck:send("GET /data/upload?name\=1001&token\=yourtoken&value\="..temp.." HTTP/1.1\r\nHost: your server address\r\nConnection: close\r\nAccept: */*\r\n\r\n")
            end)
            srv:connect(8080,"your server address")
            print("connect done")
            -- srv:close()
        else
            print("net work not avilable...")
        end
    else
        print('quit...')
        tmr.stop(1)
    end
end)

tmr.alarm(0,1000,1,function ()
    if wifi.sta.getip() == nil then
        print("offline now...")
    else
        ipaddr, netmask, gateway=wifi.sta.getip()
        print("ip address:",ipaddr)
        print("netmask:",netmask)
        print("gateway:",gateway,'\n')
        consta = 1
        tmr.stop(0)
    end
end)

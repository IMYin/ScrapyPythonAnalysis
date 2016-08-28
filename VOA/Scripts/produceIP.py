#-*-conding=utf-8-*-

from CreateProxy import IPProxy

client = IPProxy()
ips = client.ipList()
client.insertTable(ips)
services = "1 2 3 4 5"
services_pos = services.find("4")
services = services[:services_pos-1] + services[services_pos+1:]

print(services)
1235
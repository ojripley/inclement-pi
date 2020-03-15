import pihole as pi

IP = '192.168.1.155'

pihole = pi.PiHole(IP)

print(pihole.refresh())
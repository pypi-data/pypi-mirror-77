## Virtual Resource Management in Cloudless System

List of system jobs encapsulated in UDP packets which will be exchanged
between worker and coordinator hosts inside an SDN environment.

- ProbeInit: sent by collector host (in a fix-interval manner).
- ProbeAck: sent by worker & monitor host (reply to ProbeInit).
- RegisterInfo:
- RegisterAck:

#### Versions:
- `2.1.x`: with QueryAck
- `3.x.x`: without QueryAck
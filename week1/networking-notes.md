What is OSI Model?


- shortcut for (Open System Interconnection Model)
- and its has 7 layers

OSI Model layers:
-1 Application -> -2 Presentation -> -3 Session -> -4 Transport -> -5 Network -> -6 Data Link -> -7 Physical


TCP/IP 4 Layers: 
-1 Network Access (Link) 
-2 Internet
-3 Transport
-4 Application (combines OSI Session, Presentation, and Application).

The OSI model is a 7-layer theoretical framework, while TCP/IP is a 4-layer practical architecture that powers the modern internet

Encapsulation: Data wraps top-down with headers—Data → Segment (Transport) → Packet (Internet) → Frame (Link) → Bits (Physical)


Domain Name System (DNS)

• Function: 
Acts as the phonebook of the internet, translating human-readable domain names (e.g., api.myapp.com) into numerical IP addresses.


TCP Three-Way Handshake

• Connection-Oriented: 
TCP guarantees reliable, ordered data delivery with error checking.

• Three-Way Handshake Steps:

	1. SYN: The client sends a synchronize packet to the server.

	2. SYN-ACK: The server responds with a synchronize-acknowledge packet.

	3. ACK: The client replies with an acknowledgement packet, and the session opens


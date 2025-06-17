from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client


# List of ips that have already sent messages to the server
client_ips = []


# this function is executed when "/hallo" is received
def hallo_handler(client_address, server_address, message, name, poti_value):

    # adds client ips that are not yet in the client_ip list 
    ip = client_address[0]
    if ip not in client_ips:
        client_ips.append(ip)
   
    # print name message and potentiometer value
    print(name)
    print(message)
    print(f"{poti_value:.3f}")
    print("---")

    # sends "/led_blink" to all clients
    for client_ip in client_ips:
        udp = udp_client.SimpleUDPClient(client_ip, 8888)
        udp.send_message("/led_blink", True)


# starts automatically at program start  
if __name__ == "__main__":

    # connects "/hallo" with the "hallo_handler" function
    disp = dispatcher.Dispatcher()
    disp.map("/hallo", hallo_handler, needs_reply_address=True)

    # creates and starts server 
    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 12345), disp)
    server.serve_forever()
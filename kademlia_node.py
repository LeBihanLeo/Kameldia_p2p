import logging
import asyncio
import threading
from kademlia.network import Server

# Initialize the logging configuration
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

async def run(port, bootstrap_ip, bootstrap_port):
    """
    Run the Kademlia node and handle user input.
    """
    # Create a node and start listening on the specified port
    node = Server()
    await node.listen(port)

    # Bootstrap the node by connecting to the specified IP and port
    await node.bootstrap([(bootstrap_ip, bootstrap_port)])
    
    while True:
        a = input("Option 1 = set  2 = get:")
        if a == '1':
            await node.set("my-key", "my awesome value")
        elif a == '2':
            # get the value associated with "my-key" from the network
            result = await node.get("my-key")
            print(result)
        else:
            print("Bad input, try again")

def user_input_thread(port, bootstrap_ip, bootstrap_port):
    """
    Create and run the user input thread.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run(port, bootstrap_ip, bootstrap_port))

while True:
    firstNode = input("Êtes-vous la première node du réseau ? (Y ou N)\n").strip().upper()
    if firstNode == "Y" or firstNode == "N":
        break
    else:
        print("Mauvaise entrée, seulement Y ou N")
port = int(input("Veuillez entrer le port sur lequel écouter : "))

if firstNode == "N":
    bootstrap_ip = input("Veuillez entrer l'adresse IP de la première node : ")
    bootstrap_port = int(input("Veuillez entrer le port de la première node : "))
else:
    bootstrap_ip = None
    bootstrap_port = None

if firstNode == "Y":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    node = Server()
    loop.run_until_complete(node.listen(port))
else:
    input_thread = threading.Thread(target=user_input_thread, args=(port, bootstrap_ip, bootstrap_port))
    input_thread.daemon = True
    input_thread.start()

try:
    if firstNode == "Y":
        loop.run_forever()
    else:
        input_thread.join()
except KeyboardInterrupt:
    pass
finally:
    # Ajoutez ici tout code de nettoyage nécessaire
    pass

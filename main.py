import ipaddress
import json
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

app = FastAPI()

def get_hosts(network_cidr):
    try:
        net = ipaddress.ip_network(network_cidr)
        # Liste des hôtes (exclut l'adresse réseau et le broadcast)
        hosts = [str(ip) for ip in net.hosts()]
        return hosts, net
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 1 & 2 - Affichage et sauvegarde des hôtes de 192.168.10.0/26
def init_setup():
    network = "192.168.10.0/26"
    hosts, _ = get_hosts(network)
    
    # Sauvegarde dans un fichier texte
    with open("hosts_list.txt", "w") as f:
        for host in hosts:
            f.write(f"{host}\n")
    print(f"Fichier 'hosts_list.txt' créé avec {len(hosts)} hôtes.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_setup()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Network API", "endpoints": ["/hosts/fixed", "/network/info?address=192.168.1.0&mask=24"]}

# 3 - API pour retourner les hôtes de 192.168.10.0/26
@app.get("/hosts/fixed")
def get_fixed_network_hosts():
    hosts, _ = get_hosts("192.168.10.0/26")
    return {"network": "192.168.10.0/26", "hosts": hosts}

# 4 - API GET avec paramètres réseau et masque
@app.get("/network/info")
def get_network_info(address: str, mask: int):
    cidr = f"{address}/{mask}"
    try:
        net = ipaddress.ip_network(cidr, strict=False)
        hosts = [str(ip) for ip in net.hosts()]
        return {
            "network_address": str(net.network_address),
            "netmask": str(net.netmask),
            "broadcast": str(net.broadcast_address),
            "gateway": str(net.network_address + 1), # Conventionnelle
            "num_hosts": len(hosts),
            "hosts": hosts
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
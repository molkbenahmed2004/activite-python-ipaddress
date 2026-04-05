
import ipaddress

def get_hosts(network_cidr: str):
    net = ipaddress.ip_network(network_cidr, strict=False)
    return [str(ip) for ip in net.hosts()]

def save_to_file(filename, hosts):
    with open(filename, "w") as f:
        for h in hosts:
            f.write(h + "\n")


if __name__ == "__main__":
    network = "192.168.10.0/26"
    hosts = get_hosts(network)

    print("Hôtes disponibles :")
    for h in hosts:
        print(h)

    save_to_file("hosts.txt", hosts)
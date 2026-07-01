# Network Automation using Netmiko in GNS3 (ITT633)

A Python-based network automation project that automates the configuration of Cisco routers using SSH. The project focuses on automating three essential networking services:

- OSPFv2 (Open Shortest Path First)
- DHCP (Dynamic Host Configuration Protocol)
- NAT (Network Address Translation)

The network is implemented in **GNS3** using Cisco 7200 IOS routers and managed through Python scripts with the **Netmiko** library.

---

## Project Overview

Traditional network configuration requires administrators to manually configure each device through the Cisco CLI. This process is time-consuming, repetitive, and prone to human error.

This project demonstrates how Python can automate these tasks by remotely connecting to multiple Cisco routers via SSH and deploying configurations automatically.

The project includes:

- Automated OSPFv2 configuration
- Automated DHCP configuration
- Automated NAT configuration
- Multi-router SSH management
- Configuration verification

---

## Network Topology

The simulated enterprise network consists of:

- HQ Department
- Sales Department
- Finance Department
- Automation Controller
- Management Network
- NAT Cloud (Internet)

Each department has:

- 1 Cisco Router
- 1 Ethernet Switch
- 2 PCs

The routers are interconnected using OSPF and managed from a dedicated Automation Controller.

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.8 | Automation scripting |
| Netmiko | SSH communication with Cisco devices |
| GNS3 | Network simulation |
| Cisco 7200 IOS | Router emulation |
| Cisco IOS CLI | Router configuration |

---

## Features

- Configure multiple routers simultaneously
- Secure SSH connections using Netmiko
- Automated deployment of:
  - OSPFv2
  - DHCP
  - NAT
- Configuration verification
- Reusable Python scripts
- Centralized network management

---

## Project Structure

```
Network-Automation/
│
├── configs/
│   ├── ospf_config.txt
│   ├── dhcp_config.txt
│   └── nat_config.txt
│
├── scripts/
│   ├── ssh_connection.py
│   ├── 1_ospf.py
│   ├── 2_dhcp.py
│   ├── 3_nat.py
│   └── verify.py
│
├── topology/
│   └── gns3_project.gns3
│
├── requirements.txt
├── README.md
└── LICENSE
```

*(Modify the folder structure above according to your repository.)*

---

## Prerequisites

Before running the scripts:

- Python 3.8 or later
- GNS3 installed
- Cisco 7200 IOS image
- SSH enabled on all routers
- Management IP configured
- Local username and password configured
- RSA keys generated
- Netmiko installed

Install Netmiko:

```bash
pip install netmiko
```

---

## SSH Configuration

Before automation can begin, every router must be manually configured with:

- Hostname
- Management IP Address
- Local Username
- Password
- Domain Name
- RSA Key
- SSH Version 2
- VTY Login
- Transport Input SSH

Example:

```text
hostname R1-HQ

ip domain-name automation.local

username admin privilege 15 secret admin123

crypto key generate rsa modulus 2048

ip ssh version 2

line vty 0 4
 login local
 transport input ssh
```

---

## Running the Scripts

Run individual automation scripts:

```bash
python ospf.py
```

```bash
python dhcp.py
```

```bash
python nat.py
```

Or execute all configurations sequentially.

---

## Example Output

```
Connecting to R1-HQ...
Connected Successfully.

Sending Configuration...

Configuration Completed.

Disconnecting...
```

---

## Project Objectives

- Reduce manual network configuration
- Improve deployment consistency
- Minimize human errors
- Demonstrate Python network automation
- Simulate enterprise network management

---

## Future Improvements

Possible future enhancements include:

- Web-based GUI
- IPv6 support (OSPFv3, DHCPv6, NAT64)
- Integration with Ansible
- REST API support
- Configuration backup and rollback
- Network monitoring dashboard
- Configuration compliance checking
- Cloud-based deployment
- Git integration for version control
- Support for additional Cisco devices

---

## License

This project is created for educational purposes.

```
MIT License
```

---

## Acknowledgements

- Cisco Systems
- GNS3
- Python Software Foundation
- Netmiko Developers

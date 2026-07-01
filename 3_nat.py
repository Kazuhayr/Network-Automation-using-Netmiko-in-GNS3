#!/usr/bin/env python3
"""
ITT633 Group Project - Script 3: NAT Automated Configuration
Configures PAT (NAT Overload) on the edge router R1-HQ.
Injects a default route into OSPF for R2-SALES and R3-FINANCE.
Using Netmiko for SSH-based automation.
"""

from netmiko import ConnectHandler
from datetime import datetime
import time

# Connection details matching the management network layout
R1_HQ = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.1',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}

R2_SALES = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.2',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}

R3_FINANCE = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.3',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}

# R1 is the Edge Router. It requires the ACL, NAT Inside/Outside tags, and PAT setup.
# We also inject the default route into OSPF so R2 and R3 know how to reach the Internet.
R1_NAT_COMMANDS = [
    'ip access-list standard NAT_ACL',
    'permit 192.168.10.0 0.0.0.255',
    'permit 192.168.20.0 0.0.0.255',
    'permit 192.168.30.0 0.0.0.255',
    'permit 10.1.1.0 0.0.0.255',
    'permit 10.1.2.0 0.0.0.255',
    'exit',
    'ip nat inside source list NAT_ACL interface GigabitEthernet3/0 overload',
    'interface GigabitEthernet3/0',
    'ip nat outside',
    'exit',
    'interface GigabitEthernet1/0',
    'ip nat inside',
    'exit',
    'interface GigabitEthernet0/0',
    'ip nat inside',
    'exit',
    'router ospf 1',
    'default-information originate'
]

# R2 and R3 are internal routers. They do not require NAT configurations themselves.
# The script will connect to them to verify the OSPF default route propagation.
R2_NAT_COMMANDS = []
R3_NAT_COMMANDS = []

def configure_nat(device_info, commands, device_name):
    print(f"\n{'='*55}")
    print(f"  Connecting to {device_name} ({device_info['host']})...")
    print(f"{'='*55}")

    try:
        connection = ConnectHandler(**device_info)
        connection.enable()
        print(f"  [OK] Connected to {device_name}")

        if commands:
            # Push NAT configuration commands for the Edge Router
            output = connection.send_config_set(commands, delay_factor=2)
            print(output)
            print(f"  [OK] NAT configuration pushed successfully")
            
            # Save configuration
            connection.exit_config_mode()
            save_output = connection.send_command('write memory')
            print(f"  [OK] Configuration saved: {save_output.strip()}")
        else:
            print(f"  [INFO] No NAT config required for {device_name} (Internal Router).")
            print(f"  [INFO] Relying on OSPF default-route injection from R1-HQ.")

        connection.disconnect()
        return True

    except Exception as e:
        print(f"  [ERROR] Connection or deployment failed for {device_name}: {e}")
        return False

def verify_nat(device_info, device_name, is_edge=False):
    print(f"\n--- Verifying NAT/Routing on {device_name} ---")
    try:
        connection = ConnectHandler(**device_info)
        connection.enable()
        
        if is_edge:
            # Check NAT statistics on the edge router
            stats = connection.send_command('show ip nat statistics')
            print(f"\n[NAT Statistics on {device_name}]")
            print(stats)
        else:
            # Check if the internal routers received the default route (0.0.0.0) via OSPF
            route = connection.send_command('show ip route 0.0.0.0')
            print(f"\n[Default Route Verification on {device_name}]")
            print(route)
            
        connection.disconnect()
    except Exception as e:
        print(f"  [ERROR] Verification failed for {device_name}: {e}")

def main():
    print("=" * 55)
    print("  ITT633 - Automated NAT Deployment Engine")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    # Execute configurations
    results = {}
    results['R1-HQ']      = configure_nat(R1_HQ,      R1_NAT_COMMANDS, 'R1-HQ')
    results['R2-SALES']   = configure_nat(R2_SALES,   R2_NAT_COMMANDS, 'R2-SALES')
    results['R3-FINANCE'] = configure_nat(R3_FINANCE, R3_NAT_COMMANDS, 'R3-FINANCE')

    print("\n[INFO] Waiting 5 seconds for OSPF to propagate the default route...")
    time.sleep(5)

    print("\n" + "="*55)
    print("  NAT & ROUTING VERIFICATION")
    print("="*55)
    # Verify R1 edge NAT, and R2/R3 default routes
    verify_nat(R1_HQ,      'R1-HQ', is_edge=True)
    verify_nat(R2_SALES,   'R2-SALES', is_edge=False)
    verify_nat(R3_FINANCE, 'R3-FINANCE', is_edge=False)

    print("\n" + "="*55)
    print("  DEPLOYMENT SUMMARY")
    print("="*55)
    for device, status in results.items():
        print(f"  {device:<15} : {'SUCCESS' if status else 'FAILED'}")
    print(f"\n  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*55)

if __name__ == '__main__':
    main()
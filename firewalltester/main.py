from contextlib import closing
import requests
import json, socket

class Main(object):

    def __init__(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {}

        default_settings = {'servers': {}, 'webhook': ''}
        edited = False

        for key, value in default_settings.items():
            if key not in self.settings:
                self.settings[key] = value
                edited = True

        if edited:
            self.save_settings()

        self.webhook = self.settings['webhook']
        self.servers = self.settings['servers']
        self.check_servers(self.servers)

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, sort_keys=True, indent=4, separators=(',', ': '))

    def check_servers(self, servers):
        all_open_ports = {}

        for name, server in sorted(servers.items()):
            open_ports = self.check_open_ports(server)

            if open_ports:
                all_open_ports[name] = open_ports

        if all_open_ports:
            messages = []

            for name, open_ports in all_open_ports.items():
                ip = servers[name]['ip']
                open_ports = ', '.join(str(port) for port in open_ports)
                messages.append(f'**{name}** - IP *{ip}* - Open ports: **{open_ports}**')

            messages = '\n'.join(messages)
            self.send_webhook(self.webhook, f'@everyone Some of your firewalls are down!\n\n{messages}')

    def check_open_ports(self, server):
        return [port for port in server['ports'] if self.is_port_open(server['ip'], port)]

    def is_port_open(self, host, port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(0.5)
            return sock.connect_ex((host, port)) == 0

    def send_webhook(self, webhook, message):
        if not webhook:
            print(message)
            return

        for msg in [message[x:x+19980] for x in range(0, len(message), 19980)]:
            requests.post(webhook, headers={'User-Agent': 'Mozilla/5.0'}, data={'content': msg})

if __name__ == '__main__':
    main = Main()

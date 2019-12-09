from contextlib import closing
import requests
import json, socket

class Main(object):

    def __init__(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            self.settings = {}

        defaultSettings = {'servers': {}, 'webhook': ''}
        edited = False

        for key, value in defaultSettings.items():
            if key not in self.settings:
                self.settings[key] = value
                edited = True

        if edited:
            self.saveSettings()

        self.webhook = self.settings['webhook']
        self.servers = self.settings['servers']
        self.checkServers(self.servers)

    def saveSettings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, sort_keys=True, indent=4, separators=(',', ': '))

    def checkServers(self, servers):
        allOpenPorts = {}

        for name, server in sorted(servers.items()):
            openPorts = self.checkOpenPorts(server)

            if openPorts:
                allOpenPorts[name] = openPorts

        if allOpenPorts:
            message = "@everyone Some of your firewalls are down!\n\n"
            messages = []

            for name, openPorts in allOpenPorts.items():
                ip = servers[name]['ip']
                messages.append('**{0}** - IP *{1}* - Open ports: **{2}**'.format(name, ip, ', '.join(str(port) for port in openPorts)))

            message += '\n'.join(messages)
            self.sendWebhook(self.webhook, message)

    def checkOpenPorts(self, server):
        return [port for port in server['ports'] if self.isPortOpen(server['ip'], port)]

    def isPortOpen(self, host, port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(0.5)
            return sock.connect_ex((host, port)) == 0

    def sendWebhook(self, webhook, message):
        if not webhook:
            print(message)
            return

        for msg in [message[x:x+19980] for x in range(0, len(message), 19980)]:
            requests.post(webhook, headers={'User-Agent': 'Mozilla/5.0'}, data={'content': msg})

if __name__ == '__main__':
    main = Main()

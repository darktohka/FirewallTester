# FirewallTester

A small utility to automatically monitor firewalls, alerting system administrators when they fail.

Basically the inverse of Uptime Robot. When your firewalls fail, an alert is sent through a webhook link of your choice.

This webhook link is Slack-compatible and can be used with applications like Slack or Discord.

## Getting Started

First, install Python 3 on your machine, then clone the project, install the Python requirements, and run the project once to generate your `settings.json` file:

```
git clone https://github.com/darktoha/FirewallTester
python3 -m pip install -r requirements.txt
cd scripts
sudo sh run.sh
```

Next, edit the `settings.json` file to your liking:

* `servers`: A list of all servers that will be checked.
* `webhook`: A link to your Slack-compatible webhook. This value is specified by your application.

An example configuration:
```json
{
    "servers": {
        "My Server": {
            "ip": "8.8.8.8",
            "ports": [1000, 2000]
        }
    },
    "webhook": "https://hooks.slack.com/services"
}
```

Next, run the firewall tester to make sure it works:

```
sudo sh run.sh
```

After running the firewall tester, you might want to set up a cronjob to automatically test your firewall:

```
sudo crontab -e
```

Here's an example crontab configuration that will run FirewallTester installed in `/star/firewalltester` every hour:

```
0 * * * * /bin/bash /star/firewalltester/scripts/run.sh >/dev/null 2>&1
```

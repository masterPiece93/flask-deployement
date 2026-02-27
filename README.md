# Flask Web App on HTTPS

hosting a flask webapp on linux with gunicorn over vpc (@lightsail) using webserver-reverseproxy (@caddy)

|   |   |
|---|---|
| **framework** | Flask |
| **os** | Ubuntu `22.04` |
| **vps** | lightsail |
| **reverse-proxy** | caddy |

### Pre-requisite :

1. A Domain Name .
2. A LightSail ( or any other VPS ) ( with ssh setup )

[Tutorial-link](https://www.youtube.com/watch?v=vfZgHX5ttsY)

### Tutorial Commands :
Following Commands are used in sequential order in the tutotial :

```sh
sudo apt update 
```

```sh
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https 
```

```sh
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg 
```

```sh
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list 
```

```sh
sudo apt update
```

```sh
sudo apt install caddy 
```

```sh
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools 
```

```sh
sudo apt install python3-venv
```

### Caddy Debugging

Check Caddy Service :
```sh
ps aux | grep caddy
```

Kill Caddy service
```sh
sudo killall caddy
```

Check the Caddy Logs for Specific Errors: 
_The systemd status command often truncates logs. Use journalctl to see the full output and identify the specific error message Caddy encountered during startup._
```sh
journalctl -u caddy.service --no-pager | less +G
```

Reload systemd and restart the service:
```sh
sudo systemctl daemon-reload
sudo systemctl restart caddy.service
```

Syntax errors are the most common cause of failure. Run this command to check for errors in your configuration: 
```sh
caddy validate --config /path/to/Caddyfile
```

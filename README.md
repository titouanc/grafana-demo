# Demo for the "Monitoring && operations with Grafana and InfluxDB" talk

## Installing docker-compose

Docker allows you to run application in an isolated environment (a container)
on your computer. These containers bundle everything needed to run their
application, without the need to install custom packages on your system.

Docker-compose allows to compose several application into a whole system. I use
these to simplify the setup of influxdb, grafana and an example feeder script.

```bash
apt install docker docker-compose
```

## Run the demo

1. Clone this repository:

```bash
git clone https://github.com/titouanc/grafana-demo
cd grafana-demo
```

2. Grab your irclogs and place them in **feeder/irclogs**. 
   They should be given the name `#chan.format`.
   Example: `#urlab.irssi` or `#urlab35c3.weechat`

3. Start the containers:

```bash
docker-compose up --build
```

Then visit http://localhost/.
The default username:password is `admin:admin`

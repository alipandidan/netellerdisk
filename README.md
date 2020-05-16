# NetEllerDisk

NetEllerDisk is a simple Python script which is born for the sole porpose of utilizing disk and network resources in parallel to detect the actual bottleneck in complex environments

## Usage

Make sure you have at least python 3.7 installed, download the script and make it executable:

```bash
curl -o netellerdisk https://raw.githubusercontent.com/pandidan/netellerdisk/master/netellerdisk.py \
&& chmod +x netllerdisk
```
Start NetEllerDisk in server mode on your desired node:
```bash
./netellerdisk
```

Start NetEllerDisk in client mode on another node by feeding the server URL as source:
```bash
./netellerdisk --source http://192.168.13.37:8000
```

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. If you have any comments please feel free to shoot me an email.

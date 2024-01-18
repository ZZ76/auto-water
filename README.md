# auto-water

## Set python script service using systemctl
insgall systemctl if not exist:
```
sudo apt-get install -y systemd
```

systemctl file location:
```
/etc/systemd/system/auto-water.service
```

reload systemctl and enable `auto-water.service` at boot:
```
sudo systemctl daemon-reload
sudo systemctl enable auto-water.service
sudo systemctl start auto-water.service
```

## Trouble shooting
If failed to launch service, check systemctl log with:
```
journalctl -u auto-water.service
#or with -b only for current boot
journalctl -u auto-water.service -b
```
If it is package import issue, add `User=<username>` in `[Service]` section of `auto-water.service` file
or
add `Environment="PYTHON=$PYTHONPATH:/home/<username>/.local/lib/python3.9/site-packages"` to `[Service]`

to find site packages location, in python:
```
import site
site.getsitepackages()
```

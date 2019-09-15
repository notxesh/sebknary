# SEBKnary
A HTTP And DNS knary written in Python
Currently pushes all alerts too a discord web hook
Configuration is done through `.env` files
### Installing
```$> git clone https://github.com/0xesh/sebknary
$> cd sebknary
$> python3.7 -m pip install -r requirements.txt
```
Then configure your domain(s) to point to your servers IP address for
dns and general queries
Make sure to configure the `.env` file to suite your needs, the file
`exmaple.env` is the template for the `.env` file. Make sure to have
set your `WEBHOOK_DISCORD` too a valid discord webhook and set `DNS`
and `HTTP` to enable listening.
To enable `HTTPS` set `HTTP_USE_HTTPS` in the environment and provide
both the key and certificate files through `HTTPS_KEY` and `HTTPS_CERT`
respectively.
This is more of a passion project so please dont expect thorough troubleshooting
and general tips form me.
### Running
Just run `knary.py` under a screen to have it run in the background
`$> python3.7 knary.py`

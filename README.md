# Brightcoin Core
Brightcoin is a dummy cryptocurrency that implements the Bitcoin protocol.

## Installing
If you haven't already, install `docker` (it's an amazing tool to deploy webapps with).
Then run:
```bash
git clone git@github.com:vikramdurai/brightcoin
cd brightcoin
docker build -t brightcoin .
docker run -p 8080:8080 brightcoin
```
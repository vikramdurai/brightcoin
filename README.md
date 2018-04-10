# Brightcoin Core
Brightcoin is a fee-less cryptocurrency for payments (it's an alternative to Bitcoin).

## Installing
If you haven't already, install `docker` (it's an amazing tool to deploy apps with):
```bash
yes | sudo apt-get install
yes | sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
test $(sudo apt-key fingerprint 0EBFCD88 | grep 'Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88')
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
yes | sudo apt-get update
yes | sudo apt-get install docker-ce
```
Then run:
```bash
git clone git@github.com:vikramdurai/brightcoin
cd brightcoin
sudo docker build -t brightcoin .
sudo docker run -p 8080:8080 brightcoin
```
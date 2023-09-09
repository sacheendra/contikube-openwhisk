Requires at least a 3 node kubernetes cluster. One for kubernetes control place, one for openwhisk control plane, and the rest for invokers.

### Mark nodes for the help chart
```
kubectl label nodes cloud0stalluri openwhisk-role=core

kubectl label nodes -l 'openwhisk-role!=core,!node-role.kubernetes.io/control-plane' openwhisk-role=invoker
```

### Add a helm repo and deploy openwhisk
```
./helm repo add openwhisk https://openwhisk.apache.org/charts
./helm repo update
./helm install owdev openwhisk/openwhisk -n default -f mycluster.yaml
```

### Configure openwhisk cli
Use the ip of the node openwhisk controller was deployed on.
```
./wsk property set --apihost 192.168.55.3:31001
./wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
```

### Test basic function creation and invocation
./wsk -i action create hello hello.js
./wsk -i action invoke hello --result

## Running the Sebs benchmark
1. Install docker, python3-venv, libcurl4-openssl-dev, and libssl-dev on the cloud controller node.
2. Clone the sebs repo: https://github.com/spcl/serverless-benchmarks
3. Run `./install.py --openwhisk --local`
4. Activate the sebs environment `. python-venv/bin/activate`
5. Start local storage `./sebs.py storage start minio --port 9011 --output-json out_storage.json`
6. Download the `wsk` binary and add it to path. `wget https://github.com/apache/openwhisk-cli/releases/download/1.2.0/OpenWhisk_CLI-1.2.0-linux-amd64.tgz`
7. Add wsk to path `export PATH="/home/cloud_controller_stalluri/bin:$PATH"`
8. Copy storage config to example config file.
9. Run test as described in https://github.com/spcl/serverless-benchmarks/blob/master/docs/usage.md



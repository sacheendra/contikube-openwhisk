#!/bin/bash

# run experiments with increasing number of nodes

# 8 cores
kubectl label nodes cloud2 openwhisk-role=invoker
node run-experiment.js 1 8 50 exp_results_50/1node
node run-experiment.js 2 8 50 exp_results_50/1node
node run-experiment.js 4 8 50 exp_results_50/1node

# 16 cores
kubectl label nodes cloud3 openwhisk-role=invoker
node run-experiment.js 1 16 50 exp_results_50/2node
node run-experiment.js 2 16 50 exp_results_50/2node
node run-experiment.js 4 16 50 exp_results_50/2node

# 32 cores
kubectl label nodes cloud4 openwhisk-role=invoker
kubectl label nodes cloud5 openwhisk-role=invoker
node run-experiment.js 1 32 50 exp_results_50/3node
node run-experiment.js 2 32 50 exp_results_50/3node
node run-experiment.js 4 32 50 exp_results_50/3node

# 64 cores
kubectl label nodes cloud6 openwhisk-role=invoker
kubectl label nodes cloud7 openwhisk-role=invoker
kubectl label nodes cloud8 openwhisk-role=invoker
kubectl label nodes cloud9 openwhisk-role=invoker
node run-experiment.js 1 64 50 exp_results_50/4node
node run-experiment.js 2 64 50 exp_results_50/4node
node run-experiment.js 4 64 50 exp_results_50/4node

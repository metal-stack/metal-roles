#!/bin/bash

HWSKU=$(cat /etc/sonic/sonic-environment | grep HWSKU | sed "s/HWSKU=//")
sonic-cfggen -H -d --preset empty -k $HWSKU > /etc/sonic/config_db.json

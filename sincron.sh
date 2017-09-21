#!/bin/sh
#rsync -arv --rsh=/usr/bin/ssh /opt/odoo/v8/disna-sistemas odoo@192.168.5.21:/opt/odoo/v8
sshpass -p bat1bi2 rsync -arv /opt/odoo/v8/disna-sistemas odoo@192.168.5.21:/opt/odoo/v8

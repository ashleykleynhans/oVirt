#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ovirtsdk4 as sdk

# set variables
fqdn = 'host.example.com'
password = 'password'

# Create the connection to the server:
connection = sdk.Connection(
  url=f'https://{fqdn}/ovirt-engine/api',
  username='admin@internal',
  password=password,
  insecure=True,
  debug=True,
)

# Create the storage domain service and get a list of storage domains
sds_service = connection.system_service().storage_domains_service()
storage_domains = sds_service.list()

# Iterate over the storage domains and get the used and available
# disk space for each
for sd in storage_domains:
  print(f'name: {sd.name}, used: {sd.used}, available: {sd.available}')

# Close the connection to the server:
connection.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ovirtsdk4 as sdk
import re

# set variables
fqdn = 'host.example.com'
password = 'passwod'

# Create the connection to the server:
connection = sdk.Connection(
  url=f'https://{fqdn}/ovirt-engine/api',
  username='admin@internal',
  password=password,
  insecure=True,
  debug=True,
)

def get_storage_domain(dc):
  dc = dc.upper()
  storage_domain = None

  # Create the storage domain service and get a list of storage domains
  sds_service = connection.system_service().storage_domains_service()
  storage_domains = sds_service.list()

  # Iterate over the storage domains and get the used and available
  # disk space for each
  for sd in storage_domains:
    match = re.match("^\w+_(" + dc + ")_\w+$", sd.name)

    if not match:
      continue

    if storage_domain is None:
      storage_domain = sd
      continue

    if sd.available is not None and sd.available > storage_domain.available:
      storage_domain = sd

  # Close the connection to the server:
  connection.close()

  return storage_domain.name

# Get the storage domains that match example_dc and return the one with
# the most available disk space
sd = get_storage_domain('example_dc')
print(sd)

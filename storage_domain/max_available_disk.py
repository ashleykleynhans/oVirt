#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ovirtsdk4 as sdk
import re

# set variables
fqdn = 'host.example.com'
password = 'password'
dc_name = 'example_dc'

# Create the connection to the server:
connection = sdk.Connection(
  url=f'https://{fqdn}/ovirt-engine/api',
  username='admin@internal',
  password=password,
  ca_file="CA_FILE_PATH"
)

def get_storage_domain():
  storage_domain = None

  # Create the Data Centers Service
  dcs_service = connection.system_service().data_centers_service()

  # Get the list of Storage Domains for the service that Match the Data Centre Name
  dc = dcs_service.list(search=f'name={dc_name}', max=1, follow='storage_domains')
  dc = dc[0]

  for sd in dc.storage_domains:
    if storage_domain is None:
      storage_domain = sd
      continue

    if sd.available is not None and sd.available > storage_domain.available:
      storage_domain = sd

  # Close the connection to the server:
  connection.close()

  return storage_domain.name

# Get the storage domains return the one with
# the most available disk space
sd = get_storage_domain()
print(sd)

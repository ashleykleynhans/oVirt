#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ovirtsdk4 as sdk

# set variables
engine_url = 'https://host.example.com/ovirt-engine/api'
engine_user = 'admin@internal'
engine_password = 'password'
engine_cafile = 'CA_FILE_PATH'
cluster = 'cluster_name'

# Create the connection to the server:
connection = sdk.Connection(
  url=engine_url,
  username=engine_user,
  password=engine_password,
  ca_file=engine_cafile
)

def get_storage_domain():
  storage_domain = None

  # Create the Clusters Service
  clusters_service = connection.system_service().clusters_service()

  # Get the list of Storage Domains for the service that Match the Cluser Name
  clstr = clusters_service.list(search=f'name={cluster}', max=1, follow='data_center.storage_domains')
  clstr = clstr[0]

  for sd in clstr.data_center.storage_domains:
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

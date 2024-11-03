#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <storage_account_name> <resource_group>"
    exit 1
fi

# Assign command line arguments to variables
storage_account_name=$1
resource_group=$2

# Retrieve the storage account key
account_key=$(az storage account keys list --resource-group $resource_group --account-name $storage_account_name --query '[0].value' --output tsv)

# Containers to be emptied
containers=("inbox" "west" "east" "central")

# Delete all blobs in each container
for container in "${containers[@]}"; do
    az storage blob delete-batch --account-name $storage_account_name --source $container --account-key $account_key
    echo "All files in container '$container' have been deleted."
done

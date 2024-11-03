# Blob Storage Function Support Files
This repository contains several files used to support the blob_storage_function application in MGMT 59000 Cloud Computing.

Clone this repository to your Cloud Shell to use these files.

* `setup_containers.sh`
    * Requires two parameters: Storage Account Name and Resource Group Name
    * Creates four containers in the Storage Account: `inbox`, `east`, `west`, `central`

* `cleanup_containers.sh`
    * Requires two parameters: Storage Account Name and Resource Group Name
    * Uses the Azure CLI to remove all files from the aforementioned containers

* `generate_orders.py`
    * Generates random orders to use with the application
    * Accepts 1 optional parameter `-n` that specifies the number of sample orders to create (default is 10 orders)
    * Empties the contents of the `sample_orders` directory and stores new auto-generated orders in that directory
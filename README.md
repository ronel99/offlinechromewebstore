<img src="cwsoffline/cwsstore/app/static/images/favicon.png" alt="cws icon" width="200" height="200"/>

# Offline Chrome Web Store


# Chrome Web Store - Offline Store, Builder and Updater 


This enables Chrome Web Store's web presence to be mirrored for seamless use in an offline environment (e.g. air-gapped), or to run a private web store.

## Features

On the Internet connected system , **cwssync** will:
* Mirror the Chrome Extensions across platforms (Windows|Linux|Darwin);
* Mirror recommended/typical extensions from the Chrome Web Store;
* Mirror the malicious extension list.
* Optionally, mirror all extensions (--syncall, rather than the default of --sync).

On the non-Internet connected system, **cwsbuild**:
* Implements UI store assets (images and metadata) from CRX files;
* Implements the updater interface to enable use of first party extensions.

On the non-Internet connected system, **cwsstore**:
* Implements the updater interface to enable offline updating.
* Implements the extension API to enable offline extension use.
* Implements initial support for multiple versions.
* Supports custom/private extensions (follow the structure of a mirrored extension).
* Impliments `/crx` like https://clients2.google.com/service/update2/crx
* Impliments `/json` route for view raw properties of extenions and api scripting capabilities.



## Requirements
* Docker (ideally with docker-compose for simplicity)

## Getting Started - Full Offline Use - Using Docker Containers

There are three components, **cwssync** which mirrors the content on an Internet connected system, **cwsbuild** which build assets for UI store from crx files (1st and 3rd party) and **cwsstore** which provides the necessary APIs and endpoints necessary to support Chrome Extensions use. While it is designed for offline environments, it is possible, with some DNS trickery, that this could be operated as a "corporate" Chrome Web Store.

On the Internet connected system:

1. Acquire/mirror the Docker containers (cwssync / cwsbuild / cwsstore). 

    `docker-compose pull`
    
2. Setup and run the cwssync service on the Internet connected system.
    * Ensuring the artifact directory is accessible to whatever transfer mechanism you will use and cwssync.
    * Run cwssync service and ensure the artifacts are generated.
    * Wait for the sync to complete. You should see 'Sync completed' and that it is sleeping when the artifacts have finished downloading.

    ``` bash
    docker compose up cwssync
    ```

3. Copy the artifacts to the non-Internet connected system.

On the non-Internet connected system:
1. Run the **cwsbuild** service to build assets

    ``` bash
    docker compose up cwsbuild
    ```

2. Run the cwsstore service, ensuring the artifacts are accessible to the service.

    ``` bash
    docker compose up cwsstore -d
    ```
3. Configure chrome policy to add **_http://cws_intranet_domain/*_** as **ExtensionInstallSources**, see [Configure GPO](#configure-gpo) section
4. Open Chrome, hopefully you can magically install extensions.

#### Run with docker compose
``` bash
docker compose build
docker compose run cwssync
docker compose up -d cwsbuild cwsstore
```

#### How to build
```bash
# build cwssync
docker build -t cwssync -f cwsoffline/cwssync/Dockerfile .
# build cwsbuild
docker build -t cwsbuild -f cwsoffline/cwsbuild/Dockerfile .
# build cwsstore
docker build -t cwsstore -f cwsoffline/cwsstore/Dockerfile ./cwsoffline/cwsstore/
```

#### How to run with docker
``` bash
# Run the container
docker run -it -v $(pwd)/artifacts:/app/artifacts cwssync

# Run cwsbuild
docker run -it -v $(pwd)/artifacts:/app/artifacts -v $(pwd)/assets:/app/assets cwsbuild

# Run cwsstore
docker run -it -v $(pwd)/artifacts:/store/artifacts -v $(pwd)/assets:/store/assets -p 8005:8005 cwsstore
```

#### Cleanup
``` bash
# Remove cwssync exited and running images
docker ps -a | grep -E ^cws | awk '{print $1}' | xargs docker rm -f

# Remove artifacts folder after using docker
sudo rm -rf artifacts
```

#### Configure GPO
- *See [ExtensionInstallAllowlist](https://chromeenterprise.google/policies/?policy=ExtensionInstallAllowlist) chrome policy to configure allowlist for enhanced security*
- *See [ExtensionInstallSources](https://chromeenterprise.google/policies/#ExtensionInstallSources) chrome policy to configure source for custom offline store url*
- *See [ExtensionInstallForcelist](https://chromeenterprise.google/policies/#ExtensionInstallForcelist) to force install extenions from `https://cws_domain/crx`*

---

Possible Implements TODO List:
* - [ ] Add test cases.
* - [ ] ExtensionTotal get malicious extensions
* - [X] crx expand and create json job for cwsstore
* - [ ] add helm (kubernetes) support
* - [ ] fix extension container properties alignments
* - [ ] list of manually specified extensions (artifacts/specified.json)
* - [ ] implements malicious extension list
* - [ ] check possibility to implement configure DNS in a air gapped env to https://clients2.google.com/service/update2/crx and https://chromewebstore.google.com when chrome uses HSTS.
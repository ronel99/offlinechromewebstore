# Offline Chrome Web Store


# Chrome Web Store - Offline Store, Builder and Updater 


This enables Chrome Web Store's web presence to be mirrored for seamless use in an offline environment (e.g. air-gapped), or to run a private web store.

## Features

On the Internet connected system , **cwssync** will:
* Mirror the Chrome Extensions across platforms (Windows|Linux|Darwin);
* Mirror recommended/typical extensions from the Chrome Web Store;
* Mirror the malicious extension list; 
* Mirror a list of manually specified extensions (artifacts/specified.json); and
* Optionally, mirror all extensions (--syncall, rather than the default of --sync).

On the non-Internet connected system, **cwsstore**:
* Implements the updater interface to enable offline updating;
* Implements the extension API to enable offline extension use;
* Implements the malicious extension list; 
* Implements initial support for multiple versions;
* Supports custom/private extensions (follow the structure of a mirrored extension);

On the non-Internet connected system, **cwsbuild**:
* Implements ui store assets (images and metadata) from CRX files;
* Implements the updater interface to enable use of first party extensions.

Possible TODO List:
* - [ ] Add test cases.
* - [ ] ExtensionTotal get malicious extensions
* - [ ] crx expand and create json job for cwsserver
* - [ ] add helm (kubernetes) support

## Requirements
* Docker (ideally with docker-compose for simplicity)

## Getting Started - Full Offline Use - Using Docker Containers

There are three components, **cwssync** which mirrors the content on an Internet connected system, **cwsbuild** which build assets for UI store from crx files (1st and 3rd party) and **cwsstore** which provides the necessary APIs and endpoints necessary to support Chrome Extensions use. While it is designed for offline environments, it is possible, with some DNS trickery, that this could be operated as a "corporate" Chrome Web Store.

On the Internet connected system:

1. Acquire/mirror the Docker containers (cwssync/cwsbuild/cwsstore). 

    <pre><p style="color:Red;">TO-DO

    `docker-compose pull`

    </p>
    </pre>

2. Setup and run the cwssync service on the Internet connected system.
    * Ensuring the artifact directory is accessible to whatever transfer mechanism you will use and cwssync.
    * Run cwssync service and ensure the artifacts are generated.
    * Wait for the sync to complete. You should see 'Complete' and that it is sleeping when the artifacts have finished downloading.

    `docker-compose up cwssync`

3. Copy the artifacts to the non-Internet connected system.

On the non-Internet connected system:

1. On the non-Internet connected system, ensure the following DNS addresses are pointed toward the cwsstore service.
    * clients2.google.com        

    This may be achieved using a corporate DNS server, or by modifying a client's host file.

2. Run the cwsstore service, ensuring the artifacts are accessible to the service. It needs to listen on port 443.

    `docker-compose up cwsstore`

3. Using Chrome/Firefox navigate to https://update.code.visualstudio.com. You should not see any certificate warnings, if you do it's unlikely to work in.

4. Open Chrome, hopefully you can magically install extensions. The Help > Developer Tools > Network should tell you what is going on.


#### How to run
```bash
# Build the Docker image
docker build -t cwssync -f cwsoffline/cwssync/Dockerfile .

# Run the container
docker run -it -v $(pwd)/artifacts:/app/artifacts cwssync

# Remove cwssync exited and running images
docker ps -a | grep cwssync | awk '{print $1}' | xargs docker rm -f

# Remove artifacts folder after using docker
sudo rm -rf artifacts
```

#### Configure GPO
- *See [ExtensionInstallAllowlist](https://chromeenterprise.google/policies/?policy=ExtensionInstallAllowlist) chrome policy to configure allowlist for enhanced security*
- *See [ExtensionainstallSources](https://chromeenterprise.google/policies/#ExtensionInstallSources) chrome policy to configure source for custom offline store url*
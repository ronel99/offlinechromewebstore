# Offline Chrome Web Store
#### How to run

```bash
# Build the Docker image
docker build -t chrome-extension-sync .

# Run the container
docker run -v $(pwd)/downloads:/app/downloads chrome-extension-sync
```

#### Configure GPO
*See [ExtensionInstallAllowlist](https://chromeenterprise.google/policies/?policy=ExtensionInstallAllowlist) chrome policy to configure allowlist for enhanced security*

#### TODO
- [ ] ExtensionTotal get malicious extensions
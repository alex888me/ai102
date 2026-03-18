# Install Azure CLI on Fedora

Use the Microsoft signing key and RHEL 10 package source, then install `azure-cli` with `dnf`:

```bash
sudo rpm --import https://packages.microsoft.com/keys/microsoft-2025.asc
sudo dnf install -y https://packages.microsoft.com/config/rhel/10/packages-microsoft-prod.rpm
sudo dnf install azure-cli
```

Verify the installation:

```bash
az version
```

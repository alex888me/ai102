# Installing Visual Studio Code on Fedora Linux

Visual Studio Code (VSCode) can be installed on Fedora Linux using the official Microsoft repository. Follow these steps:

1. Import the Microsoft GPG key:

   ```bash
   sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
   ```

2. Add the VSCode repository to your system:

   ```bash
   sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
   ```

3. Install VSCode:

   ```bash
   sudo dnf install code
   ```

4. After installation, you can launch VSCode from the applications menu or by running:

   ```bash
   code
   ```

To update VSCode in the future, use:

```bash
sudo dnf update code
```
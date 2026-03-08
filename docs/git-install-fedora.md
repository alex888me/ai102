# Installing Git on Fedora Linux

Git is available in the default Fedora repositories. To install it, run the following command:

```bash
sudo dnf install git
```

After installation, verify that Git is installed correctly by checking its version:

```bash
git --version
```

You can now configure Git with your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
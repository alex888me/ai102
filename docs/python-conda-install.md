# Python Installation with Conda

## Installing Conda on Fedora Linux

Run the following commands as a regular user account (do not use `root`).

To install Miniconda (a minimal installer for conda) on Fedora Linux, follow these steps:

1. Download the latest Miniconda installer for Linux:

   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   ```

2. Run the installer script:

   ```bash
   bash Miniconda3-latest-Linux-x86_64.sh
   ```

3. Follow the prompts during installation. When asked to initialize conda, choose "yes" to add conda to your PATH.

4. After installation, restart your terminal or run:

   ```bash
   source ~/.bashrc
   ```

   to activate conda.


Use the following command to create a Conda environment with Python 3.14.3:

```bash
conda create -n py314 python=3.14.3
```

After creating the environment, activate it with:

```bash
conda activate py314
```

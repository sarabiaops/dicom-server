# DICOM Server using pynetdicom

This repository contains a simple DICOM server implemented using the `pynetdicom` library. The server listens for DICOM C-ECHO and C-STORE requests, logs the details, and saves received DICOM files.

## Prerequisites

- Python 3.6+
- Virtual environment (`venv`)
- AWS EC2 instance (optional, for deployment)

## Setup

### Clone the Repository

```sh
git clone https://github.com/your-username/dicom-server.git
cd dicom-server
```

### Create and Activate Virtual Environment

1. **Create a virtual environment:**

    ```sh
    python3 -m venv myenv
    ```

2. **Activate the virtual environment:**

    ```sh
    source myenv/bin/activate
    ```

### Install Dependencies

```sh
pip install pynetdicom
```

## Running the Server

### Local Machine

1. **Ensure the virtual environment is activated:**

    ```sh
    source myenv/bin/activate
    ```

2. **Run the server script:**

    ```sh
    python3 server.py
    ```

### AWS EC2 Instance

1. **SSH into your EC2 instance:**

    ```sh
    ssh -i /path/to/your-key-file.pem ubuntu@your-ec2-public-dns
    ```

2. **Install Python and Virtual Environment:**

    ```sh
    sudo apt-get update
    sudo apt-get install python3 python3-venv
    ```

3. **Clone the repository and navigate to the directory:**

    ```sh
    git clone https://github.com/your-username/dicom-server.git
    cd dicom-server
    ```

4. **Create and activate the virtual environment:**

    ```sh
    python3 -m venv myenv
    source myenv/bin/activate
    ```

5. **Install dependencies:**

    ```sh
    pip install pynetdicom
    ```

6. **Run the server script:**

    ```sh
    python3 server.py
    ```

## Security Group Configuration for EC2

Ensure your EC2 instance's security group allows inbound traffic on the required port (e.g., 8080 for testing):

- **Type**: Custom TCP Rule
- **Protocol**: TCP
- **Port Range**: 8080
- **Source**: 0.0.0.0/0 (or restrict to specific IPs as needed)

## Script Details

### server.py

This script initializes a DICOM Application Entity (AE), sets up handlers for C-ECHO and C-STORE requests, and starts the server on the specified port (default 8080).

## Logging

The server logs various details including the start and stop events, incoming requests, and any errors. The logs are printed to the console.

## Troubleshooting

If you encounter issues, ensure:

1. The virtual environment is activated.
2. All dependencies are installed.
3. The correct port is open in your EC2 security group.
4. Check the server logs for error messages.

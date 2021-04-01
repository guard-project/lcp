# Local Control Plane

[![License](https://img.shields.io/github/license/guard-project/lcp)](https://github.com/guard-project/lcp/blob/master/LICENSE)
[![Code size](https://img.shields.io/github/languages/code-size/guard-project/lcp?color=red&logo=github)](https://github.com/guard-project/lcp)
[![Repository Size](https://img.shields.io/github/repo-size/guard-project/lcp?color=red&logo=github)](https://github.com/guard-project/lcp)
[![Release](https://img.shields.io/github/v/tag/guard-project/lcp?label=release&logo=github)](https://github.com/guard-project/lcp/releases)
[![Docker image](https://img.shields.io/docker/image-size/guardproject/lcp?label=image&logo=docker)](https://hub.docker.com/repository/docker/guardproject/lcp)
[![Docs](https://readthedocs.org/projects/guard-lcp/badge/?version=latest)](https://guard-lcp.readthedocs.io)

In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.

---

- [Local Control Plane](#local-control-plane)
  - [Guide](#guide)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Display help](#display-help)
    - [Execute](#execute)
  - [Extra](#extra)

---

## Guide

See the [Swagger Schema](swagger/schema.yaml) for more details about the REST endpoints and relative formats and requirements of request and response.

## Installation

1. Prerequisite

   - python3
   - pip3

2. Clone the repository.

   ```bash
   git clone https://gitlab.com/guard-repositories/lcp.git
   cd lcp
   ```

3. Install the dependencies (optional).

   ```bash
   pip3 install -r requirements.txt
   ```

## Configuration

The configurations are stored in the [config.ini](config.ini) file.

Section             | Setting       | Default value         | Note
--------------------|---------------|-----------------------|---------------------------
local-control-plane | host          | 0.0.0.0               | IP address to accept requests.
local-control-plane | port          | 4000                  | TCP port to accept requests.
local-control-plane | https         | false                 | Accept only HTTPS requests.
auth                | enabled       | true                  | Enable JWT authentication.
auth                | header-prefix | GUARD                 | Header prefix for JWT authentication.
auth                | secret-key    | guard-secret-key      | Secret key for JWT authentication.
elastic-apm         | enabled       | false                 | Enable Elastic APM integration.
elastic-apm         | server        | http://localhost:8200 | Elastic APM server.
polycube            | host          | localhost             | IP address to contact the polycube installation.
polycube            | port          | 9000                  | Port address to contact the polycube installation.
polycube            | timeout       | 20s                   | Timeout for the connection to polycube.
log                 | config        | log.yaml              | Path of the log configuration file.

## Usage

### Display help

```bash
python3 main.py -h
```

### Execute

```bash
python3 main.py
```

## Extra

See the **Issues** for *features* in development.

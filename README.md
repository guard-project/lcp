# GUARD Local Control Plane

In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.

---

- [GUARD Local Control Plane](#guard-local-control-plane)
  - [Guide](#guide)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Display help](#display-help)
    - [Execute](#execute)
  - [Extra](#extra)

---

## Guide

See the [Swagger Schema](swagger.yml) and the relative [documentation](https://app.swaggerhub.com/apis-docs/alexcarrega/guard-lcp/0.0.1) for more details about the REST endpoints and relative formats and requirements of request and response.

## Installation

1. Prerequisite

   - python3
   - pip3

2. Clone the repository.

   ```bash
   git clone https://gitlab.com/guard-repositories/guard-local-control-plane.git
   cd guard-local-control-plane
   ```

3. Install the dependencies.

   ```bash
   pip3 install -r requirements.txt
   ```

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

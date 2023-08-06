# Cargo Virtual Environment

A virtual environment tool similar to Python's virtual environments.


## Table of Contents
* [Installation](#installation)
* [Usage](#usage)
    * [Custom toolchain](#custom-toolchain)

## Installation

```
pip install cargo-venv
```

## Usage
Leveraging `Cargo`'s built-in command mechanism, you can simply call the following command to get a virtual environment called
`venv`. 
```
cargo venv
```

However, since this is a Python script, you can specify a different name by calling:
```
cargo-venv custom-name
```

### Custom toolchain
You can also specify a custom toolchain rather than always depend on the latest. If a `rust-toolchain` file is discovered
in your project, that version will be used to install the toolchain inside your virtual environment.

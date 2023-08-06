# Cargo Virtual Environment

A virtual environment tool similar to Python's virtual environments.


## Table of Contents
* [Installation](#installation)
* [Usage](#usage)
    * [Custom toolchain](#custom-toolchain)
    * [IDE Support](#ide-support)
        * [IntelliJ Idea](#intellij-idea)

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

### IDE Support
#### IntelliJ Idea
Under `Settings > Languages and Frameworks > Rust` set the following fields to these values:
#### Toolchain Location
```
<venv-path>/.rustup/toolchains/<toolchain-version>/bin
```
#### Standard library 
```
<venv-path>/.rustup/toolchains/<toolchain-version>/lib/rustlib/src/rust
```

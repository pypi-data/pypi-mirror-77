<!-- Header -->
# [aws-sync](https://github.com/UdhavPawar/aws-sync) &nbsp; [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Sync%20AWS%20secrets%20easily%20between%20multiple%20accounts&url=https://github.com/UdhavPawar/aws-sync&hashtags=aws,secrets,github,github-profile,github-email,python3,pypi)

<!-- Labels -->
<p align="center">
    <img src="https://img.shields.io/badge/package-pip-blue.svg?style=flat">
    <img src="https://img.shields.io/badge/version-0.2-blueviolet.svg?style=flat">
    <img src="https://img.shields.io/badge/code-python-orange.svg?style=flat">
    <img src="https://img.shields.io/badge/code-python3-yellow.svg?style=flat">
    <img src="https://img.shields.io/badge/build-passing-green.svg?style=flat">
    <img src="https://img.shields.io/badge/license-MIT-ff69b4.svg?style=flat">
</p>

<!-- Jumpers -->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#contributing">Contribute</a> •
  <a href="#package">Package</a>
</p>

## Key Features

- Python package which easily syncs specifc or all secrets between multiple AWS accounts.
- In destination account, missing secrets are automatically created and existing secrets are updated in-place.
- Supports filtering to replicate specific pattern matching secrets. Defaults to replicate all secrets.
- Supports using custom KMS Encryption key. Defaults to default AWS secrets manager encryption key.

## Installation

Install package use the package manager [pip](https://pypi.org/project/aws-sync/).

> python2

![python](./svgs/py2install.svg)
```bash
pip install aws-sync
```
OR
```bash
python -m pip install aws-sync
```
> python3

![python3](./svgs/py3install.svg)

```bash
pip3 install aws-sync
```
OR
```bash
python3 -m pip install aws-sync
```
> Facing an issue? Check the [Issues](https://github.com/UdhavPawar/aws-sync/issues) section or open a new issue.


## How To Use

![example](./svgs/run.svg)

> python2 run.py
```python

```
> python3 run.py
```python3

```
> Facing an issue? Check the [Issues](https://github.com/UdhavPawar/aws-sync/issues) section or open a new issue.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change/fix.

## Package


How the code works:
```
- Let's say accountA is source account and accountB is destination account.
- If no environment filter is provided by user, then defaults to replicate all secrets.
- If no Encryption KMS Key ARN is provided by user, then defaults to use the AWS secrets manager default encryption key.
- For secret in accountA, if it is a new secret, then creates a new secret in accountB.
- If secret exists in accountB, then update it's value.
```
> package PyPi project: [aws-sync](https://pypi.org/project/aws-sync/)

## License
[MIT](https://github.com/UdhavPawar/aws-sync/blob/master/LICENSE)

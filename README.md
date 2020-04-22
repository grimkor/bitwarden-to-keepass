# Bitwarden-to-KeePass 
WORK IN PROGESS

Python script to automate exporting Bitwarden login records to KeePass.

## Usage
1. Clone repository
2. `npm i --g @bitwarden/cli`
3. `sudo apt install keepassxc`
4. From the project directory: `python3 app.py`

## Environment variables

Following environment variables are available to use and the script will auto-input these when required. As you can imagine MFA for Bitwarden is not one of these things so keep your 2FA device at the ready for the first login! (after the first login a session key provided by the Bitwarden CLI is used)

|ENV VARIABLE | Description |
|:-------------|-------------|
|`BW_USERNAME` | Bitwarden account username/email address|
|`BW_PASSWORD` | Bitwarden account password|
|`BW_SERVER` | Bitwarden server location (default set to bitwarden.com)|
|`KEEPASS_FILE`| Location of Keepass database file |
|`KEEPASS_PASSWORD`| Password to unlock KeePass database file|

If any of the above environment variables are missing when the script is run it will ask for user to input those values when first required.

## PENDING
* Option to create database to export to if KeepPass file not found.
* Add checks and validation notices for missing packages
* Setup script

## Acknowledgements
* [Bitwarden Command-line Interface](https://github.com/bitwarden/cli)
* [KeePass keepassxc-cli](https://github.com/keepassxreboot/keepassxc/blob/develop/share/docs/man/keepassxc-cli.1)
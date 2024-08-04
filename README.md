# Brew Installs

A place to keep a list of app installed by brew
This is a support repos to manage brew brew installs. 

This repos is part of a larger project to automatically configure new environments. 

## Backup Files
To produce new brew backup lists run the following commands:

```bash
brew list --formula > brew-formula.txt
brew list --cask > brew-cask.txt
```
<!-- TODO: Create a script to update backup on a cron job with versions -->

## Brew Installs
To install all the apps listed in the backup files run the following script:


Will use the default backup files `brew-cask.txt` and `brew-formula.txt`
```Python

python3 brew_reinstall.py 
```


To use custom backup files use the following command::w
```Python

python3 brew_reinstall.py --cask-file custom-cask.txt --formula-file custom-formula.txt
```



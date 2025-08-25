# Lucos Contacts - Facebook Importer

A python script to import facebook data to [lucos_contacts](https://github.com/lucas42/lucos_contacts)



## Setup

* Run `pipenv install` to install dependencies
* Create a directory call `data` and fill it with json files downloaded from facebook's graphql endpoint
* Create a `.env` file and set any necessary environment variables

## Running
`pipenv run python import.py`

## Environment Variables

* _**LUCOS_CONTACTS**_ The base url for a running instance of [lucos_contacts](https://github.com/lucas42/lucos_contacts).  Defaults to the production url
* _**KEY_LUCOS_CONTACTS**_ A valid api key for _**LUCOS_CONTACTS**_ as set by [lucos_creds](https://github.com/lucas42/lucos_creds).
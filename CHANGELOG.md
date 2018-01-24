# Changelog

## v1
* Added a class `Block` which represents a block of data
* Also created a basic system to validate blocks

## v2
* Added a class `Blockchain` which represents a chain of blocks
* Blockchains can be used as a payment system, so I added a basic
* transaction system

## v3
* Fleshed out the transaction system
* Added a new class `Address` which represents an address
* Added a list named `addresses` which is a kind of simple database

## v4
* Moved the addresses list to an SQLite3 database
* Moved the `mine` method from the `Blockchain` class to the `Address` class
* Miners now get rewards for mining

## v5
* Moved the blockchain to the database
* Moved the transaction history to the database
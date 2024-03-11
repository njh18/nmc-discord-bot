> **This repository is outdated and no longer in use as of 2022.**

<img src="./images/nmc_logo.png" width="100"/>

# Axie Infinity Discord Bot (NMC)

The Axie Infinity Discord Bot is a tool designed specifically for managing users & managers within an Axie Infinity guild - Nox Moon Cardinal (NMC). 
This bot provides a sets of commands tailored to Axie Infinity players, enabling them to easily access information related to their Axies, Matchmaking Rating (MMR), Smooth Love Potion amount (SLP), marketplace links (and more!) directly within the Discord server.

This bot had been maintained by the owners of NMC guild - [@njh18](https://github.com/njh18) and [@nephydecode](https://github.com/nephydecode), previously deployed on [replit](https://replit.com/@njh18/Loops-practice#main.py).

Join our [Discord](https://discord.gg/cpPtxMRct3)!

## 🤖 Bot Commands

> Check out the ['bot-commands' channel](https://discord.com/channels/890225444190842881/914463230708027453) in our Discord that was previously used to send commands to the bot

* [List of Commands](#commands)
* [Commands Usage Example](#example)

### List of Commands <a name="commands"></a>

#### Player Axie & Statistics Commands 🎮
* `$myaxie`: Get information about your Axies.
* `$myaxie <@user>`: Get information about the Axies of the tagged user.
* `$mymmr`: Get your MMR (Matchmaking Rating).
* `$myslp`: Get information about your SLP earnings (today's, yesterday's, average, total account)
* `$myscholarronin`: Get your scholar account's Ronin wallet information.
* `$myronin`: Get your Ronin wallet information (if you have manager permissions).

#### Price Information Commands 💰
* `$priceslp`: Get the exchange rate of SLP (Smooth Love Potion) to USD (United States Dollar) and PHP (Philippine Peso).
* `$priceslp <amt>`: Get the exchange rate of a specified amount of SLP to USD and PHP.
*Note: The commands prefixed with $price (e.g., $priceaxs, $pricephp, $priceusd, $pricesgd) also work similarly to $priceslp, providing exchange rates for different currencies.*

#### Admin / Manager Commands 🗃️
* `$myslp <@user>`: Get SLP earnings information of tagged user 
* `$clanslp <Lunar/Sol/Kopi/Oasis>`: Get entire clan's slp & mmr 
* `$onboard <@user>`: Follow process to upload user to database
* `$dbupdate`: Database update (to run after onboarding)
* `$leaderboard <rank,axieCount>`: Get axies used by leaderboard

### Example <a name="example"></a>

| Command            | Screenshot                                    |
|--------------------|-----------------------------------------------|
| `$myaxie`          | <img src="images/commands/myaxie.png" width="200"/> |
| `$myaxie <@user>`  | <img src="images/commands/myaxie-user.png" width="200"/> |
| `$mymmr`          | <img src="images/commands/mymmr.png" width="200"/> |
| `$myslp`          | <img src="images/commands/myslp.png" width="200"/> |
| `$myslp <@user>`  | <img src="images/commands/myslp-user.png" width="200"/> |
| `$myronin`  | <img src="images/commands/myronin.png" width="200"/> |
| `$priceslp`  | <img src="images/commands/priceslp.png" width="200"/> |
| `$priceeth`  | <img src="images/commands/priceeth.png" width="200"/> |
| `$onboard <@user>`  | <img src="images/commands/onboard.png" width="200"/> |

## Usage
Simply type the desired command in the Discord server's chat and the bot will respond accordingly with the requested information.

## Acknowledgements
The Axie Infinity Discord Bot relies on the Discord API, pycoingecko API, and Axie Infinity API.
![](https://github.com/Phenomenon2919/SimpleMonetaryTracker/workflows/CI/badge.svg?branch=master&event=push)
![](https://img.shields.io/github/release/Phenomenon2919/SimpleMonetaryTracker.svg)

# Simple Monetary Tracker

A simple windows desktop application to keep track of your income expenditure tally.

- Update transactions with one command.
- Supports multi profile system.
- View records with filters based on tags

## Usage

        SimpleMonetaryTracker init (<Profile_name>)             # Initialise a Profile on a machine
        SimpleMonetaryTracker set (<Profile_name>)              # Set a Profile on a machine
        SimpleMonetaryTracker profiles                          # List the profiles on a machine
        SimpleMonetaryTracker tags                              # List the tags for the set profile
        SimpleMonetaryTracker view [-E|-I] [<tag>...]           # View the transaction records for a profile based on optional filters
        SimpleMonetaryTracker (<amount>) (-E|-I) (<tag>) [<description>]        # Add a transaction to a profile by mentioning the amount*, E/I*,Tag* and Description [* Required]

Note: _-I_ denotes Income and _-E_ denotes Expense.

**Use 'bash' shell in windows for best experience**

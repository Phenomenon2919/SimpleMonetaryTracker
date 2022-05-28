# <DOCTYPE = Python3>
from docopt import docopt
from tabulate import tabulate
from Tracker import Tracker

source_path = "."

if __name__ == "__main__":

    usage = """
        Simple Expense Tracker

        Usage:
        SimpleMonetaryTracker init (<Profile_name>)
        SimpleMonetaryTracker set (<Profile_name>)
        SimpleMonetaryTracker profiles
        SimpleMonetaryTracker view [-E|-I] [<tag>...]
        SimpleMonetaryTracker (<amount>) (-E|-I) (<tag>) [<description>]

        Options:
  
            -h --help      Show this screen.

        """
    args = docopt(usage)

    tracker = Tracker(source_path=source_path)

    tracker.setup()

    if args["init"]:
        tracker.init(args["<Profile_name>"])
    elif args["set"]:
        tracker.set(args["<Profile_name>"])
    elif args["profiles"]:
        tracker.profiles()
    elif args["view"]:
        filter = {"tag_list": args["<tag>"]}
        if args["-E"]:
            filter["type"] = "E"
        elif args["-I"]:
            filter["type"] = "I"
        else:
            filter["type"] = None
        # print(filter)
        tracker.view(filter)
    elif args["<amount>"]:
        transaction = tracker.verify_transaction(
            args["<amount>"], args["<tag>"], args["-E"], args["<description>"]
        )
        if transaction["status"] == "VALID":
            print("\033[96m[-]Transaction Initiated: \033[0m")
            print(
                tabulate(
                    [transaction],
                    tablefmt="pretty",
                )
            )
            tracker.log(transaction)

            ## Debug
            # print(tabulate(view()))
            ##
        else:
            print("\033[91m[-]Transaction Invalid.\033[0m")

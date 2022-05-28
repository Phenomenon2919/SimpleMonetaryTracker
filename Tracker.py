from os.path import exists
from os import mkdir
from os import listdir
import sqlite3 as db
from docopt import docopt
import yaml
from tabulate import tabulate


class Tracker:
    def __init__(self, source_path) -> None:
        self.source_path = source_path

    def init(self, profile):

        ## Create New Expense Profile data base
        if exists(self.source_path + "/.Profiles/{}/transactions.db".format(profile)):
            opt = input(
                "\033[93m[?] Mentioned Profile exists! Do you wish to reset it? (Y/N): "
            )
            if opt == "Y":

                ## Dropping old transaction table
                conn = db.connect(
                    self.source_path + "/.Profiles/{}/transactions.db".format(profile)
                )
                cursor = conn.cursor()
                query = """
                drop table transactions
                """
                cursor.execute(query)
                conn.commit()

                print(
                    "\033[93m[/] User Profile {} is being Reset!\033[0m".format(profile)
                )

            else:
                print(
                    "\033[91m[-] No changes were done to User Profile {}\033[0m".format(
                        profile
                    )
                )
                self.set(profile)
                return
        else:
            mkdir(self.source_path + "/.Profiles/{}".format(profile))
            print("\033[93m[/] User Profile {} initializing...\033[0m".format(profile))

        conn = db.connect(
            self.source_path + "/.Profiles/{}/transactions.db".format(profile)
        )
        cursor = conn.cursor()
        query = """
        create table if not exists transactions (
            amount number,
            type char,
            tag string,
            description string,
            date string
        )
        """
        cursor.execute(query)
        conn.commit()

        print("\033[92m[+] User Profile {} has been created!\033[0m".format(profile))

        ## Set Current profile
        self.set(profile)

    def set(self, profile):

        if not exists(self.source_path + "/.Profiles/{}".format(profile)):
            print(
                "\033[91m[-]User Profile not initiallized.\n[-]User Profile could not be changed!\033[0m"
            )
            return

        ## Setting Current Profile
        try:
            with open(self.source_path + "/.TrackerConfig.yaml", "r") as f:
                config = yaml.safe_load(f)
            with open(self.source_path + "/.TrackerConfig.yaml", "w") as f:
                config["current_profile"] = profile
                yaml.safe_dump(config, f)

            print("\033[92m[+] Current User Profile set to {}\033[0m".format(profile))
        except Exception as e:
            print(
                "\033[91m[-] User Profile could not be changed\033[0m. Exception:\n"
                + str(e)
            )

    def setup(self):
        try:
            if not exists(self.source_path + "/.Profiles/"):
                mkdir(self.source_path + "/.Profiles")
            if not exists(self.source_path + "/.TrackerConfig.yaml"):
                config = {"current_profile": None, "debug": False}
                with open(self.source_path + "/.TrackerConfig.yaml", "w") as f:
                    yaml.safe_dump(config, f)

        except Exception as e:
            print("\033[91m[-]Could not complete Setup. \033[0m", e)
            exit()

    def profiles(self):

        if not exists(self.source_path + "/.Profiles/"):
            self.setup()

        profile_list = listdir(self.source_path + "/.Profiles")
        if not profile_list:
            print("\033[93m[/] No Profiles Intialized Yet.\033[0m")
            return
        for profile in profile_list:
            if profile == self.get_profile():
                print("\033[92m* {}\033[0m".format(profile))
            else:
                print("{}".format(profile))

    def get_profile(self):
        try:
            with open(self.source_path + "/.TrackerConfig.yaml", "r") as f:
                config = yaml.safe_load(f)
                return config["current_profile"]
        except Exception as e:
            print(
                "\033[91m[-] User Profile could not be read!\033[0m. Exception:\n"
                + str(e)
            )

    def verify_transaction(self, amount, tag, expense=False, description=None):

        transaction = {}
        try:
            transaction["amount"] = float(amount)
            transaction["type"] = "E" if expense else "I"
            transaction["tag"] = tag
            transaction["description"] = description
            transaction["status"] = "VALID"
        except:
            transaction["status"] = "INVALID"
        return transaction

    def log(self, transaction):

        profile = self.get_profile()
        if not profile:
            print("\033[91m[-] User Profile not set. Please set profile.\033[0m")
            return

        print("\033[93m[/] Current Profile: {}\033[0m".format(profile))

        from datetime import datetime

        date = str(datetime.now())
        conn = db.connect(
            self.source_path + "/.Profiles/{}/transactions.db".format(profile)
        )
        cursor = conn.cursor()
        query = """
            insert into transactions values(
                {},
                '{}',
                '{}',
                '{}',
                '{}'
            ) 
            """.format(
            transaction["amount"],
            transaction["type"],
            transaction["tag"][0],
            transaction["description"],
            date,
        )
        cursor.execute(query)
        conn.commit()

        print(
            "\033[92m[+] Transaction has been loged for user {}.\033[0m".format(profile)
        )

    def view(self, filter):
        ## Get Current Profile:
        profile = self.get_profile()
        if not profile:
            print("\033[91m[-] User Profile not set. Please set profile.\033[0m")
            return

        print("\033[93m[/] Current Profile: {}\033[0m".format(profile))

        conn = db.connect(
            self.source_path + "/.Profiles/{}/transactions.db".format(profile)
        )
        cursor = conn.cursor()

        query = """
            select * from transactions
        """
        if filter["type"]:
            query += "where type = '{}'".format(filter["type"])

        if filter["tag_list"]:
            final_query = ""
            for tag in filter["tag_list"]:
                if not filter["tag_list"].index(tag) == 0:
                    final_query += " union "
                if filter["type"]:
                    final_query += query + " and "
                else:
                    final_query += query + " where "
                final_query += "tag = '{}'".format(tag)
            query = final_query

        ## Debug
        # print(query)
        ##

        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            print(
                "\033[93m[/] No transactions for Profile {} yet!\033[0m".format(profile)
            )
            return
        ## Printing table
        print(
            tabulate(
                result,
                headers=["Amount", "Type", "Tag", "Decription", "DateTime"],
                tablefmt="pretty",
            )
        )

        ## Printing balance
        tally = 0
        for record in result:
            if record[1] == "E":
                tally -= float(record[0])
            else:
                tally += float(record[0])

        print(
            "\033[92m[+] Current Total Balance = \033[0m\033[1m {} \033[0m".format(
                str(tally)
            )
        )

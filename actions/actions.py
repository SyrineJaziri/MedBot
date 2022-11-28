# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import random
import pandas as pd

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# computer_choice & determine_winner functions refactored from
# https://github.com/thedanelias/rock-paper-scissors-python/blob/master/rockpaperscissors.py, MIT liscence


class ActionPlayRPS(Action):

    def name(self) -> Text:
        return "action_play_rps"

    def computer_choice(self):
        generatednum = random.randint(1, 3)
        if generatednum == 1:
            computerchoice = "rock"
        elif generatednum == 2:
            computerchoice = "paper"
        elif generatednum == 3:
            computerchoice = "scissors"

        return(computerchoice)

    def create_connection(db_file):

        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #database = r"C:\sqlite\db\pythonsqlite.db"

        #conn = create_connection("../drugs-classification.csv")
        # with conn:
        #    print(conn)

        #df = pd.read_csv("../drugs-classification.csv")
        # print(df.head())

        # play rock paper scissors
        user_choice = tracker.get_slot("choice")
        dispatcher.utter_message(text=f"You chose {user_choice}")
        comp_choice = self.computer_choice()
        dispatcher.utter_message(text=f"The computer chose {comp_choice}")

        if user_choice == "rock" and comp_choice == "scissors":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "rock" and comp_choice == "paper":
            dispatcher.utter_message(text="The computer won this round.")
        elif user_choice == "paper" and comp_choice == "rock":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "paper" and comp_choice == "scissors":
            dispatcher.utter_message(text="The computer won this round.")
        elif user_choice == "scissors" and comp_choice == "paper":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "scissors" and comp_choice == "rock":
            dispatcher.utter_message(text="The computer won this round.")
        else:
            dispatcher.utter_message(text="It was a tie!")

        return []


class ActionChooseDRUG(Action):

    def name(self) -> Text:
        return "action_choose_drug"

    def get_same_drugs(self, drug_name, df):
        found_category = df.loc[df["Drug's name"] == drug_name]["categories"].tolist()[
            0]
        same_drugs = df.loc[(df["categories"] == found_category) & (
            df["Drug's name"] != drug_name)]["Drug's name"].tolist()

        return same_drugs

    def get_illness(self, drug_name, df):
        found_illness = df.loc[df["Drug's name"] == drug_name]["Illness"]

        return found_illness

    def get_side_effects(self, drug_name, df):
        found_side_effect = df.loc[df["Drug's name"]
                                   == drug_name]["Side effects"]

        return found_side_effect

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # play rock paper scissors
        drug_choice = tracker.get_slot("drug_choice")

        dispatcher.utter_message(
            text=f"Your drugs choice is : {drug_choice}")
        df = pd.read_csv("../drugs-classification.csv")
        same_drugs = self.get_same_drugs(drug_choice, df)
        illness = self.get_illness(drug_choice, df)
        side_effect = self.get_side_effects(drug_choice, df)

        dispatcher.utter_message(
            text=f"Same drugs are : {', '.join(same_drugs)}")

        dispatcher.utter_message(
            text=f"this drug treats : {illness}")
        dispatcher.utter_message(
            text=f"the sides effects of this drug are : {side_effect}")

        return []


class ActionChooseWtToDo(Action):

    def name(self) -> Text:
        return "action_wt_to_do"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Action 'action_wt_to_do' played")
        wt_to_do_choice = tracker.get_slot("wt_to_do_choice")
        dispatcher.utter_message(
            text=f"You chose to know this: {wt_to_do_choice}")

        return []

import openai 
import json
from typing import List


class DialogGenerate:
    """
    A class to represent a Dialog Generation.
    Methods
    -------
    _dialog_generate(message):
        Call ChatGPT API
    generate_dialog():
        Generate annotated dialog
    """
    def __init__(self, 
                 openai_key:str, 
                 domain:str, 
                 domain_type:str, 
                 product:str, 
                 example:List, 
                 usract:List,
                 sysact:List, 
                 slots:List,
                 intents:List,                
                 messages=[{"role": "system", "content": "You are a intelligent assistant."}],
                 list_product=[]):

        """
        Constructs all the necessary attributes for the DialogGenerate object.

        Parameters
        ----------
            openai_key : str
                a private key of ChatGPT
            domain : str
                domain of dialog
            domain_type : str
                domain type of dialog (service or trading)
            product : str
                the product of dialog
            usract : list
                the list of user action
            sysact : list
                the list of system action
            slots : list
                the list of dictionaries with slot_name key and slot_value value
            intents : list
                the list of dictionaries with intents information (intent_name, intent_description, intent_required_slots)            
        """       
        
        
        openai.api_key = openai_key

        self.messages = messages     
        self.domain = domain 
        self.domain_type = domain_type 
        self.product = product 
        self.example = example
        self.usract = usract
        self.sysact = sysact
        self.slots = slots
        self.intents = intents
        self.list_product = list_product
           
        self.action_prompt = f"""
                                Now, you need to annotate each message of that dialogue by 
                                - Adding key "action" of USER'S MESSAGE which is taked in this list: {usract}
                                - Adding key "action" of AGENT'S MESSAGE which is taked in this list: {sysact}
                            """
        self.slot_prompt = f"""
                                Now, you need to add more information each message of that dialogue by:
                                - Adding key "slot_name" and "slot_value" which are taked in this list: 
                                "slots": {self.slots}
                            """
        self.intent_prompt = f"""
                                Now, you need to add more information each message of that dialogue by:
                                - Adding key "intents"  which is taked in this list: 
                                "intents": {self.slots}
                            """


    def _dialog_generate(self, message:str) -> str:    
        """
        Call ChatGPT 3.5 API
            Parameters:
                message (str): a message 
            Returns:
                reply (str): the reply of ChatGPT 3.5 API

        """
        self.messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=self.messages)
        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})  

        return reply  


    def _generate_dialog(self, product) -> str:
        """
        Generate dialog with ChatGPT 3.5 API
            Returns:
                final_dialog (str): an annotated dialog 

        """
        dialog_prompt = f"""
                            Task: Generate a new dialogue between USER and AGENT which AGENT is a seller bot in a {self.domain}. 
                            Requirement:  AGENT need to orient USER so that the trading success (USER agrees to participate in {self.domain} {self.domain_type}). {self.domain} {self.domain_type} in this case is {product}.
                            Format: .json code block
                            Example: {self.example}
                        """
        print("\n Generating dialog.....")
        self._dialog_generate(dialog_prompt)
        
        print("\n Annotating action.....")
        self._dialog_generate(self.action_prompt)
        
        print("\n Annotating slot.....")
        self._dialog_generate(self.slot_prompt)
        
        print("\n Annotating intent.....")
        final_dialog = self._dialog_generate(self.intent_prompt)        

        return json.loads(final_dialog)


    def generate_one_dialog(self) -> str:
        """
        Generate one dialog with ChatGPT 3.5 API
            Returns:
                an annotated dialog 

        """
        return self._generate_dialog(self.product)


    def generate_multi_dialog(self) -> List: 
        """
        Generate multiple dialog with ChatGPT 3.5 API
            Returns:
                list_dialog (list): a list of annotated dialog 

        """
        list_dialog = []
        for idx, product in enumerate(self.list_product):
            print(f"\n Generating dialog {idx}.....")
            list_dialog.append(self.generate_dialog(product))
            self.messages=[{"role": "system", "content": "You are a intelligent assistant."}]

        return list_dialog
    
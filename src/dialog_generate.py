import openai 
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

        self.dialog_prompt = f"""
                                Task: Generate a new dialogue between USER and AGENT which AGENT is a seller bot in a {self.domain}. 
                                Requirement:  AGENT need to orient USER so that the trading success (USER agrees to participate in {self.domain} {self.domain_type}). {self.domain} {self.domain_type} in this case is {self.product}.
                                Format: .json code block
                                Example: {self.example}
                            """   
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
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})  

        return reply  


    def generate_dialog(self) -> str:
        """
        Generate dialog with ChatGPT 3.5 API
            Returns:
                final_dialog (str): an annotated dialog 

        """
        self.dialog_generate(self.dialog_prompt)
        self.dialog_generate(self.action_prompt)
        self.dialog_generate(self.slot_prompt)
        final_dialog = self.dialog_generate(self.intent_prompt)

        return final_dialog 
import argparse
import json
from src.dialog_generate import DialogGenerate
    

def make_parser():
    parser = argparse.ArgumentParser("Dialog Generation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--key", type=str, required=True, help="the private key of ChatGPT API")
    parser.add_argument("--domain", type=str, default="Beauty Spa", help="the domain of dialog")
    parser.add_argument("--domain_type", type=str, default="service", help="the domain type of dialog. (service, trading, ...)")
    parser.add_argument("--product", type=str, default="haircut", help="the product of dialog")
    parser.add_argument("--example", type=list, help="the example dialog",
                        default=["USER: Hello and good morning. Could you kindly assist me in purchasing a laptop?", "AGENT: Hello and good morning. I am here to help you. Do you have any specification requirements?", 
                                                        "USER: I'm looking for a cheap i7 cpu.", "AGENT: Do you have any brand preferences?", 
                                                        "USER: I used a HP laptop earlier. It was quite nice.", "AGENT: How much are you willing to spend?", 
                                                        "USER: I am just a normal user. I would not spend more than 2400.", "AGENT: I have a HP laptop that matches your requirement. It is HP 15-da0035nx, which costs 2299.", 
                                                        "USER: Is this a good laptop for daily use?", "AGENT: Yes, indeed. It has a 3/5 score, which is excellent.", 
                                                        "USER: Please describe the features to me.", "AGENT: It is equipped with an Intel Core i7-8550U cpu, Intel UHD Graphics 620 graphics, and a 1TB hard drive.", 
                                                        "USER: I don't think 620 graphics would perform well.", "AGENT: I have sold many laptops with Intel UHD Graphics 620 graphics. I have not received any complain regarding this GPU.", 
                                                        "USER: I still doubt it will work for me or not.", "AGENT: You can take this laptop with you. I assure you will not be dissapointed.", 
                                                        "USER: Okay, I am trusting you. I would like to buy it.", "AGENT: Sure. Your booking has been placed. Is there anything else I can assist you with?", 
                                                        "USER: I want to buy a smartphone too?", "AGENT: Yes, I have wide variety of smartphone with us. Could you please tell me your requirements?", 
                                                        "USER: I want something like this. https://m.media-amazon.com/images/I/81pVQueeahL._AC_SY550_.jpg", "AGENT: It seems to be a BlackBerry phone. I have a model named Aurora which is a Blackberry smartphone.", 
                                                        "USER: Please describe the features to me.", "AGENT: It comes with a 3000mAh battery, 4 GB RAM, a 13-megapixel main camera, and an 8-megapixel secondary camera.", 
                                                        "USER: Is it in black color? Because I like black.", "AGENT: Yes, it comes in black color.", 
                                                        "USER: What about the cost ?", "AGENT: It will cost you 250 EUR.", "USER: It is quite expensive.", "AGENT: Blackberry phones are trending these days. It also matches your colour preference.", 
                                                        "USER: No No. I cannot afford it today.", "AGENT: This phone is at its best price. I would suggest you not to miss the deal.", 
                                                        "USER: No. I cannot afford it. I will just take the laptop.", "AGENT: Can I show you some cheap Blackberry phones?", 
                                                        "USER: No, I will buy it next time.", "AGENT: Alright. Your laptop has been booked. Is there anything else I could asist you with?", 
                                                        "USER: No, Thankyou for assistance.", "AGENT: You are welcome."])
    parser.add_argument("--user_action", type=list, 
                        help="the list of user actions",
                        default=["INFORM", "REQUEST", "SELECT", "CONFIRM", "REQUEST-ALTS", "BYE", "GREET", "BOOK", "NOBOOK", "OFFERBOOK", "ASK", "INFORM-INTENT", "NEGATE-INTENT", "AFFIRM-INTENT", "AFFIRM", "NEGATE", "THANK"])
    parser.add_argument("--system_action", type=list, 
                        help="the list of system actions",
                        default=["INFORM", "REQUEST", "SELECT", "CONFIRM", "OFFER", "NoOFFER", "RECOMMEND", "PROMOTION_INTRODUCTION", "NOTIFY_SUCCESS", "NOTIFY_FALIURE", "INFORM_COUNT", "OFFER_INTENT", "REQMORE", "BYE", "GREET", "OFFERBOOK", "OFFERBOOKED", "ASK", "DELIVERY_SUPPORT", "SKILL_INTRODUCTION", "SCHEDULE_RECOMMEND", "THANK"])
    parser.add_argument("--slot", type=list, 
                        help="the list of dictionaries with slot_name key and slot_value value",
                        default=[
                                                        {
                                                            "name": "service_type",
                                                            "description": "The type of beauty service",
                                                            "is_categorical": True,
                                                            "possible_values": ["haircut", "hairstyling", "hair_coloring", "manicure", "pedicure", "facial", "massage", "waxing", "eyebrow_shaping", "eyelash_extensions", "makeup", "body_treatment", "tanning", "nail_extensions", "hair_extensions", "spa_package", "eyebrow_tinting", "eyelash_tinting", "other"]
                                                        },
                                                        {
                                                            "name": "service_duration",
                                                            "description": "The duration of the beauty service",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "service_price",
                                                            "description": "The price of the beauty service",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "beautician_name",
                                                            "description": "The name of the beautician",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "customer_name",
                                                            "description": "The name of the customer",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "customer_email",
                                                            "description": "The email of the customer",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "customer_phone",
                                                            "description": "The phone number of the customer",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "appointment_date",
                                                            "description": "The date of the appointment",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "appointment_time",
                                                            "description": "The time of the appointment",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "payment_method",
                                                            "description": "The payment method chosen by the customer",
                                                            "is_categorical": True,
                                                            "possible_values": ["credit_card", "debit_card", "cash", "mobile_payment", "gift_card", "other"]
                                                        },
                                                        {
                                                            "name": "special_requests",
                                                            "description": "Any special requests from the customer",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "service_rating",
                                                            "description": "The rating given by the customer for the service",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "customer_feedback",
                                                            "description": "The feedback provided by the customer",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "appointment_confirmation",
                                                            "description": "Confirmation of the appointment",
                                                            "is_categorical": True,
                                                            "possible_values": ["yes", "no"]
                                                        },
                                                        {
                                                            "name": "location",
                                                            "description": "The location of the beauty spa",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "booking_date",
                                                            "description": "The date of the booking",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "booking_time",
                                                            "description": "The time of the booking",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "booking_duration",
                                                            "description": "The duration of the booking",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "booking_price",
                                                            "description": "The price of the booking",
                                                            "is_categorical": False
                                                        },
                                                        {
                                                            "name": "beautician_rating",
                                                            "description": "The rating given to the beautician",
                                                            "is_categorical": False
                                                        }
                                                    ])
    parser.add_argument("--intent", type=list, 
                        help="the list of dictionaries with intents information (intent_name, intent_description, intent_required_slots)",
                        default=[
                                                            {
                                                                "name": "book_appointment",
                                                                "description": "Book an appointment for a beauty service",
                                                                "slots": ["service_type", "customer_name", "customer_email", "customer_phone", "appointment_date", "appointment_time", "payment_method", "special_requests", "appointment_confirmation"]
                                                            },
                                                            {
                                                                "name": "cancel_appointment",
                                                                "description": "Cancel an existing appointment",
                                                                "slots": ["customer_name", "customer_email", "customer_phone", "appointment_date", "appointment_time"]
                                                            },
                                                            {
                                                                "name": "reschedule_appointment",
                                                                "description": "Reschedule an existing appointment",
                                                                "slots": ["customer_name", "customer_email", "customer_phone", "appointment_date", "appointment_time", "new_appointment_date", "new_appointment_time"]
                                                            },
                                                            {
                                                                "name": "check_availability",
                                                                "description": "Check the availability of a beauty service",
                                                                "slots": ["service_type", "appointment_date", "appointment_time"]
                                                            },
                                                            {
                                                                "name": "view_services",
                                                                "description": "View the list of available beauty services",
                                                                "slots": []
                                                            },
                                                            {
                                                                "name": "view_beauticians",
                                                                "description": "View the list of available beauticians",
                                                                "slots": []
                                                            },
                                                            {
                                                                "name": "view_opening_hours",
                                                                "description": "View the opening hours of the beauty spa",
                                                                "slots": []
                                                            },
                                                            {
                                                                "name": "view_pricing",
                                                                "description": "View the pricing of beauty services",
                                                                "slots": []
                                                            },
                                                            {
                                                                "name": "view_special_offers",
                                                                "description": "View any special offers or discounts",
                                                                "slots": []
                                                            },
                                                            {
                                                                "name": "provide_feedback",
                                                                "description": "Provide feedback for a beauty service",
                                                                "slots": ["customer_name", "customer_email", "customer_phone", "appointment_date", "appointment_time", "service_rating", "customer_feedback"]
                                                            },
                                                            {
                                                                "name": "check_appointment_status",
                                                                "description": "Check the status of an appointment",
                                                                "slots": ["customer_name", "customer_email", "customer_phone", "appointment_date", "appointment_time"]
                                                            },
                                                            {
                                                                "name": "check_payment_status",
                                                                "description": "Check the payment status of a beauty service",
                                                                "slots": ["customer_name", "customer_email", "customer_phone", "appointment_date", "appointment_time"]
                                                            },
                                                            {
                                                                "name": "check_beautician_availability",
                                                                "description": "Check the availability of a specific beautician",
                                                                "slots": ["beautician_name", "service_type", "appointment_date", "appointment_time"]
                                                            },
                                                            {
                                                                "name": "add_special_request",
                                                                "description": "Add a special request to an existing appointment",
                                                                "slots": ["customer_name", "customer_email", "customer_phone", "appointment_date", "appointment_time", "special_requests"]
                                                            },
                                                            {
                                                                "name": "check_service_duration",
                                                                "description": "Check the duration of a specific beauty service",
                                                                "slots": ["service_type"]
                                                            },
                                                            {
                                                                "name": "check_service_price",
                                                                "description": "Check the price of a specific beauty service",
                                                                "slots": ["service_type"]
                                                            },
                                                            {
                                                                "name": "check_service_rating",
                                                                "description": "Check the average rating of a specific beauty service",
                                                                "slots": ["service_type"]
                                                            },
                                                            {
                                                                "name": "check_beautician_rating",
                                                                "description": "Check the average rating of a specific beautician",
                                                                "slots": ["beautician_name"]
                                                            },
                                                            {
                                                                "name": "view_location",
                                                                "description": "View the location of the beauty spa",
                                                                "slots": []
                                                            },
                                                            {
                                                                "name": "make_booking",
                                                                "description": "Make a booking for multiple beauty services",
                                                                "slots": ["customer_name", "customer_email", "customer_phone", "booking_date", "booking_time", "booking_duration", "booking_price", "payment_method", "special_requests"]
                                                            }
                                                        ])

    parser.add_argument("--num_dialog", type=int, help="the number of dialogs",            
                        default=1)
    parser.add_argument("--list_product", type=list, default=[])
    
    parser.add_argument("--save_path", type=str, help="the save path (.json)", 
                        default="dialog.json")

    return parser


if __name__=="__main__":
    args = make_parser().parse_args()    
    
    if args.num_dialog == 1:
        dialog_generation = DialogGenerate(
                                args.key,
                                args.domain,
                                args.domain_type,
                                args.product, 
                                args.example,
                                args.user_action,
                                args.system_action,
                                args.slot,
                                args.intent
                            )
        
        generated_dialog = dialog_generation.generate_dialog()    

    elif args.num_dialog == len(args.list_product): 
        generated_dialog = [] 
        for product in args.list_product:
            dialog_generation = DialogGenerate(
                                    args.key,
                                    args.domain,
                                    args.domain_type,
                                    product, 
                                    args.example,
                                    args.user_action,
                                    args.system_action,
                                    args.slot,
                                    args.intent
                                )
            generated_dialog.append(dialog_generation.generate_dialog())

    with open(args.save_path, "w",  encoding ='utf8') as f:
            json.dump(generated_dialog, f, ensure_ascii = False)

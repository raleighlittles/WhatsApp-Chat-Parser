import argparse
import re
import os

WHATSAPP_CHAT_FILE_NAME = "_chat.txt"


def get_message_datetime(txt_file_line : str) -> tuple:

    message_date_regex = re.compile("\[(.*)\]")

    regex_match_obj = message_date_regex.match(txt_file_line)

    # Will look like: "[11/5/19, 11:38:00 AM]"
    # The regex match captures the enclosing brackets, but we obviously don't want those in the actual time,
    # hence the subtraction
    raw_datetime = txt_file_line[regex_match_obj.span()[0] + 1 : regex_match_obj.span()[1] - 1]

    



def convert_whatsapp_chat_to_csv(input_dir : str):

    
    message_phone_num_regex = re.compile("\](.*)\:")

    if os.path.exists(input_dir):
        chat_history_txt_file = os.path.join(input_dir, WHATSAPP_CHAT_FILE_NAME)

        with open(chat_history_txt_file) as chat_history_file_hndl:
            
            for line_num, line_contents in enumerate(chat_history_file_hndl.readlines()):

                message = dict()

                print(f"[DEBUG] Parsing line #{line_num}")



                

    else:
        raise Exception(f"Input directory specified by user: '{input_dir}' doesn't exist")
    
    

    


if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-i", "--input-dir", type=str, help="The directory where the WhatsApp chat backup is located. Must contain a txt file.")

    argparse_args = argparse_parser.parse_args()

    convert_whatsapp_chat_to_csv(argparse_args.input_dir)
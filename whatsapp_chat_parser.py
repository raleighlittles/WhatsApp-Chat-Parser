import argparse
import re
import os
import datetime
import pdb

WHATSAPP_CHAT_FILE_NAME = "_chat.txt"


def sanitize_text_line(original_txt_line) -> str:
    """
    Not sure why but the WhatsApp messages have weirdly unnecessary Unicode characters in them. For example, the default
    start message in WhatsApp looks like this in the dump:
    '[11/5/19, 11:38:00 AM] \u202a\xa0178\xa03464334\u202c: \u200eMessages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.\n'
    Whereas, when formatted correctly, it should read:
    [11/5/19, 11:38:00 AM] 17X346XX3X: Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.\n'
    (the 'XX' is to redact the phone number for privacy)
    The step below accomplishes that filtering
    """

    return original_txt_line.encode("ascii", "ignore").decode().strip()



def get_message_datetime(txt_file_line : str) -> tuple:
    """
    Extract the 'date' the message was sent (in raw form),
    returns it, AND, the Linux epoch timestamp for that date
    """

    message_date_regex = re.compile("\[(.*)\]")

    sanitized_txt_file_line = sanitize_text_line(txt_file_line)

    regex_match_obj = message_date_regex.match(sanitized_txt_file_line)

    # Will look like: "[11/5/19, 11:38:00 AM]"
    # The regex match captures the enclosing brackets, but we obviously don't want those in the actual time,
    # hence the subtraction

    raw_datetime = sanitized_txt_file_line[regex_match_obj.span()[0] + 1 : regex_match_obj.span()[1] - 1]
    # https://strftime.org/
    raw_datetime_fmt = "%m/%d/%y, %H:%M:%S %p"

    return tuple([datetime.datetime.strptime(raw_datetime, raw_datetime_fmt).strftime("%s"), raw_datetime])

    
def get_message_sender_or_receiver(txt_file_line : str) -> str:
    """
    
    """
    message_phone_num_regex = re.compile("\](.*)\:")


    msg_transmitter = re.search(message_phone_num_regex, sanitize_text_line(txt_file_line)).group(1).strip()

    return msg_transmitter



def convert_whatsapp_chat_to_csv(input_dir : str):

    if os.path.exists(input_dir):
        chat_history_txt_file = os.path.join(input_dir, WHATSAPP_CHAT_FILE_NAME)

        with open(chat_history_txt_file, 'r', encoding="utf-8") as chat_history_file_hndl:

            messages = dict()
            
            for line_num, line_contents in enumerate(chat_history_file_hndl.readlines()):

                # Line starts with a bracket, it defines the beginning of a new message
                if line_contents.startswith("["):

                    print(f"[DEBUG] Parsing line #{line_num}")

                    msg_datetime = get_message_datetime(line_contents)

                    msg_transmitter = get_message_sender_or_receiver(line_contents)

                    print(f"[DEBUG] Message datetime: {msg_datetime} | Msg transmitter: {msg_transmitter}")

                    messages["time"] = msg_datetime
                    messages["sender"] = msg_transmitter

                else:
                    # Line doesn't start with a a bracket, it's just a continuation of the previous message







                

    else:
        raise Exception(f"Input directory specified by user: '{input_dir}' doesn't exist")
    
    

    


if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-i", "--input-dir", type=str, help="The directory where the WhatsApp chat backup is located. Must contain a txt file.", required=True)

    argparse_args = argparse_parser.parse_args()

    convert_whatsapp_chat_to_csv(argparse_args.input_dir)
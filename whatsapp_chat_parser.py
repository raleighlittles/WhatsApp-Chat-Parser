import argparse
import re
import os
import datetime
import csv

WHATSAPP_CHAT_FILE_NAME = "_chat.txt"


def sanitize_text_line(original_txt_line) -> str:
    """
    Some WhatsApp messages include the Unicode left-to-right character markers (U+202A and U+202C) in them. For example, the
    start message in WhatsApp looks like this in the dump:
    '[11/5/19, 11:38:00 AM] \u202a\xa0178\xa03464334\u202c: \u200eMessages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.\n'
    Whereas, when formatted correctly, it should read:
    [11/5/19, 11:38:00 AM] 17X346XX3X: Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.\n'
    (the 'XX' is to redact the phone number for privacy)
    The step below accomplishes that filtering. 
    """

    #return original_txt_line.encode("ascii", "ignore").decode().strip()
    forbidden_unicode_chars = ["\u202a", "\u202c", "\u200e", "\xa0"]

    regex_expr = "|".join(forbidden_unicode_chars)

    return re.sub(rf"{regex_expr}", "", original_txt_line.strip())




def get_message_datetime(txt_file_line : str) -> tuple:
    """
    Extract the 'date' the message was sent (in raw form),
    returns it, AND, the Linux epoch timestamp for that date
    """

    # Will look like: "[11/5/19, 11:38:00 AM", need to filter out the brackets

    raw_datetime = txt_file_line.split("]")[0][1:]
    # https://strftime.org/
    raw_datetime_fmt = "%m/%d/%y, %H:%M:%S %p"

    return tuple([datetime.datetime.strptime(raw_datetime, raw_datetime_fmt).strftime("%s"), raw_datetime])

    
def get_message_sender_or_receiver(txt_file_line : str) -> str:
    """
    
    """
    message_phone_num_regex = re.compile("\](.*)\:")


    #msg_transmitter = str(re.search(message_phone_num_regex, sanitize_text_line(txt_file_line)).group(1).strip())
    msg_transmitter = str(re.search(message_phone_num_regex, txt_file_line).group(1).strip())

    return msg_transmitter



def get_message_contents(txt_file_line : str) -> str:

    # message_contents_regex = re.compile("(\]).+(:.+)")
    # 1 to skip the colon included

    #msg_contents = re.search(message_contents_regex, txt_file_line)

    msg_contents = txt_file_line.split(":")
    
    #return msg_contents.group(2)[1:]
    # Look at how the time is formatted, that contains 2 colons, and the third colon comes at the end of the sender:
    # Y/M/D H:M:S <Sender>: <Message>
    # we want everything after "Sender:"
    msg_contents = "".join(msg_contents[3:])
    return msg_contents



def convert_whatsapp_chat_to_csv(input_dir : str, output_csv_file : str):

    chat_history_txt_file = os.path.join(input_dir, WHATSAPP_CHAT_FILE_NAME)

    if os.path.exists(chat_history_txt_file):

        with open(chat_history_txt_file, 'r', encoding="utf-8") as chat_history_file_hndl:

            messages = list()
            
            for line_num, line_contents in enumerate(chat_history_file_hndl.readlines()):

                line_contents = sanitize_text_line(line_contents)

                # Line starts with a bracket, it defines the beginning of a new message
                if line_contents.startswith("["):

                    message = dict()

                    #print(f"[DEBUG] Parsing line #{line_num}")

                    msg_datetime = get_message_datetime(line_contents)
                    msg_transmitter = get_message_sender_or_receiver(line_contents)
                    msg_contents = get_message_contents(line_contents)

                    #print(f"[DEBUG] Message datetime: '{msg_datetime}' | Msg transmitter: '{msg_transmitter}' | Msg: '{msg_contents}'")

                    message["timestamp"] = msg_datetime[0]
                    message["datetime"] = msg_datetime[1]
                    message["sender"] = msg_transmitter
                    message["contents"] = msg_contents
                    message["id"] = line_num

                    messages.append(message)
                    

                else:
                    # Line doesn't start with a a bracket, it's just a continuation of the previous message
                    messages[-1]["contents"] += line_contents

            print(f"[DEBUG] Finished extracting {len(messages)} messages")
            export_messages_to_csv(messages, output_csv_file)

                

    else:
        raise FileNotFoundError(f"Missing {WHATSAPP_CHAT_FILE_NAME} from input directory")
        
    
def export_messages_to_csv(messages, output_csv_file):

    with open(output_csv_file, 'w') as csv_file_hndl:
        csv_writer = csv.writer(csv_file_hndl)
        # header
        csv_writer.writerow(["Msg ID", "Timestamp", "Datetime", "Sender", "Contents"])

        for msg in messages:
            csv_writer.writerow([msg["id"], msg["timestamp"], msg["datetime"], msg["sender"], msg["contents"]])

    




    


if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-i", "--input-dir", type=str, help="The directory where the WhatsApp chat backup is located. Must contain a txt file.", required=True)

    argparse_parser.add_argument("-o", "--output-csv-file", type=str, help="The output CSV file to save the parsed messages")

    argparse_args = argparse_parser.parse_args()

    input_dir = argparse_args.input_dir

    if not os.path.exists(input_dir):
        raise Exception(f"Input directory specified by user: '{input_dir}' doesn't exist")
    
    output_csv_file = argparse_args.output_csv_file

    if os.path.exists(output_csv_file):
        raise FileExistsError(f"Output file '{output_csv_file}' already exists, cannot overwrite")

    convert_whatsapp_chat_to_csv(input_dir, output_csv_file)

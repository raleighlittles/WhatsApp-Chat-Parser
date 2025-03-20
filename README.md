# About

A simple [WhatsApp](https://en.wikipedia.org/wiki/WhatsApp) chat parser, written in Python, for converting your WhatsApp chat history into a parsable CSV file.

When you download your WhatsApp chat history there will be a text file called `_chat.txt` that will have all of your chat history for that conversation.

You can run this script to convert that text file into a CSV file. This script has no dependencies outside of the standard library.

# Usage

```
usage: whatsapp_chat_parser.py [-h] -i INPUT_DIR [-o OUTPUT_CSV_FILE]

options:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input-dir INPUT_DIR
                        The directory where the WhatsApp chat backup is located. Must contain a txt file.
  -o OUTPUT_CSV_FILE, --output-csv-file OUTPUT_CSV_FILE
                        The output CSV file to save the parsed messages

```
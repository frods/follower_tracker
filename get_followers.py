import optparse
import sys
import os
import logging


import logging_config

from store import google_sheet, file as file_store
from process import urls

logging_config.configure_logging(logging.INFO)

LOGGER = logging.getLogger(__name__)

FOLLOWERS_FILE = "followers.txt"

parser = optparse.OptionParser("")

parser.add_option(
    "-u", "--url",
    help="URL to read the number of followers from",
    action="append", default=[])
parser.add_option(
    "-p", "--platforms",
    help="Include account name in platform",
    action="store_true")
parser.add_option(
    "-s", "--store_page",
    help="Store the page found from the url",
    action="store_true")
parser.add_option(
    "--linkedin_cookie",
    help="Cookie for linkedin access")

parser.add_option(
    "-f", "--file",
    help="File to store follower numbers in",
    default=FOLLOWERS_FILE)
parser.add_option(
    "-e", "--email",
    help="Email follower numbers to the given e-mail")
parser.add_option(
    "--email_account",
    help="Email to send with")
parser.add_option(
    "--email_password",
    help="Password for email_account")

parser.add_option(
    "-g", "--google_sheet",
    help="Name of google sheet to write data to")
parser.add_option(
    "-a", "--auth_file",
    help="Json file with google authentication data")
parser.add_option(
    "-w", "--worksheet_name",
    help="Name of worksheet in google_sheet to write data to")

args = sys.argv
if len(sys.argv) >= 2:
    input_file = sys.argv[1]
    if os.path.exists(input_file):
        with open(input_file, "r") as reader:
            config = []
            for line in reader.readlines():
                parts = line.split()
                config.append(parts[0])
                config.append(' '.join(parts[1:]))
            args = config + args[2:]

options, _ = parser.parse_args(args)

LOGGER.info("================================================================")
LOGGER.info("Getting followers with options:\n%s", options)

if not options.url:
    parser.print_help()
    parser.error("A URL needs to be specified")

stores = []

if options.google_sheet:
    LOGGER.info(
        "Storing to google sheet \"%s\", worksheet \"%s\", with auth %s",
        options.google_sheet, options.worksheet_name, options.auth_file)
    stores.append(google_sheet.StoreGoogleSheet(
        options.auth_file, options.google_sheet, options.worksheet_name))

if options.file:
    LOGGER.info("Storing to file %s", options.file)
    stores.append(file_store.StoreFile(
        options.file, options.email,
        options.email_account, options.email_password))

processor = urls.ProcessUrls(
    options.url, stores, options.store_page, options.platforms,
    options.linkedin_cookie)
processor.process()

for store in stores:
    store.finalize()

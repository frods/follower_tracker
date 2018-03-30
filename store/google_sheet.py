import logging

LOGGER = logging.getLogger(__name__)

try:
    import gspread
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
except ImportError:
    LOGGER.exception("Error loading gspread")
    gspread = None


LOGGER = logging.getLogger(__name__)


def strip_back(values):
    '''
    Remove empty values from end
    '''
    last_element = 0
    for index in range(len(values)-1, -1, -1):
        if values[index] != '':
            LOGGER.debug("Last non-empty element \"%s\"", values[index])
            last_element = index
            break
    LOGGER.info("Values empty from %i to %i", last_element, len(values))
    return values[:last_element + 1]


class StoreGoogleSheet:
    def __init__(self, auth_file, google_sheet, worksheet_name):
        self.auth_file = auth_file
        self.google_sheet = google_sheet
        self.worksheet_name = worksheet_name

    def store_followers(self, platform, count, date, url):
        if not gspread:
            LOGGER.info("gspread not available")
            return

        if not self.auth_file:
            LOGGER.info("no auth_file specified")
            return

        if not self.google_sheet:
            LOGGER.info("no google_sheet specified")
            return

        if not self.worksheet_name:
            LOGGER.info("no worksheet_name specified")
            return

        LOGGER.info("adding %s, %s, %s", platform, date, count)
        scope = ['https://spreadsheets.google.com/feeds']

        try:
            credentials = \
                service_account.Credentials.from_service_account_file(
                    self.auth_file)

            scoped_credentials = credentials.with_scopes(scope)
        except Exception:
            LOGGER.exception("Unable to load credentials")
            return

        LOGGER.info("Writing to spreadsheet: %s", self.google_sheet)
        gc = gspread.Client(auth=scoped_credentials)
        gc.session = AuthorizedSession(scoped_credentials)

        try:
            sheet = gc.open(self.google_sheet)
        except gspread.exceptions.SpreadsheetNotFound as e:
            LOGGER.exception(
                "Problem opening spreadsheet: %s",
                self.google_sheet)
            return

        wks = sheet.worksheet(self.worksheet_name)

        platforms = strip_back(wks.col_values(1))
        if platform in platforms:
            platform_row = platforms.index(platform) + 1
        else:
            platform_row = max(2, len(platforms) + 1)
            if platform_row >= wks.row_count:
                wks.add_rows(platform_row - wks.row_count)
            wks.update_cell(platform_row, 1, platform)

        dates = strip_back(wks.row_values(1))
        if date in dates:
            date_col = dates.index(date) + 1
        else:
            date_col = len(dates) + 1
            if date_col == 1:
                date_col += 1
            if date_col >= wks.col_count:
                wks.add_cols(date_col - wks.col_count)
            wks.update_cell(1, date_col, date)

        wks.update_cell(platform_row, date_col, count)

    def finalize(self):
        pass

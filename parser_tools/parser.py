import re


class Parser:
    """
    Regex parser
    """

    def __init__(self, text: str, currencies: str = None):
        pass

    def get_pattern(self) -> re.Pattern:
        """
        Get regex pattern for table record with currency rates
        :return: record pattern: Pattern
        """

        pass

    def get_curr_info(self) -> str:
        """
        Parse table with currency rates from html by regex
        :return: record data: str
        """

        pass

    def get_current_date(self) -> str:
        """
        Parse date from html by regex
        :return: current date: str
        """

        pass

    @staticmethod
    def check_date(date: str) -> re.Match:
        """
        Check date string by regex and return Match object
        :param date: current date: str
        :return: match result: Match
        """

        pass

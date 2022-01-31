import re
import decimal
import json


class Parser:
    """
    Regex parser
    """

    def __init__(self, text, currencies: str = None):
        self.text = text
        self.currencies = currencies.split(',') if currencies else []

    def get_pattern(self) -> re.Pattern:
        """
        Get regex pattern for table record with currency rates
        :return: record pattern: Pattern
        """

        alpha_pattern = r'[A-Z]{3}'
        alphas = []

        for code in self.currencies:
            if not code:
                continue

            if re.fullmatch(pattern=alpha_pattern, string=code):
                alphas.append(code)
            else:
                raise ValueError(f'Invalid format of code "{code}"')

        summary_alpha = alpha_pattern if not len(alphas) else r'(?:%s)' % f'{"|".join(alphas)}'

        return re.compile(
            r'[ ]{8}<tr>[\r\n]+[ ]{10}<td>(\d{3})</td>[\r\n]+[ ]{10}<td>(%s)</td>[\r\n]+[ ]{10}<td>(\d+)</td>'
            r'[\r\n]+[ ]{10}<td>([А-Яа-я ]+)</td>[\r\n]+[ ]{10}<td>([0-9,]+)</td>[\r\n]+[ ]{8}</tr>' % summary_alpha)

    def get_curr_info(self) -> str:
        """
       Parse table with currency rates from html by regex
       :return: record data: str
       """

        pattern = self.get_pattern()

        data = {
            'date': self.get_current_date(),
            'currencies': {
                match[1]: {
                    'numeric_code': match[1],
                    'alpha_code': match[2],
                    'quantity': match[3],
                    'text': match[4],
                    'value': match[5].replace(',', '.'),
                    'base_value': str(decimal.Decimal(match[5].replace(',', '.')) / decimal.Decimal(match[3])),
                } for match in pattern.finditer(self.text)
            },
        }

        return json.dumps(data, indent=4, ensure_ascii=False)

    def get_current_date(self) -> str:
        """
        Parse date from html by regex
        :return: current date: str
        """

        pattern = re.compile(r' value="(\d{2}\.\d{2}\.\d{4})" ')
        match = pattern.search(self.text)

        return match[1] if match else None

    @staticmethod
    def check_date(date: str):
        """
        Check date string by regex and return Match object
        :param date: current date: date
        :return: match result: Match
        """

        date_pattern = r'\d{2}\.\d{2}\.\d{4}'

        return re.fullmatch(pattern=date_pattern, string=str(date))

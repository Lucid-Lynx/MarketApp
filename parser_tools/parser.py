import re

from decimal import Decimal


class Parser:
    """
    Regex parser
    """

    def __init__(self, text: str):
        self.text = text

    '''
    def __init__(self, text: str, currencies: list = None):
        self.text = text
        self.currencies = currencies.split(',') if currencies else []
    '''

    @staticmethod
    def get_record_pattern() -> str:
        """
        Get regex pattern for table record with currency rates
        :return: record pattern: str
        """

        return r'[ ]{8}<tr>[\r\n]+[ ]{10}<td>(\d{3})</td>[\r\n]+[ ]{10}<td>([A-Z]{3})</td>' \
               r'[\r\n]+[ ]{10}<td>(\d+)</td>[\r\n]+[ ]{10}<td>([А-Яа-я ]+)</td>[\r\n]+[ ]{10}<td>([0-9,]+)</td>' \
               r'[\r\n]+[ ]{8}</tr>'

    @staticmethod
    def get_date_pattern() -> str:
        """
        Get regex pattern for date
        :return: date pattern: str
        """

        return r'\d{2}\.\d{2}\.\d{4}'

    '''
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
                err = f'Invalid format of code "{code}"'
                logging.error(err)
                raise ValueError(err)

        summary_alpha = alpha_pattern if not len(alphas) else r'(?:%s)' % f'{"|".join(alphas)}'

        return re.compile(
            r'[ ]{8}<tr>[\r\n]+[ ]{10}<td>(\d{3})</td>[\r\n]+[ ]{10}<td>(%s)</td>[\r\n]+[ ]{10}<td>(\d+)</td>'
            r'[\r\n]+[ ]{10}<td>([А-Яа-я ]+)</td>[\r\n]+[ ]{10}<td>([0-9,]+)</td>[\r\n]+[ ]{8}</tr>' % summary_alpha)
        '''

    def get_curr_info(self) -> dict:
        """
        Parse table with currency rates from html by regex
        :return: record data: str
        """

        pattern = re.compile(self.get_record_pattern())

        data = {
            'date': self.get_current_date(),
            'currencies': {
                match[2]: {
                    'numeric_code': match[1],
                    'alpha_code': match[2],
                    'quantity': int(match[3]),
                    'text': match[4],
                    'value': Decimal(match[5].replace(',', '.')),
                    # 'base_value': str(decimal.Decimal(match[5].replace(',', '.')) / decimal.Decimal(match[3])),
                } for match in pattern.finditer(self.text)
            },
        }

        # return json.dumps(data, indent=4, ensure_ascii=False)
        return data

    def get_current_date(self) -> str:
        """
        Parse date from html by regex
        :return: current date: str
        """

        # pattern = re.compile(r' value="(\d{2}\.\d{2}\.\d{4})" ')
        pattern = re.compile(fr' value="({self.get_date_pattern()})" ')
        match = pattern.search(self.text)

        return match[1] if match else None

    @staticmethod
    def check_date(date: str) -> re.Match:
        """
        Check date string by regex and return Match object
        :param date: current date: date
        :return: match result: Match
        """

        date_pattern = Parser.get_date_pattern()

        return re.fullmatch(pattern=date_pattern, string=str(date))

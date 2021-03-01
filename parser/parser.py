import re
import decimal
import json
import logging

logging.basicConfig(level=logging.INFO)


class Parser:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def get_pattern(numeric=None, alpha=None):
        numeric_pattern = r'\d{3}'
        alpha_pattern = r'[A-Z]{3}'

        if numeric and not re.fullmatch(pattern=numeric_pattern, string=numeric):
            raise ValueError(f'Invalid format of numeric code "{numeric}"')

        if alpha and not re.fullmatch(pattern=alpha_pattern, string=alpha):
            raise ValueError(f'Invalid format of alpha code "{alpha}"')

        summary_numeric = numeric_pattern if not numeric else numeric
        summary_alpha = alpha_pattern if not alpha else alpha

        return re.compile(
            r'[ ]{8}<tr>\r\n[ ]{10}<td>(%s)</td>\r\n[ ]{10}<td>(%s)</td>\r\n[ ]{10}<td>(\d+)</td>\r\n[ ]{10}'
            r'<td>([А-Яа-я ]+)</td>\r\n[ ]{10}<td>([0-9,]+)</td>\r\n[ ]{8}</tr>' % (summary_numeric, summary_alpha))

    def get_curr_info(self, numeric=None, alpha=None):
        pattern = self.get_pattern(numeric=numeric, alpha=alpha)

        data = {
            match[1]: {
                'numeric_code': match[1],
                'alpha_code': match[2],
                'quantity': match[3],
                'text': match[4],
                'value': match[5].replace(',', '.'),
                'base_value': str(decimal.Decimal(match[5].replace(',', '.')) / decimal.Decimal(match[3])),
            } for match in pattern.finditer(self.text)
        }

        return json.dumps(data, indent=4)

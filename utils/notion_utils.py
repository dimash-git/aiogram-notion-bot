import re
from datetime import datetime, timezone


def extract_trade_props(text):
    pattern = r'\$(\w+)\s(\w+)(?:\n\n([\d.]+))?(?:\nTP:\s([\d.]+))?(?:\nSL:\s([\d.]+))?(?:\n((.|\n)*))?'

    matches = re.match(pattern, text)

    date_utc = datetime.now().astimezone(timezone.utc).isoformat()
    ticker = matches.group(1)
    direction = matches.group(2)

    price = None
    tp = None
    sl = None

    if matches.group(3):
        price = float(matches.group(3))
    else:
        raise ValueError("Price is missing from the input message.")

    if matches.group(4):
        tp = float(matches.group(4))
    else:
        raise ValueError("TP is missing from the input message.")

    if matches.group(5):
        sl = float(matches.group(5))
    else:
        raise ValueError("SL is missing from the input message.")

    notes = matches.group(6).strip() or ''

    tr = round((tp / price - 1) / (1 - sl / price), 2)

    data = {
        'Ticker': {'title': [{'text': {'content': f"${ticker}"}}]},
        'Long/Short': {'select': {'name': direction}},
        'Target R': {'number': tr},
        'TP': {'number': tp},
        'SL': {'number': sl},
        'Date': {'date': {'start': date_utc, 'end': None}},
        'Notes': {'rich_text': [{'text': {'content': notes}}]},
        'Sum': {'number': 0},
        'Leverage': {'number': 0}
    }

    return data


def attach_trade_props(text):
    pattern = r'R:\s*([\d.]+)\nChange:\s*([\d.]+)'
    matches = re.match(pattern, text)

    if matches:
        r = float(matches.group(1))
        change = float(matches.group(2))

        data = {
            'Realized R': {'number': r},
            'Change': {'number': change},
        }

        return data

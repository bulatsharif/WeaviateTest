"""
This file consists of several lists containing the constant information needed to
the calculation or to validate information.
"""


CURRENCIES = {
    'XAG', 'XAG-BID', 'XAG-ASK', 'XAU', 'XAU-BID', 'XAU-ASK', 'XPD', 'XPD-BID', 'XPD-ASK',
    'XPT', 'XPT-BID', 'XPT-ASK', 'XRH', 'LBMA-XAG', 'LBMA-XAU-AM', 'LBMA-XAU-PM', 'LBMA-XPD-AM',
    'LBMA-XPD-PM', 'LBMA-XPT-AM', 'LBMA-XPT-PM', 'ALU', 'XCO', 'XCU', 'XGA', 'XIN', 'IRON', 'XPB',
    'XLI', 'XMO', 'NI', 'XND', 'XSN', 'XTE', 'XU', 'ZNC', 'XAU-AHME', 'XAU-BANG', 'XAU-BHOP',
    'XAU-CHAN', 'XAU-CHEN', 'XAU-COIM', 'XAU-DEHR', 'XAU-FARI', 'XAU-GURG', 'XAU-GUWA', 'XAU-HYDE',
    'XAU-INDO', 'XAU-JAIP', 'XAU-KANP', 'XAU-KOCH', 'XAU-KOLH', 'XAU-KOLK', 'XAU-LUCK', 'XAU-LUDH',
    'XAU-MADU', 'XAU-MALA', 'XAU-MANG', 'XAU-MEER', 'XAU-MUMB', 'XAU-MYSO', 'XAU-NAGP', 'XAU-NOID',
    'XAU-PATN', 'XAU-POND', 'XAU-PUNE', 'XAU-RAIP', 'XAU-SALE', 'XAU-VIJA', 'XAU-VISA', 'XAG-AHME',
    'XAG-BANG', 'XAG-CHAN', 'XAG-CHEN', 'XAG-COIM', 'XAG-HYDE', 'XAG-JAIP', 'XAG-KOLK', 'XAG-LUCK',
    'XAG-MADU', 'XAG-MANG', 'XAG-MUMB', 'XAG-MYSO', 'XAG-NAGP', 'XAG-PATN', 'XAG-PUNE', 'XAG-SALE',
    'XAG-VIJA', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AZN', 'BAM', 'BBD', 'BDT',
    'BGN', 'BHD', 'BIF', 'BIH', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BYN', 'BZD', 'CAD', 'CDF',
    'CHF', 'CLF', 'CLP', 'CNY', 'COP', 'CRC', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN',
    'ETB', 'ETH', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD',
    'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES',
    'KGS', 'KHR', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD',
    'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD',
    'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON',
    'RSD', 'RUB', 'RWF', 'SAR', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'STN', 'SVC',
    'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU',
    'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XOF', 'XPF', 'XRP', 'YER', 'ZAR', 'ZMK', 'ZMW'
}

GOLD_PURITY_MULTIPLIERS = {
    '375/9K': 0.35,
    '500/12K': 0.464,
    '583/585/14K': 0.56,
    '750/18K': 0.72,
    '850/21K': 0.8,
    '900/916/22K': 0.864,
    '958': 0.91,
    '999/24K': 1.0,
}

SILVER_PURITY_MULTIPLIERS = {
    '600': 0.3,
    '750': 0.5,
    '800': 0.66,
    '875/884': 0.84,
    '900/925': 0.9,
    '999': 1.0,
}
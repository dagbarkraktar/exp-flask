import datetime, time

def dmy_to_iso_date(dmy_date):
    """
    Convert date string from "dd.mm.yyyy" to "yyyy-mm-dd"
    """
    return datetime.date(*(time.strptime(dmy_date, "%d.%m.%Y")[0:3]))

def iso_to_dmy_date(iso_date):
    """
    Convert date string from "yyyy-mm-dd" to "dd.mm.yyyy"
    """
    return f"{iso_date[8:]}.{iso_date[5:7]}.{iso_date[0:4]}"

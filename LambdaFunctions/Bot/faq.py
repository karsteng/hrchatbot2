from enum import Enum

class FaqType(Enum):
    JOB_STILL_VACANT = 0
    JOB_FULL_OR_PARTTIME = 1


def get_content(faq_type):
    if faq_type == FaqType.JOB_STILL_VACANT:
        return "Die Stelle ist auf der Homepage jeweils tagesaktuell geschaltet. So lange sie online ist, ist die Position noch vakant. Bei Verlinkungen zu anderen Stellenportalen kann es zu Überschneidungen kommen. Der dort hinterlegte Link funktioniert nur so lange, wie die Ausschreibung online ist. Sobald er also nicht funktioniert, ist die Stelle offline und nicht mehr vakant."
    elif faq_type == FaqType.JOB_FULL_OR_PARTTIME:
        return "Alle Teilzeitstellen sind als solche gekennzeichnet. Wenn kein Hinweis auf Teilzeit in der Ausschreibung zu finden ist, handelt es sich um eine Vollzeit Stelle."

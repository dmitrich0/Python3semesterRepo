class Helper:
    """
    Вспомогательный класс с полезными методами
    """
    @staticmethod
    def parse_year_from_date_slice(date: str) -> int:
        return int(date[:4])

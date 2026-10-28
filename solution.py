# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_BOOKS = 3


def _valid_day(day):
    return type(day) is int and day >= 1


class LibraryLoan:
    def __init__(self):
        self._loans = {}       # book_id -> (name, borrow_day)
        self._suspensions = {}  # name -> [(start_day, end_day), ...]

    def borrow(self, book_id, name, day):
        if book_id not in BOOKS:
            return False
        if not _valid_day(day):
            return False
        if book_id in self._loans:
            return False
        held = [d + LOAN_DAYS for n, d in self._loans.values() if n == name]
        if len(held) >= MAX_BOOKS:
            return False
        if any(day > due for due in held):
            return False
        if any(s <= day <= e for s, e in self._suspensions.get(name, [])):
            return False
        self._loans[book_id] = (name, day)
        return True

    def return_book(self, book_id, name, day):
        if book_id not in BOOKS or book_id not in self._loans:
            return -1
        if not _valid_day(day):
            return -1
        borrower, borrow_day = self._loans[book_id]
        if borrower != name:
            return -1
        if day < borrow_day:
            return -1
        overdue = max(0, day - (borrow_day + LOAN_DAYS))
        del self._loans[book_id]
        if overdue > 0:
            self._suspensions.setdefault(name, []).append((day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        return sorted(
            ((b, d + LOAN_DAYS) for b, (n, d) in self._loans.items() if n == name),
            key=lambda x: (x[1], x[0]),
        )

class Pagination:
    def __init__(self, text, symbol_nom):
        self.text = text
        self.symbol_nom = symbol_nom
        self.pages = []

        start_index = 0

        for x in range(symbol_nom, len(text), symbol_nom):
            self.pages.append(text[start_index:x])
            start_index = x
        self.pages.append(text[start_index:])
        self.page_count = len(self.pages)
        self.item_count = len(text)

    def count_items_on_page(self, page_index):
        if 0 <= page_index < len(self.pages):
            return len(self.pages[page_index])
        else:
            raise Exception("Invalid index. Page is missing")

    def find_page(self, phrase):
        if phrase in self.text:
            first_letter_index = self.text.find(phrase) + 1
            last_letter_index = first_letter_index + len(phrase) - 1

            return [x for x in range(first_letter_index // self.symbol_nom,
                                     (last_letter_index - 1) // self.symbol_nom + 1)]

        else:
            raise Exception(f'{phrase} is missing on the page')

    def display_page(self, page_num):
        return self.pages[page_num]


pages = Pagination('Your beautiful text', 5)
print(pages.page_count)
print(pages.count_items_on_page(3))
# print(pages.count_items_on_page(4))
print(pages.find_page('beautiful'))
print(pages.display_page(2))

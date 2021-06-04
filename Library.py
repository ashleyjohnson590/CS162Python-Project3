class LibraryItem:
    """class initializes 2 private data members: library item ID and title."""
    def __init__(self, library_item_ID, title ):
        self._item_ID = library_item_ID
        """library_item_ID assumed unique"""
        self._title = title
        """title is not unique"""
        self._checked_out_by=None
        self._requested_by=None
        self._location = "ON_SHELF"
        """can be CHECKED_OUT, ON_HOLD, or ON_SHELF"""
        self._date_checked_out=0
        self.check_out_length = 0
    def check_out(self, patron_id, check_out_date):
        location = self.get_location()
        if location == "ON_SHELF":
            self.set_location("CHECKED_OUT")
            self.set_checked_out_by(patron_id)
            self.set_check_out_date(check_out_date)
        elif location == "ON_HOLD":
            requested_by = self.get_requested_by()
            if requested_by == patron_id:
                self.set_location("CHECKED_OUT")
                self.set_checked_out_by(patron_id)
                self.set_check_out_date(check_out_date)
            else:
                return "item on hold"
        elif location == "CHECKED_OUT":
            return "item not available"
        else:
            return "something is wrong"
        return "check out successful"


    def set_check_out_date(self, date):
        self._date_checked_out = date

    def returnItem(self):
        location = self.get_location()
        if location == "ON_SHELF":
            return "something is wrong, this item is not checked out"

        self.set_location("ON_SHELF")
        self.set_checked_out_by(None)
        self.set_check_out_date(0)
        return "return successful"

    def set_date_checked_out(self,date):
        self._date_checked_out=date
    def set_location(self, location):
        self._location=location
    def get_check_out_length(self):
        return self._check_out_length

    def get_item_ID(self):
        """gets ID of library item."""
        return self._item_ID
    def get_title(self):
        """returns title of library item"""
        return self._title

    def get_location(self):
        """determines if item is on shelf, on hold, or checked out."""
        return self._location
    def get_checked_out_by(self):
        """gets the name of patron who has item checked out(if any)."""
        return self._checked_out_by
    def get_requested_by(self):
        """gets the name of patron who has requested item(if any). An item can only be requested by one
        patron."""
        return self._requested_by
    def get_date_checked_out(self):
        """returns the current_date when an item is checked out."""
        return self._date_checked_out
    def get_location(self):
        """returns location of library item."""
        return self._location
    def set_checked_out_by(self, patron_id):
        self._checked_out_by=patron_id

class Book(LibraryItem):
    """class initializes check out length and returns number of days a book can be checked out(21 days)."""
    def __init__(self, library_item_ID, title, author):

        super().__init__(library_item_ID, title)
        self._check_out_length = 21
        self._author=author

    def get_author(self):
        """returns name of book author"""
        return self._author

class Album(LibraryItem):
    """class inherits from LibraryItem and adds an artist string field."""
    def __init__(self, library_item_ID, title, artist):
        super().__init__(library_item_ID, title)
        self._artist =artist
        self._check_out_length =14

    def get_artist(self):
        """returns artist of checked out albums"""
        return self._artist

class Movie(LibraryItem):
    """class inherits from LibraryItem and adds a director string field."""
    def __init__(self, library_item_ID, title, director):
        super().__init__(library_item_ID,title)
        self._check_out_length = 7
        self._director = director

    def get_director(self):
        """returns director of checked out Movie"""
        return self._director

class Patron:
    """class initializes 2 private data members: patron id, and patron name."""
    def __init__(self, patron_id, name):
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0 #initializes patron fine to zero. Fine can go negative

    def get_fine_amount(self):
        """returns total patron fine."""
        return self._fine_amount

    def add_library_item(self, item):
        """adds library item to patron cart."""
        self._checked_out_items.append(item)

    def print_fine_amount(self):
        amount = self._fine_amount
        #amount = amount # deleted/100 commented
        #amount_string = "${:.2f}".format(amount) commented
        return amount #changed return amount_string to return amount
    def remove_library_item(self, item):
        """removes library item from patron cart."""
        self._checked_out_items.remove(item)

    def amend_fine(self, fine_paid_or_charged):
        """fine is increased with a positive argument and decreased with a negative argument. Total fine can
        go negative."""
        self._fine_amount += fine_paid_or_charged


    def get_patron_name(self):
        """returns patron name. Name can not be assumed to be unique"""
        return self._name

    def get_patron_ID(self):
        """returns patron ID. ID can be assumed to be unique."""
        return self._patron_id

    def get_checked_out_items(self):
        """returns cart of checked out items"""
        return self._checked_out_items

class Library:
    def __init__(self):
        """initializes current date to zero, an empty list of library inventory, and an empty
        list of library patrons"""
        self._holdings = {} # initializes an empty dictionary of library items in library inventory.
        self._members = {} #initializes an empty dictionary of library patrons
        self._current_date = 0  # initializes current date to zero.

    def get_holdings(self):
        """returns dictionary of library inventory."""
        return self._holdings

    def get_current_date(self):
        """returns current date"""
        return self._current_date

    def add_library_item(self, item):
        """ adds a library item to holdings dictionary."""
        itemID = item.get_item_ID()
        holdings = self.get_holdings()
        holdings[itemID] = item

    def add_patron(self, patron):
        """adds a patron to members dictionary."""
        patron_num = patron.get_patron_ID()
        try:
            self._members[patron_num]
        except KeyError:
            self._members[patron_num] = patron
        except:
            message = "this patron ID already exists. Please give different patron ID."
            return message

    def lookup_library_item_from_id(self, library_item_id):
        """gets item ID and returns the library item or none if it does not exist."""
        LibraryInventory = self.get_holdings()
        try:
            myItem = LibraryInventory[library_item_id]
        except KeyError:
            eMsg = "Item ID not found: {}".format(library_item_id)
            return eMsg
        except:
            title = myItem.get_title()
            return title

    def get_members(self):
        return self._members
    def lookup_patron_from_id(self, patron_id):
        """gets patron ID and returns name or none if patron does not exist."""
        myPatrons = self.get_members()
        try:
            patronFound = myPatrons[patron_id]
        except KeyError:
            return "patron ID not found"
        return patronFound
    def get_item_from_ID(self, item_id):
        myHoldings = self.get_holdings()
        thisItem = None
        try:
            thisItem = myHoldings[item_id]
        except KeyError:
            print("library does not have item ID.{}".format(item_id))
        return thisItem





    def check_out_library_item(self, patron_id, library_item_id):
        """looks up patron ID and library item. If patron exists and library item is available, updates
          checked_out_by, date_checked_out, and location. Updates requested_by if item was on hold by patron,
          updates patron's checked_out_items, and returns check out successful."""
        myPatrons = self.get_members()
        thisPatron = None
        try:
            thisPatron = myPatrons[patron_id]
        except KeyError:
            patronError = "patron not found"
            return patronError

        myLibraryItems = self.get_holdings()
        thisItem = None
        try:
            thisItem = myLibraryItems[library_item_id]
        except KeyError:
            itemError = "item not found"
            return itemError
        thisPatron.add_library_item(thisItem)
        items = thisPatron.get_checked_out_items()
        current_date = self.get_current_date()
        myReturn = thisItem.check_out(patron_id,current_date)
        return myReturn

    def return_library_item(self, library_item_id):
        """looks up library item id and if found, updates patron's checked out items, libraryItem's location,
        and checked_out_by. Returns return successful."""

        LibraryItems = self.get_holdings()
        thisItem = None
        try:
            thisItem = LibraryItems[library_item_id]
        except KeyError:
            return "item not found"
        patron_id = thisItem.get_checked_out_by()
        patron = self.lookup_patron_from_id(patron_id)
        status = thisItem.returnItem()
        if status != "return successful":
            return "can not return item"
        patron.remove_library_item(thisItem)

        return "return successful"


    def request_library_item(self, patron_id, library_item_id):
        """looks up patron and library item id and if found, updates libraryItem's requested_by and item's location to
        on hold. returns request successful."""
        myPatrons = self.get_members()
        thisPatron = None
        try:
            thisPatron = myPatrons[patron_id]
        except KeyError:
            patronError = "patron not found"
            return patronError
        myHoldings = self.get_holdings()
        try:
            thisItem = myHoldings[library_item_id]
        except KeyError:
            itemError = "item not found"
            return itemError
        requested_by = thisItem.get_requested_by()
        item_location = thisItem.get_location()
        if requested_by != None:
            return "item already on hold"

        elif requested_by == patron_id:
            return "you already requested this item."
        else:
            if item_location == "ON_HOLD":
                print("librarian made a mistake, i am fixing it.")
            elif item_location == "CHECKED_OUT":
                checked_out_by = thisItem.get_checked_out_by()
                if checked_out_by == patron_id:
                    return "you have this item checked out, you can not put it on hold."
            else:
                thisItem.set_location("ON_HOLD")
            thisItem.requested_by = patron_id

        return "request successful"

    def pay_fine(self, patron_id, amount_paid):
        """looks up patron id and if found, updated patron's fine using amend_fine. returns payment successful."""
        myPatrons = self.get_members()
        thisPatron = None
        try:
            thisPatron = myPatrons[patron_id]
            thisPatron.amend_fine(-amount_paid) # deleted *100 #subtracts amounts in pennies paid from thisPatron
            return "payment successful"
        except KeyError:
            patronError = "patron not found"
            return patronError


    def increment_current_date(self):
        """increments current date and increases patron's fine by 10 cents for each checked out overdue item."""
        self._current_date += 1
        current_date = self._current_date
        myMembers = self.get_members()
        for member_id in myMembers.keys():
            member = myMembers[member_id]
            checked_out_items = member.get_checked_out_items()
            for item in checked_out_items:
                name = item.get_title()
                date_checked_out = item.get_date_checked_out()
                checked_out_length = item.get_check_out_length()
                time_out = current_date - date_checked_out
                over_days = time_out-checked_out_length
                if over_days >0:
                    member.amend_fine(0.10) #changed member.amend_fine(10) t0 member.amend_fine(0.10)


if __name__ == '__main__':
    BookID1 = 1
    BookTitle = "war and peace"
    BookAuthor = "Tolstoy"
    book1 = Book(BookID1, BookTitle, BookAuthor)

    BookID2 = 2
    BookTitle = "Hop on Pop"
    BookAuthor = "Suess"
    book2 = Book(BookID2, BookTitle, BookAuthor)
    patron1ID = 123
    patron1name = "Ashley"
    patron1 = Patron(patron1ID, patron1name)
    patron2ID = 456
    patron2name = "brandon"
    patron2 = Patron(patron2ID, patron2name)
    libraryPatrons = {
        patron1ID: patron1,
        patron2ID: patron2
    }
    libraryItems = {
        BookID1: book1,
        BookID2: book2
    }
    myLibrary = Library(libraryPatrons, libraryItems)
    status = myLibrary.check_out_library_item(patron2ID, BookID1)
    status = myLibrary.check_out_library_item(patron2ID, BookID2)
    for i in range(22):
        myLibrary.increment_current_date()
    p2_fine = patron2.print_fine_amount()
    print(p2_fine)
    myLibrary.pay_fine(patron2ID, 0.20)

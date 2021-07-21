from abc import ABC , abstractmethod

class User(ABC):
    def __init__(self , name , phonenumber , address , loginid , password):
        self.name = name
        self.address = address
        self.phonenumber = phonenumber
        self.__loginid = loginid
        self.__password = password
        pass

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getPhoneNumber(self):
        pass

    @abstractmethod
    def getAddress(self):
        pass

class Admin(User):

    profit = 0
    investment = 0

    def __init__(self, name , phonenumber , address , loginid , password):
        super().__init__(name , phonenumber , address , loginid , password)
        pass

    def getAddress(self):
        return self.address
    
    def getName(self):
        return self.name

    def getPhoneNumber(self):
        return self.phonenumber

class Customer(User):
    def __init__(self, name , phonenumber , address , loginid , password , amountdue , numberoforders):
        super().__init__(name , phonenumber , address , loginid , password)
        self.__amountdue = amountdue
        self.__numberoforders = numberoforders
        pass

    def getAddress(self):
        return self.address
    
    def getName(self):
        return self.name

    def getPhoneNumber(self):
        return self.phonenumber
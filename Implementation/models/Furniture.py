class Furniture:
    def __init__(self , id , name , company , price , feedback , description , type , rented , photo , interestrate , timeframe ,userid = 0):
        self.__id = id
        self.__name = name
        self.__company = company
        self.__price = price
        self.__feedback = feedback
        self.__description = description
        self.__type = type
        self.__rented = rented
        self.__photo = photo
        self.__interestrate = interestrate
        self.__timeframe = timeframe
        pass
    
    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getCompany(self):
        return self.__company

    def getPrice(self):
        return self.__price

    def getFeedback(self):
        return self.__feedback

    def getDescription(self):
        return self.__description

    def getType(self):
        return self.__type

    def getUserId(self):
        return self.__id

    def isRented(self):
        return self.__rented

    def getPhoto(self):
        return self.__photo

    def getInterestRate(self):
        return self.__interestrate

    def getTimeFrame(self):
        return self.__timeframe
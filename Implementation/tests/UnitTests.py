import unittest
import models
from models import Admin, Customer
from models import Furniture

class TestFurnitureMethods(unittest.TestCase):
    myfurniture = Furniture(1, "Center Table", "neelkamal", 4000, "Durable!", "Made of pure wood", "Table", 0, "Imagepath", 2, 365)
    
    def test_id(self):
        self.assertEqual(self.myfurniture.getId(), 1)
    
    def test_name(self):
        self.assertEqual(self.myfurniture.getName(), "Center Table")
    
    def test_Company(self):
        self.assertEqual(self.myfurniture.getCompany(), "neelkamal")
    
    def test_Price(self):
        self.assertEqual(self.myfurniture.getPrice(), 4000)
    
    def test_Feedback(self):
        self.assertEqual(self.myfurniture.getFeedback(), "Durable!")

    def test_Description(self):
        self.assertEqual(self.myfurniture.getDescription(), "Made of pure wood")

    def test_Type(self):
        self.assertEqual(self.myfurniture.getType(), "Table")

    def test_Photo(self):
        self.assertEqual(self.myfurniture.getPhoto(), "Imagepath")

    def test_Interestrate(self):
        self.assertEqual(self.myfurniture.getInterestRate(), 2)
    
    def test_Timeframe(self):
        self.assertEqual(self.myfurniture.getTimeFrame(), 365)

class TestAdminMethods(unittest.TestCase):
    my_admin = Admin("Saurav", "12345667", "india", "saurav123", "saurav")

    def test_name(self):
        self.assertEqual(self.my_admin.getName(), "Saurav")
    
    def test_PhoneNumber(self):
        self.assertEqual(self.my_admin.getPhoneNumber(), "12345667")
    
    def test_Adress(self):
        self.assertEqual(self.my_admin.getAddress(), "india")

class TestCustomerMethods(unittest.TestCase):
    my_customer = Customer("Saurav Likhar", "15667", "india", "saurav13", "saurav", 1200, 2)

    def test_name(self):
        self.assertEqual(self.my_customer.getName(), "Saurav Likhar")
    
    def test_PhoneNumber(self):
        self.assertEqual(self.my_customer.getPhoneNumber(), "15667")
    
    def test_Adress(self):
        self.assertEqual(self.my_customer.getAddress(), "india")

if __name__ == "__main__":
    unittest.main()

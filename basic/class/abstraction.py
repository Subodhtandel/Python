from abc import ABC,abstractmethod

class Account(ABC):

    balance=0

    def __init__(self):
        print("Account calling")
        pass

    @abstractmethod
    def deposite(self):
        pass

    def checkbalance(self):
        print(f"current balance is {self.balance}")

class savingAccount(Account):

    def deposite(self,amt):
        self.balance=self.balance+amt
        print(f"{amt} : credited")

class LoanAccount(Account):
    def __init__(self,amt):
        self.balance=amt

    def deposite(self,amt):
        print(f"{amt}: cradited")


s = savingAccount()
s.deposite(5000)
s.deposite(1000)
s.checkbalance()

print("********")

l =LoanAccount(50000)
l.deposite(5000)
s.deposite(1000)
l.checkbalance()
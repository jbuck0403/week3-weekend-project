# Here we assume that we have a client coming to us asking for an automated Rental Property Calculator.
# Our client's name is Brandon from a company called "Bigger Pockets".
# Below, you will find a video of what Brandon usually does to calculate his Rental Property ROI.

# Using Visual Studio Code/Jupyter Notebook, and Object Oriented Programming create a program
# that will calculate the Return on Investment(ROI) for a rental property.

# four square method
#
# 1. Income - rental income, laundry income, storage, etc.
# Total monthly income equals sum of all income streams
#
# 2. Expenses - mortgage, property taxes, insurance, utilities (electric, water, sewer, garbage, gas),
# HOA fees, expected maintenance (gardening), vacancy, capital expenditures (money set aside for big expenses [roof, repairs, etc.]),
# repairs, property management
#
# 3. Cash flow - income - expenses
#
# 4. ROI - cash flow divided by down payment + closing costs + rehab budget ([initial painting, gardening, repairs, etc.]) +
# misc. other (all things up front that need to be paid before property can start generating income)
#
# 5. eventual property sale - include a range that the property value could appreciate (conservative and liberal estimates) - cost to sell (closing costs)

from ui import clearTerminal
from financialInfo import propertyTaxRates, mortgageRates, homeInsuranceAvgYear


class PropertyCalculator:
    def __init__(self):
        self.propertyValue = 0
        self.downPayment = 0
        self.rentalIncome = 0
        self.income = 0
        self.expenses = 0
        self.expensesByItem = {}
        self.cashFlow = self.income - self.expenses
        self.roi = 0
        self.mortgageTimeline = 0
        self.mortgagePayment = 0
        self.interestRate = 0
        self.propertyTaxPayment = 0

    def runner(self):
        clearTerminal()
        print("Thank you for using our rental property calculator!")
        print(
            "We'll begin by asking you a series of questions meant to determine the overall value of your potential investment."
        )
        print("Please gather all of your information and we'll begin!")
        userInput = input("Press 'Enter' to begin, or type 'exit': ")
        if userInput == "":
            pass
        elif userInput.lower()[0] == "e":
            return

        self.calcMortgage()
        self.calcIncome()
        print(self.propertyValue)
        print(self.downPayment)
        print(self.income)
        print(self.mortgagePayment)
        print(self.interestRate)
        print(self.propertyTaxPayment)
        self.calcExpenses()
        print(self.expenses)
        print(self.expensesByItem)
        # self.returnOnInvestment()

    def calcMortgage(self):
        def calcInterest():
            self.mortgage = True
            timeline = self._userInput(
                f"How many years will you take to pay it off?\n{', '.join([str(period) for period in mortgageRates.keys()])} or another pay period: "
            )
            if timeline in mortgageRates.keys():
                self.mortgageTimeline = timeline
                self.interestRate = mortgageRates[timeline]
            else:
                self.mortgageTimeline = timeline
                self.interestRate = (
                    self._userInput("What interest rate have you been quoted?: ") / 100
                )
            loan = self.propertyValue - self.downPayment
            interest = loan * self.interestRate
            self.mortgagePayment = int((loan + interest) / (self.mortgageTimeline * 12))

        propertyValue = self._userInput("What is the value of the property?: ")
        self.propertyValue = propertyValue
        rate = propertyTaxRates[
            self._userInput(
                "In which state is this property located?: ",
                "Please enter a valid state...",
                passCondition=lambda x: x in propertyTaxRates.keys(),
                strInput=True,
            )
        ]

        self.propertyTaxPayment = int((self.propertyValue * rate / 100.0) / 12)

        mortgage = self._userInput(
            "Will you be taking out a mortgage? ('Yes' or 'No'): ", boolInput=True
        )
        if mortgage:
            downPayment = self._userInput("How much will your down payment be?: ")
            self.downPayment = downPayment
            calcInterest()
        else:
            self.downPayment = self.propertyValue
            self.mortgage = False

    def calcIncome(self):
        def suggestRent():
            if self.propertyValue > 1000000:
                highPercent = 0.005
                lowPercent = 0.001
            elif self.propertyValue > 100000:
                highPercent = 0.006
                lowPercent = 0.003
            else:
                highPercent = 0.011
                lowPercent = 0.008

            high = self._addCommas(int(self.propertyValue * 0.006))
            low = self._addCommas(int(self.propertyValue * 0.003))

            return f"We estimate you can charge between ${low} and ${high} in monthly rent based on your estimated property value of ${self._addCommas(self.propertyValue)}."

        rentalIncome = self._userInput(
            f"The primary way property owners see a return on their investment is through rental income.\n{suggestRent()}\nWhat would you estimate your rent to be?: "
        )

        self.rentalIncome = rentalIncome

        if self._userInput(
            "Do you envision other sources of income for this property? ('Yes' or 'No'): ",
            boolInput=True,
        ):
            additionalIncome = self._userInput(
                "Please enter the total amount of additional monthly income (excluding rental income) you expect from this property: "
            )
        else:
            additionalIncome = 0

        self.income = rentalIncome + additionalIncome

    def calcExpenses(self):
        def hoaDues():
            hoa = self._userInput(
                "Is there a Home Owners Association (HOA)?: ", boolInput=True
            )
            if hoa:
                hoaCost = self._userInput("What are the HOA dues?: ")
            else:
                hoaCost = 0

            return hoaCost

        def utilities():
            tenantPayUtilities = self._userInput(
                "Will the tenants be responsible for utilities (Electric/Water/Sewer/Garbage/Gas)?: ",
                boolInput=True,
            )

            if not tenantPayUtilities:
                utilities = self._userInput(
                    "Based on national averages, you can expect utilities to cost around $300.\nIs this a fair estimate for you? ('Yes' or 'No'): ",
                    boolInput=True,
                )
                if utilities:
                    utilitiesCost = 300
                else:
                    utilitiesCost = self._userInput(
                        "What do you estimate to pay for utilities?: "
                    )
            else:
                utilitiesCost = 0

            return utilitiesCost

        def propertyManagement():
            propertyManagement = self._userInput(
                "Will you be contracting a property management company? ('Yes' or 'No'): ",
                boolInput=True,
            )
            if propertyManagement:
                propertyManagementCost = self._userInput(
                    f"We estimate property management for your property to cost between ${int(self.rentalIncome * 0.06)} and ${int(self.rentalIncome * 0.12)} per month.\nWhat do you expect to pay?: "
                )
            else:
                propertyManagementCost = 0

            return propertyManagementCost

        def emergencyFund():
            defaultFund = self._userInput(
                "We recommend setting aside $100 each for irregular expenditures like maintenance and capital expenditures (roof replacement, etc.).\nWould you like to add these values? ('Yes' or 'No'): ",
                boolInput=True,
            )
            if defaultFund:
                fund = 200
            else:
                fund = self._userInput(
                    "How much to set aside for irregular expenditures?: "
                )

            return fund

        def insurance():
            defaultInsurance = self._userInput(
                f"The national average for insurance is ${self._addCommas(homeInsuranceAvgYear)}.\nMonthly, this equates to ${self._addCommas(int(homeInsuranceAvgYear / 12))}.\nDo you want to use this estimate? ('Yes' or 'No'): ",
                boolInput=True,
            )
            if defaultInsurance:
                insurance = homeInsuranceAvgYear / 12
            else:
                insurance = self._userInput(
                    "What are you estimating for your insurance payment? (Monthly): "
                )

            return insurance

        hoaCost = hoaDues()
        utilitiesCost = utilities()
        propertyManagementCost = propertyManagement()
        emergencyFundCost = emergencyFund()
        insuranceCost = insurance()

        expenses = [
            self.mortgagePayment,
            self.propertyTaxPayment,
            insuranceCost,
            hoaCost,
            utilitiesCost,
            propertyManagementCost,
            emergencyFundCost,
        ]
        expenseNames = [
            "Mortgage",
            "Property Tax",
            "Insurance",
            "HOA Dues",
            "Utilities",
            "Property Management",
            "Emergency Fund",
        ]

        expensesDict = {}

        for key, value in zip(expenseNames, expenses):
            if value == 0:
                continue
            else:
                expensesDict[key] = value

        self.expensesByItem = expensesDict
        self.expenses = sum(expensesDict.values())

    def returnOnInvestment(self):
        self.roi = roi

    def _addCommas(self, num):
        numStr = str(num)[::-1]
        numList = list(numStr)

        if len(numList) - 3 == 0:
            return num

        numMap = map(
            lambda x: x[1] + "," if (x[0] + 1) % 3 == 0 else x[1], enumerate(numList)
        )

        return "".join(numMap)[::-1]

    def _userInput(
        self,
        message,
        errorMessage="Invalid input, numbers only...",
        passCondition=lambda x: type(x) == int,
        strInput=False,
        boolInput=False,
    ):
        if boolInput:
            errorMessage = "'Yes' or 'No' only..."
            passCondition = lambda x: x == "y" or x == "n"
        error = False
        while True:
            try:
                clearTerminal()

                if error:
                    newMessage = f"{errorMessage}\n{message}"

                if strInput:
                    userInput = input(newMessage if error else message).strip().lower()
                elif boolInput:
                    userInput = (
                        input(newMessage if error else message).strip().lower()[0]
                    )
                else:
                    userInput = int(input(newMessage if error else message).strip())

                if passCondition(userInput):
                    if boolInput:
                        if userInput == "y":
                            return True
                        else:
                            return False
                    return userInput
                else:
                    error = True
                    continue
            except:
                error = True
                continue


test = PropertyCalculator()
test.runner()

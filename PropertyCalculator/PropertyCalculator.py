from PropertyCalculator.ui import clearTerminal, userInput
from PropertyCalculator.financialInfo import (
    propertyTaxRates,
    mortgageRates,
    homeInsuranceAvgYear,
)


class PropertyCalculator:
    def __init__(self):
        self.propertyValue = 0
        self.downPayment = 0
        self.rentalIncome = 0
        self.income = 0
        self.expenses = 0
        self.expensesByItem = {}
        self.cashFlow = 0
        self.cashOnCash = 0
        self.mortgageTimeline = 0
        self.mortgagePayment = 0
        self.mortgage = False
        self.interestRate = 0
        self.propertyTaxPayment = 0
        self.rehabBudget = 0
        self.miscCostItems = 0

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
        self.calcExpenses()
        self.returnOnInvestment()
        self.displayInvestment()
        self.realEstateAppreciation()

    def calcMortgage(self):
        def calcInterest():
            self.mortgage = True
            timeline = userInput(
                f"How many years will you take to pay it off?\n{', '.join([str(period) for period in mortgageRates.keys()])} or another pay period: "
            )
            if timeline in mortgageRates.keys():
                self.mortgageTimeline = timeline
                self.interestRate = mortgageRates[timeline]
            else:
                self.mortgageTimeline = timeline
                self.interestRate = (
                    userInput("What interest rate have you been quoted?: ") / 100
                )
            loan = self.propertyValue - self.downPayment
            interest = loan * self.interestRate
            self.mortgagePayment = int((loan + interest) / (self.mortgageTimeline * 12))

        propertyValue = userInput("What is the value of the property?: ")
        self.propertyValue = propertyValue

        rate = propertyTaxRates[
            userInput(
                "In which state is this property located?: ",
                "Please enter a valid state...",
                passCondition=lambda x: x in propertyTaxRates.keys(),
                strInput=True,
            )
        ]

        self.propertyTaxPayment = int((self.propertyValue * rate / 100.0) / 12)

        mortgage = userInput("Will you be taking out a mortgage?", boolInput=True)
        if mortgage:
            downPayment = userInput(
                f"How much will your down payment be?\nNew home buyers average 6% (${self._addCommas(int(self.propertyValue * 0.06))}), whereas repeat buyers average 17% (${self._addCommas(int(self.propertyValue * 0.17))}): "
            )
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

        rentalIncome = userInput(
            f"The primary way property owners see a return on their investment is through rental income.\n{suggestRent()}\nWhat would you estimate your rent to be?: "
        )

        self.rentalIncome = rentalIncome

        if userInput(
            "Do you envision other sources of income for this property?",
            boolInput=True,
        ):
            self.additionalIncome = userInput(
                "Please enter the total amount of additional monthly income (excluding rental income) you expect from this property: "
            )
        else:
            self.additionalIncome = 0

        self.income = self.rentalIncome + self.additionalIncome

    def calcExpenses(self):
        def hoaDues():
            hoa = userInput("Is there a Home Owners Association (HOA)?", boolInput=True)
            if hoa:
                hoaCost = userInput("What are the HOA dues?: ")
            else:
                hoaCost = 0

            return hoaCost

        def utilities():
            tenantPayUtilities = userInput(
                "Will the tenants be responsible for utilities (Electric/Water/Sewer/Garbage/Gas)?",
                boolInput=True,
            )

            if not tenantPayUtilities:
                utilities = userInput(
                    "Based on national averages, you can expect utilities to cost around $300.\nIs this a fair estimate for you?",
                    boolInput=True,
                )
                if utilities:
                    utilitiesCost = 300
                else:
                    utilitiesCost = userInput(
                        "What do you estimate to pay for utilities?: "
                    )
                addUtilitiesToRent = userInput(
                    f"Would you like to add utilities (${utilitiesCost}) to the rent?\nThis would bring the new rent to ${self.rentalIncome + utilitiesCost}",
                    boolInput=True,
                )
                if addUtilitiesToRent:
                    self.rentalIncome += utilitiesCost
                    self.income = self.rentalIncome + self.additionalIncome
            else:
                utilitiesCost = 0

            return utilitiesCost

        def propertyManagement():
            propertyManagement = userInput(
                "Will you be contracting a property management company?",
                boolInput=True,
            )
            if propertyManagement:
                propertyManagementCost = userInput(
                    f"We estimate property management for your property to cost between ${int(self.rentalIncome * 0.06)} and ${int(self.rentalIncome * 0.12)} per month.\nWhat do you expect to pay?: "
                )
            else:
                propertyManagementCost = 0

            return propertyManagementCost

        def emergencyFund():
            irregularPercent = 0.06
            defaultFund = userInput(
                f"We recommend setting aside ${self._addCommas(int(self.rentalIncome * irregularPercent))} per month for irregular expenditures like maintenance and capital expenditures (roof replacement, etc.).\nWould you like to add these values?",
                boolInput=True,
            )
            if defaultFund:
                fund = int(self.rentalIncome * irregularPercent)
            else:
                fund = userInput("How much to set aside for irregular expenditures?: ")

            return fund

        def insurance():
            defaultInsurance = userInput(
                f"The national average for insurance is ${self._addCommas(homeInsuranceAvgYear)}.\nMonthly, this equates to ${self._addCommas(int(homeInsuranceAvgYear / 12))}.\nDo you want to use this estimate?",
                boolInput=True,
            )
            if defaultInsurance:
                insurance = homeInsuranceAvgYear / 12
            else:
                insurance = userInput(
                    "What are your estimates for your insurance payment? (Monthly): "
                )

            return int(insurance)

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
            "Management",
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
        self.cashFlow = self.income - self.expenses

    def returnOnInvestment(self):
        agentsInvolved = userInput(
            "How many agents will be involved in the sale?: ",
            "At most 2 representatives...",
            passCondition=lambda x: type(x) == int and x >= 0 and x <= 2,
        )
        self.commission = int(((agentsInvolved * 3) / 100) * self.propertyValue)

        rehabNeeded = userInput(
            "Will the property need any repairs or upgrades before you can begin renting/utilizing?",
            boolInput=True,
        )
        if rehabNeeded:
            rehabBudget = userInput(
                "How much are you planning to budget for rehab (fixing up) on the property?: "
            )
        else:
            rehabBudget = 0

        miscCosts = userInput("Any other Miscellaneous costs?", boolInput=True)
        miscCostItems = {}
        while miscCosts:
            miscCostName = userInput(
                "Enter the name of the cost ('exit' when done): ",
                "Input cannot be blank...",
                passCondition=lambda x: x != "",
                strInput=True,
            )
            if miscCostName[0] == "e":
                break
            miscCost = userInput(
                f"How much for {miscCostName.title()}: ", passCondition=lambda x: x > 0
            )
            miscCostItems[miscCostName] = miscCost

        self.rehabBudget = rehabBudget
        self.miscCostItems = miscCostItems

        miscItems = miscCostItems.values()

        self.upFrontCost = int(
            self.downPayment
            + self.commission
            + self.rehabBudget
            + (sum(miscItems) if len(miscCostItems.values()) > 0 else 0)
        )

        self.cashOnCash = ((self.cashFlow * 12) / (self.upFrontCost)) * 100
        self.capRate = ((self.cashFlow * 12) / self.propertyValue) * 100

        self.roi = (self.cashFlow * 12) / (self.downPayment + self.upFrontCost)

    def realEstateAppreciation(self):
        appreciationLowPercent = 0.008
        appreciationHighPercent = 0.015

        appreciatedValueLow = self.propertyValue
        appreciatedValueHigh = self.propertyValue
        appreciationLow = 0
        appreciationHigh = 0

        print(f"\n\nPotential Appreciation\n")
        for idx in range(0, 10):
            if idx == 0:
                print(f"Current Value:\t${self.propertyValue}")
            else:
                appreciationLow += appreciatedValueLow * appreciationLowPercent
                appreciationHigh += appreciatedValueHigh * appreciationHighPercent
                appreciatedValueLow += appreciationLow
                appreciatedValueHigh += appreciationHigh

                print(f"Value after {idx} year{'' if idx == 1 else 's'}:")
                print(
                    f"Low: ${self._addCommas(int(appreciatedValueLow))}\tGain: ${self._addCommas(int(appreciatedValueLow - self.propertyValue))}"
                )
                print(
                    f"High: ${self._addCommas(int(appreciatedValueHigh))}\tGain: ${self._addCommas(int(appreciatedValueHigh - self.propertyValue))}\n"
                )

    def displayInvestment(self):
        clearTerminal()
        print(f"Cash Flow: ${self._addCommas(self.cashFlow)}\n")
        print(
            f"Expected Returns:\nCash on Cash: {round(self.cashOnCash, 2)}%\nCap Rate: {round(self.capRate, 2)}%\nROI: {round(self.roi, 2)}%"
        )
        print("\nAssets:")
        print(f"Property Value: ${self._addCommas(self.propertyValue)}")
        print(
            f"Income: ${self._addCommas(self.income)} with ${self._addCommas(self.rentalIncome)} from rent"
        )
        print(f"\nMonthly Expenses: ${self._addCommas(self.expenses)}")
        for item, cost in self.expensesByItem.items():
            print(f"{item}:\t${self._addCommas(cost)}")
        print(f"\nUp-Front Expenses:\t${self._addCommas(self.upFrontCost)}")
        print(f"Down Payment:\t${self._addCommas(self.downPayment)}")
        print(f"Commission:\t${self._addCommas(self.commission)}")
        print(f"Rehab Budget:\t${self._addCommas(self.rehabBudget)}")
        for item, cost in self.miscCostItems.items():
            print(f"{item.title()}:\t${self._addCommas(cost)}")

    def _addCommas(self, num):
        negative = False
        if num < 0:
            negative = True

        numStr = str(num)[::-1]
        numList = list(numStr)

        if len(numList) <= 3:
            return num

        numMap = map(
            lambda x: x[1] + ","
            if (x[0] + 1) % 3 == 0 and x[0] != len(numList) - (2 if negative else 1)
            else x[1],
            enumerate(numList),
        )

        return "".join(numMap)[::-1]

import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [na]\tNew account
    [la]\tList accounts
    [nu]\tNew user
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu))

def deposit(balance, amount, statement, /):
    if amount > 0:
        balance += amount
        statement += f"Deposit:\tR$ {amount:.2f}\n"
        print("\nDeposit successful!")
    else:
        print("\nOperation failed! The amount entered is invalid.")

    return balance, statement

def withdraw(*, balance, amount, statement, limit, number_of_withdrawals, withdrawal_limit):
    exceeded_balance = amount > balance
    exceeded_limit = amount > limit
    exceeded_withdrawals = number_of_withdrawals >= withdrawal_limit

    if exceeded_balance:
        print("\nOperation failed! Insufficient balance.")

    elif exceeded_limit:
        print("\nOperation failed! The withdrawal amount exceeds the daily limit.")

    elif exceeded_withdrawals:
        print("\nOperation failed! Maximum number of daily withdrawals exceeded.")

    elif amount > 0:
        balance -= amount
        statement += f"Withdrawal:\t\tR$ {amount:.2f}\n"
        number_of_withdrawals += 1
        print("\nWithdrawal successful!")

    else:
        print("\nOperation failed! The amount entered is invalid.")

    return balance, statement

def display_statement(balance, /, *, statement):
    print("\n================ STATEMENT ================")
    print("No transactions were made." if not statement else statement)
    print(f"\nBalance:\t\tR$ {balance:.2f}")
    print("==========================================")

def create_user(users):
    cpf = input("Enter CPF (numbers only): ")
    user = filter_user(cpf, users)

    if user:
        print("\nA user with this CPF already exists!")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    address = input("Enter address (street, number - neighborhood - city/state abbreviation): ")

    users.append({"name": name, "birth_date": birth_date, "cpf": cpf, "address": address})

    print("User created successfully!")

def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None

def create_account(agency, account_number, users):
    cpf = input("Enter the user's CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\nAccount created successfully!")
        return {"agency": agency, "account_number": account_number, "user": user}

    print("\nUser not found, account creation process terminated!")

def list_accounts(accounts):
    for account in accounts:
        line = f"""\
            Agency:\t{account['agency']}
            Account No.:\t\t{account['account_number']}
            Holder:\t{account['user']['name']}
        """
        print("=" * 100)
        print(textwrap.dedent(line))

def main():
    WITHDRAWAL_LIMIT = 3
    AGENCY = "0001"

    balance = 0
    limit = 500
    statement = ""
    number_of_withdrawals = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            amount = float(input("Enter the deposit amount: "))

            balance, statement = deposit(balance, amount, statement)

        elif option == "w":
            amount = float(input("Enter the withdrawal amount: "))

            balance, statement = withdraw(
                balance=balance,
                amount=amount,
                statement=statement,
                limit=limit,
                number_of_withdrawals=number_of_withdrawals,
                withdrawal_limit=WITHDRAWAL_LIMIT,
            )

        elif option == "s":
            display_statement(balance, statement=statement)

        elif option == "nu":
            create_user(users)

        elif option == "na":
            account_number = len(accounts) + 1
            account = create_account(AGENCY, account_number, users)

            if account:
                accounts.append(account)

        elif option == "la":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("Invalid operation, please select the desired operation again.")

main()

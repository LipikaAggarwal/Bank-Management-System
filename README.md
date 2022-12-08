# Bank-Management-System 
#### A bank management system written in Python  with GUI made using Tkinter and the database using mysql.

This program when started shows the users an initial screen having two options for **admins** and **customers**.

**Customer window**: This window gives two options either to Register (to be able to use the banking services) or to Login if already registered.

**Registration Window**: The registration window prompts the user to enter their name, desired PIN and initial deposit amount in rupees.

Care is taken in the program to handle invalid entries like if the user leaves entry fields blank or enters alphabetical characters in places meant for numeric characters. It shows an error box.

Also the PIN is masked with ‘*’ symbols for security purposes. If all the inputs are valid then the user is registered and a dialog box tells the user their account number of 11 digits which they should note down.

**Login Window**: This window asks the user for their name, account number and PIN.

The PIN is masked and if the user enters invalid information all the entry fields are cleared and they are notified for the same by an error box.

If all goes well then they are taken to the services screen.

**Services screen**: After login the user is greeted on the services screen. There are three kinds of services available to the users:

* **Deposit:** to deposit the specified amount into their account.

* **Withdraw**: to withdraw the specified amount from their account.


     If the user does not have sufficient balance to withdraw they are notified for the same in a dialog box.

* **Check balance**: to check the current available balance.

**Admin window**: This window gives an option of customer s details

**Customer details**:It allows admin to check all the details of the user with a <mark> back button </mark> takes back to the admin window.

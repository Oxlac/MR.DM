=====
Usage
=====

MR.Dm is primarily divided into 4 screens that are responsible for each step in the process of
starting a bot session. The screens are:
1. Login Screen
2. Account Selection Screen
3. Message Creation Screen
4. Message Sending Progress Screen

Login Screen
------------
The login screen is the first screen that is displayed when the program is run. If this is the first time the program is 
running then there will be no accounts visible on the login screen.


.. image:: /images/login-screen.png
    :align: center
    :alt: Login Screen

You can add an account by clicking the "Add Account" button. This will open a dialog box that will ask you to enter the
username and password of the account you wish to add. Once you have entered the username and password, click the "Add"
button to add the account to the list of accounts. You can add as many accounts as you want.

.. image:: /images/new-account-popup.png
    :align: center
    :alt: Add Account Dialog

.. note::
    The entered username must be the actual instagram username and not an email id or a phone number. MR.DM login
    functionality does not support email ids or phone numbers yet.

Account Import/Selection Screen
-------------------------------

Once you have added an account. MR.DM will automatically login to the account and display the import accounts screen.

In this screen you can create lists of accounts that you want to target with your message. There are numerous options to import
accounts. You can import accounts from:
1. Your followers
2. Your following
3. Accounts that have posted on a particular hashtag (Coming Soon)
4. Accounts that have interacted(liekd or commented) with a post under a particular hashtag (Coming Soon)
5. Manually enter a list of accounts
6. From a previously exported csv file of accounts

.. image:: /images/import-accounts.png
    :align: center
    :alt: Import Accounts Screen

To view the progress of importing accounts you can check the top right of the screen for the progress indicator

.. image:: /images/import-progress.png
    :align: center
    :alt: Import Accounts Progress

You can modify this list of accouns by selecting any account or a group of accounts and clicking the "Remove Selected"

.. image:: /images/modify-accounts.png
    :align: center
    :alt: Remove Accounts

You can also export the list of accounts to a csv file by clicking the "Export Accounts" button. This will allow you to
save the list of accounts to a csv file. You can then import this csv file later to add the accounts to the list of accounts.

.. image:: /images/export-accounts.png
    :align: center
    :alt: Export Accounts

Once you have added the accounts you want to target, click the "Next" button to move to the next screen.

Message Creation Screen
-----------------------

In this screen you can create the message that you want to send to the accounts that you have selected in the previous screen.

.. image:: /images/message-screen.png
    :align: center
    :alt: Message Creation Screen

You can create a message by entering the text in the text box. Currently the supported mesage types are:
1. Text Message
2. Link
3. A post Link
4. Photos and Videos (Coming Soon)

There is a limit of 3 messages that you can send to each account at a time. This is to prevent your account from getting
blocked by instagram and also to mitigate spamming.

Once you have created the message, click the "Next" button to move to the next screen.

Message Sending Progress Screen
-------------------------------

In this screen you can see the progress of the message sending process. You can see the current account that is being
targted and the accounts that have completed and which are remaining.

.. image:: /images/message-progress.png
    :align: center
    :alt: Message Sending Progress Screen

A chrome window will open and you will be able to see the message being sent to the accounts.

.. warning::
    Do not close the chrome window or the MR.DM window while the message sending process is going on. This will cause
    the message sending process to stop and you will have to start the process again.
This script demonstrates how to send and receive text messages programmatically via email.

## Inspiration

I can imagine many future projects that have a text messaging component.  To facilitate development of these projects, I created the TextBot class.  The `example.py` script uses the TextBot class to demonstrate basic texting functionality.

## Setup

The steps to setup a text bot are as follows:
1.  Create conda environment with `conda env create -f environment.yml`
2.  Create a gmail account
3.  Allow smtp and imap less secure app access by clicking the slider [here](https://www.google.com/settings/security/lesssecureapps)
4.  Create text bot using the TextBot class 

## Notes

To act on text message replies, it is up to the developer to create an appropriate listener.  I did not try to create a "catch all" listener as the appropriate listener behavior will vary by use case.  An example of a basic listener is included in `example.py`.

The TextBot class is set up to communicate with phone numbers of the following carriers:  AT&T, Sprint, T-Mobile, and Verizon.  In the U.S. these carriers cover the vast majority of phone numbers.  If additional carriers are needed, the TextBot class can simply be updated.

The TextBot class is agnostic of carrier when sending messages.  For a given phone number the TextBot class attempts to send the message assuming it is from each of the known carriers.  This results in "Address not found" emails being sent to the inbox for each erroneous carrier.  While seemingly inelegant, this is not an issue if the email address used is a burner.

## Resources

[This page](https://20somethingfinance.com/how-to-send-text-messages-sms-via-email-for-free) contains many of the per carrier "endpoints" for sending text messages via email.
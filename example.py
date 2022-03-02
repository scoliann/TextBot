

# Do imports
import time


# Do local imports
from TextBot import TextBot
from config import (
    s_email,
    s_password,
    s_phone_number_test,
)


def main():

    # Initialize textbot
    o_tb = TextBot(s_email, s_password)

    # Example #0:  Send a text message
    print('\n\nSending text message...')
    o_tb.send_sms(s_phone_number_test, 'This is a text message!')

    # Example #1:  Send a text message with photo
    print('\n\nSending test message with photo...')
    o_tb.send_mms(s_phone_number_test, 'This is a text message with a puppy photo!', 'images/puppy.jpg')

    # Example #2  Listen for reply messages and take basic action
    print('\n\nListening for text replies...')
    for _ in range(3):

        # Get unseen replies
        ld_emails = o_tb.get_emails(b_mark_seen=True)

        # Take a basic action
        for d_emails in ld_emails:
            s_email_id = d_emails['s_email_id']
            s_phone_number_from = d_emails['s_email_from'].split('@')[0]
            print(f'\tReceived text message {s_email_id} from: {s_phone_number_from}')

        # Wait a certain duration of time
        time.sleep(5)


if __name__ == '__main__':
    main()
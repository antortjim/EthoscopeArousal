__author__ = 'Cody Giles'
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "2.0"
__maintainer__ = "antonio.ortega@kuleuven.be"
__status__ = "Production"

import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class EmailWriter:
    """
    Send email messages from a specified address to another address
    using some predefined template
    """

    _subject_t = "IPs For RaspberryPi on %s"
    _message_t = "Hi Natalie. I am testing my package.\n Please confirm you received this message.\nYour %s ip is %s"

    def __init__(self, from_user='RPi.PAVE@kuleuven.be', to_user=['natalie.kaempf@kuleuven.vib.be']):
        self._from_user = from_user
        self._to_user = to_user
        self._smtpserver = smtplib.SMTP('smtp.kuleuven.be', 25) # Server to use.
    
    @property
    def smtpserver(self):
        return self._smtpserver     

    @staticmethod
    def connect_type(word_list):
        """
        This function takes a list of words
        Depeding which key word, returns the corresponding
        internet connection type as a string. ie) 'ethernet'.
        """
        if 'wlan0' in word_list or 'wlan1' in word_list:
            con_type = 'wifi'
        elif 'eth0' in word_list:
            con_type = 'ethernet'
        else:
            con_type = 'current'

        return con_type

    @staticmethod
    def get_message():
        """
        Generate a string reporting the ip address
        and type of connection of the RPi
        """

        arg='ip route list'  # Linux command to retrieve ip addresses.
        # Runs 'arg' in a 'hidden terminal'.
        p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
        data = p.communicate()  # Get data from 'p terminal'.

        # Split IP text block into three, and divide the two containing IPs into words.
        ip_lines = data[0].splitlines()
        split_line = ip_lines[1].split()

        # con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
        iptype = connect_type(split_line)

        """Because the text 'src' is always followed by an ip address,
        we can use the 'index' function to find 'src' and add one to
        get the index position of our ip.
        """
        ipaddr = split_line[split_line.index('src')+1]

        # Complete the message template with the obtained ip type and address
        message = self._message_t % iptype, ipaddr
        logger.info(message)
        return message
    
    def write(self):
        message = get_message()

        # Creates the text, subject, 'from', and 'to' of the message.
        msg = MIMEText(message)
        
        # Get current time/date
        today = datetime.date.today()
        
        # Complete the subject template with the obtained date and time
        msg['Subject'] = self._subject_t % today.strftime('%b %d %Y')

        # Provide a from and to address
        msg['From'] = self._from_user
        msg['To'] = ", ".join(self._to_user)

        return msg
       
    
    def send(self):
        # TODO Is this ehlo() line needed?
        # Say 'hello' to the server
        self.smtpserver.ehlo()
        
        # Write the message
        msg = self.write()
        # Send the message
        self.smtpserver.sendmail(self._from_user, to, msg.as_string())
    
    def close(self)
        # Close the smtp server.
        self.smtpserver.quit()

if __name__ == "__main__":
    writer = EmailWriter(from_user='RPi.PAVE@kuleuven.be', to_user=['natalie.kaempf@kuleuven.vib.be'])
    writer.send()
    writer.close()

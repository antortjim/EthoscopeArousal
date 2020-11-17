import logging

logging.getLogger("light").setLevel(logging.INFO)


from light import LightInteractor, get_timestamp
from email_server import EmailWriter

def main():
    schedule = {
            "2021:03:06-20:40:00": (5, 1, 0),
            get_timestamp(5): (5, 1, 0),
            get_timestamp(10): (3, 1, 0),
            get_timestamp(15): (2, 1, 0),
            get_timestamp(20): (1, 1, 0),
    }
    pins = [17, 27, 14]
    interactor = LightInteractor(schedule, pins=pins)
    email_writer = EmailWriter(from_user="RPi.PAVE@kuleuven.be", to_user="natalie.kaempf@kuleuven.be")
    
    email_writer.start()
    interactor.start()

if __name__ == "__main__":
    main()

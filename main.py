from light import LightInteractor
from email_server import EmailWriter

schedule = {
        "2021:03:06-20:40:00": (5, 1, 0)
}
pins = [17, 27, 14]
interactor = LightInteractor(schedule, pins=pins)
email_writer = EmailWriter(from_user="RPi.PAVE@kuleuven.be", to_user="natalie.kaempf@kuleuven.be")


interactor.run()
email_writer.run()

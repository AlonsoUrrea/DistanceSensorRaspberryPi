from .models import *
from sqlalchemy.orm import sessionmaker, session

import uuid
from time import sleep
from statistics import mean
from datetime import datetime

convert_m_a_cm = lambda m: m * 100

def get_session() -> session.Session:
    session = sessionmaker()
    session.configure(bind=engine)
    
    return session()
#end def

def get_raspberry(session: session.Session) -> RaspBerryPi:
    this_machine_mac_address = uuid.getnode()
    raspQ = session.query(RaspBerryPi).filter_by(mac_address=this_machine_mac_address)
    if raspQ.count() == 0:
        rasp = RaspBerryPi(mac_address=this_machine_mac_address)
        session.add(rasp)
        session.commit()

        return rasp
    else:
        return raspQ.first()
    #end if
#end def

def get_sensor(session: session.Session, trigger: int, echo: int) -> Sensor:
    rasp = get_raspberry(session)
    sensorQ = session.query(Sensor).filter_by(
        id_raspberry=rasp.id_raspberry,
        echo_gpio=echo,
        trigger_gpio=trigger
    )
    if sensorQ.count() == 0:
        sensor = Sensor(
            id_raspberry=rasp.id_raspberry,
            echo_gpio=echo,
            trigger_gpio=trigger
        )
        session.add(sensor)
        session.commit()

        return sensor
    else:
        return sensorQ.first()
    #end if
#end def

def get_sensor_by_id(session: session.Session, id) -> Sensor:
    sensorQ = session.query(Sensor).filter_by(
        id_sensor=id
    )
    if sensorQ.count() == 0:
        return None
    else:
        return sensorQ.first()
    #end if
#end def

def get_tanque(session: session.Session, sensor: Sensor) -> Tanque:
    tanqueQ = session.query(Tanque).filter_by(id_sensor=sensor.id_sensor)
    if tanqueQ.count() == 0:
        tanque = Tanque(id_sensor=sensor.id_sensor)
        session.add(tanque)
        session.commit()

        return tanque
    else:
        return tanqueQ.first()
    #end if
#end def

def init_tanque_distancia_cm(session: session.Session, tanque:Tanque):
    sensor = get_sensor_by_id(session, tanque.id_sensor)
    mediciones = []

    sensor.initDistanceSensor()
    for _ in range(10):
        mediciones.append(sensor.measure())
        sleep(1)
    #end for
    tanque.distancia_cm = convert_m_a_cm(mean(mediciones))
    session.commit()


def get_medicion(session: session.Session, tanque: Tanque) -> Medicion:
    sensor = get_sensor_by_id(session, tanque.id_sensor)
    mediciones = []

    sensor.initDistanceSensor()
    for _ in range(10):
        mediciones.append(sensor.measure())
        sleep(1)
    #end for
    medicion = Medicion()
    medicion.hora_fecha = datetime.now()
    medicion.id_sensor = sensor.id_sensor
    medicion.dato_natural = mean(mediciones)
    medicion.porcentaje = tanque.calc_porcentaje(convert_m_a_cm(medicion.dato_natural))
    session.add(medicion)
    session.commit()

    return medicion
#end def

import sqlalchemy
from sqlalchemy.orm import declarative_base
from settings import CONN_STRING

from gpiozero import DistanceSensor # sensor data

engine = sqlalchemy.create_engine(CONN_STRING)
Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id_cliente = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    nombre_completo = sqlalchemy.Column(sqlalchemy.String(100))

class RaspBerryPi(Base):
    __tablename__ = 'raspberries'
    id_raspberry = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    mac_address = sqlalchemy.Column(sqlalchemy.BigInteger)

class Sensor(Base):
    __tablename__ = 'sensores'
    id_sensor = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_raspberry  = sqlalchemy.Column(sqlalchemy.ForeignKey('raspberries.id_raspberry'))
    echo_gpio = sqlalchemy.Column(sqlalchemy.Integer)
    trigger_gpio = sqlalchemy.Column(sqlalchemy.Integer)
    __sensor__ = None

    class DistanceSensorNotInitialized(Exception):
        pass

    def initDistanceSensor(self, sensor_distance=4):
        if not self.sensorIsSet():
            from gpiozero.pins.native import NativeFactory
            DistanceSensor.pin_factory = NativeFactory()
            self.__sensor__ = DistanceSensor(echo=self.echo_gpio, trigger=self.trigger_gpio, max_distance=sensor_distance)
    def sensorIsSet(self):
        return self.__sensor__ is not None
    def measure(self):
        if self.sensorIsSet():
            return self.__sensor__.distance
        raise Sensor.DistanceSensorNotInitialized("Distance Sensor not initialized. Call Sensor().initDistanceSensor()")
    #end defs
#end class


class Tanque(Base):
    __tablename__ = 'tanques'
    id_tanque = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    distancia_cm = sqlalchemy.Column(sqlalchemy.Float)
    nombre = sqlalchemy.Column(sqlalchemy.String(64))
    id_sensor  = sqlalchemy.Column(sqlalchemy.ForeignKey('sensores.id_sensor'))
    id_cliente  = sqlalchemy.Column(sqlalchemy.ForeignKey('clientes.id_cliente'))
    
    def calc_porcentaje(self, distancia):
        if self.distancia_cm is not None:
            return (self.distancia_cm - distancia) / self.distancia_cm
        #end if
    #end def

class Medicion(Base):
    __tablename__ = 'mediciones'
    id_mediciones = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    dato_natural = sqlalchemy.Column(sqlalchemy.Float)
    porcentaje  = sqlalchemy.Column(sqlalchemy.Float)
    id_sensor  = sqlalchemy.Column(sqlalchemy.ForeignKey('sensores.id_sensor'))
    hora_fecha = sqlalchemy.Column(sqlalchemy.DateTime)
#end classes

if __name__ == '__main__':
    Base.metadata.create_all(engine)
#end if
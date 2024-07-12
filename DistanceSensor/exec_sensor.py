import getopt, sys

import argparse

from controller import *

def medir_tanque(trigger: int, echo: int):
    session = get_session()

    sensor = get_sensor(session, trigger, echo)
    tanque = get_tanque(session, sensor)
    init_tanque_distancia_cm(session, tanque)
#end def

def hacer_medicion(trigger: int, echo: int):
    session = get_session()
    sensor = get_sensor(session, trigger, echo)
    tanque = get_tanque(session, sensor)
    get_medicion(session, tanque)
#end def

def help():
    return """
Uso:
    python[3] exec_sensor.py <comando> [opciones]
    
Comandos:
    nivel                   | Medir el nivel de agua que detecta el sensor
    distancia               | Medir la distancia total vacia del recipiente
Opciones:
    -e, --echo <int>        | # GPIO de la Raspberry Pi conectado al pin echo del sensor (default 23)
    -t, --trigger <int>     | # GPIO de la Raspberry Pi conectado al pin trigger del sensor (default 24)
    -h, --help              | Esta guia de ayuda
    """
#end def

def arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="exec_sensor",
        description="Ejectutar medicion con sensor de distancia",
        usage=help()
    )
    parser.add_argument("comando", default="nivel")
    parser.add_argument("-e", "--echo", default=23, type=int)
    parser.add_argument("-t", "--trigger", default=24, type=int)

    return parser
#end def
       

def main():
    parser = arg_parser()
    args = parser.parse_args()
    if args.comando == "nivel":
        hacer_medicion(args.trigger, args.echo)
    elif args.comando == "distancia":
        medir_tanque(args.trigger, args.echo)
    #end if
#end main


if __name__ == '__main__':
    main()
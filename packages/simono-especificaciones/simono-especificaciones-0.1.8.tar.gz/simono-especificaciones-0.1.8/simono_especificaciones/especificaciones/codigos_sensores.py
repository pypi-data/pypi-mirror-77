FIELDS_SENSOR = ['id_sensor', 'guid_sensor', 'id_modulo', 'fe_registrado']

path = "main/img/sensores/"

# UNIDADES
PRECIPITACIONES  = {"milimetros": "mm",
                    "centimetros": "cm", }

VIENTO_VEL       = {"kmxhs": "Km./Hs.",
                    "None": ""}

VIENTO_DIR       = {"None": ""}

PRESION          = {"millibar": "mbar",
                    "hectopascal": "hPa"}


CODES_SENSORES = {
    #    Aclaración para módulos:
    #        No cambiar los valores del significado de las claves, 
    #        lo que si se puede es cambiar los valores de las claves.

    # Atencion! Actualizar este valor cada vez que se agregue un nuevo sensor
    # Cantidad de Sensores = 29 
    # Ver archivo indices sensores

    #####################################
    #      SENSORES DE TEMPERATURA      #
    #####################################
    "DHT11": {
        "clase": 1,
        "descripcion": "<p>El DHT11 es un sensor de temperatura y humedad digital de bajo costo. Utiliza un sensor capacitivo de humedad y un termistor para medir el aire circundante, y muestra los datos mediante una señal digital en el pin de datos (no hay pines de entrada analógica). Es bastante simple de usar, pero requiere sincronización cuidadosa para tomar datos. El único inconveniente de este sensor es que sólo se puede obtener nuevos datos una vez cada 2 segundos, así que las lecturas que se pueden realizar serán mínimo cada 2 segundos. En comparación con el DHT22, este sensor es menos preciso, menos exacto y funciona en un rango más pequeño de temperatura / humedad, pero su empaque es más pequeño y menos caro.</p><p>Características</p><ul><li>Alimentación: 3Vdc ≤ Vcc ≤ 5Vdc</li><li>Rango de medición de temperatura: 0 a 50 °C</li><li>Precisión de medición de temperatura: ±2.0 °C .</li><li>Resolución Temperatura: 0.1°C</li><li>Rango de medición de humedad: 20% a 90% RH.</li><li>Precisión de medición de humedad: 4% RH.</li><li>Resolución Humedad: 1% RH</li><li>Tiempo de sensado: 1 seg.</li></ul>",
        "fields": FIELDS_SENSOR + ['temperatura', 'humedad'],
        "modulos": {1: "TEMPERATURA", 2: "HUMEDAD"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": path +'dht11.jpg',
        "de_unidad": {1: "º", 2: "%"},
        "acumulable": {1: False, 2: False},
    },

    "DS18B20": {
        "clase": 2,
        "descripcion": "<p>El sensor DS18B20 permite medir temperaturas de hasta 125ºC de forma fácil y además está sellado en un envoltorio estanco que permite sumergirlo en un líquido o pretegerlo de la intempérie. Dado que es un sensor digital, la señal leida no se degrada debido a la distancia del cableado. Puede funcionar en modo 1-Wire con una precisión de ±0.5°C con una resolución de 12 bits. También pueden utilizarse varios sensores sobre el mismo pin ya que internamente viene programado con un ID único de 64 bits para diferenciarlos. El rango de funcionamiento es de 3 a 5V por lo que se puede utilizar en practicamente cualquier sistema de que use microcontroladores.</p><p>Características del cable</p><ul><li>Tubo de acero inoxidable de 6mm de diámetro por 30mm de largo</li><li>Largo: 91cm</li><li>Diámetro: 4mm</li><li>Contiene un sensor de temperatura DS18B20</li></ul><p>Conexión:</p><p>En función de la producción, los cables del sensor pueden variar pero seguirán según estas especificaciones:</p><ul><li>Si tienes 4 cables: Rojo es Vcc (positivo), Negro es GND (negativo) y Blanco es el cable de datos. La malla es GND.</li><li>Si tienes 3 cables: Rojo es Vcc (positivo), Azul/Negro es GND (negativo) y Amarillo/Blanco es el cable de datos.</li></ul><p>Características del sensor DS18B20</p><ul><li>Rango de temperatura: -55 a 125°C</li><li>Resolución: de 9 a 12 bits (configurable)</li><li>Interfaz 1-Wire (Puede funcionar con un solo pin)</li><li>Identificador interno único de 64 bits</li><li>Multiples sensores puede compartir el mismo pin</li><li>Precisión: ±0.5°C (de -10°C a +85°C)</li><li>Tiempo de captura inferior a 750ms</li><li>Alimentación: 3.0V a 5.5V</li></ul>",
        "fields": FIELDS_SENSOR + ['temperatura'],
        "modulos": {1: "TEMPERATURA"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": path +'DS18B20.png',
        "de_unidad": {1: "º"},
        "acumulable": {1: False},
    },

    "HDC1080": {
        "clase": 13,
        "descripcion": "<p>El HDC1080 de Imagen de Sensor de humedad digital HDC1080 de Texas Instruments es un sensor de humedad digital con sensor de temperatura integrado que proporciona una precisión excelente de medición con un consumo de energía muy bajo. El HDC1080 opera en un amplio rango de oferta y es una alternativa de bajo costo, de bajo consumo a soluciones competitivas en una amplia gama de aplicaciones comunes. Los sensores de humedad y temperatura se calibran en fábrica.</p><p>Características</p><ul><li>Precisión de humedad relativa ±2% (típica)</li><li>Temperatura de precisión ±0. 2 ° C (típico)</li><li>Excelente estabilidad en alta humedad</li><li>Resolución de medidas de 14 bits</li><li>Corriente en modo de reposo de 100 nA</li><li>Voltaje de alimentación: 2.7 V a 5.5 V</li><li>Corriente de alimentación promedio: <p>- Medición de RH de 11 bits, de 710 nA a 1 sps</p></li> - Medición de temperatura y RH de 11 bits, de 1.3 µA a 1 sps</li><li>Huella de dispositivo pequeña de 3 x 3 mm</li><li>Interfaz I2C</li></ul>",
        "fields": FIELDS_SENSOR + ['temperatura'],
        "modulos": {1: "TEMPERATURA", 2: "HUMEDAD"},
        "is_valid": True,
        "admite_monitoreo": False,
        "img": path +'HDC1080.jpg',
        "de_unidad": {1: "º", 2: "%"},
        "acumulable": {1: False, 2: False},
    },
    #####################################
    #        SENSORES MAGNETICOS        #
    #####################################
    "MAGNETICO": {
        "clase": 5,
        "descripcion": "Modulo de sensor magnético (apertura de puertas).",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "MAGNETICO"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": path + 'magenetico.jpg',
        "de_unidad": {1: ""},
        "acumulable": {1: False},
    },

    # Anteriormente en v0.0.20
    # PESSL       -> clase: 6.
    # PLUVIOMETRO -> clase:15.
    "PLUVIOMETRO": {
        "clase": 6,
        "descripcion": "<p>Descripción:</p><p>Los pluviómetros sirven para calcular la cantidad de lluvia que cae en una zona concreta durante un periodo de tiempo determinado.</p><p>El modelo base correesponde a uno de los sensores de la estación meteorológica WH1081, WS1081, TX81R</p>",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "GENERICO"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": path+'WS1081.jpg',
        "de_unidad": {1:"mm",},
        "acumulable": {1: True},
    },

    "PESSL": {
        "clase": 15,
        "descripcion": "Pluviómetro Pessl",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "GENERICO"},
        "is_valid": True,
        "admite_monitoreo": False,
        "img": path+'pessl.jpg',
        "de_unidad": {1: 'mm', },
        "acumulable": {1: True},
    },

    #####################################
    #              ACTUADORES           #
    #####################################
    "RELE": {
        "clase": 8,
        "descripcion": "<p>Los relé, permiten controlar cargas de alto voltaje con una señal pequeña. Esto nos permitirá controlar componentes de alto voltaje o alto amperaje, como bombillas o bombas de agua, etc.</p><p>El modulo posee 1 Relay de alta calidad, fabricado por Songle, con capacidad de manejar cargas de hasta 250V/10A. El módulo relay posee un led indicador de alimentación (rojo) y un led indicador de activación (vender). Este modulo a diferencia de los módulos relay de 2 o más canales no posee optoacopladores, en su lugar la activación del relay es mediante un transistor.  Este modulo Relay activa la salida normalmente abierta (NO: Normally Open) al recibir un '0' lógico (0 Voltios) y desactiva la salida con un '1' lógico (5 voltios).</p><p>Entre las cargas que se pueden manejar tenemos: bombillas de luz, luminarias, motores AC (220V), motores DC, solenoides, electroválvulas, calentadores de agua y una gran variedad de actuadores más. Se recomienda realizar y verificar las conexiones antes de alimentar el circuito, también es una buena practica proteger el circuito dentro de un case.</p>",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "GENERICO"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": path+'rele.jpg',
        "de_unidad": {1:"",},
        "acumulable": {1: False},
    },

    #####################################
    #               RASPBERRY           #
    #####################################
    "RASPBERRY": {
        "clase": 21,
        "descripcion": "<p>Sensores disponibles para capturar diferentes parametros de una Raspberry</p>",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "TEMPERATURA", 2:"PROCESADOR", 3:"USO DE DISCO"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img":None,
        "de_unidad": {1:"ºC",2:"%",3:"%"},
        "acumulable": {1: False, 2: False, 3: False},
    },
    #####################################
    #            OTROS SENSORES         #
    #####################################
    "FOTORESISTOR": {
        "clase": 3,
        "descripcion": "<p>Un LDR es un dispositivo cuya resistencia varía de acuerdo con la cantidad de luz que reciba. Son muy útiles para proyectos de control de iluminación, seguidores solares, interruptores crepusculares, etc.</p><p>Este módulo posee 2 salidas, una analógica que debes conectar a una entrada analógica y así utilizar el conversor ADC. La salida digital posee solo 2 estados: activo/apagado, el cambio de un estado a otro depende del umbral que se fije con el potenciómetro del módulo. La salida digital puede utilizarse para controlar un relay y asi realizar una acción dependiente de la intensidad de luz.</p><p>Especificaciones Técnicas</p><ul><li>Voltaje de Operación: 5V DC</li><li>Conexión de 4 cables: VCC, GND, DO, AO</li><li>Salida analógica y digital(comparador)</li><li>Opamp en modo comparador: LM393</li><li>Potenciometro para ajuste de comparador</li><li>Led rojo de encendido y verde de salida digital</li></ul>",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "GENERICO"},
        "is_valid": True,
        "admite_monitoreo": False,
        "img": path+'modulo-ldr.png',
        "de_unidad": {1:"",},
        "acumulable": {1: False},
    },

    # DESACTIVADO: redefinir módulo
    # "MHRD": {
    #     "clase": 4,
    #     "descripcion": "<p>Modulo de sensor de precipitacion (lluvia) MH-RD analógico.</p><p>Los sensores de lluvia se utilizan en la detección de agua más allá de lo que un sensor de humedad puede detectar.</p><p>El sensor de lluvia detecta el agua que completa los circuitos en las pistas impresos de sus tarjetas de sensores. La tarjeta del sensor actúa como una resistencia variable que cambiará de 100kohm cuando está mojado a 2Mohm cuando está seco. En resumen, cuanto más húmedo sea el tablero, mayor será la corriente que se llevará a cabo.</p>",
    #     "fields": FIELDS_SENSOR + ['do', 'canal_0', 'canal_1', 'canal_2', 'canal_3'],
    #     "modulos": {1: "GENERICO"},
    #     "is_valid": True,
    #     "admite_monitoreo": False,
    #     "img": path+'MHRD.jpg',
    #     "de_unidad": {1:"",},
    # },

    "HCSR501": {
        "clase": 7,
        "descripcion": "<p>Modulo de sensor de movimiento, PIR (HC-SR501).</p><p>El módulo HC-SR501 tiene 3 pines de conexión +5v, OUT (3,3v) y GND, y dos resistencias variables de calibración (Ch1 y RL2).</p><ul><li>Ch1: Con esta resistencia podemos establecer el tiempo que se va a mantener activa la salida del sensor. Una de las principales limitaciones de este módulo es que el tiempo mínimo que se puede establecer es de más o menos 3s. Si cambiamos la resistencia por otra de 100K, podemos bajar el tiempo mínimo a más o menos 0,5 s.</li><li>RL2: Esta resistencia variable nos permite establecer la distancia de detección  que puede variar entre 3-7m.</li><li>La posibilidad de mantener activa la salida del módulo durante un tiempo determinado nos permite poder usarlo directamente para prácticamente cualquier aplicación sin necesidad de usar un microcontrolador.</li></ul><p>Características</p><ul><li>Sensor piroeléctrico (Pasivo) infrarrojo (También llamado PIR)</li><li>El módulo incluye el sensor, lente, controlador PIR BISS0001, regulador y todos los componentes de apoyo para una fácil utilización</li><li>Rango de detección: 3 m a 7 m, ajustable mediante trimmer (Sx)</li><li>Lente fresnel de 19 zonas, ángulo < 100º</li><li>Salida activa alta a 3.3 V</li><li>Tiempo en estado activo de la salida configurable mediante trimmer (Tx)</li><li>Redisparo configurable mediante jumper de soldadura</li><li>Consumo de corriente en reposo: < 50 μA</li></ul>",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "GENERICO"},
        "is_valid": True,
        "admite_monitoreo": False,
        "img": path+'HCSR501.jpg',
        "de_unidad": {1:"",},
        "acumulable": {1: False},
    },

    "TSL2561": {
        "clase": 9,
        "descripcion": "<p>El TSL2561 es un sensor de luz muy preciso que mide en un rango de 0.1 a 40000 lux. A diferencia de otros sensores similares, tiene dos diodos que le permite medir tanto la luz ambiente en el espectro visible como la luz infrarroja. La placa está diseñada para funcionar tanto a 3.3 como a 5V así que lo puedes utilizar con tu microcontrolador favorito sin necesidad de componentes adicionales. Funciona mediante el bus I2C y por lo tanto es muy sencillo de hacer funcionar y puedes utilizarlo junto a otros sensores en un mismo bus.</p><p>Características:</p><ul><li>Rango muy similar el ojo humano</li><li>Medición precisa en diversos ambientes lumínicos</li><li>Temperatura de funcionamiento: -30 a 80 *C</li><li>Rango dinámico (Lux): 0.1 a 40,000 Lux</li><li>Alimentación: 2.7 - 3.6V</li><li>Interfaz: I2C (Dirección: 0x39, 0x29 o 0x49, seleccionable)</li></ul>",
        "fields": FIELDS_SENSOR + ['total', 'visible'],
        "modulos": {1: "TOTAL", 2: "VISIBLE"},
        "is_valid": True,
        "admite_monitoreo": False,
        "img": path+'TSL2561.jpg',
        "de_unidad": {1:"", 2:""},
        "acumulable": {1: False, 2: False},
    },

    # DESACTIVADO: redefinir módulo
    # "MQ2": {
    #     "clase": 10,
    #     "descripcion": "<p>Este es un sensor muy sencillo de usar, ideal para medir concentraciones de gas natural en el aire. Puede detectar concentraciones desde 300 hasta 10000 ppm.El módulo posee una salida analógica que proviene del divisor de voltaje que forma el sensor y una resistencia de carga. También tiene una salida digital que se calibra con un potenciómetro, esta salida tiene un Led indicador. La resistencia del sensor cambia de acuerdo a la concentración del gas en el aire. El MQ-2 es sensible a LPG, i-butano, propano, metano, alcohol, hidrogeno y humo.</p><p>Especificaciones Técnicas</p><ul><li>Voltaje de Operación: 5V DC</li><li>Respuesta rápida y alta sensibilidad</li><li>Rango de detección: 300 a 10000 ppm</li><li>Gas característico: 1000ppm, Isobutano</li><li>Resistencia de sensado: 1KΩ 50ppm Tolueno a 20KΩ in</li><li>Tiempo de Respuesta: ≤ 10s</li><li>Tiempo de recuperación: ≤ 30s</li><li>Temperatura de trabajo: -20 ℃ ~ +55 ℃</li><li>Humedad: ≤ 95% RH</li><li>Contenido de oxigeno ambiental: 21%</li><li>Consume menos de 150mA a 5V.</li></ul>",
    #     "fields": FIELDS_SENSOR + ['do', 'Co', 'Humo'],
    #     "modulos": {1: "GENERICO", 2: "RO"},
    #     "is_valid": True,
    #     "admite_monitoreo": False,
    #     "img": path+'mq-2.jpg',
    #     "de_unidad": {1:"", 2:""},
    # },

    "MQTT": {
        "clase": 11,
        "descripcion": "Sensor especifico del Tipo MQTT",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "GENERICO MQTT"},
        "is_valid": False,
        "admite_monitoreo": False,
        "img": '',
        "de_unidad": {1:"",},
        "acumulable": {1: False},
    },

    "ANEMOMETRO": {
        "clase": 12,
        "descripcion": "Anemometro mide velocidad del viento. El equipo base corresponde a la estación meteorológica WH1081, WS1081, TX81W yTX81D",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "VELOCIDAD"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": path+'Anemometer.jpg',
        "de_unidad": {1: VIENTO_VEL['kmxhs']},
        "acumulable": {1: False},
    }, 
            
    "WINDIR": {
        "clase": 28,
        "descripcion": "Mide la direccion del viento",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "DIRECCION"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": path + 'Anemometer.jpg',
        "de_unidad": {1:""},
        "acumulable": {1: False},
    },
            
            
    "BMP280": {
        "clase": 14,
        "descripcion": "<p>Descripción:</p><p>El sensor de presión barométrica BMP280 diseñado especialmente para aplicaciones móviles. Sus pequeñas dimensiones y su bajo consumo de energía permite la implementación en distintos dispositivos. El sensor dispone de una excelente precisión relativa de ± 0,12 hPa, lo que equivale a ± diferencia 1 M en altitud. El coeficiente de temperatura muy bajo offset (TCO) de 1,5 Pa / K se traduce en una variación de temperatura de sólo 12,6 cm / K.<p>Nota: Debido a la alta sensibilidad de este sensor, evite tocarlo con los dedos.</p><p>Características:</p><ul><li>Voltaje de alimentación: 1.71-3.6V.</li><li>Corriente de trabajo 2.8uA.</li><li>Rango para la medida de la presión barométrica: 300hPa ~ 1100hPa</li><li>Precisión de la medida de la presión barométrica: ± 1hPa</li><li>Rango de Temperatura: - 40 ~ 85°C.</li><li>Precisión en la Temperatura: ± 1°C.</li><li>Interface: I2C y SPI</li></ul>",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "PRESION"},
        "is_valid": True,
        "admite_monitoreo": False,
        "img": path+'BMP280.jpg',
        "de_unidad": {1: "hPa", },
        "acumulable": {1: False},
    },

    "AS3935": {
        "clase": 16,
        "descripcion": "<p>El AS3935 de ams es un CI de sensor de rayos programable que detecta la presencia y aproximación de actividad eléctrica potencialmente peligrosa en las inmediaciones. Detecta actividad dentro de la nube, así como relámpagos de nube a tierra, lo que permite que a menudo se puedan evaluar los riesgos de tormentas que se aproximan.</p><p>El AS3935 detecta la actividad eléctrica mientras ésta se aproxima desde una distancia de hasta 40 km. Además, el AS3935 identifica y rechaza las señales de interferencia desde fuentes artificiales comunes, tales como iluminación fluorescente, motores, hornos de microondas e interruptores.</p><p>Sobre la base de investigaciones científicas, se puede calcular estadísticamente la distancia de la tormenta a partir de las señales medidas. Esta información permite al usuario ajustar los niveles de alerta adecuados para una aplicación específica. La seguridad personal se puede establecer a un nivel prudencial, mientras que la protección de equipos debe contemplar fiabilidad, intensidad de señal y duración de la batería.</p><p>El CI flexible ofrece la capacidad de configuración que permite el funcionamiento de la pieza tanto en interiores como en exteriores con solo cambiar la configuración de ganancia en un registro.</p><p>Características y beneficios</p><ul>        <li>El detector de rayos advierte de la actividad de tormentas eléctricas en un radio de 40 km.</li><li>Cálculo de distancia a la cabeza de la tormenta de hasta 1 km en 14 pasos</li><li>Detecta tanto relámpagos nube a tierra como dentro de la nube (nube a nube)</li><li>Niveles de detección programables permiten la configuración del umbral para controles óptimos</li><li>Algoritmo integrado de rechazo de elemento perturbador artificial</li><li>Interfaz SPI e I2C para lectura de control y de registro</li><li>Ajuste de antena para compensar variaciones de componentes externos</li><li>Rango de voltaje de alimentación de 2.4 V a 5.5 V</li><li>Modo de apagado, escucha y activo</li><li>Paquete: 16LD MLPQ (4 mm x 4 mm)</li></ul>",
        "fields": FIELDS_SENSOR + ['valor'],
        "modulos": {1: "GENERICO"},
        "is_valid": True,
        "admite_monitoreo": False,
        "img": path+'AS3935.jpg',
        "de_unidad": {1: "", },
        "acumulable": {1: False},
    },

    "FLUJO_PERSONAS": {
        "clase": 17,
        "descripcion": "Flujo de personas",
        "fields": FIELDS_SENSOR + ['entrada', 'salida'],
        "modulos": {1: "GENERICO"},
        "is_valid": False,
        "admite_monitoreo": False,
        "img": '',
        "de_unidad": {1: "", },
        "acumulable": {1: False},
    },

    "CAM": {
        "clase": 18,
        "descripcion": "Cámara web USB",
        "fields": FIELDS_SENSOR,
        "modulos": {1: "CAM"},
        "is_valid": False,
        "admite_monitoreo": False,
        "img": '',
        "de_unidad": {1: "", },
        "acumulable": {1: False},
    },

    "SC200": {
        "clase": 19,
        "descripcion": "Equipo inversor SC200 Eaton",
        "fields": FIELDS_SENSOR,
        "modulos": {1: "AC", 2: "BATERIA"},
        "is_valid": False,
        "admite_monitoreo": False,
        "img": path+'SC200.jpg',
        "de_unidad": {1: "V.",2: "V."},
        "acumulable": {1: False, 2: False},
    },

    "SNMPWEBSERVER": {
        "clase": 20,
        "descripcion": "Equipo Inversor SNMP Web Server",
        "fields": FIELDS_SENSOR,
        "modulos": {1: "AC", 2: "BATERIA"},
        "is_valid": False,
        "admite_monitoreo": False,
        "img": '',
        "de_unidad": {1: "V.",2: "V."},
        "acumulable": {1: False, 2: False},

    },

    "GENERICOS": {
        "clase": 22,
        "descripcion": "Sensor generico para admitir sensores diversos.",
        "fields": FIELDS_SENSOR,
        "modulos": { 1: "TEMPERATURA",      2: "HUMEDAD",               3: "PRESION",               4: "VELOCIDAD VIENTO", 
                     5: "DIRECCION VIENTO", 6: "PRECIPITACIONES (mm.)", 7: "PRECIPITACIONES (cm.)", 8: "PUNTO DE ROCIO",
                     9: 'NIVEL DE BATERIA', 10: "RAFAGA DE VIENTO",    11: "SEÑAL GPRS",           12: "RADIACION SOLAR",
                    13: "PANEL SOLAR", 999: "OTRO"},
        "is_valid": True,
        "admite_monitoreo": False,
        "img": '',
        "de_unidad": {1: "º", 2: "%", 3: PRESION["millibar"], 4: VIENTO_VEL['kmxhs'], 5: VIENTO_DIR["None"], 6: "mm.", 7: "cm.", 8: "ºC" , 9: "V.", 10: VIENTO_VEL['kmxhs'], 11:"ASU", 12:"w/m2", 13:"", 999: ""},
        "acumulable": {1: False, 2: False,3: False, 4: False, 5: False, 6: True, 7: True, 8: False, 9: False, 10: False, 11:False, 12:False, 13:False, 999: False},
    },

    "SCT013": {
        "clase": 23,
        "descripcion": "Sensor de medición de corriente",
        "fields": FIELDS_SENSOR,
        "modulos": {1: "TENSION", 2: "CORRIENTE"},
        "is_valid": False,
        "admite_monitoreo": False,
        "img": path+'sct013.jpg',
        "de_unidad": {1: "V.", 2: "A."},
        "acumulable": {1: False, 2: False},

    },

    "BME680": {
        "clase": 24,
        "descripcion": "<p>Descripción:</p><p>El sensor Bosch BME680 agrupa en un mismo encapsulado todas las variables ambientales de mayor interés: temperatura, humedad, presión atmosférica y compuestos orgánicos volátiles (VOC), lo que permite determinar la calidad del aire monitoreado. El breakout desarrollado y producido por OpenHacks permite hacer uso de su funcionalidad de manera muy simple, incluyendo un regulador de tensión y adaptadores de nivel, además de una separación entre pines de 0.1 que facilita su uso en protoboard.</p> <p>Características:</p><p><ul><li>Exactitud en humedad relativa: ±3%</li><li>Exactitud en temperatura: ±1 ºC</li><li>Exactitud en presión: ±1 hpa</li><li>Los sensores de temperatura, humedad, presión y VOC pueden activarse o desactivarse individualmente</li><li>Condiciones de operación: -40 a +85 ºC, 0 - 100% rH, 300 - 1100 hpa</li><li>Consumo a 1Hz de refresco: 2.1uA midiendo humedad y temperatura, 3.1uA midiendo presión y temperatura, 0.09 - 12mA midiendo p/h/t/voc, 0.15uA en modo sleep</li><li>Alimentación: 3 a 5 V, con regulador de voltaje y adaptadores de nivel en la placa breakout</li><li>Interfaz: I2C / SPI</li><li>Dimensiones: 20.32 x 20.32 mm, separación entre orificios: 12.7mm, diámetro orificios: 3.17mm</li></ul></p>",
        "fields": FIELDS_SENSOR,
        "modulos": {1: "TEMPERATURA", 2: "HUMEDAD", 3: "PRESION", 4: "CALIDAD AIRE", 5: "GAS"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": path + 'BME680BREAK.jpg',
        "de_unidad": {1: "º", 2: "%", 3: "hPa", 4: "%", 5: ""},
        "acumulable": {1: False, 2: False, 3: False, 4: False, 5: False},

    },

    "YL029": {
        "clase": 25,
        "descripcion": "<p>Descripción:</p><p>Este sensor puede medir la cantidad de humedad presente en el suelo que lo rodea empleando dos electrodos que pasan corriente a través del suelo, y lee la resistencia. Mayor presencia de agua hace que la tierra conduzca electricidad más fácil (Menor resistencia), mientras que un suelo seco es un conductor pobre de la electricidad (Mayor resistencia).</p><p>Características:</p><ul><li>Pines de conexión de la tarjeta: VCC: alimentación, GND: Tierra, DO: Salida digital indicadora de superación de umbral, AO: Salida análoga de la medición de humedad</li><li>LED indicador de encendido</li><li>Dos agujeros de sujeción en el sensor de diámetro 3 mm aprox. y un agujero de sujeción en el módulo electrónico de 2 mm aprox.</li><li>Dimensiones aprox: Sensor 6 cm x 2 cm. Módulo electrónico 4 cm x 1.5 cm</li></ul><p>Especificaciones:</p><ul><li>Medida análoga de la humedad con salida de variación de voltaje (AO)</li><li>Señal digital de superación de umbral con salida para el usuario (DO) y LED indicador. La sensibilidad de disparo se puede ajustar mediante trimmer. Esta función es provista por un comparador con LM393</li><li>Voltaje de funcionamiento: 3.3V ~ 5V</li><li>VCC: conectarse a la fuente de alimentación positiva (3 ~ 5 V)</li><li>GND: conectar a la red eléctrica negativa</li></ul>",
        "fields": FIELDS_SENSOR,
        "modulos": {1: "PORCENTAJE", 2: "CONDUCTIVIDAD"},
        "is_valid": False,
        "admite_monitoreo": False,
        "img": path + 'sensor-de-humedad-en-suelo-yl-69.jpg',
        "de_unidad": {1: "%", 2:""},
        "acumulable": {1: False, 2: False},

    }, # 1-> usa canal analogico, 2: pin de rpi

    "SERVO": {
        "clase": 26,
        "descripcion": "<p>Descripción:</p><p>Sero Motor Tower Pro (Micro Servo 9g) SG90</p>",
        "fields": FIELDS_SENSOR,
        "modulos": {1: "SERVO"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": '',
        "de_unidad": {1: ""},
        "acumulable": {1: False},

    },

    ########################################
    #               VOLTAJE                #
    ########################################
    "VOLTAJE": {
        "clase": 27,
        "descripcion": "<p>Descripción:</p><p>Permite obtener el valor de voltajes: rms (Voltaje Eficaz), lista de voltajes instantaneos (vinst), fft lista de valores(Espectro en frecuencia)</p>",
        "fields": FIELDS_SENSOR + ["vrms", "vinst", "vfft"],
        "modulos": {1: "VRMS", 2: "VINST", 3: "VFFT"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": '',
        "de_unidad": {1: "volt", 2: "volt", 3: ""},
        "acumulable": {1: False, 2: False, 3: False},

    },

    "VOLTAJE_DETECTOR": {
        "clase": 29,
        "descripcion": "<p>Descripción:</p><p>Detector de presencia y Ausencia de Voltaje.</p>",
        "fields": FIELDS_SENSOR + ["value"],
        "modulos": {1: "DETECTOR"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": '',
        "de_unidad": {1: ""},
        "acumulable": {1: False},

    },
     "DIR_VIENTO": {
        "clase": 28,
        "descripcion": "<p>Permite determinar la direccion del viento</p>",
        "fields": FIELDS_SENSOR + ["velocidad"],
        "modulos": {1: "dir_viento"},
        "is_valid": True,
        "admite_monitoreo": True,
        "img": '',
        "de_unidad": {1: ""},
         "acumulable": {1: False},

     },
        
}


def get_codes():
    list_tuplas = []
    for key in CODES_SENSORES.keys():
        if CODES_SENSORES[key]["is_valid"]:
            list_tuplas.append((CODES_SENSORES[key]["clase"], key))
    return tuple(list_tuplas)


def get_sensores_acumulables():
    list_tuplas = []
    for key in CODES_SENSORES.keys():
        if CODES_SENSORES[key]["is_valid"]:
            for item_acumulable in CODES_SENSORES[key]["acumulable"].keys():
                if CODES_SENSORES[key]["acumulable"][item_acumulable]:
                    list_tuplas.append((CODES_SENSORES[key]["clase"], item_acumulable))
    return tuple(list_tuplas)


CODIGOS_SENSORES_CHOICE = get_codes()
CODIGOS_SENSORES_CHOICE_ACUMULABLES = get_sensores_acumulables()

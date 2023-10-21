from typing import Tuple

class DatosMeteorologicos:
    def __init__(self, nombre_archivo: str):
        self.nombre_archivo = nombre_archivo

    def procesar_datos(self) -> Tuple[float, float, float, float, str]:
        # Variables para calcular las estadísticas
        total_temperatura = 0
        total_humedad = 0
        total_presion = 0
        total_velocidad_viento = 0
        num_mediciones = 0
        direccion_viento_grados = []


        # Abre el archivo y lee los datos
        with open(self.nombre_archivo, 'r') as file:
            # Lee el archivo línea por línea
            for line in file:
                
                # Procesa cada línea para obtener los datos relevantes
                if line.startswith('Temperatura'):
                    total_temperatura += float(line.split(':')[1])
                elif line.startswith('Humedad'):
                    total_humedad += float(line.split(':')[1])
                elif line.startswith('Presion'):
                    total_presion += float(line.split(':')[1])
                elif line.startswith('Viento'):
                    viento_info = line.split(':')[1].split(',')
                    total_velocidad_viento += float(viento_info[0])
                    direccion_viento_grados.append(self.convertir_direccion_a_grados(viento_info[1]))

                # Incrementa el número de mediciones
                num_mediciones += 1

        # Calcula las estadísticas
        temperatura_promedio = total_temperatura / num_mediciones
        humedad_promedio = total_humedad / num_mediciones
        presion_promedio = total_presion / num_mediciones
        velocidad_viento_promedio = total_velocidad_viento / num_mediciones
        direccion_viento_predominante = self.calcular_direccion_predominante(direccion_viento_grados)

        return temperatura_promedio, humedad_promedio, presion_promedio, velocidad_viento_promedio, direccion_viento_predominante

    def convertir_direccion_a_grados(self, direccion: str) -> float:
        # Conversión de abreviaturas de dirección a grados
        abreviaturas_a_grados = {
            'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
            'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
            'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
            'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
        }
        return abreviaturas_a_grados.get(direccion, 0)

    def calcular_direccion_predominante(self, direcciones_grados) -> str:
        # Calcula el promedio de las direcciones en grados
        if not direcciones_grados:
            return 'N/A'

        # Ajusta los grados para obtener un promedio adecuado
        for i in range(len(direcciones_grados)):
            direcciones_grados[i] = direcciones_grados[i] % 360

        # Calcula el promedio de las direcciones
        direccion_promedio_grados = sum(direcciones_grados) / len(direcciones_grados)

        # Convierte el promedio de grados a la abreviatura de dirección más cercana
        abreviaturas = list({
            'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
            'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
            'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
            'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
        }.keys())

        # Encuentra la abreviatura de dirección más cercana al promedio
        direccion_predominante = min(abreviaturas, key=lambda x: abs(direcciones_grados[abreviaturas.index(x)] - direccion_promedio_grados))
        return direccion_predominante

# MaasApp/services/generate_color_service.py
import re


class GenerateColorService:
    @staticmethod
    def get_color_coded_parts(sentence):

        sentence = GenerateColorService.remove_words_in_parentheses(sentence).title()
        parts = sentence.split(';')
        color_coded_parts = []

        for i, part in enumerate(parts, start=1):
            color = GenerateColorService.get_transportation_color_code(part)

            color_coded_parts.append({'part': part, 'color': color, 'number': i})

        return color_coded_parts

    @staticmethod
    def remove_words_in_parentheses(input_string):
        regex = re.compile(r'\([^)]*\)')

        result = regex.sub('', input_string)

        return result

    @staticmethod
    def get_transportation_color_code(mode):
        # Your existing color-coding logic
        if 'Auto' in mode:
            return 'darkred'
        elif '(Elektrische) fiets' in mode:
            return 'blue'
        elif 'Motor' in mode:
            return 'darkslategray'
        elif 'Scooter' in mode:
            return 'forestgreen'
        elif 'Trein' in mode:
            return 'saddlebrown'
        elif 'Bus' in mode:
            return 'darkgreen'
        elif 'Lopen' in mode:
            return 'darkblue'
        elif 'Deelfiets' in mode:
            return 'darkorange'
        elif 'Deelauto' in mode:
            return 'indigo'
        elif 'Deelscooter' in mode:
            return 'cornflowerblue'
        elif 'Taxi' in mode:
            return 'brown'
        else:
            return '#914DFA'

from flask import Flask, jsonify, render_template
import datetime
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

def obtener_valores_uf(date, date_format):
    url = 'https://www.sii.cl/valores_y_fechas/uf/uf' + date[-4:] + '.htm'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    months = {
        '1': 'enero',
        '2': 'febrero',
        '3': 'marzo',
        '4': 'abril',
        '5': 'mayo',
        '6': 'junio',
        '7': 'julio',
        '8': 'agosto',
        '9': 'septiembre',
        '10': 'octubre',
        '11': 'noviembre',
        '12': 'diciembre'
    }
    name_month =  "mes_" + months[""+str(date_format.month)+""] + ""

    if soup.find('div', {'id': name_month}):
        filter_table = soup.find('div', {'id': name_month}).find('table', {'class': 'table table-hover table-bordered'})
        th_value = filter_table.find('th', {'width': '40'}, string=date_format.day)
        td_valor_uf = th_value.find_next_sibling('td').text.strip()  
        return td_valor_uf 
    else:
        return None
    


@app.route('/uf/<date>')
def get_uf_value(date):
    try:
        date_format = datetime.datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        return jsonify({'error': 'Formato de fecha incorrecto. Debe ser dd-mm-aaaa. Por favor revise la fecha ingresada!'}), 400
    if date_format < datetime.datetime(2013, 1, 1):
        return jsonify({'error': 'La fecha minima que se puede consultar es el 01-01-2013.'}), 400
    
    
    """ CALL API """
    valor_uf = obtener_valores_uf(date, date_format)
    
    if valor_uf is None:
        return jsonify({'error': 'No hay valores de la UF para la fecha especificada.'}), 404
    else:
        return jsonify({'fecha': date_format.strftime('%d-%m-%Y'), 'valor_uf': valor_uf})

def pagina_no_encontrada(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)    
    app.run()
    

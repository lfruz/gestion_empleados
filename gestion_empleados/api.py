from flask import jsonify, blueprints



api = blueprints.Blueprint('api',__name__)


@api.route('/mensaje/')
def mensaje():
    """Función que maneja la ruta de mensaje.

        Parameters:
        Ninguno

        Returns:
        Json con el contenido de la lista mensajes.

    """
    from mensaje import mensajes
    return jsonify(mensajes)
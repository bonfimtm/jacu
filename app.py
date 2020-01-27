import datetime
import io
import logging

import flask

app = flask.Flask(__name__)

LINE_BREAK = '\r\n'
ALLOWED_EXTENSIONS = ['txt']


@app.route('/')
def root():
    logging.info('Requesting home page')
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def send_root(path=''):
    return flask.send_from_directory('static/', path)


@app.route('/process-file', methods=['POST'])
def process_file():
    if flask.request.method == 'POST':
        mime_type = 'text/plain'
        filename = 'output_{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M'))

        input_file = flask.request.files.get('input_file', None)

        if input_file and input_file.filename != '' and is_allowed_file(input_file.filename):
            initial_content = input_file.read().decode('utf-8')
        else:
            initial_content = None

        text_stream = io.StringIO()
        if initial_content:
            text_stream.write(initial_content)
            text_stream.write(f'{LINE_BREAK}More content')
            text_stream.write(f'{LINE_BREAK}Some more content')
        else:
            text_stream.write('No initial content')
        binary_stream = io.BytesIO()
        binary_stream.write(text_stream.getvalue().encode('utf-8'))
        binary_stream.seek(0)
        text_stream.close()

        return flask.send_file(binary_stream, mime_type, True, filename)
    else:
        return f'Invalid HTTP method: {flask.request.method}'


def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=False, use_reloader=True, passthrough_errors=True)

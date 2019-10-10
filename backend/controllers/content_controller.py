import os

from response import JSONResponse, BadResponse

from models import ServicesModel, ServicesRow
from logger import logger, class_logger


@class_logger()
class ContentController:

    def __init__(self):
        self._model = ServicesModel()

    def get_action(self):
        result = self._model.get_all()
        return JSONResponse(data=result)

    def post_action(self, form_data):
        service_row = self._get_service_row(form_data)

        if service_row is not None:
            result = self._model.add_row(service_row)

            if result:
                return JSONResponse(json_mes='row success added')
            else:
                return JSONResponse(json_status='error', json_mes='error with adding row')
        else:
            logger.error(f'Not valid {form_data}')
            return BadResponse(400, 'Bad Request')

    def put_action(self, url_params, form_data):
        service_row = self._get_service_row(form_data)

        if service_row is not None:
            result = self._model.update_row(url_params, service_row)
            if result:
                return JSONResponse(json_mes='row success updated')
            else:
                return JSONResponse(json_status='error', json_mes='error with updating row')
        else:
            logger.error(f'Not valid {form_data}')
            return BadResponse(400, 'Bad Request')

    def delete_action(self, url_params):
        result = self._model.delete_row(url_params)
        if result:
            return JSONResponse(json_mes='row success deleted')
        else:
            return JSONResponse(json_status='error', json_mes='error with deleting row')

    def upload_action(self, form_data):

        if not form_data['filename']:
            logger.error(f'Not valid {form_data} for file')
            return BadResponse(400, 'Bad Request')
        elif not form_data['filename'].endswith('.csv'):
            logger.error(f'Not valid {form_data["filename"]}')
            return BadResponse(400, 'Bad Request')

        path_to_file = self._save_file(form_data)

        if path_to_file is None:
            return JSONResponse(json_status='error',
                                json_mes='error with saving file')

        result = self._model.upload_data(path_to_file)

        os.remove(path_to_file)

        if result:
            return JSONResponse(json_mes='table success updated from file')
        else:
            return JSONResponse(json_status='error',
                                json_mes='error with updating table from file')

    @staticmethod
    def _save_file(file):
        try:
            with open(file['filename'], 'wb') as wf:
                wf.write(file['data'])
            cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(cur_dir, file['filename'])
        except OSError as ex:
            logger.error(f'Cant save file: {ex}')
            return None

    @staticmethod
    def _get_service_row(form_data):
        service_row = ServicesRow(form_data)
        if service_row.is_valid():
            return service_row
        else:
            return None

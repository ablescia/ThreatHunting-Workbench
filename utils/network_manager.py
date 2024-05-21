"""
Sadadsdad
"""
from http import HTTPStatus
import json
from PyQt5.QtCore import QObject, QUrl, QByteArray, pyqtSignal
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class NetworkManager(QObject):

    check_connection_signal = pyqtSignal(bool)
    run_query_signal = pyqtSignal(object)

    def __init__(self, requestor: QObject, server_url: str, materialization_cap: int) -> None:
        super().__init__(requestor)
        self.requestor = requestor
        self.server_url = server_url
        self.materialization_cap= materialization_cap
        self.api_endpoint =  f'{self.server_url}?materialization-cap={materialization_cap}'

        self.network_access_manager = QNetworkAccessManager(self.requestor)
        self.network_request = QNetworkRequest(QUrl(self.api_endpoint))
        self.network_request.setHeader(QNetworkRequest.ContentTypeHeader, 'application/x-www-form-urlencoded')
        self.network_access_manager.finished.connect(self.__on_networkaccessmanager_request_response_handle)
        self.last_request_response = None

    def check_connection(self) -> None:
        reply = self.network_access_manager.get(self.network_request)
        reply.setProperty('request_type', 'check_connection')

    def run_query(self, query_text: str) -> None:

        reply = self.network_access_manager.post(self.network_request, QByteArray(query_text.encode('ascii')))
        reply.setProperty('request_type', 'run_query')


    def __on_networkaccessmanager_request_response_handle(self, response) -> None:

        error = response.error()
        if error == QNetworkReply.NoError:
            http_status = response.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            if http_status == HTTPStatus.OK:
                # Retrieve the request type
                request_type = response.property('request_type')

                if request_type == 'check_connection':
                    self.check_connection_signal.emit(True)
                elif request_type == 'run_query':
                    raw_response = response.readAll().data().decode('utf-8')
                    json_data = json.loads(raw_response)
                    self.run_query_signal.emit(json_data)
           
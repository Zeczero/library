import requests
import gzip
import base64
import io
import time


class Saldeo:
    BASE_URL = "https://saldeo.brainshare.pl/"
    USERNAME = ""
    TOKEN = ""

    def __init__(self, api_key: str, username:str):
        self.USERNAME = username
        self.TOKEN = api_key
    def __custom_url_encode(string): 
        return ''.join(['+' if char == ' ' else 
                    '*' if char == '*' else 
                    '%7E' if char == '~' else 
                    char if char.isalnum() or char in '-._' else 
                    f'%{byte:02X}' 
                    for char, byte in zip(string, string.encode('utf-8'))]) 
    def __gzip_and_base64_encode(content, is_file_path=False): 
        file_content = open(content, 'rb').read() if is_file_path else content.encode('utf-8') 
        gzipped_buffer = io.BytesIO() 
        with gzip.GzipFile(fileobj=gzipped_buffer, mode='wb') as gzfile: 
            gzfile.write(file_content) 
        return base64.b64encode(gzipped_buffer.getvalue()).decode('utf-8')
    def __req_id():
        return str(int(time.time() * 1_000_000)) 
    
    def __parameterize(self, sig_params: object):
        return ''.join(f"{key}{self._Saldeo._custom_url_encode('=')}{self._Saldeo.__custom_url_encode(str(value))}" for key, value in sorted(sig_params.items()))
    
    class Document:

        def __init__(self, saldeo):
            self.saldeo = saldeo

        def send(self, data: str, document_name:str,  path_to_file:str, company_program_id:str):
            command_encoded = self.saldeo.__gzip_and_base64_encode(data)
            attmt_doc_name  = self.saldeo.__gzip_and_base64_encode(path_to_file, is_file_path=True)
            company_program_id = company_program_id
            sig_params = {
                "company_program_id": company_program_id, 
                "username": self.saldeo.USERNAME + self.saldeo.TOKEN, 
                "req_id": self.saldeo.__req_id(), 
                "command": command_encoded, 
                f"attmnt_{document_name}": attmt_doc_name 
            }
            param_string = self.saldeo.__parameterize()
import requests

def check_service(url):
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return {
                "status": "UP",
                "code": response.status_code
            }
        else:
            return {
                "status": "DOWN",
                "code": response.status_code
            }
    except requests.exceptions.RequestException as error:
        return {
            "status": "ERROR",
            "message": str(error)
        }
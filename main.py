import functions_framework

@functions_framework.http
def main(request) -> None:
    try:
        dados = request.get_json(silent=True)
        return dados, 200
    except Exception as e:
        return f"Error: {str(e)}", 500
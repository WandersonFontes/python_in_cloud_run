import functions_framework

@functions_framework.http
def main(request) -> None:
    try:
        dados = request.get_json(silent=True)
        return dados, 200
    except:
        return f"Error: {request}", 500

if __name__ == "__main__":
    main(None)
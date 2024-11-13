class NumberNotFoundException(Exception):
    pass

def process_response(result: str):
    try:
        number = float(result)  
        if 0 <= number <= 100:
            return f"Model response is valid: {number}"
        else:
            raise NumberNotFoundException("Number is outside the valid range [0, 100].")
    except ValueError:
        raise NumberNotFoundException("No valid number found in the response.")

def modify_data(original_data, key, values):
    """Изменение полей в данных """
    modified_data = original_data.copy() 
    modified_data[key] = values
    return modified_data
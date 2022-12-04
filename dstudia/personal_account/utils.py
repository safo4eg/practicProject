
def show_errors(form):
    form_errors = form.errors
    form_errors_keys = form_errors.keys()
    for key in form_errors_keys:
        if form_errors[f'{key}'][0] == 'Обязательное поле.':
            form_errors[f'{key}'][0] = f'Поле {key} не может быть пустым!'
    return form_errors.values()

# Получение пользователей у которых есть хотя бы 1 заявка
def get_usernames_have_application(users):
        list_usernames = []
        list_usernames.append('g1')
        for user in users:
            if user.get_application_amount() > 0:
                list_usernames.append(user.username)
        return list_usernames



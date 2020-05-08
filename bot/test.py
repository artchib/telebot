def do_text(message):
    # chat_id = update.effective_chat.id
    # message = update.message.text

    def is_digit(string):
        if string.isdigit():
            return True
        else:
            try:
                float(string)
                return True
            except ValueError:
                return False
    print('перед началом ифа')
    if is_digit(message):
        print(f'сообщение цифра = {message}')
        text = f'= {float(message) * 71} $'
    else:
        text='Вы ввели текст, а не цифрууууу'
    print(text)

print('Введите что-то')
message = input()
do_text(message)


from config import WorkingWithDataClass

test = WorkingWithDataClass()

# result = test.create_user('Петров', 'Иннокентий',None ,'vladlenych@gmail.com')
# print(f'Пользователь успешно создан. Ваш id - {result}')

r = test.submitData(
    1,
    1,
    {'latitude': 50.909958, 'longitude': 88.217849, 'height':  515},
    {
        'beaty_title': '',
        'title': 'Кату-Ярык',
        'other_titles': '',
        'connects': 'Долину реки Чулышман с внешним миром.',
        'winter': '1B',
        'spring': '1B',
        'summer': '2B',
        'autumn': '1A'
    },
    1
)
print(f'All works, pereval ID - {r}')
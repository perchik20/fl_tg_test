realty ={0: [['1. Какой тип недвижимости вы сдаете?', ['Кондо', 'Вилла', 'Коммерческая недвижимость']],
             ['2. Укажите количество комнат', ['1', '2', '3', '4 и более']],
             ['3. Укажите количество ванных комнат', ['1', '2', '3', '4 и более']],
             '4. Укажите размер жилой площади в кв.м.',
             ['5. Укажите, есть ли бассейн', ['Частный', 'Общественный', 'Частный и Общественный', 'Отсутствует']],
             ['6. Укажите, есть ли инфраструктура для детей рядом', ['Есть', 'Нет']],
             ['7. Можно ли с животными', ['Можно', 'Нельзя']],
             '8. Укажите минимальный срок аренды (напишите цифру и день/неделя/месяц): ',
             '9. Укажите стоимость аренды в батах (текстом и цифрами): ',
             '10. Отправьте локацию из Google maps (например https://goo.gl/maps/WytUmSgCrpQf4tSHA)',
             '11. Добавьте комментарий об объекте',
             '12. Прикрепите одну фотографию объекта'],

         1: [['1. Выберите тип ТС', ['Авто', 'Мопед/Мотоцикл', 'Другой транспорт']],
            ['2. Укажите требуемый тип автомобиля:', ['Легковой', 'Внедорожник ',
                                                      'Минивэн']],
             '3. Укажите марку/модель/название',
             '4. Укажите минимальный срок аренды (напишите цифру и день/неделя/месяц): ',
             '5. Укажите стоимость аренды в батах (текстом и цифрами): ',
             '6. Напишите комментарий (условия, страховка, сроки и то, что считаете нужным сообщить):',
             '7. Отправьте одну фотографию ТС']}


tenant ={0: [['1. Какой тип недвижимости вы ищите?', ['Кондо', 'Вилла', 'Коммерческая недвижимость']],
             ['2. Укажите количество желаемых комнат', ['1', '2 и более', '3 и более', '4 и более']],
             ['3. Укажите количество желаемых ванных комнат', ['1', '2 и более', '3 и более', '4 и более']],
             '4. Укажите минимально необходимый размер жилой площади в кв.м.',
             ['5. Какой тип бассейна вам нужен', ['Частный', 'Общественный', 'Частный и Общественный', 'Не нужен']],
             ['6. Нужна ли инфраструктура для детей', ['Да', 'Нет', 'Не имеет значения']],
             ['7. Есть ли животные', ['Есть', 'Нет']],
             '8. Укажите желаемый срок аренды: ',
             '9. Укажите желаемую стоиомсть аренды: ',
             '10. Напишите комментарий (что для Вас важнo): '],

         1: [['1. Выберите тип ТС', ['Авто', 'Мопед/Мотоцикл', 'Другой транспорт']],
            ['2. Укажите требуемый тип автомобиля:', ['Легковой', 'Внедорожник ',
                                                      'Минивэн (5 и более пассажирских мест)']],
             '3. Укажите марку/модель/название, если это имееет значение, иначе нажмите кнопку ниже👇:',
             '4. Укажите желаемый срок аренды: ',
             '5. Укажите желаемую стоиомсть аренды: ',
             '6. Напишите комментарий (что для Вас важно - цвет, страховка, пробег или еще что-то): '
             ],
         2: ['2. Укажите тип недвижимости - нужно написать: ',
             '3. Площадь недвижимости в кв.м: ',
             '4. Отправьте локацию из Google maps (например https://goo.gl/maps/WytUmSgCrpQf4tSHA)',
             '5. Описание и комментарий: ',
             '6. Прикрепите одну фотографию объекта: '
             ],
         3: ['2. Тип объекта (склад, ресторан, магазин и т.д.):',
             '3. Желаемая площадь в кв.м. (Можно пропустить):',
             '4. Желаемый срок аренды в мес. (Можно пропустить):',
             '5. Желаемая арендная плата в батах (Можно пропустить):'],
         }


buy_sale =[['Выберите категорию: ', [
               'Одежда, Обувь, Аксессуары',
               'Хобби и Отдых',
               'Электроника',
               'Для дома и дачи',
               'Запчасти',
               'Товары для детей',
               'Животные',
               'Красота и Здоровье'
           ]],
           'Описание:',
           'Отправьте Фото:'
           ]

# ////////////////////////////////////////////////////////////////////////////////////////////////////

repeat_msg_0 = {0: [['Тип недвижимости: '],
                ['Количество комнат: '],
                ['Количество ванных комнат: '],
                ['Размер помещения в кв.м.'],
                ['Бассейн: '],
                ['Инфраструктура для детей: '],
                ['Животные: '],
                ['Минимальный срок аренды: '],
                ['Стоимость в батах: '],
                ['Локация: '],
                ['Комментарий: '],
                ['Контакт:']],
                1: [['Тип недвижимости: '],
                ['Количество комнат: '],
                ['Количество ванных комнат: '],
                ['Размер помещения в кв.м.: '],
                ['Бассейн: '],
                ['Инфраструктура для детей: '],
                ['Животные: '],
                ['Минимальный срок аренды: '],
                ['Стоимость в батах: '],
                ['Комментарий: '],
                ['Контакт:']],
                2: [['Тип недвижимости: '],
                ['Тип объекта: '],
                ['Размер помещения в кв.м.: '],
                ['Локация: '],
                ['Комментарий: '],
                ['Контакт:']],
                3: [['Тип недвижимости: '],
                ['Тип объекта: '],
                ['Размер помещения в кв.м.: '],
                ['Срок аренды в мес.: '],
                ['Арендная плата в батах: '],
                ['Контакт: ']]
                }

repeat_msg_1 = {0: [['1. Тип ТС: '],
                ['2. Тип автомобиля: '],
                ['3. Марка/Модель: '],
                ['4. Минимальный срок аренды: '],
                ['5. Стоимость аренды в батах: '],
                ['6. Комментарий: '],
                ['7. Контакт:']],
                1: [['1. Тип ТС: '],
                ['2. Тип автомобиля: '],
                ['3. Марка/Модель: '],
                ['4. Минимальный срок аренды: '],
                ['5. Стоимость аренды в батах: '],
                ['6. Комментарий: '],
                ['7. Контакт:']],
                2: [['1. Тип ТС: '],
                ['2. Марка/Модель: '],
                ['3. Минимальный срок аренды: '],
                ['4. Стоимость аренды в батах: '],
                ['5. Комментарий: '],
                ['6. Контакт:']]
                }


text = 'Коллеги, в этом разделе произошли изменения.\n\n' \
'В нем поселился наш Бот Бюро.\n' \
'Больше нет необходимости ставить хэштэги и листать раздел.\n' \
'Бот найдет для Вас всё, что нужно. И опубликует Ваше объявление самым лакончиным образом.\n\n' \
'Нажав на кнопку "Разместить/Найти объявления" можно\n\n' \
'Арендаторы:\n' \
'1. Найти среди вороха объявлений о сдаче транспорта в аренду именно то, что Вам нужно.\n\n' \
'2. Опубликовать свое объявление о желании взять в аренду ТС.\n\n' \
'Арендодатели:\n' \
'1. Вы можете найти все объявления потенциальных клиентов просто выбрав тип ТС с помощью Бота и связаться с ними.\n\n' \
'2. Опубликовать свое объявление ответив на несколько вопросов.\n\n' \
'Для начала работы с Ботом нажмите кнопку "Разместить/Найти объявления"\n\n' \
'По вопросам работы Бота прошу обращаться к @coolprich'

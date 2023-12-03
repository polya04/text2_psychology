#імпортуємо біблотеки
import sqlite3 #Для взаємодії з базою даних SQLite
import re #Для використання регулярних виразів
import pymorphy2  #Для лематизації слів
from tokenize_uk import tokenize_words #Для токенізації слів

#функція, яка приймає шлях до текстового файлу у якості аргументу
def delete_latin_letters(text_path):
    try:
        #Відкриваємо і читаємо вміст файлу
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()

        #Видаляємо латинські літери
        #Створюємо таблицю translation_table, яка містить пари символів для видалення латинських літер.
        translation_table = str.maketrans('', '', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        #метод translate() для видалення латинських літер з тексту
        text_without_latin = text.translate(translation_table)

        #відкриваємо файл для запису і зберігаємо змінений текст у файл
        with open(text_path, 'w', encoding='utf-8') as file:
            file.write(text_without_latin)
    #обробка помилок
    except FileNotFoundError: #блок except, який обробляє помилку
        print(f"Error: File not found at {text_path}")
    except Exception as e:
        print()
#викликаємо функцію з прикладом шляху до файлу
delete_latin_letters('psychology.txt')

#функція для видалення дефісу після якого йде пробіл
def delete_dash(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    #Використовуємо два виклики методу replace для видалення конкретних символів
    cleared_text = text.replace('- ', '')
    cleared_text = cleared_text.replace('–', '')
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(cleared_text)
#шлях до тексту
input_file_path = 'psychology.txt'
output_file_path = 'psychology.txt'

delete_dash(input_file_path, output_file_path)

#підключення до бази даних SQLite
conn = sqlite3.connect('lab_freq_dict_ps.db')
cursor = conn.cursor()

#створюємо таблицю для словоформ, ЧМ та лем
cursor.execute('''CREATE TABLE IF NOT EXISTS words_forms_freq_ps
                  (word_form TEXT,
                  gen_freq INTEGER, 
                  sample_1 INTEGER, 
                  sample_2 INTEGER,
                  sample_3 INTEGER,
                  sample_4 INTEGER,
                  sample_5 INTEGER,
                  sample_6 INTEGER,
                  sample_7 INTEGER,
                  sample_8 INTEGER,
                  sample_9 INTEGER,
                  sample_10 INTEGER,
                  sample_11 INTEGER,
                  sample_12 INTEGER,
                  sample_13 INTEGER,
                  sample_14 INTEGER,
                  sample_15 INTEGER,
                  sample_16 INTEGER,
                  sample_17 INTEGER,
                  sample_18 INTEGER,
                  sample_19 INTEGER,
                  sample_20 INTEGER)
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS part_of_speech_freq_ps
                  (part_of_speech TEXT,
                  gen_freq INTEGER,
                  sample_1 INTEGER,
                  sample_2 INTEGER,
                  sample_3 INTEGER,
                  sample_4 INTEGER,
                  sample_5 INTEGER,
                  sample_6 INTEGER,
                  sample_7 INTEGER,
                  sample_8 INTEGER,
                  sample_9 INTEGER,
                  sample_10 INTEGER,
                  sample_11 INTEGER,
                  sample_12 INTEGER,
                  sample_13 INTEGER,
                  sample_14 INTEGER,
                  sample_15 INTEGER,
                  sample_16 INTEGER,
                  sample_17 INTEGER,
                  sample_18 INTEGER,
                  sample_19 INTEGER,
                  sample_20 INTEGER)
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS lemmas_freq_ps
                  (lemma TEXT,
                  gen_freq INTEGER,
                  sample_1 INTEGER,
                  sample_2 INTEGER,
                  sample_3 INTEGER,
                  sample_4 INTEGER,
                  sample_5 INTEGER,
                  sample_6 INTEGER,
                  sample_7 INTEGER,
                  sample_8 INTEGER,
                  sample_9 INTEGER,
                  sample_10 INTEGER,
                  sample_11 INTEGER,
                  sample_12 INTEGER,
                  sample_13 INTEGER,
                  sample_14 INTEGER,
                  sample_15 INTEGER,
                  sample_16 INTEGER,
                  sample_17 INTEGER,
                  sample_18 INTEGER,
                  sample_19 INTEGER,
                  sample_20 INTEGER)
''')
#відкриваємо текстовий файл і переводимо все у нижній регістр
with open("psychology.txt",  encoding = "utf-8") as data_1:
    text_1 = data_1.read().lower()
#Видалення пунктуаційних знаків та формування списку слів
#створюємо порожній список, який буде містити текст без пункт.
without_punc_marks = []
#використовуємо бібліотеку для токенізації
tokens = list(tokenize_words(text_1))

#Фільтруються токени так, щоб залишити лише слова, видаляючи пунктуаційні знаки. Отримані слова зберігаються у змінну filtered_tokens.
filt_tokens = [token for token in tokens if re.match(r'^[^\W\d_\-\']*$', token)]
edited = ' '.join(filt_tokens) #токени об'єднуються в один рядок
without_punc_marks.append(edited) #отриманий рядок додаємо до списку

splitted_1 = str(without_punc_marks).split(' ') #розбиваємо на слова та символи за пробілом, у змінну splitted_1
print(splitted_1)

#Видаляємо пусті токени
#створюємо порожній список для них
splitted_2 = []
#перевірка наявності порожніх токенів
try:
    for i in splitted_1: #цикл для  ітерації через кожен елемент i у списку splitted_1
        if i != '': #умова для перевірки чи токен не є порожнім
            splitted_2.append(i) #якщо умова виконується - токен до списку
except: #обробка винятків (помилок)
    print('Порожні токени не виявлені')

#Відраховуємо 20000тис слововживань
count = 0 #створюємо лічильник
edited_list = [] #створюємо порожній список, де буде тільки 20 тис
for word in splitted_2: #цикл для ітерації через кожне слово (word) у списку splitted_2.
    if count == 20000: #перевіряємо чи лічильник досягнув значення 20 тис
        break #Якщо умова виконується, використовується break для вийняття з циклу
    count += 1 #додавання слова до edited_list
    edited_list.append(word)
#формуємо 20 вибірок з цього списку по 1000 слів
sample_1_list = edited_list[:1000]
sample_2_list = edited_list[1000:2000]
sample_3_list = edited_list[2000:3000]
sample_4_list = edited_list[3000:4000]
sample_5_list = edited_list[4000:5000]
sample_6_list = edited_list[5000:6000]
sample_7_list = edited_list[6000:7000]
sample_8_list = edited_list[7000:8000]
sample_9_list = edited_list[8000:9000]
sample_10_list = edited_list[9000:10000]
sample_11_list = edited_list[10000:11000]
sample_12_list = edited_list[11000:12000]
sample_13_list = edited_list[12000:13000]
sample_14_list = edited_list[13000:14000]
sample_15_list = edited_list[14000:15000]
sample_16_list = edited_list[15000:16000]
sample_17_list = edited_list[16000:17000]
sample_18_list = edited_list[17000:18000]
sample_19_list = edited_list[18000:19000]
sample_20_list = edited_list[19000:20000]

#ініціалізуємо пайморфі для отримання про текст далі
morph = pymorphy2.MorphAnalyzer(lang='uk')

#визначаємо функцію для обчислення словоформ
def count_wordforms(wordforms, word, number):
    if word in wordforms: #Проходимося по підвибірках, чи слово вже є у словнику
        try:
            wordforms[word][number] += 1 #якщо слово вже є в словоформах, то збільшуємо лічильник на 1
        except IndexError: #якщо номер виходить за межі, розширюємо список нулями та оновлюємо частоту
            wordforms[word].extend([0] * (number - len(wordforms[word]) + 1))
            wordforms[word][number] += 1
    else:  #Якщо слова нема - створюємо новий запис з нулями до списку

        wordforms[word] = [word] + [0] * number
        wordforms[word][number] += 1

wordforms = {}

#перебираємо список підвибірок
for i, sample_list in enumerate([sample_1_list, sample_2_list, sample_3_list, sample_4_list, sample_5_list,
                                  sample_6_list, sample_7_list, sample_8_list, sample_9_list, sample_10_list,
                                  sample_11_list, sample_12_list, sample_13_list, sample_14_list, sample_15_list,
                                  sample_16_list, sample_17_list, sample_18_list, sample_19_list, sample_20_list]):
    for word in sample_list:
        count_wordforms(wordforms, word, i + 1)


values1 = list(wordforms.values()) #добуваємо значення зі словника словоформ

#додаємо 0 якщо в списку менше ніж 21 елемент
for i in values1:
    while len(i) <21:
        i.append(0)

    gen_freq = sum(i[1:21])
    i.insert(1, gen_freq)

#сортуємо словоформи за спадом частоти
values1_ordered = sorted(values1, key=lambda x:x[1], reverse=True)

#вставляємо дані у створену таблицю
for i in values1_ordered:
   cursor.execute("""INSERT OR IGNORE INTO words_forms_freq_ps
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", i)
conn.commit()

#визначаємо функцію для обчислення ЧМ
part_of_speech = {}


def count_part_of_speech(tag, number):
    # Якщо тег частини мови вже присутній в словнику
    if tag in part_of_speech:
        try:
            # Спроба збільшити лічильник для вказаного номеру
            part_of_speech[tag][number] += 1
        except IndexError:
            # Якщо номер перевищує розмір списку, розширюємо його до вказаного номеру
            part_of_speech[tag].extend([0] * (number - len(part_of_speech[tag]) + 1))
            # Збільшуємо лічильник для вказаного номеру
            part_of_speech[tag][number] += 1
    else:
        # Якщо тег ще не існує в словнику, створюємо новий запис
        part_of_speech[tag] = [tag] + [0] * number
        # Збільшуємо лічильник для вказаного номеру
        part_of_speech[tag][number] += 1

# Перебираємо список підвибірок
for i, sample_list in enumerate([sample_1_list, sample_2_list, sample_3_list, sample_4_list, sample_5_list,
                                  sample_6_list, sample_7_list, sample_8_list, sample_9_list, sample_10_list,
                                  sample_11_list, sample_12_list, sample_13_list, sample_14_list, sample_15_list,
                                  sample_16_list, sample_17_list, sample_18_list, sample_19_list, sample_20_list]):
    # Перебираємо слова у кожній підвибірці та викликаємо функцію для оновлення словника
    for word in sample_list:
        parsed = morph.parse(word)[0]
        tag = parsed.tag.POS
        count_part_of_speech(tag, i + 1)

# Отримуємо значення словника частин мови
values2 = list(part_of_speech.values())

for i in values2:
    while len(i) <21:
        i.append(0)

    gen_freq = sum(i[1:21]) # adding the general frequency to the list
    i.insert(1, gen_freq)

for i in values2:
    if i[0] == None:
        values2.remove(i)

values2_ordered = sorted(values2, key=lambda x:x[1], reverse=True)



for i in values2_ordered:
   cursor.execute("""INSERT OR IGNORE INTO part_of_speech_freq_ps
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", i)
conn.commit()

# Створюємо словник для зберігання лем та їх кількостей
# Визначаємо леми за допомогою бібліотеки pymorphy2
lemmas = {}

def update_lemmas(normal_form, number):
    # Якщо лема вже присутня в словнику
    if normal_form in lemmas:
        try:
            # збільш лічильник для вказаного номеру
            lemmas[normal_form][number] += 1
        except IndexError:
            # Якщо номер перевищує розмір списку, розширюємо його до вказаного номеру
            lemmas[normal_form].extend([0] * (number - len(lemmas[normal_form]) + 1))
            # Збільшуємо лічильник для вказаного номеру
            lemmas[normal_form][number] += 1
    else:
        # Якщо лема ще не існує в словнику, створюємо новий запис
        lemmas[normal_form] = [normal_form] + [0] * number
        # Збільшуємо лічильник для вказаного номеру
        lemmas[normal_form][number] += 1

# Перебираємо вибірки та оновлюємо їх у відповідності до номеру списку
for i, sample_list in enumerate([sample_1_list, sample_2_list, sample_3_list, sample_4_list, sample_5_list,
                                  sample_6_list, sample_7_list, sample_8_list, sample_9_list, sample_10_list,
                                  sample_11_list, sample_12_list, sample_13_list, sample_14_list, sample_15_list,
                                  sample_16_list, sample_17_list, sample_18_list, sample_19_list, sample_20_list]):
    # Перебираємо слова у кожному зразку та викликаємо функцію для оновлення словника лем
    for word in sample_list:
        parsed = morph.parse(word)[0]
        normal_form = parsed.normal_form
        update_lemmas(normal_form, i + 1)

# Пропущені значення заповнюємо нулями та рахуємо загальну частоту
values3 = list(lemmas.values())
for i in values3:
    while len(i) <21:
        i.append(0)

    gen_freq = sum(i[1:21])
    i.insert(1, gen_freq)
# Сортуємо значення за частотою в зворотньому порядку (за спаданням значення частоти)
values3_ordered = sorted(values3, key=lambda x:x[1], reverse=True)
#Додаємо до табл БД
for i in values3_ordered:
   cursor.execute("""INSERT OR IGNORE INTO lemmas_freq_ps
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", i)
conn.commit()

conn.close()
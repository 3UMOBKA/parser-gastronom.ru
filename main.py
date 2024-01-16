from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import vk_api
import os
import random

# Путь к папке с изображениями
images_folder = 'images'

if not os.path.exists(images_folder):
    os.makedirs(images_folder)

def generate_url():
    # Генерируем ссылку
    random_number = random.randint(245, 60000)
    url = f"https://www.gastronom.ru/recipe/{random_number}"

    # Проверяем валидность ссылки
    response = requests.head(url)
    if response.status_code == 200:
        # Открываем файл для чтения и проверяем наличие ссылки
        with open("links.txt", "r") as file:
            links = file.readlines()
        
        if url + '\n' not in links:
            # Добавляем ссылку в файл
            return
    with open("links.txt", "a") as file:
        file.write(url + '\n')
    return follow_redirect(url)


def follow_redirect(url):
    response = requests.get(url)
    if response.history:
        # Получаем последний перенаправленный URL
        redirect_url = response.url
        return redirect_url
    else:
        return url


# Генерируем ссылку и следуем за перенаправлением


def get_name():
    try:
        name = soup.find('h1', class_='recipe__title').text
        return name
    except:
        return ''
    
        
def get_opis():
    try:
        opis = soup.find('div', class_='recipe__intro').text
        return opis
    except:
        return ''
        
def get_ingr():
    try:
        ingr = soup.find('div', class_='col-md-8 col-sm-8 col-ms-8 wide-col').find('ul').text
        return ingr
    except:
        return ''
        
def get_image():
    try:
        # Находим все элементы с классом "recipe__step"
        steps = soup.find_all("div", class_="recipe__step")
        count = 0
        # Перебираем каждый элемент и извлекаем информацию о картинке и тексте
        for step in steps:
            image_url = 'https://www.gastronom.ru'+step.find("img")["src"]  # URL картинки
            text = step.find("div", class_="recipe__step-title").text.strip() + ' ' + step.find("div", class_="recipe__step-text").text.strip()  # текст под картинкой

            # Загружаем картинку
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            
            # Создаем объект ImageDraw для добавления текста
            draw = ImageDraw.Draw(image)

            # Устанавливаем шрифт
            font = ImageFont.truetype("shrift.ttf", size=24)

            sentences = text.split('. ') 

            formatted_text = '\n'.join(sentences)

            # Помещаем текст под картинкой
            draw.text((10, image.height - 50), formatted_text, fill="black", font=font)

            # Сохраняем картинку с текстом
            image.save(images_folder+'/'+str(count+1)+'.jpg')
            count+=1
    except:
        return ''
        
def get_main_image():
    try:
        image_url = 'https://www.gastronom.ru'+soup.find("div", class_="main-slider__image-wrap").find("img")["src"]
        text = get_name()
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        # Создаем объект ImageDraw для добавления текста
        draw = ImageDraw.Draw(image)

        # Устанавливаем шрифт
        font = ImageFont.truetype("shrift.ttf", size=45)

        # Помещаем текст под картинкой
        draw.text((10, image.height - 50), text, fill="black", font=font)

        # Сохраняем картинку с текстом
        image.save(images_folder+'/'+'0'+'.jpg')
    except:
        return ''
        
def get_dop():
    try:
        dop = soup.find('div', class_='dop-information-block clearfix').find('p').text +"\n"+ soup.find('div', class_='dop-information-block dop-information-block_corner-on clearfix').find('p').text
        return dop
    except:
        return ''
        
url = generate_url()
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

get_step = ''
steps = soup.find_all("div", class_="recipe__step")
for step in steps:
    get_step+=(step.find("div", class_="recipe__step-text").text.strip())+'\n'
get_main_image()
get_image()

# Параметры аутентификации
access_token = 'vk1.a.nyT7c5yRh43CzDetMqlW1g0tSTTmdpldp03oTkEM7DxgEjpbKgH2tsw366qEfVBna16mTjXjkLr26gXYM_fSqawGCS61NbTkAxqGJPMfXyXXe3hRrh07fK5uND6svIx_NTzGFMbdMQSzJqNigsiP4ZsXptuJdy3dRM9o56rgMk4OsruJ9tHbwqbThkDzb6Fl3eiwLADGKASLdDwygXbOeA'
group_id = '199800303'



# Подключение к API ВКонтакте
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()

# Функция для загрузки изображения на сервер ВКонтакте
def upload_photo(photo_path):
    print(photo_path)
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_wall(photos=photo_path)[0]
    return f"photo{photo['owner_id']}_{photo['id']}"
    ()
# Функция для создания поста с текстом и изображениями
def create_post(message, photos):
    attachments = []
    count = 0
    for photo in photos:
        if count==9:
            break
        count+=1
        photo_url = upload_photo(photo)
        attachments.append(photo_url)
    vk.wall.post(owner_id='-' + group_id, message=message, attachments=','.join(attachments))



# Собираем все пути к изображениям в папке, отсортированные по названию
photo_paths = sorted([os.path.join(images_folder, file) for file in os.listdir(images_folder) if file.endswith('.jpg')])
if get_name()=='':
    print('Ошибка!!!')
    2 + '1'
print(photo_paths)
# Текст поста
post_message = get_name() +'\n&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;'+ get_opis() +'&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;'+ get_ingr()+'&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;\n'+ get_step.strip()+'\n&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;&#129367;\n'+ get_dop() +'\n#рецепт #кулинария #еда #готовимдома #вкусно #питание #рецептынаукр #вкуснаяеда #рецептыпросто #домашняякухня #вкусняшка #закуски #салаты #первоеблюдо #второеблюдо #десерты #выпечка #здоровоепитание #healthyfood #foodporn #cooking #homemade #food #yummy #delicious'

# Создаем пост
create_post(post_message, photo_paths)

# Получаем текущую рабочую директорию
current_directory = os.getcwd()

# Папка, в которой находятся файлы для удаления
folder_path = os.path.join(current_directory, images_folder)

# Проверяем, существует ли папка
if os.path.exists(folder_path):
    # Получаем список файлов в папке
    files = os.listdir(folder_path)
    
    # Проходимся по всем файлам и удаляем их
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

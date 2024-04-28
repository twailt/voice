from pypresence import Presence
from bs4 import BeautifulSoup
import requests
from time import sleep, time

def timer():
    start_time = time()
    while True:
        elapsed_time = time() - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        yield time_str

def get_all_anecdotes():
    url = 'https://anekdotov.net/anekdot/index-page-24.html'
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        anecdote_tags = soup.find_all('p')
        anecdotes = [tag.get_text() for tag in anecdote_tags if tag.get_text() and len(tag.get_text()) <= 128]
        return anecdotes
    except Exception as e:
        print("Error:", e)
        return []

class App:
    def __init__(self):
        self.rpc = Presence("1233142722987167756")
        self.rpc.connect()

    def run(self):
        print("Connected")
        timer_gen = timer()
        anecdotes = get_all_anecdotes()  # Получаем все анекдоты сразу при запуске
        current_anecdote_index = 0  # Индекс текущего отображаемого анекдота

        # Проверяем, есть ли анекдоты, и если есть, выводим первый сразу
        if anecdotes:
            current_anecdote = anecdotes[current_anecdote_index % len(anecdotes)]
            self.rpc.update(
                state=current_anecdote,  # Обновляем текущий анекдот
            )
            current_anecdote_index += 1

        anecdote_timer = time()  # Таймер для обновления анекдотов
        while True:
            current_time = next(timer_gen)
            # Проверяем, прошло ли 15 секунд для обновления анекдотов
            if time() - anecdote_timer >= 15:
                if anecdotes:
                    current_anecdote = anecdotes[current_anecdote_index % len(anecdotes)]
                    self.rpc.update(
                        state=current_anecdote,  # Обновляем текущий анекдот
                    )
                    current_anecdote_index += 1
                anecdote_timer = time()  # Сбрасываем таймер обновления анекдотов

            self.rpc.update(
                buttons=[
                    {
                        "label": "𝖙𝖗𝖆𝖈𝖐𝖊𝖗",
                        "url": "https://discord-tracker.com/tracker/user//"
                    }
                ],
                state=current_anecdote,  # Обновляем текущий анекдот
                details=current_time + " Анекдоты",
                large_image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlgWya6F7WVU_1WDgOiZqVU6DisUO1IVTZtcocRhZBRA&s"
            )
            sleep(1)


if __name__ == "__main__":
    app = App()
    app.run()



def twoSum(nums, target):
    seen = {}
    for i in range(len(nums)):
        diff = target - nums[i]
        if diff in seen:
            return [seen[diff], i]
        else:
            seen[nums[i]] = i

# def number(target: int, num: dict):

#     seen = {}

#     for i in range(len(num)):
#         dif = target - num[i]
#         if dif in seen:
#             return[seen[dif], i]
#         else:
#             seen[num[i]] = i
# result = number(7,[5,4,6,2,6])
# print(result)
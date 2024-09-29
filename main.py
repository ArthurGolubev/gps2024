import os
import httpx
import json
from collections import Counter

from playwright.sync_api import sync_playwright
from slugify import slugify

from plotly.subplots import make_subplots
import plotly.graph_objects as go

from schemas import ProtocolSchema

class Competition:




    def __init__(self, race_id: int, competitions_ids: list[int]) -> None:
        self.race_id = race_id
        self.competitions_ids = competitions_ids
        self.participants = []
        self.distance = ''
        self.title = ''
        self.downloaded_protocols = []




    def download_protocols(self) -> None:
        for competition in self.competitions_ids:
            n = self.trys(
                self._get_participants,
                competition=competition
            )

            for i in range(n // 100 + 1):
                self.participants += self.trys(
                    self._get_page_competition,
                    competition=competition,
                    from_number=i * 100
                )
                
            self.downloaded_protocols.append(
                self._save_to_json(competition=competition)
            )
        return self.downloaded_protocols
    


    def create_charts(self, protocol_json_file: str) -> None:
        with open(protocol_json_file, 'r') as f:
            protocol = json.loads(f.read())
            p = ProtocolSchema(**protocol)
            print(p.distance.en)
            finish_time = []
            gender = []
            ages = []
            cities = []

            def round_to_15(finish_time: str):
                if finish_time:
                    h, m, s = finish_time.split(':')
                    total_time = int(h) * 60 + int(m)
                    rounded = total_time // 30 * 30
                    return f"{rounded // 60}:{rounded % 60 if rounded % 60 > 0 else '00'}"

            for participant in p.participants:
                if p.competition_id == participant.race_distance_id:
                    rounded = round_to_15(participant.race_time)
                    finish_time.append(rounded)
                    gender.append(participant.athlete.gender.name)
                    ages.append(participant.athlete.birth_year)
                    cities.append(participant.athlete.city.name)

            finish_time = Counter(finish_time)
            dnf = finish_time.pop(None, 0)
            # print(finish_time)
            gender = Counter(gender)
            cities = Counter(cities)
            ages = Counter(ages)
            ages.pop(None, None)
            ages = dict(sorted(ages.items()))
            ages_groups = {
                '10-18': 0,
                '19-25': 0,
                '26-30': 0,
                '31-35': 0,
                '36-40': 0,
                '41-45': 0,
                '46-55': 0,
                '55+': 0,
            }
            for k, v in ages.items():
                if 2024 - int(k) < 19:
                    ages_groups['10-18'] += v
                elif 2024 - int(k) < 26:
                    ages_groups['19-25'] += v
                elif 2024 - int(k) < 31:
                    ages_groups['26-30'] += v
                elif 2024 - int(k) < 36:
                    ages_groups['31-35'] += v
                elif 2024 - int(k) < 40:
                    ages_groups['36-40'] += v
                elif 2024 - int(k) < 46:
                    ages_groups['41-45'] += v
                elif 2024 - int(k) < 56:
                    ages_groups['46-55'] += v
                else:
                    ages_groups['55+'] += v

            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=(
                    "Кол-во финишеров за пройденное время",
                    "Соотношение полов",
                    "Распределение участников по возрастным группам",
                    "Соотношение участников по городам",
                ),
                specs=[[{"type": "bar"}, {"type": "pie"}], [{"type": "bar"}, {"type": "pie"}]],

            )
            fig.add_trace(
                go.Bar(
                    x=list(finish_time.keys()),
                    y=list(finish_time.values()),
                    name='Участники',
                    text=list(finish_time.values()),
                    legendgroup='Время',
                    showlegend=False
                ),
                row=1,
                col=1
            )
            fig.add_trace(
                go.Pie(
                    values=list(gender.values()),
                    # x=list(ages.keys()),
                    # y=list(ages.values()),
                    name='Участники',
                    legendgroup='Время',
                    showlegend=False,
                    text=list(gender.keys()),
                ),
                row=1,
                col=2
            )
            fig.add_trace(
                go.Bar(
                    # labels=list(gender.keys()),
                    # values=list(gender.values()),
                    x=list(ages_groups.keys()),
                    y=list(ages_groups.values()),
                    text=list(ages_groups.values()),
                    legendgroup='Возрастные группы',
                    showlegend=False
                ),
                row=2,
                col=1
            )
            fig.add_trace(
                go.Pie(
                    labels=[f"{k} - {v}" for k, v in cities.items()],
                    values=list(cities.values()),
                    # x=list(cities.keys()),
                    # y=list(cities.values()),
                    text=list(cities.keys()),
                    legendgroup='Возрастные группы',
                    showlegend=True,
                ),
                row=2,
                col=2
            ).update_traces(
                textposition='inside'
            )

            fig.update_layout(
                title={
                    'text': "Горный поход за сутки 2024",
                    'font': {
                        'size': 32
                    },
                    'y': 0.98,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'subtitle': {
                        'text': f"{p.distance.ru}<br> {sum(finish_time.values())} уч."
                    },
                    
                },
                height=1080,
                width=1500,
                margin=dict(t=200),
                legend=dict(y=0.5),
            ).update_yaxes(
                title_text="Количество",
                row=1,
                col=1
            ).update_yaxes(
                title_text="Количество",
                row=2,
                col=1
            ).update_xaxes(
                title_text="Время",
                row=1,
                col=1
            ).update_xaxes(
                title_text="Возрастная группа",
                row=2,
                col=1
            )

            fig.show()
            folder = p.title.en + '/charts'
            os.makedirs(folder, exist_ok=True)
            fig.write_html(f"{folder}/{p.distance.en}.html")
            fig.write_image(f"{folder}/{p.distance.en}.svg")
            fig.write_image(f"{folder}/{p.distance.en}.jpeg")
        




    def trys(self, func: callable, **kwargs) -> None:
        for _ in range(3):
            try:
                return func(**kwargs)
            except Exception as e:
                print(e)




    def _get_participants(self, competition: int) -> int:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f'https://toplist.run/race/{self.race_id}/protocol/{competition}')
            participants = page.locator(".v-data-table-footer__info").text_content().split(' ')[-1]
            distance = page.locator(".active.protocol-header__distances__items__item").text_content()
            self.distance = {"ru": distance, "en": slugify(distance)}
            title = page.locator(".protocol-header__info__title").text_content()
            self.title = {"ru": title, "en": slugify(title)}
            browser.close()

            return int(participants)




    def _get_page_competition(self, competition: int, from_number: int) -> list:
        url = f"https://toplist.run/api/competition/{self.race_id}/{competition}?from={from_number}&length=100"
        result = httpx.get(url).json()
        return result.get('competition')




    def _save_to_json(self, competition) -> None:
        folder = self.title['en']
        os.makedirs(folder, exist_ok=True)
        file_name = self.distance['en'] + '.json'
        with open(f"{folder}/{file_name}", 'w') as f:
            f.write(
                json.dumps({
                    'title': self.title,
                    'distance': self.distance,
                    'race_id': self.race_id,
                    'competition_id': competition,
                    'participants': self.participants,
                },
                indent=4
            ))
        return f"{folder}/{file_name}"






if __name__ == '__main__':
    gps2024 = Competition(
        race_id=7348,
        competitions_ids=[22217, 22122, 22121, 22120]
    )
    # protocols = gps2024.download_protocols()
    gps2024.create_charts('gornyi-pokhod-za-sutki-2024/20-km-700-m-pervoprokhodtsy.json')
    gps2024.create_charts('gornyi-pokhod-za-sutki-2024/40-km-1500-m-liubiteli.json')
    gps2024.create_charts('gornyi-pokhod-za-sutki-2024/55-km-2000-m-sportsmeny.json')
    gps2024.create_charts('gornyi-pokhod-za-sutki-2024/75-km-2500-m-professionaly.json')

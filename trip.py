from dataclasses import dataclass
from itertools import zip_longest
import datetime

tcr = {
    "Воронеж": "ул. Кирова, дом 11, 3 этаж",
    "Екатеринбург": "ул. Хохрякова, дом 10, БЦ «Палладиум»",
    "Ижевск": "ул. Ленина, дом 21, БЦ «Форум» ",
    "Иннополис": "ул. Университетская, дом 7, АДЦ им. А. С. Попова",
    "Казань": "ул. Островского, дом 98, БЦ «URBAN»",
    "Краснодар": "Кубанская набережная, дом 39, 2 этаж",
    "Москва": "Инновационный центр «Сколково», Большой бульвар, дом 42, стр. 1",
    "Нижний Новгород": "ул. Алексеевская, дом 10/16, БЦ «Лобачевский PLAZA»",
    "Новосибирск": "ул. Советская, дом 5, БЦ «Кронос»",
    "Новосибирск. Академгородок": "ул. Николаева, дом 11, Технопарк Новосибирского Академгородка, 4 этаж",
    "Омск": "ул. Гагарина, дом 14, БЦ «На Гагарина», 5 этаж",
    "Пермь": "ул. Куйбышева, дом 95б, БЦ «Green Plaza», 8 этаж",
    "Ростов-на-Дону": "ул. Суворова, дом 91, БЦ «Лига Наций»",
    "Рязань": "ул. Кудрявцева, дом 56",
    "Самара": "пр. Карла Маркса, 201Б, БЦ «Башня», 10 этаж",
    "Санкт-Петербург": "ул. Херсонская, дом 12/14, БЦ «Ренессанс Правда»",
    "Саратов": "ул. Вавилова, дом 38/114, БЦ «Ковчег», офис 914",
    "Сочи": "Триумфальный проезд, дом 1",
    "Таганрог": "ул. Чехова, дом 98А, 2 этаж",
    "Томск": "ул. Советская, дом 78, 2 этаж",
    "Уфа": "ул. Гоголя, дом 60, БЦ «Капитал»",
    "Чебоксары": "ул. Ярославская, дом 27, БЦ «Республика», 7 этаж",
    "Челябинск": "ул. Кирова, дом 159, офис 907, БЦ «Челябинск-Сити»",
}


@dataclass
class Stay:
    where: str
    nights: int
    additional: list[datetime.date] = None

    @property
    def has_office(self):
        if self.where in tcr:
            return "has office"
        return ""

    @property
    def pretty(self):
        res = str(self.nights)
        if self.additional:
            res += f"({len(self.additional)})"
        return res + " nights"


@dataclass
class TripHop:
    source: str
    dest: Stay
    km: int
    time: float

    date_start: datetime.date = None
    date_end: datetime.date = None

    after_work: bool = False
    day_off: bool = False


trip = [
    TripHop("Екатеринбург", Stay("Уфа", 1), 529, 7),
    TripHop("Уфа", Stay("Самара", 1), 466, 6.5),
    TripHop("Самара", Stay("Саратов", 3), 418, 5),
    TripHop("Саратов", Stay("Волгоград", 2), 374, 4.9),
    TripHop("Волгоград", Stay("Астрахань", 2), 425, 5.5),
    TripHop("Астрахань", Stay("Кисловодск", 7), 674, 8),
    TripHop("Кисловодск", Stay("Ставрополь", 2), 189, 2.5),
    TripHop("Ставрополь", Stay("Краснодар", 5), 300, 4),
    TripHop("Краснодар", Stay("Сочи", 10), 300, 5.5),
    TripHop("Сочи", Stay("Геленжик", 2), 246, 5),
    TripHop("Геленжик", Stay("Ростов-на-Дону", 2), 443, 5),
    TripHop("Ростов-на-Дону", Stay("Воронеж", 1), 567, 5.5),
    TripHop("Воронеж", Stay("Москва", 7), 520, 5.5),
    TripHop("Москва", Stay("Санкт-петербург", 8), 709, 6),
    TripHop("Санкт-петербург", Stay("Москва", 0), 709, 6),
    TripHop("Москва", Stay("Казань", 4), 834, 7.5),
    TripHop("Казань", Stay("Ижевск", 1), 384, 4.5),
    TripHop("Ижевск", Stay("Пермь", 1), 289, 4),
    TripHop("Пермь", Stay("Екатеринбург", 0), 360, 4.5),
]

start_date = datetime.date(2025, 4, 10)
for day in (start_date,):
    current_date = day
    for hop, next_hop in zip_longest(trip, trip[1:]):
        # print(hop.source, current_date, 'for', hop.dest.nights, 'nights', 'is holiday', current_date.isoweekday() > 5)
        hop.date_start = current_date
        hop.dest.additional = []
        current_date += datetime.timedelta(days=hop.dest.nights)

        if hop.source in tcr:
            cap = 3
        else:
            cap = 2

        for x in range(0, 7):
            if current_date.isoweekday() > 5:
                break
            if not next_hop:
                break

            if next_hop.time < 5:
                # print('you have to go after work', current_date)
                hop.after_work = True
                break
            if hop.dest.nights >= cap:
                # print('you have to get day off', current_date, next_hop.source, next_hop.dest.where)
                hop.day_off = current_date
                break
            hop.dest.additional.append(current_date)
            hop.dest.nights += 1
            current_date += datetime.timedelta(days=1)
        hop.date_end = current_date

for hop in trip:
    print(
        f"{hop.source:>15} - {hop.dest.where:<15} {str(hop.time).rjust(5)}h, "
        f"{hop.date_start} - {hop.date_end}, after work:{int(hop.after_work):<1}, day off:{bool(hop.day_off):<1}",
        f"{hop.dest.where:>15} - {hop.dest.pretty} {hop.dest.has_office}",
    )

benz_price_ai95 = 60
stay_price_high = 10_000
stay_price_low = 6_000
nights = sum(t.dest.nights for t in trip)
days_to_sleep = sum(t.dest.nights - 1 for t in trip if t.dest.nights)
days_in_move = len(trip)
days_in_total = days_in_move + days_to_sleep
final_date = start_date + datetime.timedelta(days=days_in_total)

print(sum(t.km for t in trip), "km")
print(sum(t.time for t in trip), "hours")
print(days_in_move, "days in move")
print(days_in_total, "days total")
print(nights, "nights to sleep")
print(nights * stay_price_low, "rub lo hotel")
print(nights * stay_price_high, "rub hi hotel")
print(sum(t.km for t in trip) / 100 * 9 * benz_price_ai95, "rub benz")

print(final_date, "return day if start", start_date)

import calendar
import matplotlib.pyplot as plt
import datetime
from matplotlib.patches import Patch


def date_range(start, end, step=1):
    current = start
    while current <= end:
        yield current
        current += datetime.timedelta(days=step)


def generate_travel_calendar(trip: list[TripHop]):
    cities = set(t.dest.where for t in trip)
    colors = plt.get_cmap("tab20", len(cities))
    city_color_map = {city: colors(i) for i, city in enumerate(cities)}
    may_days = [
        datetime.date(2025, 5, 1),
        datetime.date(2025, 5, 2),
        datetime.date(2025, 5, 8),
        datetime.date(2025, 5, 9),
    ]

    months = sorted(set(dt.strftime("%Y-%m") for dt in [t.date_start for t in trip]))
    after_work_days = [t.day_off for t in trip if t.day_off]
    leave_days = [t.after_work for t in trip if t.after_work]
    add_days = [a for t in trip if t.day_off for a in t.dest.additional]

    fig, axes = plt.subplots(len(months), 1, figsize=(7, len(months) * 3))

    travel_plan = {}
    for t in trip:
        for d in date_range(t.date_start, t.date_end):
            travel_plan[d] = t.dest.where

    if len(months) == 1:
        axes = [axes]

    leave_hatch = "."
    add_hatch = "\\"
    after_work_hatch = "+"

    for ax, month in zip(axes, months):
        year, month = map(int, month.split("-"))
        cal = calendar.monthcalendar(year, month)

        ax.set_xticks(range(7))
        ax.set_xticklabels(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"])
        ax.set_yticks(range(len(cal)))
        ax.set_yticklabels(["Week {0}".format(i + 1) for i in range(len(cal))])

        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                if day == 0:
                    continue
                date = datetime.date(year, month, day)
                hatch = None
                if date in leave_days:
                    hatch = leave_hatch
                if date in add_days:
                    hatch = add_hatch
                if date in after_work_days:
                    hatch = after_work_hatch
                if date in may_days:
                    hatch = "x"
                if date in travel_plan:
                    city = travel_plan[date]
                    ax.add_patch(
                        plt.Rectangle((day_idx, week_idx), 1, 1, color=city_color_map[city], alpha=0.7, hatch=hatch)
                    )
                    ax.text(
                        day_idx + 0.5, week_idx + 0.5, str(day), ha="center", va="center", fontsize=10, color="black"
                    )
                else:
                    ax.text(day_idx + 0.5, week_idx + 0.5, str(day), ha="center", va="center", fontsize=10)

        ax.set_xlim(0, 7)
        ax.set_ylim(len(cal), 0)
        ax.set_title(datetime.date(year, month, 1).strftime("%B %Y"))
        ax.set_frame_on(False)

    legend_patches = [Patch(color=city_color_map[t.dest.where], label=t.dest.where) for t in trip]
    legend_patches.append(Patch(edgecolor="black", hatch=leave_hatch, label="Отгулы"))
    legend_patches.append(Patch(edgecolor="black", hatch=add_hatch, label="Доп дни"))

    fig.legend(handles=legend_patches, title="Cities", loc="upper right")
    fig.legend(handles=legend_patches, title="Cities", loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    fig.subplots_adjust(right=0.75)

    plt.show()


generate_travel_calendar(trip)

calendar_colors: dict[str, int | None] = {
    "#51FF51": None,  # Övrigt
    "#9393FF": 1,  # Fysik
    "#C8F759": 2,
    "#80FF80": 2,  # Idrott
    "#80FF00": 2,  # Mentorstid
    "#DF00DF": 3,
    "#FF8080": 4,
    "#E9C187": 4,  # ?
    "#FFFF00": 5,  # Kör
    "#FFFF64": 5,  # Övrig musik
    "#DDDD00": 5,  # 4? Kör2
    "#FFB9FF": 6,  # ? Engelska
    "#FF8000": 6,  # Samhällskunskap
    "#00FFFF": 7,  # Frukostkonsert
    "#FFFFFF": 8,  # Lunch + Gymnasiearbete
    "#0080FF": 9,  # Matte
    "#808000": 10,  # ? Biologi
    "#008000": 10,
}


def get_calendar_color(html_color: str) -> int | None:
    if (html_color in calendar_colors.keys()):
        return calendar_colors[html_color]
    print(f"COLOR has no match in Google Calendar's colors: {html_color}")
    return None

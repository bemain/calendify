calendar_colors: dict[str, int | None] = {
    "#51FF51": None,  # Övrigt
    "#9393FF": 1,  # Fysik
    "#D5D1AE": 1,  # ? Filosofi
    "#D0FE8B": 1,  # ? Psykologi
    "#C8F759": 2,
    "#80FF80": 2,  # Idrott
    "#80FF00": 2,  # Mentorstid
    "#66BDA3": 2,  # Naturkunskap
    "#DF00DF": 3,  # Svenska
    "#FF46FF": 3,  # Svenska som andraspråk
    "#FF8080": 4,
    "#E9C187": 4,  # ?
    "#F1E8A5": 4,  # GeMu 1
    "#FFFF00": 5,  # Kör
    "#FFFF64": 5,  # Övrig musik
    "#DDDD00": 5,  # 4? Kör2
    "#FFB9FF": 6,  # ? Engelska
    "#FF8000": 6,  # Samhällskunskap
    "#00FFFF": 7,  # Frukostkonsert
    "#8CFFFF": 7,  # Geografi
    "#FFFFFF": 8,  # Lunch + Gymnasiearbete
    "#0080FF": 9,  # Matte
    "#000080": 9,  # Historia, MuHi
    "#808000": 10,  # Biologi
    "#008000": 10,
    "#002F17": 10,  # ? Religion
    "#FF4040": 11,  # Franska 4
    "#FF1515": 11,  # Tyska 4
    "#FF1C1C": 11,  # Spanska 3
    "#FF0000": 11,  # Spanska 1, Tyska 1
    "#FF0909": 11,  # Franska 1
}


# TODO: Write an algorithm to find the closest correllation.
def get_calendar_color(html_color: str) -> int | None:
    if html_color in calendar_colors.keys():
        return calendar_colors[html_color]
    print(f"COLOR has no match in Google Calendar's colors: {html_color}")
    return None

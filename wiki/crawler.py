end_lotm = 1394
lotm_time_stamps = [213, 482, 732, 946, 1150, 1266, 1353, end_lotm]
end_sidestories = 1445
end_coi = end_sidestories + 1179
base_url = "https://lordofthemysteries.fandom.com/wiki/"
url_cats = {
    "wechat": {
        "url": "Category:Archived",
        "exact_chapter": end_coi,
        "chapter_range": None,
        "exclusions": set(),
    },
    "lotm_portal": {
        "url": "Portal:Lord_of_Mysteries",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "coi_portal": {
        "url": "Portal:Circle_of_Inevitability",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "settings": {
        "url": "Category:Settings",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "notes": {
        "url": "Category:Author%27s_Notes/Book_One",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "organizations":{
        "url": "Category:Organizations",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "items":{
        "url": "Category:Items",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "terminology":{
        "url": "Category:Terminology",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "locations":{
        "url": "Category:Location",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "characters":{
        "url": "Category:Characters",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "book_one_content":{
        "url": "Category:Book_One_Content",
        "exact_chapter": end_sidestories,
        "chapter_range": None,
        "exclusions": set(),
    },
    "book_two_content":{
        "url": "Category:Book_Two_Content",
        "exact_chapter": end_coi,
        "chapter_range": None,
        "exclusions": set(),
    },
    "alive":{
        "url": "Category:Alive",
        "exact_chapter": end_coi,
        "chapter_range": None,
        "exclusions": set(),
    },
    "deceased":{
        "url": "Category:Deceased",
        "exact_chapter": end_coi,
        "chapter_range": None,
        "exclusions": set(),
    },
}

specific_urls = {
    "An_Ordinary_Person%27s_Daily_Life_(Side_Story)": {
        "exact_chapter": end_sidestories,
        "chapter_range": None,
    },
    "Volume_1:_Clown": {
        "exact_chapter": lotm_time_stamps[0],
        "chapter_range": None,
    },
    "Volume_2:_Faceless": {
        "exact_chapter": lotm_time_stamps[1],
        "chapter_range": None,
    },
    "Volume_3:_Traveler": {
        "exact_chapter": lotm_time_stamps[2],
        "chapter_range": None,
    },
    "Volume_4:_Undying": {
        "exact_chapter": lotm_time_stamps[3],
        "chapter_range": None,
    },
    "Volume_5:_Red_Priest": {
        "exact_chapter": lotm_time_stamps[4],
        "chapter_range": None,
    },
    "Volume_6:_Lightseeker": {
        "exact_chapter": lotm_time_stamps[5],
        "chapter_range": None,
    },
    "Volume_7:_The_Hanged_Man": {
        "exact_chapter": lotm_time_stamps[6],
        "chapter_range": None,
    },
    "Volume_8:_Fool": {
        "exact_chapter": lotm_time_stamps[7],
        "chapter_range": None,
    },
}

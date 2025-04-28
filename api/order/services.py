from api.order.models import DeliveryForDrivers, AddCargo


def match_cargo_to_driver(cargo):
    matched_drivers = DeliveryForDrivers.objects.filter(
        weight__gte=cargo.weight,
        volume__gte=cargo.volume,
        where=cargo.loading,
        when=cargo.when
    )

    if cargo.GPS_monitoring:
        matched_drivers = matched_drivers.filter(GPS_monitoring=True)

    return matched_drivers


"""
Qanday Filterlar qilish mumkin?
AddCargo modeli uchun:
Yuk turiga (cargo_type) qarab filter
(masalan, faqat ma'lum turdagi yuklarni ko'rsatish, masalan: Furniture, Food va h.k.)

Yuk vazniga (weight) qarab filter
(masalan, weight__gte=1000, ya'ni faqat 1000kg dan og'ir yuklar)

O'lchamlarga (length, width, height, volume) qarab filter
(masalan, hajmi 10m³ dan katta yuklar)

Qayerdan yuklanmoqda (loading) va qayerga tushirilmoqda (unloading) filteri
(masalan, loading__region="Toshkent" va unloading__region="Samarqand")

Narxga (bid_price) yoki valyutaga (bid_currency) qarab filter
(masalan, faqat USD narxli yuklar yoki bid_price__lte=10000)

Qachon yuklanadi (when) bo'yicha filter
(masalan, faqat ready_to_download holatdagi yuklar)

GPS monitoring mavjudligi (GPS_monitoring) bo'yicha filter
(GPS_monitoring=True bo'lgan yuklar)

Xizmat turi (services) bo'yicha filter
(masalan, faqat Express Delivery xizmatlari)

DeliveryForDrivers modeli uchun:
Mashina turiga (car_model) qarab filter
(masalan, faqat truck yoki semitrailer)

Mashina kuzov turiga (car_body_type) qarab filter
(masalan, flatbed, container, van)

Yuklash usuli (loading) bo'yicha filter
(masalan, faqat top yoki back orqali yuklaydiganlar)

Qayerdan (where) va qayerga (where_to) olib borilmoqda bo'yicha filter
(masalan, where=District(Toshkent) va where_to=District(Samarqand))

Vaznga (weight) va hajmga (volume) qarab filter
(masalan, faqat 5 tonna dan kam yuk tashiydiganlar)

Narx (bid_price) va valyuta (bid_currency) bo'yicha filter

GPS monitoring bor yo'qligiga qarab filter
(faqat GPS monitoringli transportlar)
"""

from api.order.models import DeliveryForDrivers, AddCargo


# def match_cargo_to_driver(cargo):
#     filters = {}
#
#     if cargo.weight is not None:
#         filters['weight__gte'] = cargo.weight
#
#     if cargo.volume is not None:
#         filters['volume__gte'] = cargo.volume
#
#     if cargo.loading is not None:
#         filters['where'] = cargo.loading
#
#     if cargo.when:
#         filters['when'] = cargo.when
#
#     matched_drivers = DeliveryForDrivers.objects.filter(**filters)
#     if cargo.GPS_monitoring:
#         matched_drivers = matched_drivers.filter(GPS_monitoring=True)
#
#     print(matched_drivers)
#     return matched_drivers


def match_where_to_driver(cargo):
    filters = {}
    if cargo.loading is not None:
        filters['where'] = cargo.loading
    if cargo.unloading is not None:
        filters['where_to'] = cargo.unloading

    matched_cargo = DeliveryForDrivers.objects.filter(**filters)
    return matched_cargo


def match_where_to_cargo(driver):
    filters = {}
    if driver.where is not None:
        filters['loading'] = driver.where
    if driver.where_to is not None:
        filters['unloading'] = driver.where_to

    matched_cargo = AddCargo.objects.filter(**filters)
    return matched_cargo


def get_locations_cargo(cargo):
    filters = {}
    if cargo.loading is not None:
        filters['loading'] = cargo.loading
    if cargo.unloading is not None:
        filters['unloading'] = cargo.unloading

    get_cargo = AddCargo.objects.filter(**filters)
    return get_cargo


def get_locations_driver(driver):
    filters = {}
    if driver.where is not None:
        filters['where'] = driver.where
    if driver.where_to is not None:
        filters['where_to'] = driver.where_to

    get_cargo = DeliveryForDrivers.objects.filter(**filters)
    return get_cargo

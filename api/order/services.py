from api.order.models import DeliveryForDrivers, AddCargo


def match_cargo_to_driver(cargo):
    filters = {}

    if cargo.weight is not None:
        filters['weight__gte'] = cargo.weight

    if cargo.volume is not None:
        filters['volume__gte'] = cargo.volume

    if cargo.loading is not None:
        filters['where'] = cargo.loading

    if cargo.when:
        filters['when'] = cargo.when

    matched_drivers = DeliveryForDrivers.objects.filter(**filters)
    if cargo.GPS_monitoring:
        matched_drivers = matched_drivers.filter(GPS_monitoring=True)

    print(matched_drivers)
    return matched_drivers


def match_where_where_to(cargo):
    filters = {}
    if cargo.loading is not None:
        filters['where'] = cargo.loading
    if cargo.unloading is not None:
        filters['where_to'] = cargo.unloading

    matched_cargo = DeliveryForDrivers.objects.filter(**filters)
    return matched_cargo

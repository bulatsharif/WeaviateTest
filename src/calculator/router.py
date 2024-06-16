from fastapi import APIRouter, HTTPException

from src.calculator.schemas import ZakatOnProperyCalculated, ZakatOnProperty, ZakatOnLivestockResponse, \
    ZakatOnLivestock, ZakatUshrResponse, ZakatUshrRequest, ZakatUshrItem, NisabValue

router = APIRouter(
    prefix="/calculator",
    tags=["Zakat Calculator"]
)

@router.post("/zakat-property", response_model=ZakatOnProperyCalculated)
async def calculate_zakat_on_property(property: ZakatOnProperty):
    zakat_value = (
        (
            property.cash + property.cash_on_bank_cards + property.silver_jewelry + property.gold_jewelry
            + property.purchased_product_for_resaling + property.unfinished_product + property.produced_product_for_resaling
            + property.purchased_not_for_resaling + property.used_after_nisab + property.rent_money + property.stocks_for_resaling
            + property.income_from_stocks
        ) * 0.025
    )
    if zakat_value == 0:
        raise HTTPException(status_code=400, detail="No assets were added")
    calculated_value = ZakatOnProperyCalculated(zakat_value=zakat_value)
    return calculated_value




@router.post("/zakat-livestock", response_model=ZakatOnLivestockResponse)
async def calculate_zakat_on_livestock(livestock: ZakatOnLivestock):
    calculated_livestock = ZakatOnLivestockResponse(
        camels=0,
        cows=0,
        buffaloes=0,
        sheep=0,
        goats=0,
        horses=0,
        nisab_status=False
    )
    if livestock.camels and livestock.camels > 5:
        calculated_livestock.camels = 1
        calculated_livestock.nisab_status = True
    if livestock.cows and livestock.cows > 30:
        calculated_livestock.cows = 1
        calculated_livestock.nisab_status = True
    if livestock.buffaloes and livestock.buffaloes > 30:
        calculated_livestock.buffaloes = 1
        calculated_livestock.nisab_status = True
    if livestock.sheep and livestock.sheep > 40:
        calculated_livestock.sheep = 1
        calculated_livestock.nisab_status = True
    if livestock.goats and livestock.goats > 40:
        calculated_livestock.goats = 1
        calculated_livestock.nisab_status = True
    if livestock.horses:
        calculated_livestock.horses = int(livestock.horses * 0.025)
        if livestock.horses > 0:
            calculated_livestock.nisab_status = True
    return calculated_livestock


@router.post("/zakat-ushr", response_model=ZakatUshrResponse)
async def calculate_zakat_ushr(request : ZakatUshrRequest):
    zakat_ushr_value = []

    for crop in request.crops:
        if not crop.is_ushr_land:
            zakat_rate = 0
        elif crop.is_irrigated:
            zakat_rate = 0.05
        else:
            zakat_rate = 0.10

        zakat_type_value = crop.quantity * zakat_rate
        zakat_ushr_value.append(ZakatUshrItem(type=crop.type, quantity=zakat_type_value))

    response = ZakatUshrResponse(zakat_ushr_value=zakat_ushr_value)

    return response

@router.get("/nisab-value", response_model=NisabValue)
async def get_nisab_value():
    nisab_value = NisabValue(nisab_value=36741)
    return nisab_value
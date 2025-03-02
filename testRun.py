import os

from apiLib import *


logger.report_name = f"reports/report_{os.path.basename(__file__)}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

with Store(base_url="https://petstore.swagger.io/v2") as test_case:
    test_case(name="Тестирование модуля Store")
    with GetStoreInventory(name='Получение запасов питомцев по статусам', base_url=test_case.base_url) as test_step:
        test_step.action_get()
        test_step.check_status_code(expected=200)
        test_step.check_pets_status(expected=1)

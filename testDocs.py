import csv


class Logger:
    def __init__(self):
        self.__report_name = None
        self.__case_result = dict()
        self.__step_result = dict()
        self.__test_case = None
        self.__fieldnames = ['test_case', 'test_step', 'action', 'params', 'check_desc', 'check_result', 'expected', 'actual', 'exc_info']

    @staticmethod
    def __check_report_name(value):
        value_parts = value.split('_')
        if len(value_parts) != 3:
            raise ValueError("Название отчета должно содержать три части: report_filename_datetime")
        return True

    def __getattr__(self, item):
        return False

    def __setattr__(self, key, value):
        if key == 'report_name' and self.__check_report_name(value):
            object.__setattr__(self, key, value)
        else:
            object.__setattr__(self, key, value)

    @property
    def report_name(self):
        return self.__report_name

    @report_name.setter
    def report_name(self, report_name):
        self.__report_name = report_name
        with open(self.__report_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.__fieldnames, delimiter=';')
            writer.writeheader()

    def __call__(self, func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if 'action' in func.__name__:
                self.__step_result.update(result)
                self.__step_result.update(kwargs)
            elif 'check' in func.__name__:
                self.__step_result.update(result)
                self.__step_result.update(kwargs)
                self.__step_result.update(self.__case_result)
                print(self.__step_result)
                with open(self.report_name, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.__fieldnames, delimiter=';')
                    writer.writerow(self.__step_result)
                self.__step_result = dict()
            elif 'testcase' in func.__doc__:
                # for step in self.case_result:
                #     # step.update(func(*args, **kwargs))
                #     print(step)
                self.__case_result['test_case'] = result['testcase']
            elif 'teststep' in func.__doc__:
                self.__step_result['test_step'] = result['test_step']
            else:
                self.__step_result.update(result)
                self.__step_result.update(kwargs)
            return func
        return wrapper


logger = Logger()


class TestCase:
    def __init__(self, parametrize=None):
        self.parametrize = parametrize
        self.name = None
        self.test_steps = []

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    @logger
    def __call__(self, name, *args, **kwargs):
        """testcase"""
        self.name = name
        return {
            "testcase": self.name
        }


class TestStep:
    def __init__(self, name):
        self.name = name

    def __enter__(self, *args, **kwargs):
        self(*args, **kwargs)
        return self

    def __exit__(self, *args, **kwargs):
        pass

    @logger
    def __call__(self, *args, **kwargs):
        """teststep"""
        # self.name = name
        # self.description = description
        return {
            "test_step": self.name
        }

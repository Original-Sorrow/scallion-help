import re
import ujson
from xml.etree import ElementTree
from tqdm import tqdm


class _xml_to_json:
    def __init__(self, mode, file):
        self.__mode = mode
        self.file = file

    @staticmethod
    def __parsing_xml(file):
        tree = ElementTree.parse(file)
        root = tree.getroot()
        d = {}
        for child in tqdm(root, desc="Просматриваю xml"):
            if child.tag not in d:
                d[child.tag] = []
            dic = {}
            for child2 in child:
                if child2.tag not in dic:
                    dic[child2.tag] = child2.text
            d[child.tag].append(dic)
        json = []
        for json_ in tqdm(d['XmlMatchOutput'], desc="Записываю в json"):
            json.append(
                dict(
                    GeneratedDate=json_["GeneratedDate"],
                    Hash=json_["Hash"],
                    PrivateKey=json_["PrivateKey"],
                    PublicModulusBytes=json_["PublicModulusBytes"],
                    PublicExponentBytes=json_["PublicExponentBytes"]
                )
            )
        return json

    def __many_files(self):
        for file in open(file=self.file, mode="r", encoding="utf-8"):
            print(file.replace("\n", ""))
            data = self.__parsing_xml(file=file.replace("\n", ""))
            new_filename = file.replace("xml", "json").replace("\n", "")
            with open(file=f'{new_filename}', mode="w") as f:
                ujson.dump(data, f, sort_keys=True, indent=4)

    def __one_file(self):
        data = self.__parsing_xml(file=self.file)
        with open(file=f"{self.file.replace('xml', 'json')}", mode="w") as f:
            ujson.dump(data, f, sort_keys=True, indent=4)

    def _main__work_file(self):
        if str(self.__mode) == "1":
            self.__one_file()
        if str(self.__mode) == "2":
            self.__many_files()


class _string_work:
    def __init__(self, mode, file):
        self.__mode = mode
        self.file = file

    @staticmethod
    def __string_count(string):
        currCh = string[:1]
        currCount = 1
        result = 0
        for ch in string[1:]:
            if ch != currCh:
                if currCount > 1:
                    result += currCount
                currCh = ch
                currCount = 1
            else:
                currCount += 1

        if currCount > 1:
            result += currCount
        return result

    def __result_from_files(self):
        for fil in open(file=self.file, mode="r", encoding="utf-8"):
            self.file = fil.replace("\n", "")
            self.__result_from_file()

    def __result_from_file(self):
        with open(file=f"{self.file.replace('xml', 'json')}", mode="r", encoding="utf-8") as file:
            json = ujson.load(file)
            data = []
            for st in tqdm(json, desc="Считаю баллы"):
                string = re.sub(r'[^\w\s]+|\d+', r'', rf'{st["Hash"].replace(".onion", "")}').strip()
                data.append(
                    dict(original_str=st["Hash"],
                         points=self.__string_count(string=string)))
        __data = sorted(data, key=lambda p: p['points'], reverse=True)
        with open(file=f"{self.file.replace('xml', 'json')}_find", mode="w") as f:
            ujson.dump(__data, f, sort_keys=True, indent=4)

    def _main__string(self):
        if str(self.__mode) == "1":
            self.__result_from_file()
        if str(self.__mode) == "2":
            self.__result_from_files()


class main(_string_work, _xml_to_json):
    def __init__(self):
        self.__action_choice = input(
            "1) Домены из файла в json\n"
            "2) Поиск красивого домена\n"
            "3) Всё и сразу\n\n"
            ">> "
        )
        if str(self.__action_choice) != "1" and str(self.__action_choice) != "2" and str(self.__action_choice) != "3":
            print("Выбран неверный вариант")
            return
        self.__mode_input = input(
            "1) Один файл\n"
            "2) Несколько файлов из списка\n\n"
            ">> "
        )
        if str(self.__mode_input) != "1" and str(self.__mode_input) != "2":
            print("Выбран неверный вариант")
            return
        self.__file = input("Путь к файлу: ")
        _string_work.__init__(self, mode=self.__mode_input, file=self.__file)
        _xml_to_json.__init__(self, mode=self.__mode_input, file=self.__file)
        if str(self.__action_choice) == "1":
            super()._main__work_file()
            return
        elif str(self.__action_choice) == "2":
            super()._main__string()
            return
        elif str(self.__action_choice) == "3":
            super()._main__work_file()
            super()._main__string()
            return


if __name__ == "__main__":
    main()

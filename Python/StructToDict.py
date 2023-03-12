class StructToDict:
    def __init__(self, string: str):
        # 保存结构体字符串
        self.str_struct = string.strip()
        # 初步处理的结果列表
        self.struct_list_old = []
        # 简化处理的结果列表，仅保留变量名和对应的大小
        self.struct_list_new = []
        # 基础类型及其大小的对应关系
        self.base_type_list = [
            {8: ['char', 'unsigned char', 'BYTE']},
            {16: ['short', 'unsigned short', 'WORD16', 'SWORD16']},
            {32: ['int', 'unsigned int', 'WORD32', 'SWORD32']},
            {64: ['long', 'unsigned long', 'WORD64', 'SWORD64']}
        ]

    # 消除非static警告
    def remove_warning(self):
        pass

    # 获取当前类型的大小，基础类型返回大小，非基础类型返回-1，可用于判断是否为基础类型
    def get_type_size(self, string: str) -> int:
        for base_type in self.base_type_list:
            for size, type_list in base_type.items():
                if type_list.count(string) != 0:
                    return size
        return -1

    # 获取已知的结构体的名称，因为一个结构体可能有多个名称，因此返回列表
    def get_struct_list_new_keys(self) -> list:
        base_list = []
        for item in self.struct_list_new:
            for key in item.keys():
                base_list += key.split(' ')
        return base_list

    # 按结构体拆分字符串，返回结构体列表
    def split_str_by_struct(self, string: str) -> list:
        self.remove_warning()
        result_list = []
        while string.find('}') != -1:
            result_list.append(string[:string.find(';', string.find('}')) + 1])
            string = string[string.find(';', string.find('}')) + 1:]
        return result_list

    # 获取结构体名称，一个结构体可能有多个名称，返回列表
    def get_struct_name(self, string: str) -> list:
        self.remove_warning()
        result_list = []
        # 0个或1个
        first = string[string.find('struct') + len('struct'):string.find('{')].strip()
        # 可能有多个，用逗号隔开
        second = string[string.rfind('}') + 1:string.rfind(';')].strip().split(',')
        second.append(first)
        for item in second:
            if item.strip() == '':
                continue
            result_list.append(item.strip())
        return result_list

    # 获取结构体变量的名称、类型、大小、是否为数组
    def get_struct_para(self, string: str) -> dict:
        result_dict = {}
        string = string[string.find('{') + 1:string.rfind('}')].strip()
        for item in string.split(';'):
            if item.strip() == '':
                continue
            # 数组类型
            if item.strip().find('[') != -1:
                result_dict[item[item.rfind(' '):item.rfind('[')].strip()] = {
                    "type": item[:item.rfind(' ')].strip(),
                    "size": self.get_type_size(item[:item.rfind(' ')].strip()),
                    "arr_len": int(item[item.find('[') + 1:item.find(']')])
                }
            # 位域
            elif item.strip().find(':') != -1:
                result_dict[item[item.rfind(' '):item.rfind(':')].strip()] = {
                    "type": item[:item.rfind(' ')].strip(),
                    "size": int(item[item.rfind(':') + 1:].strip()),
                    "arr_len": 1
                }
            # 普通类型
            else:
                result_dict[item[item.rfind(' '):].strip()] = {
                    "type": item[:item.rfind(' ')].strip(),
                    "size": self.get_type_size(item[:item.rfind(' ')].strip()),
                    "arr_len": 1
                }
        return result_dict

    # 当前结构体的大小是否可以确定，确定条件: 该结构体的所有元素的大小已知(基础类型或对应类型的结构体大小已知)
    def is_struct_can_be_simplify(self, struct: dict) -> bool:
        for para in struct['struct_para'].values():
            if not (self.get_type_size(para['type']) != -1 or self.get_struct_list_new_keys().count(para['type']) != 0):
                return False
        return True

    # 简化结构体
    def simplify_structure_content(self, struct: dict) -> dict:
        struct_name = ''
        for item in struct['struct_name']:
            struct_name += item + ' '
        struct_name = struct_name.strip()
        result_dict = {struct_name: {}}

        for key, value in struct['struct_para'].items():
            if self.get_type_size(value['type']) != -1:
                result_dict[struct_name][key] = value['size'] * value['arr_len']
            else:
                for i in range(len(self.struct_list_new)):
                    for j in self.struct_list_new[i].keys():
                        if j.find(value['type']) != -1:
                            if value['arr_len'] == 1:
                                result_dict[struct_name][key] = self.struct_list_new[i][j]
                            else:
                                arr = []
                                for k in range(value['arr_len']):
                                    arr.append(self.struct_list_new[i][j])
                                result_dict[struct_name][key] = arr
        return result_dict

    # 将结构体合并
    def merge_struct(self):
        while len(self.struct_list_old) != 0:
            need_del = []
            for i in range(len(self.struct_list_old)):
                if self.is_struct_can_be_simplify(self.struct_list_old[i]):
                    self.struct_list_new.append(self.simplify_structure_content(self.struct_list_old[i]))
                    need_del.append(i)
            for i in need_del:
                del self.struct_list_old[i]

    # 解析每个结构体，获取结构体名称和内容
    def convert_str_to_dict(self):
        for item in self.split_str_by_struct(self.str_struct):
            self.struct_list_old.append({
                "struct_name": self.get_struct_name(item),
                "struct_para": self.get_struct_para(item)
            })

    def all_step(self) -> dict:
        self.convert_str_to_dict()
        self.merge_struct()
        return self.struct_list_new[len(self.struct_list_new) - 1]


# 将结构体字符串转化为字典
def transform(str_struct: str) -> dict:
    return StructToDict(str_struct).all_step()

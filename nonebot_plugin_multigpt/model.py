import os
import json

class JsonDataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_from_file()

    def _load_from_file(self):
        """从JSON文件中加载数据到内存"""
        if not os.path.exists(self.file_path):
            return {}  # 如果文件不存在，返回一个空字典
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)  # 加载并返回JSON数据

    def get_entry(self, entry_id, default=None):
        """获取特定ID的条目，如果不存在则返回默认值"""
        return self.data.get(entry_id, default)

    def set_entry(self, entry_id, key, value):
        """设置特定ID的条目的键值，如果条目不存在则创建它"""
        if entry_id not in self.data:
            self.data[entry_id] = {}
        self.data[entry_id][key] = value

    def save_to_file(self):
        """将内存中的数据保存到JSON文件"""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

file_path = os.path.join("data", "gptmodel.json")
manager = JsonDataManager(file_path)
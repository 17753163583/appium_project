import json

from Common.logger import log_decorator
from logger import logger

data_key_json_file_name = '../TestData/data_key_dict.json'


@log_decorator
def append_data_key_to_json(publish, data_key):
    with open(data_key_json_file_name, 'r', encoding='utf-8') as f:
        json_data_dict = json.load(f)
        publish_value = json_data_dict[publish]

        publish_value.append({"data_key": data_key, "start_time": "", "end_time": ""})
    with open(data_key_json_file_name, 'w', encoding='utf-8') as f:
        json.dump(json_data_dict, f)
        logger.info("惩罚信息已在文件中创建")


@log_decorator
def remove_data_key_to_json(publish, data_key):
    with open(data_key_json_file_name, 'r', encoding='utf-8') as f:
        json_data_dict = json.load(f)
        publish_value_dict_list = json_data_dict[publish]
        for publish_dict in publish_value_dict_list:
            if publish_dict['data_key'] == data_key:
                publish_value_dict_list.remove(publish_dict)

                with open(data_key_json_file_name, 'w', encoding='utf-8') as f:
                    json.dump(json_data_dict, f)
                    logger.info("惩罚信息已在文件中删除")


if __name__ == '__main__':
    create_data_key_dict()
    append_data_key_to_json('is_forbid_speak', '1')
    # remove_data_key_to_json('is_forbid_speak', '1')

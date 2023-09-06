import functools
import re


class StringUtil:
    @staticmethod
    def float_to_str(number: float):
        return "{0:0.2f}".format(number)

    @staticmethod
    @functools.lru_cache(maxsize=114514)
    def get_cleaned_question(question):
        # 问题清洗,去无关标点
        punc = [
            # "，",
            # ",",
            # "。",
            # ".",
            # "？",
            # "?",
            # "!",
            # "！",  # 全角和半角的标点
            # "“", "”", "\"", '\'', '’', '‘', '(', ")", '（', "）", "：", "；", ":", ";", '{', "}", '「', "」",  # 全角和半角的分隔符
            "\n",
            "\t",
            "\r",  # 几乎可以理解为用户的恶意输入
        ]
        new_text = [w for w in question if w not in punc]
        question_cleaned = "".join(new_text)

        # 全 / 半角符号清洗
        puncs_to_fix = {
            "：": ":",
            "；": ";",
            "“": '"',
            "”": '"',
            "（": "(",
            "）": ")",
            "「": "{",
            "」": "}",
        }

        for key, value in puncs_to_fix.items():
            question_cleaned = re.sub(key, value, question_cleaned)

        return question_cleaned

    @staticmethod
    def convert_to_full_width_char(unicode_str: str, reverse=False):
        """
        把字符从半角转换成全角(if applicable, 如果已经是全角了就不管了)
        Args:
            unicode_str: 原始输入(必须是长度为1的str, 代表char, 因为Python没有原生的char)
            reverse: 是否反过来转换 (即全角转半角)
        Returns:
            全角字符。
        """
        # 咋整进来了个string,我们要char!!!
        if len(unicode_str) > 1:
            return unicode_str

        # 数字和百分比都不管
        if (
            unicode_str.isalnum()
            or unicode_str == "."
            or unicode_str == "%"
            or unicode_str == "-"
        ):
            return unicode_str

        inside_code = ord(unicode_str)

        # 半角转全角
        if not reverse:
            if inside_code < 0x0020 or inside_code > 0x7E:  # 不是半角字符就返回原来的字符
                return unicode_str
            if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为: 半角 = 全角 - 0xfee0
                inside_code = 0x3000
            else:
                inside_code += 0xFEE0
        # 全角转半角
        else:
            if inside_code == 0x3000:
                inside_code = 0x0020
            else:
                inside_code -= 0xFEE0
            if inside_code < 0x0020 or inside_code > 0x7E:  # 转完之后不是半角字符返回原来的字符
                return unicode_str

        return chr(inside_code)

    @staticmethod
    @functools.lru_cache(16384)
    def get_jaccard_similarity(left_str: str = None, right_str: str = None):
        left_str = set(left_str)
        right_str = set(right_str)

        return len(left_str & right_str) / len(left_str | right_str)

    @staticmethod
    @functools.lru_cache
    def wash_str_wo_chn_puncs(old_str: str):
        # 全 / 半角符号清洗
        puncs_to_fix = {
            "：": ":",
            "；": ";",
            "“": '"',
            "”": '"',
            "（": "(",
            "）": ")",
            "「": "{",
            "」": "}",
        }
        old_str = str(old_str)

        for key, value in puncs_to_fix.items():
            old_str = re.sub(key, value, old_str)

        return old_str

    @staticmethod
    @functools.lru_cache
    def is_chinese(uchar):
        return True if "\u4e00" <= uchar <= "\u9fa5" else False

    @staticmethod
    @functools.lru_cache
    def reserve_chinese_chars(content):
        """
        筛去所有不是中文的字符，返回过滤后的字符串
        Args:
            content:

        Returns:过滤后的字符串。
        """
        return "".join([char for char in content if Util.is_chinese(char)])

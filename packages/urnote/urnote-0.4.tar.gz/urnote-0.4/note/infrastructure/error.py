from note.infrastructure import config


class ErrorMessage:
    def __init__(self, description, solution):
        self.description = description
        self.solution = solution

    def format(self, error):
        description = self.description(self=error) if hasattr(
            self.description, '__call__') else self.description
        solution = self.solution(self=error) if hasattr(
            self.solution, '__call__') else self.solution
        return description, solution


class AppError(Exception):
    def __init__(self, msg):
        self.msg = msg

    @property
    def message(self):
        return self.message


class UserError(Exception):
    def __init__(self):
        self.msg = None

    @property
    def message(self) -> tuple:
        """
        Returns:
            (描述，解决方案)
        """
        return self.msg.format(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FileContentError(UserError):
    WRONG_GRADE = ErrorMessage(
        description=(
            '错误命令"{self.grade}"\n'
            '位置:{self.location}[{self.question}]'.format),
        solution='输入"{name} --docs"查看使用说明'.format(
            name=config.APP_NAME)
    )

    WRONG_FILE_ENCODING = ErrorMessage(
        description='文件"{self.location}"无法打开'.format,
        solution='使用UTF-8编码的文件,或者修改"./NOTE/ignore.default"文件忽略'
    )

    @classmethod
    def wrong_command(cls, location=None, question=None, grade=None):
        return cls(cls.WRONG_GRADE, location, question, grade)

    @classmethod
    def wrong_encoding(cls, location=None):
        return cls(cls.WRONG_FILE_ENCODING, location)

    def __init__(self, error_msg, location=None, question=None,
                 grade=None):
        self.msg = error_msg

        self.location = location

        self.question = question
        self.grade = grade


class ArgParserError(UserError):
    def __init__(self, message):
        self._message = message

    @property
    def message(self) -> tuple:
        solution = '输入"{} --help"查看帮助信息'.format(config.APP_NAME)
        return self._message, solution


class CMDError(UserError):
    INIT_CMD_ERROR = ErrorMessage(
        description=(
            '无法使用命令"init"创建重复或嵌套的工作空间,'
            '已存在工作空间:{self.root_dir}'.format),
        solution=''
    )

    UNINITIALIZED = ErrorMessage(
        description='未找到工作空间',
        solution='使用命令"{app_name} init"创建工作空间'.format(
            app_name=config.APP_NAME)
    )

    PURGE_EXIST_BUT_NOT_EMPTY = ErrorMessage(
        description='{purge_path}目录已存在且不为空'.format(
            purge_path=config.PURGE_DIR_NAME),
        solution='手动清空{purge_path}目录'.format(
            purge_path=config.PURGE_DIR_NAME)
    )

    FILE_NOT_IN_CURRENT_WORKSPACE = ErrorMessage(
        description='目标路径不在工作空间中',
        solution=''
    )

    @classmethod
    def duple_init(cls, root_dir):
        return cls(cls.INIT_CMD_ERROR, root_dir=root_dir)

    @classmethod
    def uninitialized(cls):
        return cls(cls.UNINITIALIZED)

    @classmethod
    def purge_exist_but_not_empty(cls):
        return cls(cls.PURGE_EXIST_BUT_NOT_EMPTY)

    @classmethod
    def file_not_in_current_workspace(cls):
        return cls(cls.FILE_NOT_IN_CURRENT_WORKSPACE)

    def __init__(self, error_msg=None, root_dir=None):
        self.msg = error_msg
        self.root_dir = root_dir

    @property
    def message(self) -> tuple:
        return super().message

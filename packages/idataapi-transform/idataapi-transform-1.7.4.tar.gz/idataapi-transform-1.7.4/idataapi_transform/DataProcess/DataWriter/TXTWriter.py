import logging
from .BaseWriter import BaseWriter


class TXTWriter(BaseWriter):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.f_out = open(config.filename, config.mode, encoding=config.encoding)
        self.total_miss_count = 0
        self.success_count = 0

    def write(self, responses):
        miss_count = 0
        for each_response in responses:
            if self.config.expand:
                each_response = self.expand_dict(each_response, max_expand=self.config.expand)

            if self.config.filter:
                each_response = self.config.filter(each_response)
                if not each_response:
                    miss_count += 1
                    continue

            self.f_out.write(self.config.join_val.join(str(value) for value in each_response.values()) + self.config.new_line)
            self.success_count += 1

        self.total_miss_count += miss_count
        logging.info("%s write %d item, filtered %d item" % (self.config.filename, len(responses), miss_count))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f_out.close()
        logging.info("%s write done, total filtered %d item, total write %d item" %
                     (self.config.filename, self.total_miss_count, self.success_count))

    def __enter__(self):
        return self

"""Implementation of Parser to parse experiment from the logs."""

import glob
from typing import Optional

from ml_logger.parser import base as base_parser
from ml_logger.parser.config import (
    parse_json_and_match_key as default_config_line_parser,
)
from ml_logger.parser.experiment.experiment import Experiment
from ml_logger.parser.metric import metrics_to_df
from ml_logger.parser.metric import (
    parse_json_and_match_key as default_metric_line_parser,
)
from ml_logger.types import LogType, ParseLineFunctionType


class Parser(base_parser.Parser):
    """Class to parse an experiment from the log dir."""

    def __init__(
        self,
        parse_config_line: ParseLineFunctionType = default_config_line_parser,
        parse_metric_line: ParseLineFunctionType = default_metric_line_parser,
    ):
        """Class to parse experiment from the logs.

        Args:
            parse_config_line (ParseLineFunctionType):
                Function to parse a config line in the log file. The function
                should return None if the line is not a valid config log
                (eg error messages)
            parse_metric_line (ParseLineFunctionType):
                Function to parse a metric line in the log file. The function
                should return None if the line is not a valid metric log
                (eg error messages)
        """
        self.log_key = "logbook_type"
        self.log_type = "experiment"
        self.parse_line = self._wrap_parse_line(parse_config_line, parse_metric_line)

    def _wrap_parse_line(
        self,
        parse_config_line: ParseLineFunctionType,
        parse_metric_line: ParseLineFunctionType,
    ) -> ParseLineFunctionType:
        def fn(line: str) -> Optional[LogType]:
            log = parse_config_line(line)
            if log is not None:
                if self.log_key not in log:
                    log[self.log_key] = "config"
            else:
                log = parse_metric_line(line)
                if log is not None and self.log_key not in log:
                    log[self.log_key] = "metric"
            return log

        return fn

    def parse(self, filepath_pattern: str) -> Experiment:
        """Load one experiment from the log dir.

        Args:
            filepath_pattern (str): filepath pattern to glob
        Returns:
            Experiment
        """
        configs = []
        metric_logs = []
        paths = glob.glob(filepath_pattern)
        for file_path in paths:
            for log in self._parse_file(file_path=file_path):
                # At this point, if log is not None, it will have a key self.log_key
                if log is not None:
                    if log[self.log_key] == "config":
                        configs.append(log)
                    elif log[self.log_key] == "metric":
                        metric_logs.append(log)
        if len(configs) == 0:
            config = None
        else:
            config = configs[-1]
        return Experiment(
            config=config, metrics=metrics_to_df(metric_logs=metric_logs), info={},
        )

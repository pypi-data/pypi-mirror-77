from configparser import ConfigParser
from os.path import dirname, basename
from pathlib import Path

from simses.analysis.analysis_factory import AnalysisFactory
from simses.analysis.evaluation.evaluation import Evaluation
from simses.analysis.evaluation.evaluation_merger import EvaluationMerger
from simses.commons.log import Logger
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig
from simses.constants_simses import BATCH_DIR


class StorageAnalysis:

    def __init__(self, path: str, config: ConfigParser):
        self.__path: str = path
        self.__batch_path: str = str(Path(self.__path).parent).replace('\\','/') + '/' + BATCH_DIR
        self.__simulation_name: str = basename(dirname(self.__path))
        self.__log: Logger = Logger(__name__)
        self.__config: GeneralAnalysisConfig = GeneralAnalysisConfig(config)
        self.__analysis_config: ConfigParser = config

    def run(self):
        result_path: str = self.__config.get_result_for(self.__path)
        factory: AnalysisFactory = AnalysisFactory(result_path, self.__analysis_config)
        evaluations: [Evaluation] = factory.create_evaluations()
        evaluation_merger: EvaluationMerger = factory.create_evaluation_merger()
        files_to_transpose: [str] = list()
        self.__log.info('Entering analysis')
        for evaluation in evaluations:
            self.__log.info('Running evaluation ' + type(evaluation).__name__)
            evaluation.run()
            evaluation.write_to_csv(result_path)
            evaluation.write_to_batch(path=self.__batch_path, name=self.__simulation_name,
                                      run=basename(dirname(result_path)))
            files_to_transpose.extend(evaluation.get_files_to_transpose())
            evaluation.close()
        Evaluation.transpose_files(files_to_transpose)
        self.__config.write_config_to(result_path)
        evaluation_merger.merge(evaluations)
        factory.close()
        self.close()

    def close(self):
        self.__log.close()

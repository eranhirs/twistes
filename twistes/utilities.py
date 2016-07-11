from twistes.consts import EsConst
from twistes.exceptions import ScanError


class EsUtils(object):

    @staticmethod
    def extract_hits(results):
        EsUtils.validate_scan_result(results)
        if EsUtils.has_results(results):
            return results[EsConst.HITS][EsConst.HITS]
        else:
            return []

    @staticmethod
    def has_results(results):
        return results and \
               EsConst.HITS in results and \
               EsConst.HITS in results[EsConst.HITS] and \
               EsConst.TOTAL in results[EsConst.HITS] and \
               results[EsConst.HITS][EsConst.TOTAL] > 0 and \
               results[EsConst.HITS][EsConst.HITS]

    @staticmethod
    def is_get_query_with_results(results):
        """
        :param results: the response from Elasticsearch
        :return: true if the get query returned a result, false otherwise
        """
        return results and EsConst.FOUND in results and results[EsConst.FOUND] and EsConst.FIELDS in results

    @staticmethod
    def validate_scan_result(results):
        """ Check if there's a failed shard in the scan query"""
        if results[EsConst.SHARDS][EsConst.FAILED] and results[EsConst.SHARDS][EsConst.FAILED] > 0:
            raise ScanError(
                'Scroll request has failed on %d shards out of %d.' %
                (results[EsConst.SHARDS][EsConst.FAILED], results[EsConst.SHARDS][EsConst.TOTAL])
            )

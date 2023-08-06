from malaya.path import PATH_SUMMARIZE, S3_PATH_SUMMARIZE
from malaya.supervised import t5 as t5_load
from herpetologist import check_type
import os

_t5_availability = {
    'small': [
        '122MB',
        'ROUGE-1: 0.33854',
        'ROUGE-2: 0.14588',
        'ROUGE-L: 0.23528',
    ],
    'base': [
        '448MB',
        'ROUGE-1: 0.34103',
        'ROUGE-2: 0.14994',
        'ROUGE-L: 0.23655',
    ],
}


def available_t5():
    """
    List available T5 models.
    """
    return _t5_availability


@check_type
def t5(model: str = 'base', compressed: bool = True, **kwargs):

    """
    Load T5 model to generate a summary given a string.

    Parameters
    ----------
    model : str, optional (default='base')
        Model architecture supported. Allowed values:

        * ``'base'`` - T5 Base parameters.
        * ``'small'`` - T5 Small parameters.

    compressed: bool, optional (default=True)
        Load compressed model, but this not able to utilize malaya-gpu function. 
        This only compressed model size, but when loaded into VRAM / RAM, size uncompressed and compressed are the same.

    Returns
    -------
    result: malaya.model.t5.SUMMARIZATION class
    """

    model = model.lower()
    if model not in _t5_availability:
        raise Exception(
            'model not supported, please check supported models from malaya.summarization.abstractive.available_t5()'
        )

    from malaya.model.t5 import SUMMARIZATION

    return t5_load.load(
        path = PATH_SUMMARIZE,
        s3_path = S3_PATH_SUMMARIZE,
        model = model,
        model_class = SUMMARIZATION,
        compressed = compressed,
        **kwargs,
    )

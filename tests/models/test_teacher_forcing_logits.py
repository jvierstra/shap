""" This file contains tests for the TeacherForcingLogits class.
"""

import numpy as np
import pytest

import shap


def test_method_get_teacher_forced_logits_for_encoder_decoder_model():
    """ Tests if get_teacher_forced_logits() works for encoder-decoder models.
    """

    transformers = pytest.importorskip("transformers")
    requests = pytest.importorskip("requests")

    name = "hf-internal-testing/tiny-random-BartModel"
    try:
        tokenizer = transformers.AutoTokenizer.from_pretrained(name)
        model = transformers.AutoModelForSeq2SeqLM.from_pretrained(name)
    except requests.exceptions.RequestException:
        pytest.xfail(reason="Connection error to transformers model")

    wrapped_model = shap.models.TeacherForcing(model, tokenizer, device='cpu')

    source_sentence = np.array(["This is a test statement for verifying working of teacher forcing logits functionality"])
    target_sentence = np.array(["Testing teacher forcing logits functionality"])

    # call the get teacher forced logits function
    logits = wrapped_model.get_teacher_forced_logits(source_sentence, target_sentence)

    assert not np.isnan(np.sum(logits))

def test_method_get_teacher_forced_logits_for_decoder_model():
    """ Tests if get_teacher_forced_logits() works for decoder only models.
    """

    transformers = pytest.importorskip("transformers")
    requests = pytest.importorskip("requests")

    name = "hf-internal-testing/tiny-random-gpt2"
    try:
        tokenizer = transformers.AutoTokenizer.from_pretrained(name)
        model = transformers.AutoModelForCausalLM.from_pretrained(name)
    except requests.exceptions.RequestException:
        pytest.xfail(reason="Connection error to transformers model")

    model.config.is_decoder = True

    wrapped_model = shap.models.TeacherForcing(model, tokenizer, device='cpu')

    source_sentence = np.array(["This is a test statement for verifying"])
    target_sentence = np.array(["working of teacher forcing logits functionality"])

    # call the get teacher forced logits function
    logits = wrapped_model.get_teacher_forced_logits(source_sentence, target_sentence)

    assert not np.isnan(np.sum(logits))

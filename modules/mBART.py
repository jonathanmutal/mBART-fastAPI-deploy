import torch

from settings.settings import logger
from typing import List, Dict

from transformers import (AutoConfig,
                          MBartForConditionalGeneration,
                          MBart50TokenizerFast)


if torch.cuda.is_available():
    logger.info("A gpu is detected.")
    logger.info(f"There are {torch.cuda.device_count()} GPUs availables")
    logger.info(f"we are using {torch.cuda.get_device_name(0)}")
    device = torch.device(0)


class mBART:
    def __init__(self, configuration: Dict[str, str]):
        """
        The init method.
        configuration: it's a dictionary where contains some of the hyperparameters on decoding.
        """
        self.config = configuration
        self.config += AutoConfig.from_pretrained(self.config["model_path"])
        self.model = MBartForConditionalGeneration.from_pretrained(self.config["model_path"])
        self.tokenizer = MBart50TokenizerFast.from_pretrained(self.config["model_path"], use_fast=True)
        logger.info(self.tokenizer.src_lang)
        # if we want to use a GPU
        if self.config['GPU']:
            if torch.cuda.is_available():
                # we load the model in the GPU.
                self.init_to_gpu()
                logger.info("A gpu is used to inference the model.")
            else:
                # if there is no GPU available, we set GPU to false
                self.config["GPU"] = False
        logger.info("The model is initialized")

    def init_to_gpu(self):
        """
        Load the model into GPU and put it in eval mode (see more pytorch).
        """
        self.model.to(device)
        self.model.eval()

    def pre_process(self, input: List[str]) -> List[str]:
        """
        Pre-process the input. You can change the method if you need any pre-processing.
        """
        return input

    def translate(self, input: List[str]) -> List[str]:
        """
        Translate the input to the target language (set on the configuration file .yml).
        """
        encoded_gsw = self.tokenizer(
                        self.pre_process(input),
                        return_tensors="pt",
                        truncation=True,
                        padding=True,
                        max_length=self.conf.max_length
                    )

        if self.config["GPU"]:
            # we put the matrix into the GPU.
            encoded_gsw.to(device)

        # we generate the tokens.
        generated_tokens = self.model.generate(
            **encoded_gsw,
            num_beams=self.config["num_beams"]
        )

        return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

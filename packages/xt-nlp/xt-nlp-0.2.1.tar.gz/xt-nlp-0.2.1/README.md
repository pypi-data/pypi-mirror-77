# xt-nlp

This directory includes the most recent and complete version of the BERT model training code (April 30th 2019). 

## Training NLP Model

### Usage

To train a new BERT model, complete the following steps:

1. __Choose which model you plan to train:__

    * Standard BERT-Base-Uncased, BERT-Large-Cased. etc.
        * Recommend using BERT-Base-Uncased: Base is avoid space problems, uncased yields better results
    * BioBERT (Three different versions: PubMed, PMC, PubMed + PMC)
        * Recommend using PubMed + PMC. Find models [here](https://github.com/naver/biobert-pretrained). Model also downloaded in INSERT DIR
    * SciBERT
    * Already partially finetuned model (from above) 
  
2. __Specify the file path for the following files below:__ Note that Standard BERT models are downloaded to a cache directory with `pytorch-pretrained-bert`

    * If fintuning set `s.finetune` boolean to `True`. The following settings depend on the specific model used
        - `s.model_config_file` : name of model config file for training from fine tuned model
        - `s.model_checkpoint_file` : name of `.bin` file for training from fine tuned model
    * Standard BERT:
        - `s.model_type`: set to `bert-base-uncased` etc.
        - `s.bert_standard_cache`: set to path you want to download the pretrained weight to. Note this is optional. If left empty, the weights will download to a default location in the `pytorch-pretrained-bert` library. 
    * BioBERT:
        - `s.model_type`: set to `biobert`
        - `s.biobert_raw_model_path`: path of converted biobert model (see [Converting BioBERT from TF to PyTorch](#Converting-BioBERT-from-TF-to-PyTorch)
        - `s.biobert_vocab_path`: path of `vocab.txt` for BioBERT model
    * SciBERT: 
        - currently not supported

3. __Specify output directories for the model, log and results files.__ Look at the `out_path` and `log_path` varibles in `run_train.py`. A new folder will be created in these directories for each run. Folder names follow the `new_folder` varible in `run_train.py`. The following files are created each run:

    * `models/[new folder]/ans_type.pkl` : list of strings containing all answer types for the run. This file is important! It specifies the order of the answer types!
    * `models/[new folder]/config.json` : See above
    * `models/[new folder]/hyperparams.json` : JSON of all values of SESSettings object for train
    * `models/[new folder]/pytorch_model_END.bin` : Model saved at the end of training
    * `models/[new folder]/pytorch_model_END.bin` : Model saved after epoch with highest f1 validation score
    * `models/[new folder]/results_[all answer types]_enum[epoch number].txt` : Text results of all answers over all epochs in all validation examples. The file contains the original text, following by the top predictions. Each prediction has the start and end logit raw score, as well as predicted final answer. 

4. __Load the data you plan to annotate.__ The `run_train.py` file depends on loading whatever your example text is into a list of SESExample objects. These functions are defined in `data_loader_main.py`. These functions are called in `get_examples()` in `utils.py`. Depending on your data, you may need to change the function in `get_examples()` or write your own. Some of the functions in `data_loader_main.py` are as follows:
    * `brat_read_select`: Only reads brat annotations of answer types in the argument answer set
    * `brat_read_everything`: Reads all answer types in brat annotation files
 
 5. __Choose run hyperparameters.__ The file `run_train.py` is setup for hyperparameter optimization.
 
 6. __Run the training__. From the root directory of the this repo, run `python run_train.py`

## Inference with BERT

### Usage

1. __Choose which model you plan to train:__

    * For a stanard BERT model,set `s.model_type` to be 'bert-standard'. 
    * For a BioBERT model, set `s.model_type` to be 'biobert'.
   
2. __Specify the file path for the following files below:__ Note that Standard BERT models are downloaded to a cache directory with `pytorch-pretrained-bert`

    * `s.model_config_file` : path of model config file for training from fine tuned model
    * `s.model_checkpoint_file` : path of `.bin` file for training from fine tuned model
    * `s.model_ans_list_file` : path of `ans_type.pkl` file containing answers types of model 

3. __Run (or call) `run_infer`.__ This  function will return character level logits for the string input.  

## Converting-BioBERT-from-TF-to-PyTorch

When downloading BioBERT from [repo](https://github.com/naver/biobert-pretrained), you must convert the TF checkpoint to a pytorch model. See this [post](https://github.com/huggingface/pytorch-pretrained-BERT/issues/312#issuecomment-472237583)

## Extensions and ToDo

 - Train model from SciBERT baseline and look for improvements.
 - Masking of tokens in finetuning. By masking tokens (replacement with random words and [MASK] token) in the answer/all text, the model should hopefully learn to use the context around the answers to infer what the correct answer is. This prevents the model learning to lookup vocabulary when training on small datasets.
 - Testing different types of layers/network sizes on the last layer of BERT's output. Currently we have multiple fully connected layers for each token. Layers are of size (0 to the length of ans_type). Deeper networks or other architectures might allow for BERT to answer 20+ different types of answer types without losing accuracy. 
 
 ## Datasets and Models

- `coop_spring2019/josh/data_sender_address_total_BRAT_DATASET` : contains brat annotation and txt files for labels of data, sender, address, and total in receipts. The text extraction and original receipts can be found in `coop_spring2019/josh/pdf_xtract_text`. 

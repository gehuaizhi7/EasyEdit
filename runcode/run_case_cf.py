import os
import os.path
import sys
import json
import random
sys.path.append('..')
from easyeditor import (
    FTHyperParams, 
    IKEHyperParams, 
    KNHyperParams, 
    MEMITHyperParams, 
    ROMEHyperParams, 
    LoRAHyperParams,
    MENDHyperParams,
    SERACHparams
    )
from easyeditor import BaseEditor
from easyeditor.models.ike import encode_ike_facts
from sentence_transformers import SentenceTransformer
from easyeditor import KnowEditDataset

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--editing_method', required=True, type=str)
    parser.add_argument('--hparams_dir', required=True, type=str)
    parser.add_argument('--data_dir', required=True, type=str)
    parser.add_argument('--ds_size', default=None, type=int)
    parser.add_argument('--metrics_save_dir', default='./output', type=str)
    parser.add_argument('--datatype', default=None,type=str)
    parser.add_argument('--train_data_path', type=str)
    parser.add_argument('--pre_file', default='./seq_pre.json', type=str)

    args = parser.parse_args()

    if args.editing_method == 'FT':
        editing_hparams = FTHyperParams
    elif args.editing_method == 'IKE':
        editing_hparams = IKEHyperParams
    elif args.editing_method == 'KN':
        editing_hparams = KNHyperParams
    elif args.editing_method == 'MEMIT':
        editing_hparams = MEMITHyperParams
    elif args.editing_method == 'ROME':
        editing_hparams = ROMEHyperParams
    elif args.editing_method == 'LoRA':
        editing_hparams = LoRAHyperParams
    elif args.editing_method == 'MEND':
        editing_hparams = MENDHyperParams
    else:
        raise NotImplementedError





  

    # datas = KnowEditDataset(args.data_dir,size=args.ds_size)
    # if args.datatype == 'counterfact' or args.datatype == 'recent' or args.datatype == 'zsre':
    #     prompts=[data['prompt'] for data in datas]
    #     subjects=[data['subject'] for data in datas]
    #     target_new = [data['target_new'] for data in datas]
        
    #     portability_r =[data['portability_r'] for data in datas]
    #     portability_s =[data['portability_s'] for data in datas]
    #     portability_l =[data['portability_l'] for data in datas]

    #     portability_reasoning_prompts=[]
    #     portability_reasoning_ans=[]
    #     portability_Logical_Generalization_prompts=[]
    #     portability_Logical_Generalization_ans=[]
    #     portability_Subject_Aliasing_prompts=[]
    #     portability_Subject_Aliasing_ans=[]
        
    #     portability_data = [portability_r,portability_s,portability_l]
    #     portability_prompts = [portability_reasoning_prompts,portability_Subject_Aliasing_prompts,portability_Logical_Generalization_prompts]
    #     portability_answers = [portability_reasoning_ans,portability_Subject_Aliasing_ans,portability_Logical_Generalization_ans]
    #     for data, portable_prompts, portable_answers in zip(portability_data,portability_prompts,portability_answers):
    #         for item in data:
    #             if item is None:
    #                 portable_prompts.append(None)
    #                 portable_answers.append(None)
    #             else:
    #                 temp_prompts = []
    #                 temp_answers = []
    #                 for pr in item:
    #                     prompt=pr["prompt"]
    #                     an=pr["ground_truth"]
    #                     while isinstance(an,list):
    #                         an = an[0]
    #                     if an.strip() =="":
    #                         continue
    #                     temp_prompts.append(prompt)
    #                     temp_answers.append(an)
    #                 portable_prompts.append(temp_prompts)
    #                 portable_answers.append(temp_answers)
    #     assert len(prompts) == len(portability_reasoning_prompts) == len(portability_Logical_Generalization_prompts) == len(portability_Subject_Aliasing_prompts)
        
    #     locality_rs = [data['locality_rs'] for data in datas]
    #     locality_f = [data['locality_f'] for data in datas]
    #     locality_Relation_Specificity_prompts=[]
    #     locality_Relation_Specificity_ans=[]
    #     locality_Forgetfulness_prompts=[]        
    #     locality_Forgetfulness_ans=[]
        
    #     locality_data = [locality_rs, locality_f]
    #     locality_prompts = [locality_Relation_Specificity_prompts,locality_Forgetfulness_prompts]
    #     locality_answers = [locality_Relation_Specificity_ans,locality_Forgetfulness_ans]
    #     for data, local_prompts, local_answers in zip(locality_data,locality_prompts,locality_answers):
    #         for item in data:
    #             if item is None:
    #                 local_prompts.append(None)
    #                 local_answers.append(None)
    #             else:
    #                 temp_prompts = []
    #                 temp_answers = []
    #                 for pr in item:
    #                     prompt=pr["prompt"]
    #                     an=pr["ground_truth"]
    #                     while isinstance(an,list):
    #                         an = an[0]
    #                     if an.strip() =="":
    #                         continue
    #                     temp_prompts.append(prompt)
    #                     temp_answers.append(an)
    #                 local_prompts.append(temp_prompts)
    #                 local_answers.append(temp_answers)
    #     assert len(prompts) == len(locality_Relation_Specificity_prompts) == len(locality_Forgetfulness_prompts)
    #     locality_inputs = {}
    #     portability_inputs = {}
        
    #     locality_inputs = {
    #         'Relation_Specificity':{
    #             'prompt': locality_Relation_Specificity_prompts,
    #             'ground_truth': locality_Relation_Specificity_ans
    #         },
    #         'Forgetfulness':{
    #             'prompt':locality_Forgetfulness_prompts,
    #             'ground_truth':locality_Forgetfulness_ans
    #         }
    #     }
    #     portability_inputs = {
    #         'Subject_Aliasing':{
    #             'prompt': portability_Subject_Aliasing_prompts,
    #             'ground_truth': portability_Subject_Aliasing_ans
    #         },
    #         'reasoning':{
    #             'prompt': portability_reasoning_prompts,
    #             'ground_truth': portability_reasoning_ans           
    #         },
    #         'Logical_Generalization':{
    #             'prompt': portability_Logical_Generalization_prompts,
    #             'ground_truth': portability_Logical_Generalization_ans           
    #         }
    #     }
    # if args.datatype == 'wikibio':
    #     prompts=[data['prompt'] for data in datas]
    #     subjects=[data['subject'] for data in datas]
    #     target_new = [data['target_new'] for data in datas]
        
    #     locality_rs = [data['locality_rs'] for data in datas]
    #     locality_f = [data['locality_f'] for data in datas]
    #     locality_Relation_Specificity_prompts=[]
    #     locality_Relation_Specificity_ans=[]
        
    #     locality_data = [locality_rs]
    #     locality_prompts = [locality_Relation_Specificity_prompts]
    #     locality_answers = [locality_Relation_Specificity_ans]
    #     for data, local_prompts, local_answers in zip(locality_data,locality_prompts,locality_answers):
    #         for item in data:
    #             if item is None:
    #                 local_prompts.append(None)
    #                 local_answers.append(None)
    #             else:
    #                 temp_prompts = []
    #                 temp_answers = []
    #                 for pr in item:
    #                     prompt=pr["prompt"]
    #                     an=pr["ground_truth"]
    #                     while isinstance(an,list):
    #                         an = an[0]
    #                     if an.strip() =="":
    #                         continue
    #                     temp_prompts.append(prompt)
    #                     temp_answers.append(an)
    #                 local_prompts.append(temp_prompts)
    #                 local_answers.append(temp_answers)
    #     assert len(prompts) == len(locality_Relation_Specificity_prompts)
    #     portability_inputs = None
    #     locality_inputs = {}
    #     locality_inputs = {
    #         'Relation_Specificity':{
    #             'prompt': locality_Relation_Specificity_prompts,
    #             'ground_truth': locality_Relation_Specificity_ans
    #         }
    #     }


    location = "../data/counterfact.json"


    REMOTE_ROOT = "https://memit.baulab.info/data/dsets"

  
    if not location.exists():
            remote_url = f"{REMOTE_ROOT}/counterfact.json"
            print(f"{location} does not exist. Downloading from Internet")
            data_dir.mkdir(exist_ok=True, parents=True)
            torch.hub.download_url_to_file(remote_url, location)
        
    with open(location, "r") as f:
        data = json.load(f)

    prompts = []
    ground_truth = []
    target_new = []
    subjects = []
    
    for datai in data:
        prompts.append(datai["requested_rewrite"]["prompt"].format(datai["requested_rewrite"]["subject"]))
        ground_truth.append(datai["requested_rewrite"]["target_true"]["str"])
        target_new.append(datai["requested_rewrite"]["target_new"]["str"])
        subjects.append(datai["requested_rewrite"]["subject"])
    print(prompts[0])
    print(ground_truth[0])
    print(target_new[0])
    print(subjects[0])






    
    # ## edit descriptor: prompt that you want to edit
    # prompts = [
    #     'A cat is a kind of'
    # ]
    # ## You can set `ground_truth` to None !!!(or set to original output)
    # ground_truth = ['animal']
    # ## edit target: expected output
    # target_new = ['plant']
    # subjects = ['cat']



  
    hparams = editing_hparams.from_hparams(args.hparams_dir)

    # args.pre_file = f"./{hparams.model_name.split('/')[-1]}_{args.datatype}_pre_edit.json"
    # print(args.pre_file)
    # if args.pre_file is not None and os.path.exists(args.pre_file):
    #     pre_edit = json.load(open(args.pre_file,'r'))
    #     assert len(pre_edit) == len(prompts)
    # else:
    #     pre_edit = None
    # if args.editing_method == 'IKE':
    #     train_ds = KnowEditDataset(args.train_data_path)
    #     sentence_model = SentenceTransformer(hparams.sentence_model_name).to(f'cuda:{hparams.device}')
    #     encode_ike_facts(sentence_model, train_ds, hparams)
    # else:
    #     train_ds = None
    
    editor = BaseEditor.from_hparams(hparams)
    metrics, edited_model, _ = editor.edit(
        prompts=prompts,
        target_new=target_new,
        ground_truth=ground_truth,
        subject=subjects,
        # locality_inputs=locality_inputs,
        # portability_inputs=portability_inputs,
        # train_ds=train_ds,
        keep_original_weight=True,
        # pre_file=args.pre_file,
        # pre_edit = pre_edit,
    )
    if not os.path.exists(args.metrics_save_dir):
        os.makedirs(args.metrics_save_dir)
    # json.dump(metrics, open(os.path.join(args.metrics_save_dir, f'{args.editing_method}_results.json'), 'w'), indent=4)

    file_path = os.path.join(args.metrics_save_dir, f'{args.editing_method}_counterfact_results.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(metrics, f, indent=4)

        
    # print(metrics)
    # print("!!!!!")
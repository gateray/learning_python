#!/usr/bin/env python
# coding:utf8
import json

class BeanFactory:
    @staticmethod
    def getInstance(cls_str,model_str='model.beans'):
        mod =  __import__(model_str,fromlist=1)
        return getattr(mod,cls_str)()

    @staticmethod
    def dict2obj(d,cls_str,model_str='model.beans'):
        #if not isinstance(d,dict):return d
        obj = BeanFactory.getInstance(cls_str,model_str)
        for k,v in d.items():
            if hasattr(obj,k):setattr(obj,k,v)
        return obj

    @staticmethod
    def json2obj(json_str):
        def hook(dic):
            flag = False
            if type(dic) not in [list,tuple,dict]:return dic
            if isinstance(dic,dict) and 'cls_name' in dic:
                flag = True
                for k,v in dic.items():
                    dic[k] = hook(v)
                if flag:
                    pth = dic['cls_name'].split('.')
                    cls_str = pth[-1]
                    model_str = '.'.join(pth[:-1])
                    return BeanFactory.dict2obj(dic,cls_str,model_str)
            elif isinstance(dic,dict):#dict
                for k,v in dic.items():
                    dic[k] = hook(v)
                    return dic
            else:#list
                for i,elm in enumerate(dic):
                    dic[i] = hook(elm)
                    return dic
        return json.loads(json_str,object_hook=hook)


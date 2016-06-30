#!/usr/bin/env python
#__*__coding:utf8__*__
#

import re
import os
    
cache = {}
isDirty = False

#字符串添加高亮控制
def hl(s):
    return '\033[1;32m'+s+'\033[0m'

#将查询结果集中的关键字转换为高亮字符串
def kw2hl(kw,rs_dict):
    if len(kw) == 0:
        return rs_dict
    hl_rs_dict = {}
    for o_k in rs_dict.keys():
        #hl_rs_dict[o_k]={}
       # hl_rs_dict[hl(kw)]={}
        for i_k,i_v in rs_dict[o_k].items():
            if str(o_k) == kw:
                if hl(kw) not in hl_rs_dict:
                    hl_rs_dict[hl(kw)] = {} 
                hl_rs_dict[hl(kw)]=rs_dict[o_k].copy()
                if len(kw) < 3:
                    if kw == i_v:
                        hl_rs_dict[hl(kw)][i_k] = hl(kw)
                elif kw in i_v:
                    hl_rs_dict[hl(kw)][i_k] = rs_dict[o_k][i_k].replace(kw,hl(kw)) 
            else:
                if o_k not in hl_rs_dict:
                    hl_rs_dict[o_k] = {}
                if len(kw) < 3:
                    if kw == i_v:
                        hl_rs_dict[o_k][i_k] = hl(kw)
                elif kw in i_v:
                    hl_rs_dict[o_k][i_k] = rs_dict[o_k][i_k].replace(kw,hl(kw))
                else:
                    hl_rs_dict[o_k][i_k] = rs_dict[o_k][i_k]
    return hl_rs_dict   

#高亮后的动态格式化输出
def pr_result(hl_rs_dict,ishl=True):
    f_d = {'id':False,'name':False,'phone':False,'company':False,'email':False}
    fm_d = {'id':'{id:>5}','name':'{name:>20}','phone':'{phone:>20}','company':'{company:>30}','email':'{email:>35}'}
    title_fm_d = fm_d.copy()
    x = 114
    table = []
    if ishl:
    #找出那些字段需要修改显示格式
        for id,inner_d in hl_rs_dict.items():
            if not f_d['id']:
                if '\033[' in str(id):
                    f_d['id'] = True
            for k,v in inner_d.items():
                if not f_d[k]:
                    if '\033[' in v:
                        f_d[k] = True
            if f_d['id'] and f_d['name'] and f_d['phone'] and f_d['company'] and f_d['email']:
                break
        #修改匹配字段的显示格式
        for k,v in f_d.items():
            if v:
                t = fm_d[k].rpartition(fm_d[k][(fm_d[k].rfind('>')+1):-1])
                fm_d[k] = t[0] + str(int(t[1])+17) + t[2]
                title_fm_d[k] = t[0] + str(int(t[1])+6) + t[2]  
                x += 6
    #设置表标题和表体的显示格式字符串
    fm_str = fm_d['id'] + fm_d['name'] + fm_d['phone'] + fm_d['company'] + fm_d['email']
    title_fm_str = title_fm_d['id'] + title_fm_d['name'] + title_fm_d['phone'] + title_fm_d['company'] + title_fm_d['email']     
    #打印表标题
    print title_fm_str.format(**{'id':'ID','name':'Name','phone':'PhoneNum','company':'Company','email':'EmailAddress'}) 
    print '-'*x
    #打印表体
    for id, v in hl_rs_dict.items():
        nv = v.copy()
        nv['id'] = id 
        table.append(nv)
    for row in table:
        print fm_str.format(**row)

#创建条目
def create(id,inner_dict):
    if id in cache:
        return  False
    else:
        cache[id] = inner_dict
        return True

#修改指定id条目
def update(id,inner_dict):
    if id not in cache:
        return False
    else:
        cache[id] = inner_dict
        return True

#从缓存中查找匹配关键字的数据
def query(kw):
    rs = {}
    tid = 0
    if len(kw) == 0:
        return cache
    if re.match(r'^\d{1,3}$',kw):
        tid = int(kw)
    #精确匹配查询
    if len(kw) < 3:
        for id,inner_dict in cache.items():
            if tid == id:
                rs[id] = cache[id]
                continue
            for k,v in inner_dict.items():
                if kw == v:
                    rs[id] = cache[id]
    #模糊匹配查询
    else:
        for id,inner_dict in cache.items():
            if kw in str(id):
                rs[id] = cache[id]
                continue
            for k,v in inner_dict.items():
                if kw in v:
                    rs[id] = cache[id]
    return rs  
        

#将用户输入字符串转换为id列表
def convert2idlist(s):
    ids = []
    list = s.split(',')
    for i in list:
        if '-' in i:
            start = int(i.split('-')[0])
            end = int(i.split('-')[1])+1
            for j in range(start, end):
                ids.append(j)
        else:
            ids.append(int(i)) 
    return ids
    
#从cache中移除与id匹配的条目
def delete(ids):
    global cache
    global isDirty
    d_flag = False
    for id in ids:
        if id in cache:
            del cache[id] 
            print 'id: %d delete success!' % (id)
            d_flag = True
        else:
            print 'id: %d not exist!' %(id)
    if d_flag:
       isDirty = True 

#从指定的file中读取全部内容到cache
def generateCache(ptfn):
    l = []
    with open(ptfn,'r') as f:
        l = f.readlines()
    for line in l:
        ll = line.split()
        cache[int(ll[0])] = {'name':ll[1], 'phone':ll[2], 'company':ll[3], 'email':ll[4]}
    print 'Load cache success!'

#从缓存flush到文件
def flush2file(ptfn):
    if not isDirty:
        return
    allLines = []
    for id,inner_dict in cache.items():
        line = str(id)+' '+inner_dict['name']+' '+inner_dict['phone']+' '+inner_dict['company']+' '+inner_dict['email']+'\n'
        allLines.append(line)
    with open(ptfn,'w') as f:
        f.writelines(allLines)
    print 'Flush success!'

#主菜单
def showMainMenu():
    menu_dict = {'c': createMenu, 'r': readMenu, 'u': updateMenu, 'd': deleteMenu}
    while True:
        print '''
    添加用户（C）
    查询用户（R）
    更新用户（U）
    删除用户（D）
    退出（Q）'''
        try:
            choice = raw_input('Your choice: ').strip().lower()[0]
        except Exception:
            continue
        if choice in 'crud':
            if menu_dict[choice]():
                continue
            else:
                flush2file('stu_list.txt')
                exit()
        elif choice == 'q':
            flush2file('stu_list.txt')
            exit()
        else:
            print 'wront input, try again!'
            continue

def input_id():
    while True:
        try:
            id = int(raw_input('ID：').strip())
            if id <= 999:
                return id
            print '数字不能大于999,请重新输入！' 
        except ValueError:
            print 'id只能是3为数字,请重新输入！'
        
def input_name():
    while True:
        name = raw_input('用户名：').strip()
        if len(name)==0:
            print '用户名不能为空，请重新输入！'
            continue
        if len(name)>15:
            print '用户名不能超过15位，请重新输入！'
            continue
        return name
        
def input_phone():
    while True:
        phone = raw_input('手机号：').strip()
        if re.match(r'^\d{11}$',phone):
            return phone
        print '手机号只能为11为数字，请重新输入！'

def input_company():
    while True:
        company = raw_input('公司：').strip()
        if len(company) == 0:
            print '公司名称不能为空，请重新输入！'
            continue
        if len(company) >25:
            print '字符长度不能超过25位，请重新输入！'
            continue
        return company

def input_email():
    while True:
        email = raw_input('电子邮箱：').strip()
        if re.match(r'^[^@\s]+@([^\s@.]+\.)+[A-Za-z]{2,3}$', email):
            return email
        print 'Email格式不对，请重新输入！'

def input_kw():
    while True:
        kw = raw_input('请输入一个用户关键字: ').strip()
        if len(kw) == 0:
            print '将列出所有用户：'
        return kw
 
#添加菜单：
def createMenu():
    while True:
        print '-'*20 + 'Create a user' + '-'*20
        id = input_id() 
        name = input_name()
        phone = input_phone()
        company = input_company()
        email = input_email()
        print 'Your input is below:\n\tid: %d name: %s phone: %s company: %s email: %s' % (id, name, phone, company, email)
        if raw_input('Save it?(y/n)').strip().lower() == 'y':
            if create(id,{'name':name,'phone':phone,'company':company,'email':email}):
                print 'Save success!'
                global isDirty
                isDirty = True
            else:
                print 'id已存在，创建失败！'
        else:
            #不保存则返回上一级菜单
            return True
        if raw_input('create continue?(y/n)').strip().lower() in 'y':
            continue
        else:
            return True
    
#查询菜单：
def readMenu():
    while True:
        print '-'*20 + 'Search users' + '-'*20
        kw = input_kw()
        rs = query(kw)
        if rs:
            if len(kw) == 0:
                pr_result(rs,False)  
            else:
                pr_result(kw2hl(kw,rs))
            print '共找到%d条记录' % (len(rs))
        else:
            print '没有找到匹配的结果!' 
        if raw_input('Continue?(y/n)').strip().lower() in 'y':
            continue
        else:
            return True
 
#更新菜单：
def updateMenu():
    while True:
        print '-'*20 + 'Udate a user' + '-'*20
        kw = input_kw()
        rs = query(kw)
        if rs:
            pr_result(kw2hl(kw,rs))  
            print '共找到%d条记录' % (len(rs))
            id = input_id()
            if id in rs:
                print 'ID %d用户信息如下：'
                pr_result({id:rs[id]}) 
                print '请输入你的修改：'
                if update(id, {'name':input_name(),'phone':input_phone(),'company':input_company(),'email':input_email()}):
                    print 'Update success!'
                    global isDirty
                    isDirty = True
                else:
                    print '更新失败！'
            else:
                print 'id: %d不在包含"%s"的结果集中！' %(id,kw)     
        else:
            print '没有找到匹配的结果!' 
        if raw_input('Continue?(y/n)').strip().lower() in 'y':
            continue
        else:
            return True
        

#删除菜单：
def deleteMenu():
    while True:
        print '-'*20 + 'Delete users' + '-'*20
        kw = input_kw()
        rs = query(kw)
        if rs:
            pr_result(kw2hl(kw,rs))
            print '共找到%d条记录' % (len(rs))
            while True:
                ids_str = raw_input('请输入要删除的用户ID 如(1,3,6或1-3,5,7-8): ').strip()        
                if re.match(r'^(\d+|\d+-\d+)(,\d+|,\d+-\d+)*$|^\d+-\d+$',ids_str):
                    break
                print '输入格式有误，请重新输入！'
            ids = convert2idlist(ids_str)            
            new_ids = []
            for id in ids:
                if id in rs:
                    new_ids.append(id)
            if len(new_ids) > 0:
                new_rs = {}
                for id in new_ids:
                    new_rs[id] = rs[id]
                pr_result(new_rs)    
                if raw_input('以上条目将被删除，确认(y),放弃(n)? ').strip().lower() == 'y':
                    delete(new_ids)
            else:
                print 'id不在包含"%s"的结果集中！' %(kw)
        else:
            print '没有找到匹配的结果!'
        if raw_input('Continue?(y/n)').strip().lower() in 'y':
            continue
        else:
            return True

if __name__ == '__main__':
    generateCache('stu_list.txt')
    try:
        showMainMenu()
    except KeyboardInterrupt:
        flush2file('stu_list.txt') 
        print '\n',
        exit()

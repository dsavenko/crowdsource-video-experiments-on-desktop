#
# Collective Knowledge: CK-powered Caffe crowdbenchmarking (very early prototyping)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

line='================================================================'

ffstat='ck-stat-flat-characteristics.json'

form_name='wa_web_form'
onchange='document.'+form_name+'.submit();'

hextra='<i><center>\n'
hextra+='This is a community-driven R&D: \n'
hextra+=' [ <a href="http://cKnowledge.org/ai">collaborative AI optimization</a> ], '
hextra+=' [ <a href="https://github.com/dividiti/ck-crowdsource-dnn-optimization">Desktop app to crowd-optimize DNN engines and models</a> ], '
hextra+=' [ <a href="https://github.com/ctuning/ck-tensorflow">CK-TensorFlow</a> ], '
hextra+=' [ <a href="https://github.com/dividiti/ck-caffe">CK-Caffe</a> ], '
hextra+=' [ <a href="https://en.wikipedia.org/wiki/Collective_Knowledge_(software)">CK intro</a>, \n'
hextra+='CK papers: <a href="https://www.researchgate.net/publication/304010295_Collective_Knowledge_Towards_RD_Sustainability">1</a> and \n'
hextra+='<a href="https://arxiv.org/abs/1506.06256">2</a>; \n'
hextra+='<a href="https://www.youtube.com/watch?v=Q94yWxXUMP0">YouTube intro</a> ] \n'
hextra+='</center></i>\n'
hextra+='<br>\n'

selector=[{'name':'Type', 'key':'caffe_type'},
          {'name':'Network', 'key':'nn_type'},
          {'name':'Platform', 'key':'plat_name'},
          {'name':'CPU', 'key':'cpu_name', 'new_line':'yes'},
          {'name':'OS', 'key':'os_name'},
          {'name':'GPGPU', 'key':'gpgpu_name'}]

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# crowdsource these experiments

def crowdsource(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    return {'return':1, 'error':'TBD. For now use https://github.com/dividiti/ck-crowdsource-dnn-optimization as a front-end'}
                                                                                                               
##############################################################################
# show results

def show(i):
    """
    Input:  {
               (crowd_module_uoa) - if rendered from experiment crowdsourcing
               (crowd_key)        - add extra name to Web keys to avoid overlapping with original crowdsourcing HTML
               (crowd_on_change)  - reuse onchange doc from original crowdsourcing HTML
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    st=''

    cmuoa=i.get('crowd_module_uoa','')
    ckey=i.get('crowd_key','')

    conc=i.get('crowd_on_change','')
    if conc=='':
        conc=onchange

    hi_uid=i.get('highlight_uid','')

    h=''
#    h='<hr>\n'
    h+='<center>\n'
    h+='\n\n<script language="JavaScript">function copyToClipboard (text) {window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);}</script>\n\n' 

#    h+='<h2>Aggregated results from desktop-based DNN crowd-benchmarking</h2>\n'

    h+=hextra

    # Check host URL prefix and default module/action
    rx=ck.access({'action':'form_url_prefix',
                  'module_uoa':'wfe',
                  'host':i.get('host',''), 
                  'port':i.get('port',''), 
                  'template':i.get('template','')})
    if rx['return']>0: return rx
    url0=rx['url']
    template=rx['template']

    url=url0
    action=i.get('action','')
    muoa=i.get('module_uoa','')

    st=''

    url+='action=index&module_uoa=wfe&native_action='+action+'&'+'native_module_uoa='+muoa
    url1=url

    # List entries
    ii={'action':'search',
        'module_uoa':work['self_module_uid'],
        'add_meta':'yes'}

    if cmuoa!='':
        ii['module_uoa']=cmuoa

    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']

    # Check unique entries
    choices={}
    wchoices={}

    for q in lst:
        d=q['meta']
        meta=d.get('meta',{})

        for kk in selector:
            kx=kk['key']
            k=ckey+kx

            if k not in choices: 
                choices[k]=[]
                wchoices[k]=[{'name':'','value':''}]

            v=meta.get(kx,'')
            if v!='':
                if v not in choices[k]: 
                    choices[k].append(v)
                    wchoices[k].append({'name':v, 'value':v})

    # Prepare query div ***************************************************************
    if cmuoa=='':
        # Start form + URL (even when viewing entry)
        r=ck.access({'action':'start_form',
                     'module_uoa':cfg['module_deps']['wfe'],
                     'url':url1,
                     'name':form_name})
        if r['return']>0: return r
        h+=r['html']

    for kk in selector:
        k=ckey+kk['key']
        n=kk['name']

        nl=kk.get('new_line','')
        if nl=='yes':
            h+='<br>\n<div id="ck_entries_space8"></div>\n'

        v=''
        if i.get(k,'')!='':
            v=i[k]
            kk['value']=v

        # Show hardware
        ii={'action':'create_selector',
            'module_uoa':cfg['module_deps']['wfe'],
            'data':wchoices.get(k,[]),
            'name':k,
            'onchange':conc, 
            'skip_sort':'no',
            'selected_value':v}
        r=ck.access(ii)
        if r['return']>0: return r

        h+='<b>'+n+':</b> '+r['html'].strip()+'\n'

    # Check hidden
    if hi_uid!='':
        h+='<input type="hidden" name="highlight_uid" value="'+hi_uid+'">\n'

    h+='<br><br>'

    # Prune list
    plst=[]
    for q in lst:
        d=q['meta']
        meta=d.get('meta',{})

        # Check selector
        skip=False
        for kk in selector:
            k=kk['key']
            n=kk['name']
            v=kk.get('value','')

            if v!='' and meta.get(k,'')!=v:
                skip=True

        if not skip:
            plst.append(q)

    # Check if too many
    lplst=len(plst)
    if lplst==0:
        h+='<b>No results found!</b>'
        return {'return':0, 'html':h, 'style':st}
    elif lplst>50:
        h+='<b>Too many entries to show ('+str(lplst)+') - please, prune list further!</b>'
        return {'return':0, 'html':h, 'style':st}

    # Prepare table
    h+='<table border="1" cellpadding="7" cellspacing="0">\n'

    ha='align="center" valign="top"'
    hb='align="left" valign="top"'

    h+='  <tr style="background-color:#dddddd">\n'
    h+='   <td '+ha+'><b>All raw files</b></td>\n'
    h+='   <td '+ha+'><b>Type</b></td>\n'
    h+='   <td '+ha+'><b>Network</b></td>\n'
    h+='   <td '+ha+'><b>FWBW</b></td>\n'
    h+='   <td '+ha+'><b>FW</b></td>\n'
    h+='   <td '+ha+'><b>BW</b></td>\n'
    h+='   <td '+ha+'><b>Accuracy<br>(TP1 / TP5)</b></td>\n'
    h+='   <td '+ha+'><b>Chars</b></td>\n'
    h+='   <td '+ha+'><b>Platform</b></td>\n'
    h+='   <td '+ha+'><b>CPU</b></td>\n'
    h+='   <td '+ha+'><b>GPGPU</b></td>\n'
    h+='   <td '+ha+'><b>OS</b></td>\n'
    h+='   <td '+ha+'><b>Fail?</b></td>\n'
    h+='   <td '+ha+'><b>Choices</b></td>\n'
    h+='   <td '+ha+'><b>User</b></td>\n'
    h+='   <td '+ha+'><b>Replay</b></td>\n'
    h+='  <tr>\n'

    # Dictionary to hold target meta
    tm={}

    ix=0
    bgraph={'0':[]} # Just for graph demo
    if hi_uid!='':
        bgraph['1']=[]

    # Sort
    splst=sorted(plst, key=lambda x: x.get('meta',{}).get('characteristics',{}).get('run',{}).get('time_fwbw_ms',0))

    for q in splst:
        ix+=1

        duid=q['data_uid']
        path=q['path']

        d=q['meta']

        meta=d.get('meta',{})

        params=d.get('choices',{}).get('params',{}).get('params',{})

        tp=meta.get('caffe_type','')
        nn=meta.get('nn_type','')

        plat_name=meta.get('plat_name','')
        cpu_name=meta.get('cpu_name','')
        os_name=meta.get('os_name','')
        gpgpu_name=meta.get('gpgpu_name','')

        plat_uid=meta.get('platform_uid','')
        cpu_uid=meta.get('cpu_uid','')
        os_uid=meta.get('os_uid','')
        gpu_uid=meta.get('gpu_uid','')
        gpgpu_uid=meta.get('gpgpu_uid','')

        user=meta.get('user','')

        te=d.get('characteristics',{}).get('run',{})

#        bgc='afffaf'
        bgc='dfffdf'
        fail=d.get('state',{}).get('fail','')
        fail_reason=d.get('state',{}).get('fail_reason','')
        if fail=='yes':
            if fail_reason=='': fail_reason='yes'
            bgc='ffafaf'
        elif hi_uid!='' and duid==hi_uid:
            bgc='9fff9f'
            bgraph['0'].append([ix,None])
            bgraph['1'].append([ix,x0])

        bg=' style="background-color:#'+bgc+';"'

        h+='  <tr'+bg+'>\n'

        x=work['self_module_uid']
        if cmuoa!='': x=cmuoa
        h+='   <td '+ha+'>'+str(ix)+')&nbsp;<a href="'+url0+'&wcid='+x+':'+duid+'">'+duid+'</a></td>\n'

        h+='   <td '+ha+'>'+tp+'</a></td>\n'

        h+='   <td '+ha+'>'+nn+'</a></td>\n'

        # Characteristics
        # Check if has statistics
        dstat={}
        fstat=os.path.join(path,'ck-stat-flat-characteristics.json')
        if os.path.isfile(fstat):
            r=ck.load_json_file({'json_file':fstat, 'dict':dstat})
            if r['return']>0: return r
            dstat=r['dict']

        x=''

        # Check if has stats
        x0=dstat.get("##characteristics#run#time_fwbw_ms#min",None)
        x0e=dstat.get("##characteristics#run#time_fwbw_ms#exp",None)
        x1=dstat.get("##characteristics#run#time_fwbw_ms#center",None)
        x2=dstat.get("##characteristics#run#time_fwbw_ms#halfrange",None)
        if x1!=None and x2!=None:
            x=('%.0f'%x1)+'&nbsp;&PlusMinus;&nbsp;'+('%.0f'%x2)+'&nbsp;ms.'

        h+='   <td '+ha+'>'+x+'</td>\n'

        if fail!='yes' and x0!=None and duid!=hi_uid:
            bgraph['0'].append([ix,x0])
            if hi_uid!='': bgraph['1'].append([ix,None])

        x1=dstat.get("##characteristics#run#time_fw_ms#center",None)
        x2=dstat.get("##characteristics#run#time_fw_ms#halfrange",None)
        if x1!=None and x2!=None:
            x=('%.0f'%x1)+'&nbsp;&PlusMinus;&nbsp;'+('%.0f'%x2)+'&nbsp;ms.'

        h+='   <td '+ha+'>'+x+'</td>\n'

        x1=dstat.get("##characteristics#run#time_bw_ms#center",None)
        x2=dstat.get("##characteristics#run#time_bw_ms#halfrange",None)
        if x1!=None and x2!=None:
            x=('%.0f'%x1)+'&nbsp;&PlusMinus;&nbsp;'+('%.0f'%x2)+'&nbsp;ms.'

        h+='   <td '+ha+'>'+x+'</td>\n'

        # Accuracy - for now hardwired - later should get directly from experiment description
        x=''
        if nn=='bvlc, alexnet':
            x='0.568279&nbsp;/&nbsp;0.799501'
        elif nn=='bvlc, googlenet':
            x='0.689299&nbsp;/&nbsp;0.891441'
        elif nn=='deepscale, squeezenet, 1.1':
            x='0.583880&nbsp;/&nbsp;0.810123'
        elif nn=='deepscale, squeezenet, 1.0':
            x='0.576801&nbsp;/&nbsp;0.803903'

        h+='   <td '+ha+'>'+x+'</td>\n'

        # Check all characteristics
        x=''
        x5=''
        for k in sorted(te):
            v=te[k]

            kx="##characteristics#run#"+k

            kx1=dstat.get(kx+'#center',None)
            kx2=dstat.get(kx+'#halfrange',None)

            x6=''
            if type(v)==int:
                if kx1!=None and kx2!=None:
                    x6=str(kx1)+' +- '+str(kx2)
                else:
                    x6=str(v)
            elif type(v)==float:
                if kx1!=None and kx2!=None:
                    x6=('%.1f'%kx1)+' +- '+('%.1f'%kx2)
                else:
                    x6=('%.1f'%v)

            if x6!='':
                x5+=str(k)+'='+x6+'\n'

#        x5=x5.replace("'","\'").replace('"',"\\'").replace('\n','\\n')
        x5=x5.replace("\'","'").replace("'","\\'").replace('\"','"').replace('"',"\\'").replace('\n','\\n')
        if x5!='':
            x+='<input type="button" class="ck_small_button" onClick="alert(\''+x5+'\');" value="All">'

        h+='   <td '+ha+'>'+x+'</td>\n'

        # Platform, etc ...
        x=plat_name
        if plat_uid!='':
            x='<a href="'+url0+'&wcid='+cfg['module_deps']['platform']+':'+plat_uid+'">'+x+'</a>'
        h+='   <td '+ha+'>'+x+'</td>\n'

        x=cpu_name
        if cpu_uid!='':
            x='<a href="'+url0+'&wcid='+cfg['module_deps']['platform.cpu']+':'+cpu_uid+'">'+x+'</a>'
        h+='   <td '+ha+'>'+x+'</td>\n'

        x=gpgpu_name
        if gpgpu_uid!='':
            x='<a href="'+url0+'&wcid='+cfg['module_deps']['platform.gpgpu']+':'+gpgpu_uid+'">'+x+'</a>'
        h+='   <td '+ha+'>'+x+'</td>\n'

        x=os_name
        if os_uid!='':
            x='<a href="'+url0+'&wcid='+cfg['module_deps']['platform']+':'+os_uid+'">'+x+'</a>'
        h+='   <td '+ha+'>'+x+'</td>\n'

        x=fail_reason
        if x=='': 
            x='No'
        else:
            fail_reason=fail_reason.replace("\'","'").replace("'","\\'").replace('\"','"').replace('"',"\\'").replace('\n','\\n')
            x='Yes <input type="button" class="ck_small_button" onClick="alert(\''+fail_reason+'\');" value="Log">'

        h+='   <td '+ha+'>'+x+'</td>\n'

        # Params
#        x='<table border="0" cellpadding="0" cellspacing="2">\n'
        x=''
        for k in sorted(params):
            v=params[k]
            x+=str(k)+'='+str(v)+'\n'
#            x+='<tr><td>'+str(k)+'=</td><td>'+str(v)+'</td></tr>\n'
#        x+='</table>\n'
#        x=x.replace("'","\'").replace('"',"\\'").replace('\n','\\n')
        x=x.replace("\'","'").replace("'","\\'").replace('\"','"').replace('"',"\\'").replace('\n','\\n')

        x1=''
        if x!='':
            x1='<input type="button" class="ck_small_button" onClick="alert(\''+x+'\');" value="See">'

        h+='   <td '+ha+'>'+x1+'</td>\n'

        h+='   <td '+ha+'><a href="'+url0+'&action=index&module_uoa=wfe&native_action=show&native_module_uoa=experiment.user">'+user+'</a></td>\n'

        h+='   <td '+ha+'><input type="button" class="ck_small_button" onClick="copyToClipboard(\'ck replay caffe\');" value="Replay"></td>\n'

        h+='  <tr>\n'

    h+='</table>\n'
    h+='</center>\n'

    if cmuoa=='':
        h+='</form>\n'

    if len(bgraph['0'])>0:
       ii={'action':'plot',
           'module_uoa':cfg['module_deps']['graph'],

           "table":bgraph,

           "h_lines":[1.0],

           "ymin":0,

           "ignore_point_if_none":"yes",

           "plot_type":"d3_2d_bars",

           "display_y_error_bar":"no",

           "title":"Powered by Collective Knowledge",

           "axis_x_desc":"Experiment",
           "axis_y_desc":"Neural network total time (ms.)",

           "plot_grid":"yes",

           "d3_div":"ck_interactive",

           "image_width":"900",
           "image_height":"400",

           "wfe_url":url0}

       r=ck.access(ii)
       if r['return']==0:
          x=r.get('html','')
          if x!='':
             st+=r.get('style','')

             h+='<br>\n'
             h+='<center>\n'
             h+='<div id="ck_box_with_shadow" style="width:920px;">\n'
             h+=' <div id="ck_interactive" style="text-align:center">\n'
             h+=x+'\n'
             h+=' </div>\n'
             h+='</div>\n'
             h+='</center>\n'

    return {'return':0, 'html':h, 'style':st}

##############################################################################
# replay experiment (TBD)

def replay(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    return {'return':1, 'error':'TBD'}

    # TBD - take params from remote/local experiment and pre-set ...
    # Run locally, i.e. do not share stats unless requested ...

#    i['action']='crowdsource'
#    i['module_uoa']=cfg['module_deps']['experiment.bench.caffe']

    return ck.access(i)

##############################################################################
# submit statistics to repository

def submit(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    ck.out('submit statistics to repository')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

    return {'return':0}

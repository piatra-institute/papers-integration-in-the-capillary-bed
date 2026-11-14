#!/usr/bin/env python3
"""Offline, deterministic analysis. Downloads belong only in fetch_sources.py."""
from pathlib import Path
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('VECLIB_MAXIMUM_THREADS','1')
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/when-support-computes-matplotlib')
import json, platform, time, subprocess, sys
from xml.etree import ElementTree as ET
import numpy as np
import scipy
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from capnet.network import build, CELL_LENGTH_UM, PA_UNITS_PER_NODE
from capnet.model import Solver, Params, R_GAS,TEMP_K,FARADAY,K_IN,K_REST,K_KIR,C_CAP,C_PA_UNIT,R_GJ_PA
from capnet.experiment import parameters,pack,sample,trace,Protocol,residual,flow,filter_trace,BOUNDS,BASE,connected_patch

HERE=Path(__file__).resolve().parent
OUT=HERE/'output';FIG=HERE.parent/'paper'/'figures'
SEED=20261114
DT=2.; RECORD=10.; CANDIDATES=8192; LOCAL_CANDIDATES=512
TRAIN=[Protocol((site,),(k,)) for site in ('tip0','level3','level2') for k in (6.,8.,10.,12.)]
KLEVELS=(6.,8.,10.,12.);DELAYS=(0.,100.,250.,500.)
MODEL_LABELS={'distributed':'Distributed Kir','passive':'Passive cable','sensor_only':'Active distal branches / passive trunk','capillary_linear':'Capillary-linear / active arteriole','arteriole_linear':'Active capillary / linear arteriole','dynamic_filter':'Pooled dynamic filter','independent_sensors':'Independent-sensor oracle'}


def plain(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [plain(z) for z in x]
    return x


def training(so,p,mode='distributed'):
    rest=so.rest(p)
    return np.stack([trace(so,p,q,mode=mode,rest=rest)[1][:,:,0] for q in TRAIN],axis=1)


def broad_trace(so,p,mode='distributed'):
    so.net.sites['broad']=connected_patch(so.net,16)
    tt,hh=trace(so,p,Protocol(('broad',),(10.,),onset=0,duration=18000,end=23000),mode=mode)
    return tt,hh[:,:,0]


def broad_features(tt,hh):
    return np.stack([hh[:,(tt>17900)&(tt<=18000)].mean(axis=1),hh[:,(tt>22900)].mean(axis=1)],axis=1)


def window(t,q):
    end=q.onset+q.delay+q.duration
    return (t>end-100)&(t<=end)


def summary_range(x):
    return {'min':float(np.min(x)),'median':float(np.median(x)),'max':float(np.max(x))}


def identifiability_diagnostics(so,nominal,fitmask):
    diagnostics=[]
    for eps in (.005,.001,.0001,.00001):
        jac=[];perturbations=[]
        for j in range(3):
            xp=nominal.copy();xm=nominal.copy();xp[j]*=np.exp(eps);xm[j]*=np.exp(-eps)
            yp=training(so,parameters(xp))[0][:,fitmask].ravel();ym=training(so,parameters(xm))[0][:,fitmask].ravel()
            tp,hp=broad_trace(so,parameters(xp));tm,hm=broad_trace(so,parameters(xm));bp=broad_features(tp,hp)[0];bm=broad_features(tm,hm)[0]
            yp=np.concatenate([yp,10*bp]);ym=np.concatenate([ym,10*bm]);jac.append((yp-ym)/(2*eps))
            perturbations.append({'parameter_index':j,'plus_endpoint_mv':float(bp[0]),'plus_recovery_mv':float(bp[1]),'minus_endpoint_mv':float(bm[0]),'minus_recovery_mv':float(bm[1]),'both_reversible':bool(abs(bp[1])<1 and abs(bm[1])<1)})
        jac=np.array(jac).T;sv=np.linalg.svd(jac,compute_uv=False)
        cov=np.linalg.pinv(jac.T@jac);cor=cov/np.sqrt(np.outer(np.diag(cov),np.diag(cov)))
        diagnostics.append({'log_parameter_step':eps,'singular_values':sv,'condition_number':float(sv[0]/sv[-1]),'perturbations':perturbations,'all_perturbations_reversible':all(x['both_reversible'] for x in perturbations)})
    # The smallest step is reported; larger steps expose crossing of the recovery boundary.
    return sv,cor,diagnostics


def run_tests():
    junit=OUT/'tests.xml';log=OUT/'tests.log'
    proc=subprocess.run([sys.executable,'-m','pytest',str(HERE/'tests'),'-q','--junitxml='+str(junit)],cwd=HERE,capture_output=True,text=True)
    log.write_text(proc.stdout+proc.stderr)
    print(proc.stdout,flush=True)
    if proc.returncode:raise RuntimeError('Required test suite failed; see output/tests.log')
    suites=ET.parse(junit).getroot().findall('.//testsuite')
    counts={key:sum(int(x.attrib.get(key,0)) for x in suites) for key in ('tests','errors','failures','skipped')}
    if counts['tests']==0 or any(counts[key] for key in ('errors','failures','skipped')):raise RuntimeError('Required test suite incomplete')
    return {'status':'PASS',**counts,'log':'simulation/output/tests.log','junit':'simulation/output/tests.xml'}


def main():
    start=time.time();OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
    test_result=run_tests()
    rng=np.random.default_rng(SEED);net=build();so=Solver(net,DT)
    candidates=sample(rng,CANDIDATES);p=parameters(candidates);rest=so.rest(p)
    footprint_screen={}
    for footprint in (8,16):
        net.sites['broad']=connected_patch(net,footprint)
        tt,zz=trace(so,p,Protocol(('broad',),(10.,),onset=0,duration=18000,end=23000),rest=rest,dt_record=1000.,record=[net.zone2])
        amplitude=zz[:,17,0];recovery=zz[:,-1,0]
        mask=(amplitude>=19.6)&(amplitude<=26.8)&(rest[:,net.zone2]>=-45)&(rest[:,net.zone2]<=-25)
        reversible=mask&(abs(recovery)<1.)
        footprint_screen[str(footprint)]={'cell_count':footprint,'endpoint_count':int(mask.sum()),'reversible_count':int(reversible.sum()),'rejected_recovery_count':int(mask.sum()-reversible.sum()),'endpoint_matched_recovery_mv':summary_range(recovery[mask]),'endpoint_matched_amplitude_mv':summary_range(amplitude[mask])}
        print('Footprint screen',footprint,footprint_screen[str(footprint)],flush=True)
    endpoint_accepted=candidates[mask]
    accepted=candidates[reversible]
    if len(accepted)<2:raise RuntimeError('Insufficient reversible physiological-screen ensemble')
    long_t,long_h=broad_trace(so,parameters(accepted));long_feat=broad_features(long_t,long_h)
    # Final waveform sampling confirms the same duration, recovery and magnitude.
    confirm=(abs(long_feat[:,1])<1.)&(long_feat[:,0]>=19.6)&(long_feat[:,0]<=26.8)
    accepted=accepted[confirm];long_h=long_h[confirm];long_feat=long_feat[confirm]
    keep_amp=long_feat[:,0];best=int(np.argmin(abs(keep_amp-23.2)))
    nominal=accepted[best];pn=parameters(nominal);pfilter_base=parameters([.4,.06,50.])
    nominal_long_h=long_h[best];target_broad=long_feat[best]
    print(f'Endpoint screen {len(endpoint_accepted)}/{CANDIDATES}; reversible screen {len(accepted)}; nominal {nominal}',flush=True)
    target=training(so,pn)[0]
    fitmask=np.arange(target.shape[-1])%5==4
    fit_target=target[:,fitmask].ravel()
    fits={'distributed':{'parameters':nominal,'rmse_mv':0.,'free_parameters':3}}
    fitted={'distributed':pn}
    for mode in ('passive','sensor_only','capillary_linear','arteriole_linear'):
        def objective(x):
            pr=parameters([x[0],x[1],np.exp(x[2])])
            weak=training(so,pr,mode)[0][:,fitmask].ravel()-fit_target
            bt,bh=broad_trace(so,pr,mode);br=broad_features(bt,bh)[0]-target_broad
            return np.concatenate([weak,10*br])
        bounds=([.2,.02,np.log(10)],[.8,.1,np.log(200)])
        sols=[]
        for x0 in (nominal,np.array([.4,.06,50.]),np.array([.7,.03,30.])):
            sols.append(least_squares(objective,[x0[0],x0[1],np.log(x0[2])],bounds=bounds,max_nfev=60,ftol=1e-7,xtol=1e-7,gtol=1e-7))
        sol=min(sols,key=lambda z:np.sum(z.fun**2));fp=np.array([sol.x[0],sol.x[1],np.exp(sol.x[2])]);fitted[mode]=parameters(fp)
        fits[mode]={'parameters':fp,'rmse_mv':float(np.sqrt(np.mean(sol.fun[:-2]**2))),'free_parameters':3,'success':bool(sol.success),'function_evaluations':sol.nfev,'multistart_objective_sse':[float(np.sum(z.fun**2)) for z in sols],'multistart_parameters':[[float(z.x[0]),float(z.x[1]),float(np.exp(z.x[2]))] for z in sols],'broad_endpoint_error_mv':float(sol.fun[-2]/10),'broad_recovery_error_mv':float(sol.fun[-1]/10),'objective':'single-site weak traces plus broad18s endpoint and5s recovery; each anchor weighted10, same bounds and three starts'}
        print(mode,fits[mode]['rmse_mv'],fp,flush=True)
    passive_base=training(so,pfilter_base,'passive')[0]
    filter_bt,filter_bh=broad_trace(so,pfilter_base,'passive')
    def fobj(theta):
        weak=(filter_trace(passive_base,theta)[:,fitmask]-target[:,fitmask]).ravel()
        br=broad_features(filter_bt,filter_trace(filter_bh,theta))[0]-target_broad
        return np.concatenate([weak,10*br])
    fsol=least_squares(fobj,[1.,.1,30.],bounds=([0,-50,.1],[100,50,1000]),max_nfev=300)
    theta=fsol.x;fits['dynamic_filter']={'parameters':theta,'rmse_mv':float(np.sqrt(np.mean(fsol.fun[:-2]**2))),'free_parameters':3,'success':bool(fsol.success),'broad_endpoint_error_mv':float(fsol.fun[-2]/10),'broad_recovery_error_mv':float(fsol.fun[-1]/10),'input':'fixed literature BASE passive cable (.4nS,.06nS,50MOhm); no fitted driver parameters or paired observations'}
    fits['independent_sensors']={'rmse_mv':0.,'free_parameters':0,'privilege':'exact single-site waveform for every tested site, including held-out topology; no paired trace'}
    # Local synthetic-data uncertainty is distinct from published-endpoint screening.
    local=nominal*np.exp(rng.uniform(-.20,.20,(LOCAL_CANDIDATES,3)))
    local=np.minimum(np.maximum(local,BOUNDS[0]),BOUNDS[1])
    local=np.vstack([nominal,local]);ldata=training(so,parameters(local))
    lrms=np.sqrt(np.mean((ldata[:,:,fitmask]-target[None,:,fitmask])**2,axis=(1,2)))
    local_bt,local_bh=broad_trace(so,parameters(local));local_bf=broad_features(local_bt,local_bh)
    lmask=(lrms<=.25)&(local_bf[:,0]>=19.6)&(local_bf[:,0]<=26.8)&(abs(local_bf[:,1])<1.)
    lkeep=local[lmask];lkeep_rms=lrms[lmask]
    sv,cor,sensitivity_scales=identifiability_diagnostics(so,nominal,fitmask)
    print('Local synthetic uncertainty retained',len(lkeep),'condition',sv[0]/sv[-1],flush=True)
    pair_rows=[];traces={};geometries=[];single_cache={};solver_cache={}
    pair_names={'T1':[('siblings','tip0','tip1'),('distant','tip0','tip4')], 'T2':[('siblings','tip0','tip1'),('distant','tip0','tip4'),('separate_trees','tip0','tip8')], 'T3':[('siblings','tip0','tip1'),('distant','tip0','tip4'),('bridge_tips','tip3','tip4')]}
    # Singleton waveforms may be generated for residuals/oracle after fitting;
    # fitted parameters are frozen and never updated with these observations.
    def get_trace(top,model,sites,k,delay=0.,dt=DT,block=()):
        key=(top,model,sites,k,delay,dt,block)
        if key in traces:return traces[key]
        if (top,dt) not in solver_cache:solver_cache[top,dt]=Solver(build(top),dt)
        ss=solver_cache[top,dt];q=Protocol(sites,(k,)*len(sites),delay=delay)
        if model=='independent_sensors':
            ta,a=get_trace(top,'distributed',(sites[0],),k,0.,dt,block)
            z=a.copy()
            if len(sites)>1:
                _,b=get_trace(top,'distributed',(sites[1],),k,0.,dt,block)
                shift=int(round(delay/RECORD));bs=np.zeros_like(b)
                if shift:bs[shift:]=b[:-shift]
                else:bs=b
                z+=bs
        elif model=='dynamic_filter':
            # Drive from fixed passive cable, not refitted passive rival.
            ta,raw=trace(ss,pfilter_base,q,mode='passive',block_nodes=block,block_fraction=.9 if block else 0.)
            z=np.stack([filter_trace(raw[0,:,j],theta) for j in range(raw.shape[-1])],axis=-1)
        else:
            ta,z=trace(ss,fitted[model],q,mode=model,block_nodes=block,block_fraction=.9 if block else 0.)
            z=z[0]
        traces[key]=ta,z
        return ta,z
    for top in pair_names:
        for geometry,a,b in pair_names[top]:
            for k in KLEVELS:
                for delay in DELAYS:
                    for model in fits:
                        t,ab=get_trace(top,model,(a,b),k,delay)
                        _,sa=get_trace(top,model,(a,),k)
                        _,sb=get_trace(top,model,(b,),k)
                        sh=int(delay/RECORD);sb0=np.zeros_like(sb)
                        if sh:sb0[sh:]=sb[:-sh]
                        else:sb0=sb
                        r=residual(sa[:,0],sb0[:,0],ab[:,0]);q=Protocol((a,b),(k,k),delay=delay);w=window(t,q)
                        row={'topology':top,'geometry':geometry,'k_mm':k,'delay_ms':delay,'model':model,'window_start_ms':q.onset+delay+q.duration-100,'window_end_ms':q.onset+delay+q.duration,'single_a_mv':float(np.mean(sa[w,0])),'single_b_mv':float(np.mean(sb0[w,0])),'paired_mv':float(np.mean(ab[w,0])),'residual_mv':float(np.mean(r['voltage'][w])),'peak_abs_residual_mv':float(np.max(abs(r['voltage']))),'flow_residual':float(np.mean(r['flow'][w])),'saturation_only':float(np.mean(r['saturation'][w])),'beyond_saturation':float(np.mean(r['beyond_saturation'][w]))}
                        pair_rows.append(row)
        print('Pairs finished',top,flush=True)
    for k in KLEVELS:
        for delay in DELAYS:
            contrast={'k_mm':k,'delay_ms':delay,'models':{}}
            for model in fits:
                vals=[r for r in pair_rows if r['topology']=='T1' and r['k_mm']==k and r['delay_ms']==delay and r['model']==model]
                sib=next(r for r in vals if r['geometry']=='siblings');far=next(r for r in vals if r['geometry']=='distant')
                contrast['models'][model]=sib['residual_mv']-far['residual_mv']
            contrast['minimum_rival_gap_mv']=min(abs(contrast['models']['distributed']-v) for m,v in contrast['models'].items() if m!='distributed')
            contrast['nondistributed_rival_gap_mv']=min(abs(contrast['models']['distributed']-contrast['models'][m]) for m in ('passive','capillary_linear','dynamic_filter','independent_sensors'))
            geometries.append(contrast)
    # Grid selection uses nominal model only; uncertainty evaluated at SAME selected window.
    chosen=max(geometries,key=lambda z:z['minimum_rival_gap_mv'])
    ck=chosen['k_mm'];cd=chosen['delay_ms'];q=Protocol(('tip0','tip1'),(ck,ck),delay=cd)
    print('Selected design',chosen,flush=True)
    ensemble_results={}
    for label,xx in [('published_screen',accepted),('synthetic_single_match',lkeep)]:
        pp=parameters(xx);rr=so.rest(pp)
        t,ab=trace(so,pp,q,rest=rr)
        _,ac=trace(so,pp,Protocol(('tip0','tip4'),(ck,ck),delay=cd),rest=rr)
        w=window(t,q);gc=np.mean(ab[:,w,0]-ac[:,w,0],axis=1)
        rivals=np.array([v for m,v in chosen['models'].items() if m!='distributed']);lo=float(np.min(gc));hi=float(np.max(gc));robust_gap=min(0. if lo<=v<=hi else min(abs(lo-v),abs(hi-v)) for v in rivals)
        ensemble_results[label]={'interval_minimum_rival_gap_mv':float(robust_gap),'n':len(xx),'geometry_contrast_mv':summary_range(gc),'all_geometry_contrasts_mv':gc,'parameters':xx,'minimum_abs_contrast_mv':float(np.min(abs(gc))),'sign_consistent':bool(np.all(gc>0) or np.all(gc<0))}
    # Focal perturbation in unstimulated common trunk, rebaseline and remeasure singles.
    block=(15,16,17);drug={}
    for model in fits:
        vals={}
        for state,bb in [('control',()),('trunk_kir_90pct_block',block)]:
            t,ab=get_trace('T1',model,('tip0','tip1'),ck,cd,block=bb)
            _,ac=get_trace('T1',model,('tip0','tip4'),ck,cd,block=bb)
            _,s0=get_trace('T1',model,('tip0',),ck,block=bb)
            _,s1=get_trace('T1',model,('tip1',),ck,block=bb)
            _,s4=get_trace('T1',model,('tip4',),ck,block=bb)
            sh=int(cd/RECORD);shift=lambda x:np.pad(x[:-sh],((sh,0),(0,0))) if sh else x
            w=window(t,q)
            r1=ab-s0-shift(s1);r4=ac-s0-shift(s4)
            vals[state]={'geometry_contrast_mv':float(np.mean((r1-r4)[w,0])),'capillary_geometry_contrast_mv':float(np.mean((r1-r4)[w,1])),'single_site_mv':float(np.mean(s0[w,0])),'sibling_residual_mv':float(np.mean(r1[w,0])),'distant_residual_mv':float(np.mean(r4[w,0]))}
        vals['drug_geometry_change_mv']=vals['trunk_kir_90pct_block']['geometry_contrast_mv']-vals['control']['geometry_contrast_mv']
        drug[model]=vals
    t,aa=get_trace('T1','distributed',('tip0','tip1'),ck,cd,dt=1.)
    _,bb=get_trace('T1','distributed',('tip0','tip1'),ck,cd,dt=.5)
    _,cc=get_trace('T1','distributed',('tip0','tip1'),ck,cd,dt=2.)
    w=window(t,q)
    conv={'dt_ms':[2.,1.,.5],'max_trace_error_2_vs_half_mv':float(np.max(abs(cc-bb))),'window_error_2_vs_half_mv':float(abs(np.mean(cc[w,0]-bb[w,0]))),'max_trace_error_1_vs_half_mv':float(np.max(abs(aa-bb)))}
    near_model=min((m for m in fits if m!='distributed'),key=lambda m:abs(chosen['models']['distributed']-chosen['models'][m]))
    conv['nearest_rival']=near_model;conv['geometry_contrast_by_dt']={}
    for ds in (2.,1.,.5):
        ccvals={}
        for mm in ('distributed',near_model):
            td,sib=get_trace('T1',mm,('tip0','tip1'),ck,cd,dt=ds)
            _,far=get_trace('T1',mm,('tip0','tip4'),ck,cd,dt=ds)
            ccvals[mm]=float(np.mean((sib-far)[window(td,q),0]))
        ccvals['nearest_gap_mv']=abs(ccvals['distributed']-ccvals[near_model]);conv['geometry_contrast_by_dt'][str(ds)]=ccvals
    conv['geometry_error_2_vs_half_mv']=abs(conv['geometry_contrast_by_dt']['2.0']['distributed']-conv['geometry_contrast_by_dt']['0.5']['distributed'])
    conv['gap_error_2_vs_half_mv']=abs(conv['geometry_contrast_by_dt']['2.0']['nearest_gap_mv']-conv['geometry_contrast_by_dt']['0.5']['nearest_gap_mv'])
    drug_near=min((m for m in fits if m!='distributed'),key=lambda m:abs(drug['distributed']['drug_geometry_change_mv']-drug[m]['drug_geometry_change_mv']))
    conv['pharmacology_by_dt']={}
    for ds in (2.,.5):
        dd={}
        for mm in ('distributed',drug_near):
            vals={}
            for state,bbnodes in [('control',()),('block',(15,16,17))]:
                td,sib=get_trace('T1',mm,('tip0','tip1'),ck,cd,dt=ds,block=bbnodes)
                _,far=get_trace('T1',mm,('tip0','tip4'),ck,cd,dt=ds,block=bbnodes)
                vals[state]=float(np.mean((sib-far)[window(td,q),0]))
            dd[mm]=vals['block']-vals['control']
        dd['nearest_gap_mv']=abs(dd['distributed']-dd[drug_near]);conv['pharmacology_by_dt'][str(ds)]=dd
    conv['drug_nearest_rival']=drug_near
    conv['drug_change_error_2_vs_half_mv']=abs(conv['pharmacology_by_dt']['2.0']['distributed']-conv['pharmacology_by_dt']['0.5']['distributed'])
    conv['drug_gap_error_2_vs_half_mv']=abs(conv['pharmacology_by_dt']['2.0']['nearest_gap_mv']-conv['pharmacology_by_dt']['0.5']['nearest_gap_mv'])
    # Optional KATP pathway, effective input conductance is an explicit assumed load.
    kt=Protocol(('tip0','tip1'),(.1,.1),delay=0)
    _,kat=trace(so,pn,kt,katp=True)
    _,kas=trace(so,pn,Protocol(('tip0',),(.1,)),katp=True)
    kw=window(t,kt)
    # Pair prediction errors compare complete held-out timecourses, not only selected statistic.
    errors={}
    for model in fits:
        error=[];rvalues=[]
        for row in pair_rows:
            if row['model']!=model:continue
            a,b=next((a,b) for geo,a,b in pair_names[row['topology']] if geo==row['geometry'])
            _,pred=get_trace(row['topology'],model,(a,b),row['k_mm'],row['delay_ms'])
            _,truth=get_trace(row['topology'],'distributed',(a,b),row['k_mm'],row['delay_ms'])
            error.extend((pred[:,0]-truth[:,0]).tolist());rvalues.append(row['residual_mv'])
        errors[model]={'paired_rmse_mv':float(np.sqrt(np.mean(np.square(error)))),'window_residual_mv':summary_range(rvalues)}
    _,sym0=get_trace('T1','distributed',('tip0',),ck);_,sym1=get_trace('T1','distributed',('tip1',),ck);_,sym4=get_trace('T1','distributed',('tip4',),ck)
    symmetry_error=float(max(np.max(abs(sym0-sym1)),np.max(abs(sym0-sym4))))
    # A parameter corner fixed before examining paired results: weak Kir, high leak.
    weak=parameters([.2,.1,100]);wt,wa=trace(so,weak,Protocol(('tip0',),(8.,)));_,wb=trace(so,weak,Protocol(('tip0','tip1'),(8.,8.)));weak_w=window(wt,Protocol(('tip0','tip1'),(8.,8.)))
    weak_result={'parameters':[.2,.1,100.],'single_peak_mv':float(np.max(wa[0,:,0])),'pair_residual_peak_abs_mv':float(np.max(abs(wb[0,:,0]-2*wa[0,:,0]))),'pair_window_residual_mv':float(np.mean(wb[0,weak_w,0]-2*wa[0,weak_w,0])),'end_recovery_mv':float(wb[0,-1,0])}
    outer=parameters([.4,.06,1000.]);_,oa=trace(so,outer,Protocol(('tip0',),(8.,)));_,ob=trace(so,outer,Protocol(('tip0','tip1'),(8.,8.)));outer_result={'r_gj_mohm':1000.,'single_peak_mv':float(np.max(oa[0,:,0])),'pair_residual_peak_abs_mv':float(np.max(abs(ob[0,:,0]-2*oa[0,:,0])))}
    effect=abs(chosen['models']['distributed'])
    nearest=chosen['minimum_rival_gap_mv']
    zsum=2.8015852181129683
    # Four independent condition means after shared singleton/baseline cancellation.
    precision={'two_sided_alpha':.05,'power':.8,'zsum':zsum,'independent_condition_sd_mv':1.,'condition_mean_se_required_mv':nearest/(2*zsum),'replicates_per_condition_at_sd_1mv':int(np.ceil((2*zsum/max(nearest,1e-12))**2)),'contrast_se_required_mv':nearest/zsum,'assumption':'four independent condition means for residual geometry contrast; repeated frames are not independent replicates; prespecified design/window, normal approximation'}
    drug_effect=abs(drug['distributed']['drug_geometry_change_mv']);drug_gap=abs(drug['distributed']['drug_geometry_change_mv']-drug[drug_near]['drug_geometry_change_mv'])
    drug_precision={'nearest_rival':drug_near,'nearest_gap_mv':drug_gap,'condition_mean_se_to_detect_drug_effect_mv':drug_effect/(np.sqrt(8)*zsum),'condition_mean_se_to_distinguish_nearest_rival_mv':drug_gap/(np.sqrt(8)*zsum),'replicates_per_condition_to_detect_at_sd1mv':int(np.ceil((np.sqrt(8)*zsum/max(drug_effect,1e-12))**2)),'assumption':'eight independent means for drug-minus-control geometry residual; idealized block and predeclared nominal design'}
    results={'schema':1,'execution':{'status':'PASS','tests':test_result,'seed':SEED,'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'constants':{'gas_constant':R_GAS,'temperature_k':TEMP_K,'faraday':FARADAY,'potassium_in_mm':K_IN,'potassium_rest_mm':K_REST,'kir_slope_mv':K_KIR,'capacitance_cap_pf':C_CAP,'capacitance_pa_unit_pf':C_PA_UNIT,'pa_gap_resistance_mohm':R_GJ_PA,'cell_length_um':CELL_LENGTH_UM,'pa_units_per_node':PA_UNITS_PER_NODE,'pa_nodes':15,'pa_length_um':300,'t1_capillary_cells':45,'t2_capillary_cells':90,'t3_capillary_cells':48,'tip_site_cells':2,'broad_site_cells':16,'pulse_ms':500,'step_ms':DT,'record_ms':RECORD,'anchor_objective_weight':10,'passive_slope_floor_ns':.001,'flow_max_diameter_fraction':.3,'flow_hyperpolarization_scale_mv':10,'poiseuille_power':4,'pharmacology_block_fraction':.9,'katp_effective_conductance_ns':.1,'local_match_threshold_mv':.25,'local_log_perturbation':.2,'fit_protocol_count':len(TRAIN)+1,'weak_fit_protocol_count':len(TRAIN),'branch_levels':4,'cells_per_segment':3,'pa_readout_distance_um':240,'t2_attachment_spacing_um':120,'tip_site_mean_distance_um':220,'protocol_onset_ms':100,'fit_sample_ms':50,'distal_active_capillary_nodes_t1':42,'rest_drift_tolerance_mv_per_ms':1e-10,'free_parameter_count':3,'pair_conditions':len(pair_rows)//len(fits),'topology_count':3,'recovery_observation_ms':23000,'recovery_post_offset_ms':5000,'baseline_settling_check_ms':8000},'literature':{'longden2017_hyperpolarization_mv':23.2,'longden2017_sem_mv':1.8,'longden2017_latency_ms':240,'longden2017_latency_sem_ms':30,'calibration_lower_mv':19.6,'calibration_upper_mv':26.8,'baseline_lower_mv':-45,'baseline_upper_mv':-25,'measured_gbar_kir_mean':.18,'measured_gbar_kir_sd':.1,'measured_gkir_3mm_mean':.18*np.sqrt(3),'measured_gkir_3mm_sd':.1*np.sqrt(3),'measured_gbg_mean_ns':.06,'measured_gbg_sd_ns':.04,'calibration_strong_duration_ms':18000,'calibration_strong_k_mm':10,'calibration_endpoint_window_ms':100,'single_site_literature_target_note':'Published amplitude and reversibility screen at matched18s duration;2SEM acceptance and1mV recovery threshold are adopted design constraints, not raw-data likelihood. Exposure connected exposure footprint16cells is a structural assumption, with8cell sensitivity also evaluated. No latency calibration or external validation.'},'parameter_bounds':{'g_kir_ns':BOUNDS[:,0],'g_bg_ns':BOUNDS[:,1],'r_gj_mohm':BOUNDS[:,2]},'nominal_parameters':dict(zip(['g_kir_ns','g_bg_ns','r_gj_mohm'],nominal)),'fixed_parameters':{'g_kir_pa_ns':.65,'g_bg_pa_ns':.2,'e_bg_mv':-30,'e_bg_pa_mv':-30,'dv_kir_mv':25},'calibration':{'footprint_shape':'BFS-connected left distal subtree; selected16-cell structural assumption shared by every model','broad_node_indices':connected_patch(net,16),'broad_source_to_readout_distance_um':{'min':float(np.min(net.dist_um[connected_patch(net,16)])+240),'mean':float(np.mean(net.dist_um[connected_patch(net,16)])+240),'max':float(np.max(net.dist_um[connected_patch(net,16)])+240)},'footprint_screen':footprint_screen,'candidate_count':CANDIDATES,'accepted_count':len(accepted),'nominal_strong_response_mv':keep_amp[best],'post_offset_check_ms':5000,'recovery_threshold_mv':1.,'reversible_accepted_count':len(accepted),'endpoint_accepted_count':len(endpoint_accepted),'rejected_after_duration_and_recovery_count':int(mask.sum()-len(accepted)),'long_duration_response_mv':summary_range(long_feat[:,0]),'long_duration_recovery_mv':summary_range(long_feat[:,1]),'long_duration_ms':18000,'long_post_offset_check_ms':5000,'accepted_recovery_mv':summary_range(long_feat[:,1]),'nominal_recovery_mv':float(target_broad[1]),'nominal_one_mv_onset_ms':float(long_t[np.where(nominal_long_h>=1.)[0][0]]),'nominal_baseline_settling_error_mv':float(np.max(abs(so.rest(pn,t_end=8000)-so.rest(pn)))),'accepted_strong_response_mv':summary_range(keep_amp),'accepted_parameter_ranges':{n:summary_range(accepted[:,i]) for i,n in enumerate(['g_kir','g_bg','r_gj'])},'baseline_pa_mv':float(so.rest(pn)[0,net.zone2]),'nominal_selection':'closest to published mean among reversible18s-screen accepted draws; no paired response used','single_trace_provenance':'synthetic nominal model; twelve local protocols plus connected broad exposure on T1 only; every fifth10ms sample in local traces','fits':fits},'identifiability':{'sensitivity_steps':sensitivity_scales,'reported_log_step':.00001,'reported_step_stays_reversible':sensitivity_scales[-1]['all_perturbations_reversible'],'log_sensitivity_singular_values':sv,'condition_number':float(sv[0]/sv[-1]),'local_linear_correlation':cor,'broad_anchor_in_jacobian':True,'local_candidate_count':len(local),'matched_count':len(lkeep),'match_rmse_mv':summary_range(lkeep_rms),'matched_parameter_ranges':{n:summary_range(lkeep[:,i]) for i,n in enumerate(['g_kir','g_bg','r_gj'])},'meaning':'finite-design local sensitivity and tolerance set, neither posterior probability nor population confidence interval'},'heldout':{'errors':errors,'rows':pair_rows,'geometry_grid':geometries},'outer_coupling_sensitivity':outer_result,'simpler_suffices':weak_result,'design':{'matched_singleton_max_difference_mv':symmetry_error,'selected':chosen,'ensemble':ensemble_results,'pharmacology':drug,'pharmacology_precision':drug_precision,'precision':precision,'selection':'nominal-grid maximum minimum absolute geometry-contrast gap from all refitted rivals; equal-depth sibling vs distant T1 tips; no experimental outcomes observed','window_start_ms':q.onset+q.delay+q.duration-100,'window_end_ms':q.onset+q.delay+q.duration},'convergence':conv,'katp_scenario':{'single_mv':float(np.mean(kas[0,kw,0])),'paired_mv':float(np.mean(kat[0,kw,0])),'residual_mv':float(np.mean(kat[0,kw,0]-2*kas[0,kw,0])),'interpretation':'assumed effective capillary-node KATP input; no explicit pericyte compartment or metabolic kinetics'}}
    prov=HERE/'data'/'parameters.json'
    if prov.exists():results['parameter_provenance']=json.loads(prov.read_text())
    results['execution']['elapsed_seconds']=time.time()-start
    (OUT/'results.json').write_text(json.dumps(plain(results),indent=2,allow_nan=False)+'\n')
    np.savez_compressed(OUT/'calibration_traces.npz',times=np.arange(10,1610,10),target=target,local_parameters=local,local_rmse=lrms,screen_parameters=candidates,screen_amplitude=amplitude,screen_accepted=mask)
    figure_results(results,get_trace,pair_names)
    print(json.dumps({'accepted':len(accepted),'nominal':nominal.tolist(),'design':plain(chosen),'seconds':time.time()-start,'reversible_accepted_count':len(accepted),'endpoint_accepted_count':len(endpoint_accepted),'rejected_after_duration_and_recovery_count':int(mask.sum()-len(accepted)),'long_duration_response_mv':summary_range(long_feat[:,0]),'long_duration_recovery_mv':summary_range(long_feat[:,1]),'long_duration_ms':18000,'long_post_offset_check_ms':5000},indent=2),flush=True)


def figure_results(r,get_trace,pairs):
    plt.rcParams.update({'font.size':14,'axes.labelsize':14,'axes.titlesize':15,'legend.fontsize':13,'pdf.fonttype':42})
    ck=r['design']['selected']['k_mm'];cd=r['design']['selected']['delay_ms']
    fig,axes=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    ax=axes[0,0]
    for model in ['distributed','sensor_only','arteriole_linear','dynamic_filter']:
        t,sib=get_trace('T1',model,('tip0','tip1'),ck,cd);_,far=get_trace('T1',model,('tip0','tip4'),ck,cd)
        ax.plot(t,sib[:,0]-far[:,0],label={'distributed':'Distributed','sensor_only':'Distal-active','arteriole_linear':'Arteriole-linear','dynamic_filter':'Filter'}[model],lw=2)
    ax.axvspan(r['design']['window_start_ms'],r['design']['window_end_ms'],color='.85',alpha=.5)
    ax.set(xlabel='Time (ms)',ylabel='Sibling minus distant pair (mV)',title='A  Geometry contrast');ax.legend(loc='upper right')
    ax=axes[0,1]
    vals=np.array([[next(g for g in r['heldout']['geometry_grid'] if g['k_mm']==k and g['delay_ms']==d)['models']['distributed'] for d in DELAYS] for k in KLEVELS])
    lim=max(abs(vals.min()),abs(vals.max()));im=ax.imshow(vals,origin='lower',aspect='auto',cmap='RdBu_r',vmin=-lim,vmax=lim)
    ax.set(xticks=range(4),xticklabels=[int(x) for x in DELAYS],yticks=range(4),yticklabels=[int(x) for x in KLEVELS],xlabel='Second input delay (ms)',ylabel='Local potassium (mM)',title='B  Timing and intensity');fig.colorbar(im,ax=ax,label='mV')
    ax=axes[1,0]
    modes=list(MODEL_LABELS);values=[r['design']['selected']['models'][m] for m in modes]
    ax.barh(range(len(modes)),values,color=['#175b86']+['#8ba9ba']*6);ax.set(yticks=range(len(modes)),yticklabels=['Distributed','Passive','Distal-active','Capillary-linear','Arteriole-linear','Dynamic filter','Independent oracle'],xlabel='Fixed-window geometry contrast (mV)',title='C  Fitted models');ax.axvline(0,color='k',lw=.7)
    ax=axes[1,1]
    data=[r['design']['ensemble'][key]['all_geometry_contrasts_mv'] for key in ['published_screen','synthetic_single_match']]
    ax.boxplot(data,tick_labels=['Source\nscreen','Single-site\nfit'],showfliers=True)
    ax.axhline(r['design']['selected']['models']['distributed'],color='#175b86',ls='--');ax.set(ylabel='Geometry contrast (mV)',title='D  Parameter sensitivity')
    fig.savefig(FIG/'paired_predictions.pdf');fig.savefig(FIG/'paired_predictions.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(1,1,figsize=(8,5),layout='constrained')
    t,a=get_trace('T1','distributed',('tip0',),ck);_,b=get_trace('T1','distributed',('tip1',),ck);_,ab=get_trace('T1','distributed',('tip0','tip1'),ck,cd)
    shift=int(cd/RECORD);bs=np.pad(b[:-shift],((shift,0),(0,0))) if shift else b
    rr=residual(a[:,0],bs[:,0],ab[:,0])
    for key,label in [('flow','Total flow residual'),('saturation','Output-transform residual'),('beyond_saturation','Beyond output transform')]:ax.plot(t,rr[key],label=label,lw=2)
    ax.set(xlabel='Time (ms)',ylabel='Residual in normalized flow',title='Electrical and output-transform contributions');ax.legend();fig.savefig(FIG/'saturation_decomposition.pdf');fig.savefig(FIG/'saturation_decomposition.png',dpi=170);plt.close(fig)

if __name__=='__main__':main()

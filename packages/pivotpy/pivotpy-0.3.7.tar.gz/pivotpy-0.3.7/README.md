# PivotPy
> A Python Processing Tool for Vasp Input/Output. A CLI is available in Powershell, see [Vasp2Visual](https://github.com/massgh/Vasp2Visual).


## Install
`pip install pivotpy`

## How to use
- See [Full Documentation](https://massgh.github.io/pivotpy/).
- For CLI, use [Vasp2Visual](https://github.com/massgh/Vasp2Visual).
- Run in Azure [![Run in Azure](https://notebooks.azure.com/launch.png)](https://testazurenotebooks-massaz.notebooks.azure.com/j/notebooks/index.ipynb)

```
import pivotpy as pp
print(', '.join(pp.__all__))
```

    Dic2Dot, read_asxml, exclude_kpts, get_ispin, get_summary, get_kpts, get_tdos, get_evals, get_bands_pro_set, get_dos_pro_set, get_structure, export_vasprun, interpolate_data, ps_to_py, ps_to_std, select_dirs, select_files, invert_color, plot_bands, modify_axes, quick_bplot, add_text, add_legend, add_colorbar, create_rgb_lines, quick_rgb_lines, quick_color_lines, init_figure, select_pdos, collect_dos, quick_dos_lines, rgb_to_plotly, plotly_to_html, plotly_rgb_lines, plotly_dos_lines, show, savefig
    

```
import os 
os.chdir('E:/Research/graphene_example/ISPIN_1/bands')
xml_data=pp.read_asxml()
vr=pp.export_vasprun(elim=[-5,5])
vr.keys()
```




    dict_keys(['sys_info', 'dim_info', 'kpoints', 'kpath', 'bands', 'tdos', 'pro_bands', 'pro_dos', 'poscar', 'xml'])



```
print(pp.exclude_kpts(xml_data=xml_data))
pp.get_summary(xml_data=xml_data)
```

    14
    




    {'SYSTEM': 'C2',
     'NION': 2,
     'TypeION': 1,
     'ElemName': ['C'],
     'ElemIndex': [0, 2],
     'ISPIN': 1}



## Example Plot: Graphene Spin Polarized

```
import pivotpy as pp 
import matplotlib.pyplot as plt 
vr1=pp.export_vasprun('E:/Research/graphene_example/ISPIN_2/bands/vasprun.xml')
vr2=pp.export_vasprun('E:/Research/graphene_example/ISPIN_2/dos/vasprun.xml')
axs=pp.init_figure(ncols=3,widths=[1,1,1],sharey=True,wspace=0.05,figsize=(10,2.6))
elements=[0,0,[0,1]]
orbs=[[0],[1],[2,3]]
orblabels=['s','p_z','(p_x+p_y)']
colors=['r',(0,0.9,0),'b']
ti_cks=dict(xt_indices=[0,30,60,-1],xt_labels=['Γ','M','K','Γ'])
args_dict=dict(elements=elements,orbs=orbs,orblabels=orblabels,elim=[-20,15])
pp.quick_bplot(path_evr=vr1,ax=axs[0],**ti_cks,elim=[-20,15])
pp.quick_rgb_lines(path_evr=vr1,ax=axs[1],**args_dict,**ti_cks)
lg_k={'ncol': 3}
pp.quick_dos_lines(path_evr=vr2,ax=axs[2],vertical=True,include_dos='pdos',**args_dict,colors=colors,legend_kwargs=lg_k)
pp.add_colorbar(ax=plt.gcf().add_axes([0.399,1.02,0.23,0.05]),ticklabels=[r'$s^{⇅}$',r'$p_z^{⇅}$',r'$(p_x+p_y)^{⇅}$'])
pp.show() 
```


![svg](docs/images/output_6_0.svg)


## Brillouin Zone (BZ) Processing
Look in `pivotpy.sio` module for details on generating mesh and path of KPOINTS as well as using Materials Projects' API to get POSCAR right in the working folder with command `get_poscar`. Below is a screenshot of interactive BZ plot. You can `double click` on blue points and hit `Ctrl + C` to copy the high symmetry points relative to reciprocal lattice basis vectors. (You will be able to draw kpath in `Pivotpy-Dash` application and generate KPOINTS automatically from a web interface later on!). 

```
from IPython.display import Image
Image('./docs/images/plot_bz.jpg')
```




![jpeg](output_8_0.jpg)



## Plotting Two Calculations Side by Side 
- Here we will use `shift_kpath` to demonstrate plot of two calculations on same axes side by side

```
import matplotlib.pyplot as plt
import pivotpy as pp 
vr1=pp.export_vasprun('E:/Research/graphene_example/ISPIN_1/bands/vasprun.xml')
shift_kpath=vr1.kpath[-1] # Add last point from first export in second one.
vr2=pp.export_vasprun('E:/Research/graphene_example/ISPIN_2/bands/vasprun.xml',shift_kpath=shift_kpath)
last_k=vr2.kpath[-1]
axs=pp.init_figure(figsize=(5,2.6))
K_all=[*vr1.kpath,*vr2.kpath] # Merge kpath for ticks
kticks=[K_all[i] for i in [0,30,60,90,120,150,-1]]
ti_cks=dict(xticks=kticks,xt_labels=['Γ','M','K','Γ','M','K','Γ'])
pp.quick_bplot(path_evr=vr1,ax=axs)
pp.quick_bplot(path_evr=vr2,ax=axs,txt='Graphene(Left: ISPIN=1, Right: ISPIN=2)',ctxt='m')
pp.modify_axes(ax=axs,xlim=[0,last_k],ylim=[-10,10],**ti_cks)
```


![svg](docs/images/output_10_0.svg)


## Interpolation 

```
import pivotpy as pp
k=vr1.kpath
ef=vr1.bands.E_Fermi
evals=vr1.bands.evals-ef
#Let's interpolate our graph to see effect. It is useful for colored graphs.
knew,enew=pp.interpolate_data(x=k,y=evals,n=10,k=3)
plot=plt.plot(k,evals,'b',lw=5,label='real data')
plot=plt.plot(k,evals,'w',lw=1,label='interpolated',ls='dashed')
pp.add_text(ax=plt.gca(),txts='Graphene')
```


![svg](docs/images/output_12_0.svg)


## Running powershell commands from python.
Some tasks are very tideious in python while just a click way in powershell. See below, and try to list processes in python yourself to see the difference!

```
gu.ps_to_std(ps_command='(Get-Process)[0..4]')
```

    Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
    -------  ------    -----      -----     ------     --  -- -----------
    563      49    39564      75820      17.41  16184   1 AltC
    271      17     6072      24916       1.67   6776   1 ApplicationFrameHost
    147       9     1360       5832              5320   0 armsvc
    413      22   300208      39312       7.42   3556   0 audiodg
    331      17     4724       6628       2.38  14560   1 CastSrv
    

## Using Plotly in pivotpy
- See video!
<div><iframe width="560" height="315" src="https://www.youtube.com/embed/uda0ubF-cnQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
- Interact with chart below, hover, zoom, pan and more!
<div><iframe width="700" height="400" frameborder="0" scrolling="no" src="//plotly.com/~massgh/36.embed"></iframe></div>

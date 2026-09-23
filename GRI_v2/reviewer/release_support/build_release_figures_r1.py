import csv, hashlib, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE=Path(__file__).resolve().parent
BASE=HERE.parent if HERE.name == 'release_support' else HERE
OUT=BASE/'figures'
OUT.mkdir(parents=True, exist_ok=True)
PDFMETA={'Creator':'BioSystems deterministic release figure builder','CreationDate':None,'ModDate':None}

# Figure 1: evidence architecture
fig = plt.figure(figsize=(11,6.4))
ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
boxes = [
    (0.05,0.69,0.23,0.18,'Stage A / B1','RNA architecture\n+ context attack','STATIC / SAME SOURCE'),
    (0.385,0.69,0.23,0.18,'P0 holdout','DISCOVERY -> REPLICATION\n-> FINAL_HOLDOUT','BOUNDED INTERNAL'),
    (0.72,0.69,0.23,0.18,'Stage C1','Methylation H1\n+ cross-layer H2/H3','STATIC / FROZEN'),
    (0.19,0.29,0.27,0.18,'Tumor-normal control','TN-A1 / TN-P20 / TN-C1','SPECIFICITY / CONTROL'),
    (0.54,0.29,0.27,0.18,'External prostate P1','450K primary + n=32\n+ EPIC sensitivity','INDEPENDENT TRANSPORT'),
]
for x,y,w,h,title,body,tag in boxes:
    p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.015',fill=False,linewidth=1.5)
    ax.add_patch(p)
    ax.text(x+w/2,y+h*0.73,title,ha='center',va='center',fontsize=12,fontweight='bold')
    ax.text(x+w/2,y+h*0.46,body,ha='center',va='center',fontsize=9.2)
    ax.text(x+w/2,y+h*0.16,tag,ha='center',va='center',fontsize=8.4)
# arrows kept out of box text
for p0,p1 in [((0.28,0.78),(0.385,0.78)),((0.615,0.78),(0.72,0.78)),((0.49,0.69),(0.32,0.47)),((0.61,0.69),(0.675,0.47))]:
    ax.add_patch(FancyArrowPatch(p0,p1,arrowstyle='-|>',mutation_scale=14,linewidth=1.1,connectionstyle='arc3,rad=0.0'))
ax.text(0.5,0.105,'Claim ceiling: static architecture and bounded transport only. No causal direction, recovery failure, treatment response, or universal boundary.',ha='center',va='center',fontsize=9.6,wrap=True)
ax.text(0.5,0.955,'BioSystems revised evidence architecture',ha='center',va='top',fontsize=16,fontweight='bold')
fig.savefig(OUT/'Figure_1_Evidence_Architecture.pdf',bbox_inches='tight',metadata=PDFMETA)
plt.close(fig)

# Figure 2: C1 summary as endpoint-specific evidence table, not common-scale bars
rows=[
('H1', 'Methylation spectral organization', '+0.1280', '32/32 positive', 'q=3.10e-10', 'within-layer construction test'),
('H2', 'Methylation-RNA patient geometry', '+0.2295', '32/32 positive', 'q=3.10e-10', 'within-cancer observed vs shuffle; raw cross-cancer magnitude is floor-sensitive'),
('H3a','Patient-specific Hallmark coupling', '+0.0981', '32/32 positive', 'q=3.10e-10', 'patient identity attack'),
('H3b','Same-label Hallmark advantage', '+0.02125','29/32 positive','q=1.28e-6','small / support-sensitive semantic branch'),
]
fig=plt.figure(figsize=(11.2,5.5)); ax=fig.add_axes([0,0,1,1]); ax.axis('off')
ax.text(0.5,0.94,'Frozen Stage C1 aggregate architecture',ha='center',fontsize=16,fontweight='bold')
cols=[0.05,0.14,0.52,0.65,0.78]
headers=['Endpoint','Quantity','Median effect','Direction support','Global inference']
for x,h in zip(cols,headers): ax.text(x,0.84,h,fontsize=10,fontweight='bold',ha='left')
for i,(ep,q,effect,support,qv,note) in enumerate(rows):
    y=0.70-i*0.155
    ax.add_patch(FancyBboxPatch((0.035,y-0.055),0.93,0.115,boxstyle='round,pad=0.008',fill=False,linewidth=0.8))
    ax.text(cols[0],y,ep,fontsize=11,fontweight='bold',va='center')
    ax.text(cols[1],y,q,fontsize=9.5,va='center')
    ax.text(cols[2],y,effect,fontsize=10,va='center')
    ax.text(cols[3],y,support,fontsize=9.5,va='center')
    ax.text(cols[4],y,qv,fontsize=9.5,va='center')
    ax.text(0.14,y-0.038,note,fontsize=8.3,va='center')
ax.text(0.5,0.055,'Endpoint effects use different constructions and scales. They are not combined or ranked as a master scalar.',ha='center',fontsize=9.5)
fig.savefig(OUT/'Figure_2_C1_Static_Summary.pdf',bbox_inches='tight',metadata=PDFMETA)
plt.close(fig)

# Figure 3: tumor-normal multiomic
cancers=['BRCA','LIHC','PRAD','THCA','UCEC']
data={
'H1 dS':[-0.1673,-0.1000,-0.1367,-0.2513,-0.1502],
'H2 dCKA':[0.0226,0.0095,-0.0620,-0.3256,-0.3486],
'H3a dA_patient':[-0.0049,-0.0287,0.0438,-0.0300,-0.1364],
'H3b dA_label':[0.0116,0.0000,0.0487,0.0027,0.0416],
}
fig=plt.figure(figsize=(11,7.5))
lefts=[0.08,0.55,0.08,0.55]; bottoms=[0.56,0.56,0.12,0.12]
for (name,values),left,bottom in zip(data.items(),lefts,bottoms):
    ax=fig.add_axes([left,bottom,0.38,0.32])
    yy=np.arange(len(cancers)); ax.barh(yy,values,alpha=0.75); ax.axvline(0,linewidth=0.9)
    ax.set_yticks(yy,cancers); ax.invert_yaxis(); ax.set_title(name); ax.set_xlabel('tumor - adjacent normal')
fig.suptitle('TN-C1 multiomic tumor-normal control: reorganization rather than tumor-only architecture',fontsize=15,y=0.97)
fig.text(0.5,0.025,'H1 is lower in tumor in 5/5 cancers but the exact n=5 pan-cancer test is resolution-limited (p=0.0625; BH q=0.125). H2/H3a are heterogeneous; H3b is small and unresolved.',ha='center',fontsize=9.5,wrap=True)
fig.savefig(OUT/'Figure_3_TN_C1_Multiomic.pdf',bbox_inches='tight',metadata=PDFMETA)
plt.close(fig)

# Figure 4: RNA tumor-normal aggregate
coords=['C_in,pair','C_in,PC1','C_out']
primary=np.array([-0.0560717,-0.0730223,-0.1085434]); paired=np.array([-0.0657291,-0.0719590,-0.0964471])
fig,ax=plt.subplots(figsize=(9.5,5.5)); x=np.arange(3); w=0.34
b1=ax.bar(x-w/2,primary,w,label='TN-A1 primary'); b2=ax.bar(x+w/2,paired,w,label='TN-P20 paired sensitivity')
ax.axhline(0,linewidth=0.8); ax.set_xticks(x,coords); ax.set_ylabel('median tumor - adjacent normal'); ax.set_title('RNA architecture is lower in tumor in the frozen unadjusted tissue-state contrast'); ax.legend(frameon=False)
for i,bar in enumerate(b1): ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()/2,'12/12',ha='center',va='center',fontsize=8.5)
for i,bar in enumerate(b2): ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()/2,('13/13' if i<2 else '12/13'),ha='center',va='center',fontsize=8.5)
ax.text(0.0,-0.22,'Primary BH q=4.88e-4 for all three coordinates. Paired sensitivity BH q=3.66e-4, 3.66e-4, and 0.00342, respectively.',transform=ax.transAxes,fontsize=9)
fig.tight_layout(); fig.savefig(OUT/'Figure_4_TN_RNA_Control.pdf',bbox_inches='tight',metadata=PDFMETA); plt.close(fig)

# Figure 5: external P1 transport
endpoints=['H1 dS','H2 dCKA','H3a dA_patient']; lanes=['450K n=30','450K n=32','EPIC n=26']
external_vals=np.array([[0.303090,0.019724,-0.040489],[0.317045,0.016723,-0.007331],[0.358394,-0.017032,0.030769]])
qs=np.array([[0.003,0.4065,0.813],[0.003,0.426,0.549],[0.003,0.69,0.5175]])
fig=plt.figure(figsize=(11,7.2))
for j,ep in enumerate(endpoints):
    ax=fig.add_axes([0.08+0.31*j,0.34,0.25,0.48]); yy=np.arange(3)
    ax.barh(yy,external_vals[:,j],alpha=0.75); ax.axvline(0,linewidth=0.9)
    ax.set_yticks(yy,lanes if j==0 else []); ax.invert_yaxis(); ax.set_title(ep); ax.set_xlabel('effect')
    # q-values in a fixed right-side text column to avoid overlap
    for i,q in enumerate(qs[:,j]): ax.text(0.98,i,f'q={q:g}',transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=8.3)
fig.suptitle('Independent prostate P1: H1 transports; H2/H3a show no detectable transport',fontsize=15,y=0.95)
fig.text(0.5,0.22,'Primary 450K: P1_PARTIAL_TRANSPORT. EPIC reproduces H1; H2/H3a remain null-compatible. Opposite small effect signs trigger the frozen procedural label P1_REPRESENTATION_DEPENDENT, not a real platform-effect claim.',ha='center',fontsize=10,wrap=True)
fig.text(0.5,0.115,'Secondary paired RNA: C_in,pair = -0.01348, C_in,PC1 = -0.00864, C_out = +0.00099; all BH q=0.504 (not confirmed).',ha='center',fontsize=9.5,wrap=True)
fig.savefig(OUT/'Figure_5_External_P1_Transport.pdf',bbox_inches='tight',metadata=PDFMETA); plt.close(fig)

# exact source values used by release visuals
rows=[]
for ep,q,effect,support,qv,note in rows if False else []: pass
c1=[('H1',0.1280,'32/32 positive; q=3.10e-10'),('H2',0.2295,'32/32 positive; q=3.10e-10'),('H3a',0.0981,'32/32 positive; q=3.10e-10'),('H3b',0.02125,'29/32 positive; q=1.28e-6')]
for ep,v,n in c1: rows.append(['C1_AGGREGATE',ep,v,n])
for c in cancers:
    idx=cancers.index(c)
    for ep,arr in data.items(): rows.append(['TN_C1',c+' '+ep,arr[idx],'tumor-minus-normal'])
for c,v in zip(coords,primary): rows.append(['TN_A1',c,v,'primary median'])
for c,v in zip(coords,paired): rows.append(['TN_P20',c,v,'paired sensitivity median'])
for i,lane in enumerate(lanes):
    for j,ep in enumerate(endpoints): rows.append(['EXTERNAL_P1',lane+' '+ep,external_vals[i,j],f'q={qs[i,j]}'])
with open(BASE/'release_support'/'release_visual_source_values.csv' if (BASE/'release_support').is_dir() else BASE/'release_visual_source_values.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['source_block','quantity','value','note']); w.writerows(rows)
hash_path=(BASE/'release_support'/'release_visual_hashes.tsv' if (BASE/'release_support').is_dir() else BASE/'release_visual_hashes.tsv')
with open(hash_path,'w') as f:
    f.write('file\tsha256\n')
    for p in sorted(OUT.glob('*.pdf')):
        f.write(f'{p.name}\t{hashlib.sha256(p.read_bytes()).hexdigest()}\n')